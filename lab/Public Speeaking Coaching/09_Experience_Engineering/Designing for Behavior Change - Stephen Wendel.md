# **Designing for Behavior Change**

SECOND EDITION

## Applying Psychology and Behavioral Economics **Stephen Wendel**


**Designing for Behavior Change**


by Stephen Wendel


Copyright © 2020 Stephen Wendel. All rights reserved.


Printed in Canada.


Published by O’Reilly Media, Inc., 1005 Gravenstein Highway North,
Sebastopol, CA 95472.


O’Reilly books may be purchased for educational, business, or sales
promotional use. Online editions are also available for most titles
( _[http://oreilly.com](http://oreilly.com/)_ ). For more information, contact our
corporate/institutional sales department: 800-998-9938 or
_corporate@oreilly.com_ .


Acquisitions Editor: Jennifer Pollock Indexer: WordCo Indexing Services, Inc.


Production Editor: Katherine Tozer Cover Designer: Karen Montgomery


Proofreader: Kim Wimpsett


November 2013: First Edition


June 2020: Second Edition


**Revision History for the Second Edition**


2020-05-29: First Release


See _[http://oreilly.com/catalog/errata.csp?isbn=9781492056034](http://oreilly.com/catalog/errata.csp?isbn=9781492056034)_ for release
details.


The O’Reilly logo is a registered trademark of O’Reilly Media, Inc.
_Designing for Behavior Change_, the cover image, and related trade dress
are trademarks of O’Reilly Media, Inc.


The views expressed in this work are those of the author, and do not
represent the publisher’s views. While the publisher and the author have
used good faith efforts to ensure that the information and instructions
contained in this work are accurate, the publisher and the author disclaim all
responsibility for errors or omissions, including without limitation
responsibility for damages resulting from the use of or reliance on this
work. Use of the information and instructions contained in this work is at
your own risk. If any code samples or other technology this work contains
or describes is subject to open source licenses or the intellectual property
rights of others, it is your responsibility to ensure that your use thereof
complies with such licenses and/or rights.


978-1-492-05603-4


[MBP]


# **Preface**

Eight years ago, when I started writing the first edition of this book,
behavioral science consisted of a few prominent researchers and PhD
students scattered across business schools and psych departments, along
with some humorous books about the mistakes people make. Very few
companies were trying to bridge the gap between academic theory and real
products that helped real people in their lives. Personally, I had to scrounge
to find companies where anyone was even familiar with the research, let
alone formally trained in it. The idea of intentionally designing products to
change user behavior was strange or even alarming to many people. There
were pockets of innovative work—from the UK government’s Nudge Unit
to BJ Fogg’s Persuasive Technology Lab to the behavioral consulting firm
ideas42—but they were not well known outside of their communities.


That’s all changed now. In partnership with the Action Design Network and
the Behavioral Science Policy Association—two nonprofit organizations
dedicated to fostering the practical application of behavioral science, which
didn’t exist eight years ago—we recently surveyed the landscape of applied
behavioral science. Over two hundred teams, representing behavioral
science teams with over 1,500 members, responded—and we know there
are many more out there.


There are now dedicated teams applying behavioral science to develop new
products, communications, and policies that serve their users across the
world: from Qatar to Spokane, Washington. While Silicon Valley firms like
Google and Uber are well represented, so are stalwart mainline companies
like Walmart and Aetna, with dozens of small consulting shops scattered
around the US, Europe, and beyond.


What are they doing? While each effort is unique, each of these groups is
trying to develop products, communications, or policies that cause their
users to do _something different_ in their lives. In other words, they are
designing for behavior change. Whereas traditional design is fundamentally


about solving a user need, behavioral design is about solving a user need
where doing so entails, in a sense, “solving the user” too: changing the
person in order to solve the problem.


And that’s where this book comes in. This is a guidebook on how to do it
yourself: how to identify behavioral problems your users face, develop
clever solutions to help them overcome those obstacles, iteratively learn
from the process, build a team that does this, and make it successful in an
organization. And, underneath it all, how to think about this work in an
ethical, thoughtful way and avoid the serious mistakes and abuses that some
practitioners are facing now—and that threaten our field as a whole.


Along the way, I’ll try to teach you the fundamental understanding of the
mind that many behavioralists like me have: of a quirky, elegant, but
necessarily imperfect decision-making process that guides your users’
decisions and actions. I’ll give you the core lessons and a framework to
understand the research literature, but this book isn’t fundamentally about
behavioral science theory (for me, Nobel Laureate Daniel Kahneman’s
_Thinking, Fast and Slow_ is still the best introductory book on behavioral
science out there—I highly recommend it). Instead, our focus will be on
_action_ : what you can do, in your work, right now.


## **How This Book (and This New Edition) Came** **About**

In 2019, O’Reilly asked if I could do a second edition of the book, updating
it for tremendous growth in the field since it first came out. I was happy to
do so—if only to celebrate that growth and help support its further
advancement in my small way.


The ideas and process I discuss here come, foremost, from my own
experience working in this field over the last 11 years: first at the personal
finance company HelloWallet, and now at the investment research company
Morningstar. It is enriched by countless conversations with other
practitioners in the field: those with existing teams and those just seeking to
enter the field. I’m particularly grateful to the Action Design Network, the
nonprofit organization that I helped start in 2013, which has grown far
beyond my dreams or certainly my intentions, with events all across North
America on applied behavioral science. I will also be weaving in lessons
from the survey I mentioned before, which we believe is the largest and
most comprehensive survey of teams designing for behavior change ever
conducted (though the way the field is growing, it won’t be for long!).


Personally, I started doing applied behavioral science while completing my
PhD and working at HelloWallet. HelloWallet began as many start-ups do:
with a great deal of energy, a clear problem to solve, and a fundamentally
misguided notion of how to solve it. We wanted to help everyday
Americans improve their finances—and wrote an application that
encouraged them to set up budgets and save for the future. There was just
one little problem: everyone already knew how to do that. The problem
people faced wasn’t a lack of understanding; it was that they didn’t act on
it. There was a tremendous gap between people’s intentions and their
actions.


Thankfully, in addition to having a great (but misguided) idea, we had the
ability to measure whether we were being successful. We looked at whether
people used our app. They didn’t. We also looked at whether it was helping
the few people who used it to improve their finances. It wasn’t. I’m


thankful for those hard lessons because it’s better to know _early_ when
something isn’t working and to be able to learn from that and do better—
which will be a recurring theme throughout this book.


At HelloWallet, we set up an engine for behavioral experimentation:
building scientific experiments into the underlying platform of the
application. My motto was to make it “easier to test than to argue”—i.e.,
where product managers or designers disagreed about which version of a
feature would more effectively change spending behavior, it was better to
test both approaches in the field than to argue about which _might_ be right.
And by and large we succeeded—both in making it easy to run tests and in
having the impact we sought.


We found that we could help people change their bank habits, to cut the
money they lost to ATM and other banks fees by 25%; for lower-income
families that equated to nearly a day’s wages per month. We found that we
could successfully nudge people to put aside money for savings by giving
them a simple and easy-to-understand display of their finances, compared to
that of their peers. And we also found that some of our efforts—like
congratulating people on their budgeting success—actually backfired: they
spent more! We quickly discontinued that feature. The first edition of
_Designing for Behavior Change_ was, in many ways, a description of what
we were learning as we learned it. It detailed the process we were using in
practice. In fact, the book arose out of an internal guidebook that I’d written
for my teammates on applied behavioral science.


Since then, I’ve gained a great deal more experience with the challenges of
designing products that help people change behavior. But, I’ve also verified
that the fundamental approach was sound; the four-step process laid out in
the book is what I still use today—though I’ve started using different names
for the steps. I’ve modified the process around the edges, making it more
efficient and flexible, but it is still tremendously useful in my own work.
After the first edition, I also subsequently learned that many other teams
had independently developed a similar iterative approach.


About five years ago, I moved to Morningstar (along with some of my
teammates from HelloWallet) and was given the opportunity to set up a
much larger behavioral science team. We work across the company, on
issues ranging from effective investing to retirement saving and spending to
challenges of internal decision making. We conduct applied research both
with our in-house team and with leading behavioral scientists from
academia.


This edition draws upon my more recent work at Morningstar, formal and
informal consulting I’ve done with other organizations in our space, and
especially work through the Action Design Network. The Action Design
Network has grown from our initial monthly meetup in DC to a broad base
of volunteers organizing events across 15 North American cities. Through
it, I was able to learn from the challenges many other teams face, the
approach they use, and their solutions.


In this new edition of the book, I’ve sought to bring together these diverse
streams of insight to a coherent guidebook for practitioners to help you
learn from the best of our knowledge in the field so you can design your
own products to more effectively help users change their own behavior.


## **Who This Book Is For**

As you can probably tell by now, this book is aimed at practitioners—the
people who design and build products or communications with specific
behavioral goals. Teams that design for behavior change should generally
include the following roles, and individuals in each of these roles will find
practical, how-to instructions in this book:


Interaction designers, information architects, user researchers,
human factors experts, human–computer interaction (HCI)
practitioners, and other UX folks


Product managers, product owners, and project managers


Marketing and communications professionals


Behavioral scientists (including behavioral economists,
psychologists, and judgment and decision-making experts)
interested in products and communications that apply the research
literature


The person doing the work of designing for behavior change could be any
one of these people. At Morningstar, we have each of these roles, but most
of my team is composed of behavioral researchers. This work can be, and
often is, done wonderfully by UX folks. They are closest to the look and
feel of the product and have its success directly in their hands. This
approach enriches their current practice by adding an extra theoretical layer
to design hypotheses and tests.


Product owners and managers are also well positioned to seamlessly
integrate the skills of designing for behavior change to make their products
effective. Finally, there are other behavioral scientists (like me) working in
applied product development and consulting at organizations like ideas42
and the Center for Advanced Hindsight. So, the people designing for
behavior change probably wear other hats as well.


In addition, this book is for entrepreneurs and managers. If you’ve ever read
_Nudge, Blink_, or _Predictably Irrational_,1 and wondered how you could


apply them to your own product and users, read on. While the book is about
helping users take action in their lives, that doesn’t mean that designing for
behavior change is incompatible with a for-profit business model.
Businesses make a profit; that’s how they exist. So, you’ll find suggestions
for building a successful business model on voluntary behavior change. If
in addition to making a profit, you are helping your users take action and
change their behavior, this book can help you do it.


Nonprofit entities and some government agencies often explicitly focus on
helping users change their behavior; _Designing for Behavior Change_ can
[help. For example, the UK’s Behavioural Insights Team is widely applying](https://www.bi.team/)
behavioral research to public policy and services around the world. Where
relevant, I’ll note parts that are particularly important for nongovernmental
organizations (NGOs) and government agencies. Because it’s more compact
to write, I’ll refer primarily to “companies” here. In almost all cases, I
really mean companies, organizations, and relevant government agencies.


Finally, my expertise is software development, so I’ll use the terminology
that I use in my day-to-day life—applications, software, and programs. You
don’t need to be in software development to find this relevant to you. In
fact, some of the most innovative work in persuasive design, one of the
fields that this book draws inspiration from, is in the design of everyday
objects.2 As you apply _Designing for Behavior Change_ to your work,
whether in software or beyond, I’d love to talk with you and share notes!
You can reach me at _steve@behavioraltechnology.co_ .

### **Combining Research, Data, and Product Expertise**


One of the book’s recurring themes is that understanding how the mind
works is not enough to build behaviorally effective products.


In addition to behavioral science research, we need two sets of skills to
support the process. First, we need to plan for data analysis (both qualitative
and quantitative) and for refinement and iteration based on that data. That
means adding metrics to the application and conducting user research to


understand individual behavior, analyzing the data, and making
improvements over time based on it.


Second, we need to build products that people actually enjoy using. I know
it sounds obvious, but it’s something that’s often forgotten as we build
products designed to educate, motivate, or otherwise help our users. We
tend to focus on the behavior change (and how important it is) and forget
the fact that people still have to _choose_ to use our products. Users avoid
boring, frustrating, ugly applications, so we should remember the lessons of
good product design, from identifying user needs and frustrations to
designing an intuitive, beautiful user interface.


When you bring these raw ingredients together—behavioral research,
product design or marketing expertise, and data analysis—you have what’s
needed to design for behavior change:


### **What You Need to Know to Benefit from This Book**

This book gives you enough knowledge in each of these three areas to get
oriented and to start working on concrete products and communications. It
covers most of the behavioral research you’ll need to finish the products as
well, but at some point along the way, you’ll need people who are experts in
qualitative or quantitative data and in product design. Chapter 17 provides a
detailed look at the skills required for a team that designs for behavior
change, including where you can find (or develop) them.


If you _are_ an expert in one of these areas, all the better. The book will show
you how designing for behavior change builds upon and complements your
existing expertise. You’ll find out how to leverage your existing skills to


play a leading role in the development of behaviorally effective products
and communications within your organization.

## **What Types of Behaviors This Can Help With**


The techniques I’ll talk about here assume that the product will support an
action that people aspire to but have had difficulty undertaking. Learning a
language. Sticking to a diet. Meeting new people. This may seem like it
applies only to a narrow set of products, but I’ve found that there are two
big groups of behaviors that fit these criteria:


Behaviors that users want to change _within their daily lives_


Behaviors _within the product itself_ that are part of using the
product effectively


Or, from the perspective of the company making the product, behavior
change is either:


The core value of the product for users


Required for users to extract the value of the product


In the first case, users have some behavioral problem in their daily lives and
buy the product to help them with it. In the second case, users have some
other need that the product solves, but they must adapt and change their
behavior in order for the product to deliver on its promise.


The first case includes:


Controlling diabetes


Paying off credit card debts


Getting back in shape


Getting involved in their communities


Often these behaviors relate to big-picture social issues like health and
wellness. When we design products that support these behaviors, we help
the individual and impact our society at the same time. Oracle Utilities’s
Opower and Google’s Nest, for example, are products that help individuals
decrease individual energy usage: saving people money and helping the
environment at the same time. Other products that change behavior in this
way are Fitbit (exercise) and Weight Watchers (diet).



As I send this book off for final production, the coronavirus COVID-19 is
spreading across the globe. We’ve seen a rapid mobilization in the
healthcare community, including work by behavioral scientists to help
promote social distancing and handwashing behavior.3 Researchers are
mounting large-scale, rapid turnaround studies to test techniques to keep
people safe—by applying behavioral science to the design of
communications and products.4 It’s an impressive display of the power of
behavioral science to help people take action that’s in the best interest of the
individual and society as a whole.5


The second type of behavioral change is far more mundane. Individuals
often seek to change behavior as a means to an end. Let’s say a user wants
to learn a new language and gets a software package to help do it. Simply
learning how to effectively use the software can take some substantial
changes in behavior _within the product_ —building new habits to log in daily
and practice the language, overcoming fears about looking foolish while
doing it, and so on. The user wants to take an action (learning the language)
but struggles. A well-designed product can help the user make those
personal adjustments.


This second type, and the products that require it, is much broader than the
first. It covers the sweep of voluntary changes in behavior that people might
make to benefit from products they’ve already chosen to use. It touches
upon a huge swath of the consumer product space, from Yelp to Square to
Rosetta Stone. Some examples of actions that occur _within software_
_products_ that one might try to improve include:


Organizing email contacts



3



4



5


Drawing decent flowcharts


Formatting documents


As with many other behavioral scientists and designers, I believe that no
design is neutral.6 Anything we design that interacts with other people—
communications, products, services, etc.—has an impact on their behavior
and ultimately their lives and outcomes. Here, we talk about how to make
that process intentional and, hopefully, beneficial.


For both types of behavior change, the goal is to develop products that help
users take action and to deliver the value that the company offers. This
voluntary, transparent support for behavior change helps companies be
successful as well.


## **What This Book Is Not About**

If you’re looking for a book on how to make people do something _you_ want
them to do (even if they don’t want to do it), you’re in the wrong place. I’m
not necessarily judging your motives or aims; I just can’t help you much.


In particular, this book isn’t designed to help with persuasion. There are
many ethical and thoughtful uses of persuasion—and we all seek to
persuade each other in our daily lives. While there are many similarities
with designing for _voluntary_ behavior change, other issues arise such as
educating users about a product, building a convincing argument, rhetorical
delivery, building rapport over time, and more. We won’t cover them here.
The topic of voluntary (i.e., pre-persuasion) behavior change is big enough
as it is!


In addition, this book isn’t intended to help with trickery or coercion (for
both practical and ethical reasons). Sadly, there are many companies trying
to do just that, though—and it’s dangerous for our field. I’ll delve into the
details of what’s happening across our industry and how we’re starting to
face well-deserved backlash from both government regulators and
thoughtful technologists in Chapter 4.

## **The Chapters Ahead**


In the following pages, I walk you through each of the skills you need to
design for behavior change, starting with a firm foundation in how the mind
makes decisions. Then, I show each step that’s required to develop a new
product: moving from discovery to design to implementation and
refinement. I introduce each concept where it is first needed. In Part III, I
step back and give some additional information on the scope of the industry
(and where the jobs are), how to build a behavioral team at your
organization, and likely problems you’ll face along the way. That’s it.


However, if you’re looking for a more formal chapter outline, here you go:


_Part I: How the Mind Works_


Chapter 1 arms you with your first skill: an understanding of how the
mind makes decisions. You’ll get an overview of the current literature
on decision making, as well as a dozen key lessons and their
implications for the design process.


Chapter 2 then describes the six high-level factors that must come
together at the same time for a person to take action. They form the
CREATE Action Funnel—Cue, Reaction, Evaluation, Ability, Timing,
and Experience—which shows you what needs to be addressed in your
product and where users usually drop off.


Chapter 3 looks at the reverse problem: how to help your users stop
unwanted habits or improve poor decisions.


Chapter 4 delves into detail about the ethical challenge facing the field:
how too many practitioners have used these techniques to manipulate
users into buying (or overusing) their products, how we’re fooling
ourselves if we think we wouldn’t do the same under the right (or
wrong) conditions, and how we can tackle these problems head on.


_Part II: A Blueprint for Behavior Change_


Chapter 5 introduces you to the larger process of designing for behavior
change—how your new knowledge about the mind can be used in
practice—using the acronym DECIDE: Define the problem, Explore the
context, Craft the intervention, Implement within the product,
Determine its impact, and Evaluate next steps.


Chapter 6 starts charting your course by defining the problem: the
overall outcomes you hope the product will deliver and who it seeks to
help. From there, it demonstrates how to elicit a potential idea for
behavior change—how, specifically, your users will get fit or take
control of their finances, for example.


Chapter 7 explores the context in which your users will act with a
behavioral map: a narrative of how the product team envisions user
interaction with the product and how users will change their behavior. It
then evaluates the various behaviors they _could_ change in light of their


needs, interests, and prior experience. It refines your initial plan to
finalize the specific behavior the product will support.


Chapter 8 introduces you to the meat of the DECIDE process: designing
the intervention itself. We look, at a high level, at the main strategies
you can use to help users change behavior, using the story of a fish
stranded on the beach.


In Chapters 9 and 10, we look at how to craft specific interventions,
based on behavioral research, to support your users to take action.
Chapter 9 presents interventions that are appropriate when users face
problems of Cue, Reaction, or Evaluation; next, Chapter 10 looks at
interventions for Ability, Timing, and Experience.


Chapter 11 wraps up the discussion of crafting an intervention with two
extensions: how you can handle multi-step complex interventions and
how to help the user hinder negative unwanted actions.


Chapter 12 presents some tips for implementing the intervention within
the product itself. Applied behavioral science doesn’t require a
particular development approach or technology; it does, however,
require high-quality data on outcomes. We discuss how to build those
metrics, and the ability to measure changes in them, in the initial
product development—rather than as a hacked-up afterthought.


Chapter 13 focuses on determining the product’s impact, its success or
failure. It starts with the most powerful tool there is for impact
measurement: the humble A/B test. Since most readers are likely
familiar with A/B tests already, this chapter dives into the details of how
to use it effectively to gather rigorous data and the common pitfalls that
practitioners face.


Chapter 14 looks at other ways to determine impact, when A/B tests or
other randomized control trials aren’t available. I cover how to utilize
statistical models to gain insight. I talk about the challenges of gauging
the causal impact of software on real-world behavior and how to
overcome them.


Chapter 15 concludes the DECIDE blueprint for behavioral design by
helping you Evaluate next steps after your implementation. It looks at
how to find problems that limit impact, including how qualitative and
quantitative analyses are both needed, and work hand in hand.


_Part III: Build Your Team and Make It Successful_


Chapter 16 provides the results from the Behavioral Teams survey in
detail. Case studies are scattered throughout the book, but here we dig
into the numbers: how large the field is, where the jobs are, and what
challenges and successes other teams are having.


Chapter 17 looks at what it takes to start applying behavioral science at
your organization with a team of 1 or a team of 20. We look at how to
make the case to stakeholders in-house and the skillset you or other
team members will need.


Finally, Chapter 18 wraps things up with a quick review of the
designing for behavior change process and key takeaways on how to
make it happen in your organization. It also covers many of the
questions that can arise when putting these lessons into practice.


At the end of the book, there’s information for those who are looking to
dive even deeper:


Glossary of Terms: a glossary of key terms, like _behavioral map_
and _data bridge_


Bibliography: a comprehensive list of the works cited in this book


In the first edition of this book, there was a list of online resources
[(Appendix B). We’ve moved that online. Each of the core chapters in Part I](https://www.behavioraltechnology.co/resources)
ends with “A Short Summary of the Ideas” if you only have a few minutes.
They are a useful wrap-up that also give advice if you’re just looking for an
informal process to sketch things out before you jump in head first.


The core chapters of Part II wrap up with “Putting It into Practice”—
sections with concrete examples and exercises to help you put each


chapter’s ideas to work.

## **Let’s Talk**


My hope with this book is to further the conversation about voluntary
behavior change and help build up the tools needed to develop behaviorally
effective products. However, even after writing two editions (and likely
even after 20) I have no illusions about the completeness of this work—
there’s still a tremendous amount to figure out. We’re all going to learn as
we go along.


Personally, I’m always looking to learn, share, and collaborate, so don’t
hesitate to reach out if you have a cool story to share, an idea for a research
project that would further develop the field, or an idea for a behaviorchanging project that you’d like to bounce off someone. You can find me
under _sawendel_ on Twitter, LinkedIn, and AngelList; my contact
information is on my website, _[http://about.me/sawendel](http://about.me/sawendel)_ .


If you think there’s something that can be improved in this book or find
something that is inaccurate, please reach out to me and tell me about it.
One of the many benefits of working with O’Reilly Media as a publisher is
that a lot of you will be reading this book in an electronic format and can
quickly get an updated version of the book if corrections need to be made.
For those who are reading this in paper form, I’ll keep a list of corrections,
additions, and other updates online at _[behavioraltechnology.co](https://behavioraltechnology.co/)_ .

## **O’Reilly Online Learning**


**NOTE**


For more than 40 years, _[O’Reilly Media](http://oreilly.com/)_ has provided technology and business training,
knowledge, and insight to help companies succeed.


Our unique network of experts and innovators share their knowledge and
expertise through books, articles, and our online learning platform.
O’Reilly’s online learning platform gives you on-demand access to live
training courses, in-depth learning paths, interactive coding environments,
and a vast collection of text and video from O’Reilly and 200+ other
publishers. For more information, visit _[http://oreilly.com](http://oreilly.com/)_ .

## **How to Contact Us**


Please address comments and questions concerning this book to the
publisher:


O’Reilly Media, Inc.


1005 Gravenstein Highway North


Sebastopol, CA 95472


800-998-9938 (in the United States or Canada)


707-829-0515 (international or local)


707-829-0104 (fax)


We have a web page for this book, where we list errata, examples, and any
additional information. You can access this page at
_[https://oreil.ly/designing-for-behavior-change](https://oreil.ly/designing-for-behavior-change)_ .


Email _[bookquestions@oreilly.com](mailto:bookquestions@oreilly.com)_ to comment or ask technical questions
about this book.


For news and information about our books and courses, visit
_[http://oreilly.com](http://oreilly.com/)_ .


Find us on Facebook: _[http://facebook.com/oreilly](http://facebook.com/oreilly)_


Follow us on Twitter: _[http://twitter.com/oreillymedia](http://twitter.com/oreillymedia)_


Watch us on YouTube: _[http://www.youtube.com/oreillymedia](http://www.youtube.com/oreillymedia)_

## **Permissions**


Since the first publication of _Designing for Behavior Change_, I’ve
continued to build upon and refine the theoretical and practical tools
presented in the book. The tools that I use with my own team, that I’ve
trained other companies and organizations with, are extensions of those
initial ideas (and indeed, the first edition itself was a description of our
practice and approach at HelloWallet at the time). In this edition, I’ve
brought together a number of those artifacts and lessons from applying this
approach over that last six years. In particular:


The exercises in the “Putting It in Practice” sections of Chapters 6–
[14 incorporate parts of a workbook I developed for my team at](https://oreil.ly/behavior-change-wkbk)
HelloWallet to apply these concepts.


Chapter 13 incorporates sections from a guide to experiments I
wrote for my team at Morningstar.


Chapters 1, 3, and 4 incorporate part of an introduction to
behavioral science that I wrote for a book exploring the
applications of behavioral science to one’s personal and spiritual
life.


Chapter 16 describes a survey I conducted in 2019 with the
nonprofit organizations the Behavioral Science Policy Association
and Action Design Network, and have published separately on our
websites.


In each case, the source material was used as a starting point, often with
significant adaptations and changes. All materials are used with permission.

## **Acknowledgments**


With the first edition of this book, I had many people to thank for their help
in developing the ideas and process presented within. The list has only
grown.


I continue to talk with and gain inspiration from people I started working
with on the first edition—from Rob Pinkerton and Katy Milkman to the
Action Design Team, especially Zarak Khan, Matthew Ray and Erik
Johnson. Here, I’d like to call attention to additional people I’ve learned
from since that first edition. Top of the list would be my intellectual
sparring partner, Ryan Murphy, and my team at Morningstar: Heymika
Bhatia, Sarwari Das, Jatin Jain, Sam Lamas, Sagneet Kaur, Alistair Murray,
Sarah Newcomb, Shwetabh Sameer, Stan Treger, and Leon Zeng. Many
thanks to Ray Sin as well, for your thoughtful research. Outside of
Morningstar, I’m particularly grateful to Paul Adams, Julián Arango,
Florent Buisson, May C., Jesse Dashefsky, Clay Delk, Barbara Doulas,
Darrin Henein, Fumi Honda, Peter Hovard, Anne-Marie Léger, Jens Oliver
Meiert, Brian Merlob, Shafi Rehman, Neela Saldanha, Nelson Taruc, and
Mark Wyner for their comments on the draft.


In terms of the rich stream of behavioral research that I draw upon here,
there are simply too many people than can be thanked. Even though it is not
the current fashion to do so in popular-press books, I make a point to cite
authors of the specific studies I reference throughout the body of the book,
though I don’t have space to offer a full literature review. For some readers,
this may seem overly academic or, frankly, boring. That’s certainly not my
goal! Rather, it is the simple acknowledgment of the many thoughtful
researchers who have done great work and that both I and you, as readers of
this book, benefit from. I want never to overstate my ingenuity or to dim the
glow of their bright light. My primary error, I fear, is not giving enough
credit to the amazing work of other researchers. Please accept my apologies
for any citations that are missing.


And as always, I’d like to thank Alexia, Luke, and Mark—for putting up
with me and my obsession with writing and for loving me nevertheless.


1 Thaler and Sunstein (2008), Gladwell (2005), Ariely (2008).


2 [Dan Lockton has a set of papers that provide an extensive review of the various domains in](https://danlockton.com/publications)

which intentional behavior change has been applied.


3 [See recommendations to the Irish government, for example.](https://oreil.ly/PPEYJ)


4 [Kwon (2020); Jachimowicz (2020)](https://oreil.ly/GwXA4)


5 We’ve also seen what happens when incomplete _lessons_ from behavioral science are divorced

from the _process_ of science (including rigorous testing and empirical validation)—in the furor
over the UK government’s initial resistance to strict social distancing based on the concept of
[behavioral fatigue. See Yates (2020) for the political debate, and UK Behavioural Scientists](https://oreil.ly/KdYx2)
(2020) for a thoughtful response calling for proper scientific testing of the concept before using
it in government policy with lives at stake.


6 In _Nudge_, Thaler and Sunstein make this case, for example, and a discussion of the

unintentional and intentional impact of design has long been a part of the design community
(e.g., Nusca 2019, Vinh 2018).


# **Part I. How the Mind Works**


# **Chapter 1. Deciding and Taking** **Action**

_On the day I got married, I was lying on the bathroom floor of the church_
_because my back hurt to move. I’d been out of commission and in bed for_
_almost three weeks, but now my family and my wife-to-be, Alexia, were_
_waiting for me in the aisles. My best man Paul had to pull me up from the_
_floor and get me out there to say my vows. My back had seized up weeks_
_before because I hadn’t been getting enough exercise._


_Now I was born skinny, but that hides the fact that I’ve had musculoskeletal_
_problems all my life—lower back problems, pinched nerves in my hands and_
_neck, and so forth. I’ve seen many doctors over the years, and they’ve all_
_said about the same thing: you’ll be OK, if you just exercise regularly._


_So I’ve long known about the importance of exercise; I don’t have a_
_problem with motivation. There’s nothing more motivating or scarier than_
_almost canceling your own wedding. I’ve certainly intended to exercise._
_But, like many other people who struggle with this, I haven’t done as much_
_as I should._


_For me, and for many others, there’s a gap between our sincere intention to_
_act and what actually happens. There’s something more going on in our_
_heads and in our lives than a simple cost–benefit analysis about what we_
_should do. Even though the benefits clearly outweigh the costs, we struggle._
_To change this pattern—to help ourselves and others take action when_
_needed—we must first understand how our minds are wired._


In my research and that of many other behavioral scientists in the field,
we’ve found that people don’t always make decisions and take action in a
straightforward way. People struggle to turn their intentions into action.
People struggle sometimes to make good decisions—even if, at another
time, they might have done fine.


We recognize this for ourselves and our own lives, but we tend to forget this
when it comes to our users. We assume that if they like our products, they’ll
use them. If they want to do something, they’ll figure out how. But they
don’t.


I’m not the only person who struggles with a lack of exercise. Many of your
users might too. Or, they struggle with poor eating or bad sleep habits or
distractions that keep them from their family and friends. Often, motivation
isn’t the problem: like me, they know what they should do and even want to
do it. Other things get in their way. This book is about how to help your
users, and all of us, change behavior when we need to.

## **Behavior Change…**


All around us, people try to change our and each other’s behavior. Negative
examples are often obvious: from ads that entice us to buy stuff we don’t
need to apps that try to swallow our attention and time. Positive examples
are there too, but perhaps not as obvious; for example, the loving parent
teaching a child to share. Support programs helping addicts break free from
their demons. Apps helping us track our weight and encouraging us as we
diet and exercise.


In a sense, we’re all in the “behavior change” business. When we’re falling
short of our own goals and want to make a change in our lives, that usually
means our behavior must change first. Moreover, we’re a social species; in
order to achieve our goals, even altruistic goals of helping another person
succeed, often someone must do something differently. To effect change _is_
to effect behavior change.


Yet we rarely talk about it that way. In the product world, we talk about
features delivered, user needs met, and so forth. Those things are all
important, certainly, but none of them matters unless people adopt and
apply our products (i.e., we need our users to change their behavior in a
meaningful way).


Perhaps we don’t talk about behavior change so directly because it’s
uncomfortable: we don’t want to be seen as manipulative or coercive. So
we end up with sanitized conversations distanced from real people changing
their behavior because of our products and communications: key
performance indicators for adoption and retention; objectives and key
results for click-through rates and usage.


It shouldn’t be that way. When we don’t talk about what we’re actually
doing, we are both less effective at helping others when we should and
more likely to try to change behavior in ways we shouldn’t. This book is
about designing products intentionally to change behavior—how to
ethically and thoughtfully help others succeed, without, I hope, falling into
trickery or manipulation.


In this book we’ll have an open discussion about how to help people decide
what to do and how to help them act on their intentions and personal goals.
We’ll talk about how to build products that influence that process and how
to assemble and run a team that does so. Nothing presented here is perfect,
but I hope this book can help you make better products and better serve
your users.

## **…And Behavioral Science**


One of the best toolsets to accomplish this task—intentionally designing for
behavior change—comes from behavioral science. And, in addition to being
useful, behavioral science is fascinating.


Behavioral science is an interdisciplinary field that combines psychology
and economics, among other disciplines, to gain a more nuanced
understanding of how people make decisions and translate those decisions
into action. Behavioral scientists have studied a wide range of behaviors,
from saving for retirement to exercising.1 Along the way, they’ve found
ingenious ways to help people take action when they would otherwise
procrastinate or struggle to follow through.


One of the most active areas of research in behavioral science is how our
environment affects our choices and behavior, and how a change in that
environment can then affect those choices and behaviors. Environments can
be thoughtfully and carefully designed to help us become more aware of
our choices, shape our decisions for good or for ill, and spur us to take
action once we’ve made a choice. We call that process _choice architecture_,
or _behavioral design_ .


Over the past decade, there has been a tremendous growth of research in the
field and also of best-selling books that share its lessons, including Richard
Thaler and Cass Sunstein’s _Nudge_, Daniel Kahneman’s _Thinking, Fast and_
_Slow_, and Dan Ariely’s _Predictably Irrational_ .2 They give fun introductions
to the field, including anecdotes of how:


Putting a picture of a fly in the center of a men’s urinal can help
reduce the mess that men make far more than exhorting them not
to make a mess.


Giving people many small bags of popcorn makes them eat less of
it.3


In fact, Thaler and Kahneman have each won the Nobel Prize largely
because of their work in behavioral science.


That said, we’re not trying to re-create _Nudge_ or _Predictably Irrational_
here. This book is about _how to apply lessons from behavioral science to_
_product development_ ; in particular, how to help our users do something they
want to do, but struggle with. Whether that’s dieting, spending time with
their kids, or breaking a social media app’s hold on their lives. It’s about
arming you with a straightforward process to design for behavior change _._


Some of those lessons are what you’d expect: when designing a product,
look out for unnecessary frictions or for areas where a user loses selfconfidence. Build habits via repeated action in a consistent context. Some
of those lessons are far less expected, and you may not even want to hear
them; for example, most products, most of the time, will have no unique
impact on their user’s lives. For that reason, we need to test early and often,


and use rigorous tools to do so. Other lessons are simply fun and surprising;
for example, make text _harder_ to read if it’s important that users make a
careful and deliberative decision.


With that, let’s dive into a primer on behavioral science!




## **Behavioral Science 101: How Our Minds Are** **Wired**

Last summer, my family and I were on vacation and having a great time.
One afternoon, we decided we’d eaten out way too much and we wanted
something cheaper and more familiar than another restaurant meal. So we
went to a grocery store.


Now, the first thing we looked for was cereal. We found the aisle and there
were far too many options to choose from. As they often do, our kids were
running up and down the aisle, pulling and swinging each other around.
Somehow, all of that movement makes them unable to hear us telling them
to stop. It’s clearly loads of fun—until they crash into something. So we had
to make a quick decision.


Unfortunately, my kids and I have lots of allergies. My allergies are lethal,
and my kid’s allergies cause pain but thankfully not too much more. So as
we’re standing in the aisle trying to make a choice and keep our kids out of
trouble, my wife and I were torn: we simply couldn’t read all of the boxes
for their ingredients.


Thankfully, we have some simple rules we know to follow. Any cereal with
cartoons on the box is automatically out; those are often crammed full of
sugar, and our kids have enough energy already. Second, cereals that are
gluten free (which one of our sons needs) usually proclaim it proudly on the
box—easy to scan for. And third, after decades of practice, I have a really
useful habit: I automatically pick up food and recognize ingredients on the
list that would kill me. It only takes a split second and I hardly think about
it unless I see something that’s a problem.


After a little while, we picked up a nice bag of corn flakes, grabbed a box of
some granola-like stuff, and went on to the next aisle. No problem.
Unfortunately, we did forget to grab milk and a few other things in that
aisle. We’d intended to get them, but in the moment, we missed those items
on our mental checklist.


Now, when we got home, the granola stuff was actually really good. The
corn flakes were terrible—in all of the hurry, we missed a key sign: dust on
the bag. They’d been sitting there a long time, and everyone else clearly
knew not to buy them.


In everyday life and in (true) stories like this one, we can find the core
lessons of behavioral science if we know where to look. I like to start with a
basic, and often overlooked, one: as human beings, we’re all limited. We
can’t instantly know which cereal is best just by thinking about them. We
have to take time and energy to sort through the options and make a
decision. That time and energy is scarce—if we spend too much time on
one thing, there’s a cost (like our kids crashing to the shelves). Similarly,
we’re limited in our attention, our willpower, our ability to do math in our
heads, and so on. You get the picture.


Our limitations aren’t _bad_, per se; they just are facts of life. For example, I
can’t even imagine what it would mean to have _unlimited attention_ —to be
simultaneously aware of absolutely everything at once. That’s just not how
we’re made.


Given these limitations, our minds are really good at making the best of
what we have. We _economize_ on our time, attention, and mental energy by
using simple rules of thumb to make decisions; for example, by excluding
cereals with cartoons. As researchers, we call these results of thumb
_heuristics_ . Another way our minds economize is by making split-second
_nonconscious_ judgments; for example, _nonconscious habits_ are automated
associations in our heads that trigger us to take a particular action when we
see a specific trigger (like scanning for deadly ingredients whenever I see
unknown food). Habits free up our conscious minds to think about other
things.


While these economizing techniques are truly impressive, they aren’t
perfect. They falter in two big ways. First, we don’t always make the right
decision; for example, sometimes we don’t pay attention to something
important (dust on the bag). As researchers, we often call the results of a
heuristic or other shortcut going awry a _cognitive bias_ : a systematic


difference between how we’d expect people to behave in a certain
circumstance and what they actually do.4 Second, even when we make the
right choice, our inherent human limitations mean we don’t always follow
through on our intentions (getting the milk). We call that the _intention–_
_action gap_ .


And finally, context matters immensely. It mattered that our kids were
running around; we had less of our limited attention to pay to the task
(reading ingredients, remembering milk). If milk were in a different aisle,
we might have seen it and remembered it. If our kids weren’t running
around…never mind. That wouldn’t happen.


So, if I were to put decades of behavioral research into a few bullet points
(please forgive me, my fellow researchers!), it would be these:


_We’re limited_ beings in attention, time, willpower, etc.


_We’re of two minds_ : our actions depend on both conscious thought
and nonconscious reactions, like habits.


In both cases, our minds _use shortcuts_ to economize and make
quick decisions because of these limitations.


Our decisions and our behavior are _deeply affected by the context_
we’re in, worsening or ameliorating our biases and our intention–
action gap.


One can _cleverly and thoughtfully design a context_ to improve
people’s decision making and lessen the intention–action gap.


Let’s look at each of these points in a bit more detail.

### **We’re Limited**


Who hasn’t forgotten something at some point in their lives? Heck, who
hasn’t forgotten something in the last hour, or the last five minutes?
Forgetfulness is one of our many human frailties. Personally, the older I get,
the longer that list seems to grow. There are sadly many ways in which our


minds are limited and lead us to make choices that aren’t the best, including
limited attention, cognitive capacity, and memories.


These limitations string together. In terms of our _attention_, there are nearly
an infinite number of things we could be paying attention to at any moment.
We could be paying attention to the sound of our own heartbeat, the person
who is trying to speak to us, the interesting conversation someone else is
having near us, or the report that’s overdue and we need to complete.
Unfortunately, researchers have shown again and again that our conscious
minds can really pay proper attention to only one thing at a time. Despite all
of the discussion in the popular media about multitasking, multitasking is a
myth.5 Certainly we can _switch_ our attention back and forth; we can move
from focusing on one thing to focusing on another—and we can do so again
and again and again. But the reality is, switching focus frequently is costly;
it slows us down, and it makes it harder for us to think clearly. Given that
we can only focus on one thing at a time and that there are so many things
that we could focus on (many of them urgent and interesting), it’s no
wonder that sometimes we aren’t thinking about what we’re doing.



Similarly, our _cognitive capacity_ is limited: we simply can’t hold many
unrelated ideas or pieces of information in our minds at the same time. You
may have heard the famous story about why phone numbers in the United
States are seven digits plus an area code: researchers found that we could
hold seven unrelated numbers in our heads at a time, plus or minus two.6
And, of course, there are so many other ways in which our cognitive
capacity is limited. For one, we have a particularly difficult time dealing
with probabilities and uncertain events, and with realistically predicting the
likelihood of something happening in the future. We tend to over-predict
rare but vivid and widely reported events like shark attacks, terrorist
attacks, and lightning strikes.7



6



7



In addition, we can become overwhelmed or paralyzed when faced with a
wide range of options, even as we consciously seek out more choices and
options. Researchers call this the _paradox of choice_ : our conscious minds
believe that having more choices is almost always better, but when it
actually comes time to make a decision and we’re faced with our limited


cognitive capacity and the difficulty of the choice ahead of us, we may
balk.8


Lastly, when it comes to our memories, they simply aren’t perfect, and
nothing is going to change that. And, for most of us, having a “not perfect”
memory is a significant understatement. Our memories usually aren’t
crystal-clear videos, but a set of crib notes from which we reconstruct
mental videos and pictures. We remember events that occur frequently (like
eating breakfast) in a stylized format, losing the details of the individual
occurrences and remembering instead a composite of that repeated
experience. Additionally, in some circumstances, we remember the peak
and the end of an extended experience, not a true record of its duration or
intensity.9


What do all of these cognitive limitations mean? They are important to
product people for two main reasons. First, these cognitive limitations mean
that _sometimes our users don’t make the best choices_, even when something
is in their best interest _._ It’s not that they’re bad people; it’s that they are,
simply, people. They get distracted, they forget things, they get
overwhelmed. We shouldn’t interpret a few bad choices as a sign that they
are fundamentally disinterested in doing better (or using our product);
instead, it’s just that their simple human frailties may be at work. We can
design products to avoid overburdening users’ limited faculties.10


Second, our limitations matter because our minds cleverly work around
them by having two semi-independent systems in the brain and by using
lots and lots of shortcuts. When developing products and communications,
we should understand those shortcuts and use them to our advantage or
work around them.


### **We’re of Two Minds**



You can think about the brain as having two types of thinking: one is
deliberative and the other is reactive; it’s a useful metaphor for a complex
underlying process.11 Our reactive thinking (aka _intuitive_, or System 1) is
blazingly fast and automatic, but we’re generally not conscious of its inner
workings. It uses our past experiences and a set of simple rules of thumb to
almost immediately give us an intuitive evaluation of a situation—an
evaluation we feel through our emotions and through sensations around our
bodies like a “gut feeling.”12 It’s generally quite effective in familiar
situations, where our past experiences are relevant, and does less well in
unfamiliar situations.


Our deliberative thinking (aka _conscious_, or System 2) is slow, focused,
self-aware, and what most of us consider “thinking.” We can rationally
analyze our way through unfamiliar situations and handle complex
problems with System 2. Unfortunately, System 2 is woefully limited in
how much information it can handle at a time—like struggling to hold more
than seven unrelated numbers in short-term memory at once! It thus relies
on System 1 for much of the real work of thinking. These two systems can



11



12


work independently of each other, in parallel, and can disagree with each
other—like when we’re troubled by the sense that, despite our careful
thinking, “something is just wrong” with a decision we’ve made.13



What this means is that we’re often not “thinking” when we act. At least,
we’re not choosing consciously. Most of our daily behavior is governed by
our intuitive mode. We’re acting on habit (learned patterns of behavior), on
gut instinct (blazingly fast evaluations of a situation based on our past
experiences), or on simple rules of thumb (cognitive shortcuts or heuristics
built into our mental machinery).14 Researchers estimate that roughly half
of our daily lives are spent executing habits and other intuitive behaviors,
and not consciously thinking about what we’re doing.15 Our conscious
minds usually become engaged only when we’re in a novel situation, or
when we intentionally direct our attention to a task.16



14



15



16



Unfortunately, our conscious minds believe that they are in charge all the
time, even when they aren’t. In his book, _The Happiness Hypothesis_
(Cambridge 2006) _,_ philosopher Jonathan Haidt builds on the Buddha’s
metaphor of a rider and an elephant to explain this idea. Imagine that there
is a huge elephant with a rider sitting atop it. The elephant is our immensely
powerful but uncritical, intuitive self. The rider is our conscious self, trying
to direct the elephant where to go. The rider thinks it’s always in charge, but
it’s the elephant doing the work; if the elephant disagrees with the rider, the
elephant usually wins.


To see this in action, you can read fascinating studies of people whose left
and right brains have been surgically separated and can’t (physically) talk to
one another. The left side makes up convincing but completely fabricated
stories about what the right side is doing.17 That’s the rider standing on top
of an out-of-control elephant crying out that everything is under control!18
Or, more precisely, crying out that every action that the elephant takes is
absolutely what the rider wanted them to do—and _the rider actually_
_believes it._



17



18



Thus, we can _do_ one thing and _think_ about something different at the same
time. We might be walking to the office, but we’re actually thinking about


all of the stuff we need to do when we get there (Figure 1-1). The rider is
deeply engaged in preparing for the future tasks, and the elephant is doing
the work of walking. In order for behavior change to occur, we need to
work with both the rider and elephant.19


_Figure 1-1. While the mind consciously thinks about what needs to be done at work, the subconscious_

_mind keeps the body walking (habits and skills), avoids shadowy alleys (an intuitive response), and_

_follows the sweet smell of a bakery (habit)_


### **We Use Shortcuts, Part I: Biases and Heuristics**

Both our conscious minds and our nonconscious minds rely heavily on
shortcuts to make the best of our limited faculties. Our minds’ myriad
shortcuts (heuristics) help us sort through the range of options we face on a
day-to-day basis and make rapid, reasonable decisions about what to do.


These heuristics are a mix of rules we use throughout our lives with obvious
consequence:


_Status quo bias_


If you’re faced with many options to choose from and you can’t devote

time and energy to think them through, or you aren’t sure what to do

with them, what’s generally the best thing to do? Don’t change

anything. _We should generally assume people will stick with the status_

_quo_ . That’s true whether it’s a deep-seated historical status quo or one

that is arbitrarily chosen and presented as the status quo: to change is to

risk loss.20


_Descriptive norms—we’re deeply affected by social signals_


Another way we handle uncertainty in a decision is to look at what other

people are doing and try to do the same (aka _descriptive norms_ ).21 This

is one of our most basic shortcuts. For example, “People here are

drinking and having a good time, so it’s OK if I do as well.”


_Confirmation bias_


We tend to seek out, notice, and remember information already in line

with our existing thinking.22 For example, if someone has a strong

political view, they may notice and remember news stories that support

that view and forget those that don’t. In a sense, this tendency allows


our minds to focus on what appears to be relevant in a sea of

overwhelming information. It has a side effect, though: it leads us to

ignore new information that might help us gain a truer picture of the

world or try new things.


_Present bias_


Our limited attention also applies to _time_ : we can only focus on a single

moment at once. Our minds appear to use a simple shortcut: what seems

to be most important? The present. We give undue attention to the

present and value things we get now over future benefits, even if it puts

our long-term health and welfare at risk. While formally studied in

economics since the 1990s, the concept is an ancient one: the desire for

instant gratification and the procrastination that comes with it.23


_Anchoring_


It’s often quite difficult to make a clear and thorough assessment of an

answer. And so, when we don’t know a number—like the probability of

an event or the price of an object—we often start with an initial estimate

(whether our own or one provided to us) and make adjustments up or

down based on additional information and feedback. Unfortunately,

these adjustments are often insufficient—and the initial anchor has a

strong effect on the results.24 Anchoring is one of many ways in which

we make judgments that are _relative to a reference point_ .


Others are interesting and seemingly narrow shortcuts that guide how we
act, like these:


_Availability heuristic_


When things are particularly easy to remember, we believe that they are

more likely to occur.25 For example, if I’d recently heard news about a

school shooting, I’d naturally think that it is much more common than it

actually is.


_IKEA effect_


When we invest time and energy in something—even if our contribution

is objectively quite small—we tend to value the resulting item or

outcome much more.26 For example, after we’ve assembled IKEA

furniture, we often value it more than similar furniture someone else

assembled (even if it’s of higher quality)—our sweat equity doesn’t

matter in terms of market value, but it does to us.


_Halo effect_


If we have a good assessment about someone (or something) overall, we

sometimes judge other characteristics of the person (or thing) too

positively—as if they have a “halo” of skill and quality.27 For example,

if we like someone personally, we might overestimate their skill at

dancing, even if we knew nothing about their dancing ability.


There are over a hundred of these shortcuts (heuristics) or other tendencies
of the mind (biases) that researchers have identified. Unfortunately, these
shortcuts can also lead us astray as we try to make good choices in our
lives. For example, if you’re a religious person living in a place where
people don’t speak about religion, descriptive norms apply a subtle (or notso-subtle) pressure to avoid doing so yourself. Or a homeless person might
look and smell dirty, and the (negative) halo effect could lead others to
think negatively about them; they might see the person as less honest and
less smart than they really are. While I’ve mentioned some negative


outcomes from our shortcuts and biases, it’s important to understand that, at
their root, our shortcuts are clever ways to handle the limited resources that
our minds have.


Let’s take a closer look at another way in which our minds economize:
habits.


### **We Use Shortcuts, Part II: Habits**



We use the term _habit_ loosely in everyday speech to mean all sorts of
things, but a concrete way to think about one is this: a habit is a repeated
behavior that’s triggered by cues in our environment. It’s _automatic_ —the
action occurs outside of conscious control, and we may not even be aware
of it happening.28 Habits save our minds work; we effectively _outsource_
control over our behavior to cues in the environment.29 That keeps our
conscious minds free for other, more important things, where conscious
thought really is required.



28



29



Habits arise in one of two ways.30 First, we can build habits through simple
repetition: whenever you see X (a _cue_ ), you do Y (a _routine_ ). Over time,
your brain builds a strong association between the cue and the routine and
doesn’t need to think about what to do when the cue occurs—it just acts.
For example, whenever you wake up in the morning (cue), you get out of
bed at the same spot (routine). Rarely do you find yourself lying in bed,
awake, agonizing over which exact part of the bed you should exit by.
That’s how habits work—they are so common, and so deeply ingrained in
our lives, that we rarely even notice them.


Sometimes there is also a third element, in addition to a cue and routine: a
_reward_, something good that happens at the end of the routine. The reward
pulls us forward—it gives us a reason to repeat the behavior. It might be
something inherently pleasant, like good food, or the completion of a goal
we’ve set for ourselves, like putting away all of the dishes.31 For example,
whenever you walk by the café and smell coffee (cue), you walk into the
shop, buy a double mocha espresso with cream (routine), and feel
chocolate-caffeine goodness (reward). We sometimes notice the big habits
—like getting coffee—but other, less obvious habits with rewards (checking
our email and receiving the random reward of getting an interesting
message) may not be noticed.


Once the habit forms, the reward itself doesn’t directly drive our behavior;
the habit is automatic and outside of conscious control. However, the mind
can “remember” previous rewards in subtle ways, intuitively wanting (or



30



Sometimes there is also a third element, in addition to a cue and routine: a
_reward_, something good that happens at the end of the routine. The reward
pulls us forward—it gives us a reason to repeat the behavior. It might be
something inherently pleasant, like good food, or the completion of a goal
we’ve set for ourselves, like putting away all of the dishes.31 For example,
whenever you walk by the café and smell coffee (cue), you walk into the
shop, buy a double mocha espresso with cream (routine), and feel
chocolate-caffeine goodness (reward). We sometimes notice the big habits
—like getting coffee—but other, less obvious habits with rewards (checking
our email and receiving the random reward of getting an interesting
message) may not be noticed.


32



craving) them.32 In fact, the mind can continue wanting a reward that it will
never receive again, and may not even enjoy when it does happen!33 I’ve
encountered that strange situation myself—long after I formed the habit of
eating certain potato chips, I still habitually eat them even though I don’t
enjoy them and they actually make me sick.34 This isn’t to say that rewards
aren’t important after the habit forms—they can push us to consciously
repeat the habitual action and can make them even more resistant to change.


The same characteristics that make habits hard to root out can be
immensely useful. Thinking of it another way, once “good” habits are
formed, they provide the most resilient and sustainable way to maintain a
new behavior. Charles Duhigg, in _The Power of Habit_ (Random House,
2012), gives a great example. In the early 1900s, advertising man Claude C.
Hopkins moved American society from being one in which very few people
brushed their teeth to a majority brushing their teeth in the span of only 10
years. He did it by helping Americans form the habit of brushing:35



33



34


_Figure 1-2. Pepsodent advertisement from 1950, highlighting a cue to trigger the habit of tooth-_

_[brushing (courtesy of Vintage Adventures)](http://vintage-adventures.com/)_


He taught people a cue—feeling for tooth film, the somewhat
slimy, off-white stuff that naturally coats our teeth (apparently, it’s
harmless in itself) (Figure 1-2).


When people felt tooth film, the response was a routine—brushing
their teeth (using Pepsodent, in this case).


The reward was a minty tingle in their mouths—something they
felt immediately after brushing their teeth.


Over time, the habit (feel film, brush teeth) formed, strengthened by the
reward at the end. And so did a craving—wanting to feel the cool tingling
sensation that Pepsodent caused in their mouths that people associated with
having clean, beautiful teeth.


Stepping back from Duhigg’s example, let’s look again at the three pieces
of a reward-driven habit:


The _cue_ tells us to act now. The cue is a clear and unambiguous
signal in the environment (like the smell of coffee) or in the
person’s body (like hunger). BJ Fogg and Jason Hreha categorize
the two ways that they work on behavior into _cue behaviors_ and
_cycle behaviors_ based on whether the cue is something else that
happens and tells you it’s time to act (brushing teeth after eating
breakfast) or the cue occurs on a schedule, like at a specific time of
day (preparing to go home at 5 p.m. on a weekday).36


The _routine_ can be something simple (hear phone ring, answer it)
or complex (smell coffee, turn, enter Starbucks, buy coffee, drink
it), as long as the scenario in which the behavior occurs is
consistent. Where conscious thought is not _required_ (i.e.,
consistency allows repetition of a previous action without making
new decisions), the behavior can be turned into a habit.


The _reward_ can occur every time—like drinking our favorite brand
of coffee—or on a more complex _reward schedule_ . A reward
schedule is the frequency and variability with which a reward
occurs each time the behavior occurs. For example, when we pull
the arm or press the button on a slot machine, we are randomly
rewarded: sometimes we win, sometimes we don’t. Our brains _love_
random rewards. In terms of timing, rewards that occur
immediately after the routine are best—they help strengthen the
association between cue and routine.


Researchers are actively studying exactly how rewards function, but one of
the likely scenarios goes like this: when these three elements are combined,


37



over time the cue becomes associated with the reward.37 When we see the
cue, we _anticipate_ the reward and it tempts us to act out the routine to get it.
The process takes time, however—varying by person and situation from a
few weeks to many months. And again, the desire for the reward can
continue long after the reward no longer exists.38



38


### **We’re Deeply Affected by Context**

And finally, we turn to the last big lesson: _the importance of context_ on our
behavior _._ What we do is shaped by our contextual environment in obvious
ways, like when the architecture of a building focuses our attention and
activity toward a central courtyard. It’s also shaped in nonobvious ways by
the people we talk and listen to (our _social environment_ ), what we see and
interact with (our _physical environment_ ), and the habits and responses
we’ve learned over time (our _mental environment_ ). These nonobvious
effects can show themselves even in slight changes in wording of a
question. We’ll examine how the environment affects human behavior
throughout this book, but let’s start with one famous example:


Suppose there’s an outbreak of a rare disease, which is expected to
kill six hundred people. You’re in charge of crafting the
government’s response.


You have two options:


Option A will result in two hundred people saved.


Option B will result in a one-third probability that six hundred
people will be saved and a two-thirds probability nobody will be
saved.


_Which option would you choose?_


Now suppose there’s another outbreak of a different disease, which is also
expected to kill six hundred people. You have two options:


Option C will result in the certain death of four hundred people.


Option D will result in the one-third probability that nobody dies
and two-thirds probability everyone dies.


_Which option would you choose now?_


Presented with these options, people generally prefer Option A in the first
situation and Option D in the second. In Tversky and Kahneman’s early
studies using these situations,39 72% of people choose A (versus 28% for
B), but only 22% choose C (versus 78% for D). Which, as you’ve probably
caught on, doesn’t make much sense, since for both A and C, four hundred
people face certain death and two hundred will be saved. Logically, if
someone prefers A, that person should also choose C. But that isn’t what
happens, on average.


Many researchers believe there is such a stark difference in people’s choices
for these two mathematically equivalent options (A and C) _because of how_
_the choices are framed._ One is framed as a _gain_ of two hundred lives and
the other is framed as a _loss_ of four hundred lives.40 The text of C leads us
to focus on the loss of four hundred lives (instead of the simultaneous gain
of two hundred), while the text of A leads us to focus on the gain of two
hundred lives (instead of the loss of four hundred). And people tend to
avoid uncertain or risky options (B and D) when there is a positive or _gain_
frame (A versus B) and seek risks when faced with a negative or _loss_ frame
(C versus D).


That’s, well, _odd._ It shows how relatively minor changes in wording can
lead to radically different choices. However, it is especially odd since this
isn’t something that people would explain themselves. If they were faced
with both sets of choices, they wouldn’t say, “Well, I recognize that A and
C have exactly the same outcomes, but I just intuitively don’t like thinking
about a loss, even when I know it’s a trick of the wording.” Instead, the
person might simply say: “knowing that I can save people is important (A),
and I really don’t like the thought of knowingly letting people go to certain
death (C).”


Or to use the rider and elephant metaphor again, the rider thinks they’re in
control, but the elephant really is. Our conscious rider explains our behavior


after it’s happened, without knowing the real reason. We are, as social
psychologist Tim Wilson nicely puts it, “strangers to ourselves.”41 To bring
this back to product development, our users take actions that they don’t
understand but will try to explain after the fact.


Our lack of self-knowledge also extends to what we’ll do in the future.
We’re bad at forecasting the level of emotion we’ll feel in future situations
and at forecasting our own behavior in the future.42 For example, people
can significantly overestimate the impact of future negative events on their
emotions, such as a divorce or medical problem. We’re not only affected by
the details of our environment, we don’t often recognize that our
environment has affected us in the past, so we don’t consider the influence
when we’re thinking about what we’ll do in the future. In a product
development context, this means that asking people what they will do or
what they think will happen to them in the future is fraught with problems.


Tversky and Kahneman’s study demonstrates one of the key principles of
behavioral science: reference dependence. In absolute terms, outcomes of
options A and C are identical. But the first frame sets the reference point as
people dying and the potential to save them; the second sets the reference
point as people living and the potential to let them die. Whether something
is a loss or a gain depends on our reference point. And, as you can see in
Tversky and Kahneman’s study, that reference point is malleable: it’s
subject to design.

### **We Can Design Context**


Because our environment affects our decision making and behavior,
redesigning that environment can change decision making and behavior. We
can thoughtfully develop product designs and communications that take this
knowledge into account and help people make better decisions, use habits
wisely, and follow through on their intentions to act, which is the focus of
the rest of this book.

## **What Can Go Wrong**


We’ve touched upon the areas in which the quirks of our minds can lead to
bad outcomes a bit already. It’s useful to make these areas more explicit and
clearer, though, since that understanding is the foundation of making things
better. We can distinguish two major branches of research, both of which
are useful for our purposes. Broadly, behavioral science helps us understand
quirks of _decision making_ and quirks of _action_ .

### **Quirks of Decision Making**


The shortcuts that our minds use lead us to rapid and generally good
decisions without evaluating all of the options thoroughly. They’re
necessary, letting us make the best of our limited faculties, and are generally
very helpful—until they aren’t.


Think about what happens when you’re visiting a new town and you’re
walking around looking for a bite to eat:


You might look on your phone to see which restaurant has the
highest and most ratings. Or, you might peek in the window to see
where other people are eating—it’s never a good sign if a place is
deserted, right? That’s the _social proof_ heuristic: if you aren’t sure
what to do, copy what other people are doing.


You might have seen ads touting a particular restaurant, and when
you pass by the sign, it catches your eye. If you’ve at least heard of
it, that’s good! The _availability heuristic_ supports that feeling.


You might notice a chain you’ve been to and liked recently and
figure that what’s been good recently probably will be good again.
That, among other things, is a _recency bias_ helping you choose.


You might look at their prices and see that one place is offering
burgers at $10, and another at $2. You’re all for saving money, but
that’s just too much: there must be something wrong with the $2
place. That’s the shortcut of _price as a signal of quality_ .


In each case, the shortcuts help us make quick decisions. None of them is
perfect, certainly. We could find ways to make them better, but by and large,
these are all reasonable choices. Most importantly, they are fast: they save
us from spending hours and hours reviewing all of the pros and cons of
each restaurant in the city, judging them in terms of their taste and nutrition
on 50 dimensions, the time to reach each one, their ambiance and likely
social environment, and so on. Shortcuts like these make decisions possible
and avoid decision paralysis.


Switching contexts, let’s think about investing money in the stock market.
You’ve recently received a windfall and you’re looking to invest some of it
for the future. You don’t have much experience in investing, so what do you
do?


You might look online to see what everyone else is talking about
and investing in, using social proof. Awesome! Except that’s how
bubbles are made: think Bitcoin or the dot-com bubble.


You might invest in things you’ve heard of, using the _availability_
_heuristic_ . Excellent! Except, again, that’s how bubbles are made.


You might look at what’s performed well in the past and invest in
that, using _recency bias._ The problem is that past performance
doesn’t predict future performance. Not a great guide.


You might look at prices—if a stock has a really high price, it must
be a good investment, right? OK, you know where that goes.


And so forth. You get the picture.


When shortcuts work well, we often don’t notice them; we effortlessly and
quickly come to a decision. Or, in the rare cases we do notice them, we call
them _clever_ . In the research community, we refer to them, in the positive
sense, as fast and frugal heuristics (where heuristic is another word for
shortcut).43


When the same shortcuts get us into trouble, however, we call them foolish:
how could I have been so stupid as to follow the crowd? Since you’re


reading this book, you’ve probably come across the term _bias_, which is
intimately related to these shortcuts. A bias, strictly speaking, is a tendency
of thought or action. It is neither positive nor negative; it just is. Most
people, including many researchers, use it explicitly in the negative sense,
as in a “deviation from an objective standard, such as a normative model”
of how people _should_ behave.44 A shortcut or heuristic gone awry creates a
bias.


Once we call something a bias, it’s easy to jump to the logical conclusion:
well, we just need to get rid of them! Remove people’s biases! It’s not that
simple. It’s precisely because these shortcuts are so clever and smart that
they are hard to change. If we simply did foolish things, we’d eventually
learn not to do them (either in our own lives or across the history of our
species). But these shortcuts are not foolish at all: they are immensely
valuable. They are sometimes out of context and used at the wrong time.
We can’t and shouldn’t be able to simply stop social proof or the
availability heuristic. That would wreak more havoc than it would solve.


The reality is that _we can’t completely avoid_ using mental shortcuts. Rather,
by understanding how our conscious and nonconscious shortcuts are
triggered by the details of our environment, we can learn to avoid some of
the negative outcomes that result from their use. So the first challenge of
behavioral science—of designing for behavior change—is to help people
make better decisions, given the valuable but imperfect shortcuts we all use.

### **Quirks of Action**


_I, myself, am made entirely of flaws, stitched together with good_
_intentions._

—Augusten Burroughs


Behavioral science also helps us understand the quirks of our behavior,
above and beyond our decisions, especially why we decide to do one thing
and actually do something else. This understanding starts with the same
base as for decisions: that we’re limited beings with limited attention,
memory, willpower, etc. Our minds still use clever shortcuts to help us


economize and avoid taxing our limited resources. But these facts make
themselves felt in different ways after we’ve made a decision. In particular,
we have errors of inaction and errors of unintentional action.


In the research literature, the _intention–action gap_ is one of the major errors
of inaction. We’ve all felt this gap in one way or another. For example, do
you have a friend with a gym membership, or exercise equipment at home,
that they just don’t use that often? Do they really enjoy giving money to a
gym? Of course not. They really intended to go to the gym when they first
signed up, or to use that fancy machine when they first bought it. It’s just
that they didn’t. The benefits of the gym are still clear. And despite all of
their past failures, they keep hoping and believing that they’ll get it together
and go regularly. But something else gets in the way that _isn’t_ motivation.
So they keep paying—and keep failing to go.


With the intention–action gap, the intention to act is there, but people don’t
follow through and act on it. It’s not that people are insincere or lack
motivation; the gap happens because of how our minds are wired. It
illustrates one of the core lessons of behavioral science: _good intentions and_
_the sincere desire to do something, aren’t enough_ .


And unintentional action? I don’t mean revelry that we regret the next
morning. Rather, I mean behaviors that we don’t intend even while we’re
doing them, often because we aren’t aware or thinking about them. One
cause of these we’ve already looked at: habits. Our habits allow us to take
action without thought—effortlessly riding a bike, navigating the interface
of common applications, or playing sports. But naturally, they can also go
awry.


Do you know someone who just can’t stop eating junk food? Each night,
when they get home tired and need a break, on the way to the couch, they
pick up a candy bar and a bag of chips and sit down with the laptop to
watch videos. An hour or so later, they take a break and notice the
crumpled-up wrapper and bag and throw them away. They’re still hungry
and hardly noticed the snacks on their way into their mouth.


There are many other examples, like when we get hooked on cigarettes (it
appears the _habit_ is more powerful than the nicotine, in fact),45 on latenight TV binging, or on incessantly checking social media apps. Habits, as
learned patterns of behavior, are inherently neutral. We learn bad habits just
as we learn good habits: through repetition. Our minds automate them in
order to save us cognitive work. For the person eating junk food, maybe it
was a particularly rough time at work, or maybe it was when they first
moved to the city and didn’t know where to get good groceries that set up
the automated routine. Regardless of the source, once that junk food habit
was set, it was hard to shake.


Just as with our decision-making shortcuts, try to imagine a world in which
we didn’t have habits—one where we had to carefully think though every
decision, every action, as if we were a teenager first learning to drive a car.
We’d be exhausted wrecks in no time. We can’t not rely on habits, nor ask
users of our products not to do so. Rather, as developers of behaviorchanging products and communications, we need to understand them and
work with (or around) them. Shortcuts gone awry, habits that people wish
they didn’t have, and the yawning gap between people’s intentions and their
actions: these are the problems that we’re here to solve. These are why we
design for behavior change.


## **A Map of the Decision-Making Process**

We’ve talked about the different ways in which our minds make our
decisions, from careful deliberative thought to shortcuts to fully automated
habits. We can think about these mental tools as being part of a spectrum,
based on how much thought is involved. Unfamiliar situations (like, for
most people, math puzzles) require a lot of conscious thought. Walking to
your car doesn’t. Similarly, high-stakes decisions like “Which job should I
take?” also pull in more conscious thought than “Which bagel should I
eat?” Frequently repeated, low-stakes decisions like “Which way should I
hold my tooth brush this morning?” don’t require much thought at all and
can turn into habits.


The spectrum in Figure 1-3 provides the _default, lowest energy_ way that our
minds would respond if we didn’t intentionally do something differently.


_Figure 1-3. In familiar situations, our minds can use habits and intuitive responses to save work_


Here are some simple examples, using a person who is thinking about going
on a diet and doesn’t have much past experience with diets:


_Eating potato chips out of a bag_


Very familiar. Very little thought. Habit.


_Picking out what to get at your favorite buffet bar_


Familiar. Little thought. Intuitive response or assessment.


_Signing up for dieting workshops at the office_


Semi-familiar. Some thought. Self-concept guides choice.


_Judging whether a cheeseburger will violate your diet’s calorie limit for the_
_day_


Unfamiliar. Thought required, but with easy ways to simplify.46

Heuristic.


_Making a weekly meal plan for the family based on the individual calorie_
_and nutrient counts of hundreds of foods_


Unfamiliar. Lots of attention and thought. Conscious, cost–benefit

calculations.


Table 1-1 provides a bit more detail on where each of the tools on the
spectrum are likely to be used.


_Table 1-1. The various tools the mind uses to choose the right action_


**Mechanism** **Where It’s Most Likely to be Used**


Habits Familiar cues trigger a learned routine







Active mindset or
self-concept



Ambiguous situations with a few possible interpretations





Focused,
conscious
calculation



Unfamiliar situations where a conscious choice is required or very
important decisions we direct our attention toward



This spectrum doesn’t mean that we always use habits in familiar situations,
or that we only use our conscious minds in unfamiliar ones. Our conscious
minds can and do take control of our behavior and focus strongly on
behaviors that otherwise would be habitual. For example, I can think very
carefully about how I sit in front of the computer to improve my posture;
that’s something I normally don’t think about because it’s so familiar. That
takes effort, however. Remember that our conscious attention and capacity
are sorely limited. We only bring in the big guns (conscious, cost-benefit
calculations) when we have a good reason to do so: when something
unusual catches our attention, when we really care about the outcome and
try to improve our performance, and so on.


As behavior change practitioners, it’s a whole lot easier to help people _take_
_actions_ that are near the “eat another potato chip in the bag” side of the
spectrum, rather than the “thoughtfully plan meals” side. But it’s much


harder for people to _stop actions_ on the potato chip–eating side than on the
meal-planning side. The next two chapters will look at both, though: how to
create the good and how to stop the bad.

## **A Short Summary of the Ideas**


Behavioral science provides a powerful set of tools to help us both
understand how people make decisions and take action and to help them
make better decisions or follow through on their intent to take action if they
would like our help.


Here’s what you need to know:


_We’re limited beings_


We have limited attention, time, willpower, etc. For example, there are

nearly an infinite number of things that your users could be paying

attention to at any moment.


_Our minds use shortcuts(aka heuristics)_


We use them to economize and make quick decisions because of our

limitations. Heuristics applied in the wrong context are one cause of

_biases_ : negative and unintended tendencies in behavior or decision

making. Often because of these biases, there’s a significant gap between

people’s intentions and their actions.


_We’re of two minds_


What we decide and what we do depends on both conscious thought and

nonconscious reactions, like habits. What this means is that your users

are often not “thinking” when they act. At least, they’re not choosing

consciously.


_Decision and behavior are deeply affected by context_


This worsens or ameliorates our biases and our intention–action gap.

What your users do is shaped by our contextual environment in obvious

ways, like when the architecture of a site directs them to a central home

page or dashboard. It’s also shaped in nonobvious ways: by the people

they talk and listen to (the _social environment_ ), by what we see and

interact with (their _physical environment_ ), and the habits and responses

they’ve learned over time (their _mental environment_ ).


_We can cleverly and thoughtfully design a context_


We do so to improve people’s decision making and lessen the intention–

action gap. And that is the point of _Designing for Behavior Change_ and

this toolkit.


1 There are hundreds, if not thousands, of papers and books one can draw from. Benartzi and

Thaler (2004) is a good start for retirement research.


2 Ariely (2008), Thaler and Sunstein (2008), Kahneman (2011)


3 [Krulwich (2009); Soman (2015)](https://oreil.ly/D_iSB)


4 Soman (2015). Not all biases are directly caused by heuristics gone awry, but many can be

traced back to time- or energy-saving devices in the mind. One major category that isn’t from
heuristics consists of identity-preserving biases (mental quirks that make us feel better about
ourselves), like overconfidence bias.


5 [Hamilton (2008)](https://oreil.ly/90J55)


6 Miller (1956)


7 For example, see Manis et al. (1993). These outcomes are actually the result of reasonable but

imperfect shortcuts that our minds use to _counter_ our limitations; we’ll talk about those
shortcuts shortly.


8 [See Schwartz (2004, 2014), Iyengar (2010), and Solman (2014). As we should expect with all](https://oreil.ly/iVV7f)

behavioral mechanisms and lessons, the paradox of choice isn’t universal or without
disagreement.


9 Kahneman et al. (1993)


10 As many designers have argued, including Krug (2006).


11 That is, the family of theories referred to as _dual process theory_ in psychology. Dual process

theories give a useful abstraction—a simplified but generally accurate way of thinking about—
the vast complexity of our underlying brain processes.


12 Damasio et al. (1996)


13 There are great books about dual process theory and the workings of these two parts of our

mind. Kahneman’s _Thinking, Fast and Slow_ (Farrar, Straus and Giroux, 2011) and Malcolm
Gladwell’s _Blink_ (Back Bay Books, 2005) are two excellent places to start; I’ve created a list of
resources on how the mind works (including dual process theory).


14 The boundaries between “habit” and other processes (intuition, etc.) are somewhat blurry; but

these terms help draw out the differences among types of System 1 responses. See Wood and
Neal (2007) for the distinction between habits and other automated System 1 behaviors; see
Kahneman (2011) for a general discussion of System 1.


15 Wood (2019); Dean (2013)


16 I’m indebted to Neale Martin for highlighting the situations in which the conscious mind does

become active. See his book _Habit_ (FT Press, 2008) for a great summary of the literature on
when intuitive and deliberative processes are at play.


17 Gazzaniga and Sperry (1967)


18 This isn’t to say that the rider is equivalent to the left side of the brain and the elephant to the

right side. Our deliberative and intuitive thinking isn’t neatly divided in that way. Instead, this
is just one of the many examples of how rationalizations occur when our deliberative mind is
asked to explain what happens outside of its awareness and control. Many thanks to Sebastian
Deterding for catching that unintended (and wrong!) implication of the passage.


19 Heath and Heath (2010)


20 See Samuelson and Zeckhauser (1988) for the initial work on status quo bias.


21 Gerber and Rogers (2009)


22 Watson (1960)


23 See Laibson (1997) for initial modeling work in economics; O’Donoghue and Rabin (2015)

for a relatively recent summary.


24 Tversky and Kahneman (1974)


25 Tversky and Kahneman (1973)


26 [Norton et al. (2011)](https://oreil.ly/nPot9)


27 Nisbett and Wilson (1977)


28 See Bargh et al. (1996) for a discussion of the four core characteristics of automatic

behaviors, such as habits: uncontrollable, unintentional, unaware, and cognitively efficient
(doesn’t require cognitive effort).


29 Wood and Neal (2007)


30 [There are nice summaries at News in Health and CBS News.](https://oreil.ly/0Kspd)


31 Ouellette and Wood (1998)


32 There’s an active debate in the field about how exactly the notion of a reward affects a person

_after_ the habit is formed. See Wood and Neal (2007) for a discussion.


33 [See Berridge et al. (2009) on the difference between](https://doi.org/10.1016/j.coph.2008.12.014) _wanting_ and _liking_ . The difference

between wanting and liking is a possible explanation for why certain drugs instill strong
craving in addicts although taking them long stopped being pleasurable.


34 And yes, for those of you who recall this example from the first edition of the book, it’s still

true today.


35 Duhigg’s story also is an example of the complex ethics of behavior change. Hopkins

accomplished something immensely beneficial for Americans and American society. He was
also wildly successful in selling a commercial product in which demand was partially built on
a fabricated “problem” (the fake problem of tooth film, which is harmless, rather than tooth
decay, which is not).


36 [Fogg and Hreha (2010)](https://doi.org/10.1007/978-3-642-13226-1_13)


37 This is one form of _motivated cueing_, in which there is a diffuse motivation applied to the

context that cues the habit (Wood and Neal 2007). There is active debate in the field on how,
exactly, motivation affects habits that have already formed.


38 [Duration is covered in Lally et al. (2010), and delay in Berridge et al. (2009); Wood (2019).](https://doi.org/10.1016/j.coph.2008.12.014)


39 Tversky and Kahneman (1981)


40 Many researchers accept this explanation, but not all. As often happens in science, there is a

divergence of opinion on why framing effects like this occur. An alternative view is that people
make a highly simplified analyses of the options and the two different options have two
different simplified answers. See Kühberger and Tanner (2010) for one such perspective.


41 Wilson (2002); see Nisbett and Wilson (1997b) for an early summary.


42 Emotion and other examples are covered in Wilson and Gilbert (2005), and behavior in

Wilson and LaFleur (1995).


43 Gigerenzer and Todd (1999); Gigerenzer (2004)


44 Soll et al. (2015), building on Baron (2012)


45 Wood (2019)


46 One such commonly used heuristic is the volume of the food—yes, how big it is. Barbara

Rolls, director of the Penn State Laboratory for the Study of Human Ingestive Behavior,
developed a diet that leverages this heuristic to help people lose weight (see Rolls 2005).


# **Chapter 2. Creating Action**

_Americans are over 1.5 trillion dollars in debt with student loans—yet over_
_two million students who are eligible to receive free government aid don’t_
_apply each year._ 1 _They don’t ask for free money._ 2


_When asked, students say that they didn’t apply because they didn’t know_
_about their eligibility. However, Harvard researchers ran an experiment to_
_see if that was really the case, and they found that a lack of information_
_about aid eligibility doesn’t affect application rates one way or another._
_Their research illustrates one of the core lessons in behavioral science:_
_people don’t always know why they act the way they do, and the real_
_reasons may not be obvious._


_Kristen Berman, cofounder of Irrational Labs, set to work on increasing aid_
_applications with her team. They determined that students had to spend_
_almost an hour to apply and undertake 20 separate actions. They believed_
_that cognitive overload affected the students. They would mull over whether_
_or not to apply and avoid making a decision because of its complexity. They_
_postponed it until the next day, then the next day, and so on._


_To help counter that overload (and procrastination), Irrational Labs ran an_
_experiment in which they sent simple text messages to students. The_
_message told them that applying for aid was part of the enrollment process_
_(which it is, it’s just a step that many students skip), and reminded them to_
_complete it by the deadline. In other words, the “decision” was already_
_made._


_For students who hadn’t applied in the previous year, that simple text_
_message tripled the odds of applying. Extending that to the US student_
_population, approximately 230,000 more students would apply for financial_
_aid each year with that intervention. Hence another core lesson of_
_behavioral science: when we understand the obstacle people face, we can_
_help them take action._


## **From Problems to Solutions**

Where does this understanding of the quirks of the mind leave us? It gives
us the tools we need to help people make better decisions and change their
behavior.


To give you a preview of where we’re headed, there are two main sets of
tools we’ll use to help our users. The first addresses the intention–action
gap. Just thinking about the action more isn’t enough. Instead, we need to
look at all of the pieces that come into play to create an action. There’s a
core lesson underlying those behavioral interventions: past a certain point,
motivation isn’t the sole, or even main, determinant. There are many things
we might want to do or be willing to do. Which one we actually do is highly
dependent on context—and thus the specific moment.


People take action (or fail to) in a specific moment. Our will and desire are
certainly important—but it’s not enough, especially when we’re looking to
design for behavior change (i.e., to do differently than the present). We need
to understand what brings one action to the fore and not others.


For that, we have the CREATE framework: a _Cue_, which starts an
automatic, intuitive _Reaction_, potentially bubbling up into a conscious
_Evaluation_ of costs and benefits, the _Ability_ to act, the right _Timing_ for
action, and the overwhelming power of past _Experience_ .


These are the prerequisites for most conscious action.


We’ll use the second set of tools for poorly thought through decisions and
unintentional behaviors: we’ll make them more intentional by interfering
with habits and slowing down rash decisions. You can think about replacing
a habit or stopping a mental shortcut as CREATE in reverse: removing one
or more of the key factors that leads to the negative decision or behavior. In
particular, we’ll avoid the _Cue_, replace the _Reaction_, rethink the _Evaluation_,
or remove the _Ability_ .

## **A Simple Model of When, and Why, We Act**


From moment to moment, why do we undertake one action and not
another? The six CREATE factors must align simultaneously before
someone will take _conscious_ action. Behavior change products help people
close the intention–action gap by influencing one or more of these
preconditions: Cue, Reaction, Evaluation, Ability, Timing, and Experience.


To illustrate these six factors, let’s say you’re sitting on the couch watching
TV. There’s an app on your phone you downloaded last week that helps you
plan and prepare healthy meals for your family. When, and why, would you
suddenly get up, find your mobile phone, and start using the app?


It’s an odd question, I know. We don’t often think about user behavior in
this way—we usually assume that somehow our users find us, love what
we’re doing, and come back whenever they want to. But researchers have
learned that there’s more to it than that, based on how the mind makes
decisions. So, imagine you’re watching TV. What needs to happen for you
to use the meal planning app _right now_ ?


_Cue_


The possibility of using the app needs to somehow cross your mind.

Something needs to cue you to think about it: maybe you’re hungry or

you see a commercial about healthy food on TV.


_Reaction_


Second, you’ll intuitively react to the idea of using the app in a fraction

of a second. Is using the app interesting? Are other people you know

using it? What other options come to mind, and how do I feel about

them?


_Evaluation_


Third, you might briefly think about it consciously, evaluating the costs

and benefits. What will you get out of it? What value does the app


provide to you? Is it worth the effort of getting up and working through

some meal plans?


_Ability_


Fourth, you’ll check whether actually using the app now is feasible. Do

you know where your mobile phone is? Do you have your username

and password for the app? If not, you’ll need to solve those logistical

problems before using the app.


_Timing_


Fifth, you’d gauge _when_ you should take the action. Is it worth doing

now or after the TV show is over? Is it urgent? Is there a better time?

This may occur before or after checking for the ability to act. Both have

to happen, though.


_Experience_


Sixth, even if logically using the app is worth the effort and it makes

sense to use it now, if we tried the app before (or something like it) and

it made us feel inadequate or frustrated us, we’d be loath to try again.

Our idiosyncratic personal experiences can overwhelm any “normal”

reaction we might have.


These six mental processes—detecting a cue, reacting to it, evaluating it,
checking for ability, determining if the timing is right, and interpreting it all
through the lens of our past experiences—are gates that can block or
facilitate action. You can think of them as “tests” that any action must pass:
all must complete successfully in order for you to consciously, intentionally,
engage in the action. And, they all have to come together at the same time.3
For example, if you don’t have the urgency to stop watching TV and act


now, you certainly could do it later. But when “later” comes, you’ll still
face these six tests. You’ll reassess whether the action is urgent at that point
(or whether something else, like walking the dog, takes precedence). Or
maybe the cue to act will be gone and you’ll forget about the app altogether
for a while.


So, products that encourage us to take a particular action have to somehow
cue us to think about the action, avoid negative intuitive reactions to it,
convince our conscious minds that there’s value in the action, convince us
to do it now, and ensure that we can actually take the action. That’s a lot to
do! Much of this book talks about how to organize, simplify, and structure
that process (and then test whether you’ve got it right).


If someone already has a habit in place and the challenge is merely to
execute that habit, the process is mercifully shorter. The first two steps (Cue
and Reaction) are the most important ones, and, of course, the action still
needs to be feasible. Evaluation, Timing, and Experience can play a role,
but a lesser one, because the conscious mind is on autopilot.


Let’s go into more detail about the six preconditions for conscious action.


### **Cue**

At every moment of every day, we’re deciding what to do next. The
universe of things we might do with our time is truly infinite. Our minds
can’t handle that much information and they protect us from being
overloaded by using a set of mental filters. For example, _inattentional_


_blindness_ means we simply don’t see things we aren’t looking for when
we’re concentrating heavily. That’s what happened in Chabris and Simons’s
famous studies where half of the people watching a group pass a basketball
back and forth failed to see a guy in a gorilla outfit walking across the
screen!5 Our mental filters, out of necessity, let us consider only a fraction
of what’s possible. A similar effect happens when we’re at noisy, crowded
parties—we can focus on the person talking to us, despite what otherwise
would catch our attention and pull us in.6


In addition, _confirmation bias_ shapes what we notice in our environment.
When confronted with a complex environment or lots of information,
concepts that we often think about and agree with bubble up to our
attention. We’ve all seen this on social media or political discussions, where
it seems like people only focus on things that support their case or political
persuasion. Like with many of our mental quirks, this is a good and useful
mechanism gone awry: our minds help us pay attention to what we
probably want to focus on, out of a sea of overwhelming information. It
also just makes us narrow-minded jerks in political conversation.

So what cues attention? We start thinking about an action for two reasons:7


_External cues_


Something in our environment can trigger us (like an email or text

message) to think about it. It could be a pair of running shoes that

makes us think of running or something more overt, like a friend calling

us on the phone and asking why we aren’t out running in the park with

them.


_Internal cues_


Our minds can drift into thinking about the action on its own, through

some unknown web of associated ideas (which may themselves have



5



6



been cued externally or by an internal state like hunger).8


Sometimes, cues can capture our attention no matter what—like a car that’s
about to hit us. Other times, we are explicitly looking for cues to act—like
scanning over subject lines in our inbox or looking for notifications on our
mobile phones. It’s even possible that we honestly have no idea why an
action bubbles up in our minds.




### **Reaction**


Once the mind starts thinking about a potential action, there is an automatic
reaction from System 1—the lightning fast, intuitive, and largely
nonconscious part of the brain discussed in Chapter 1 and Kahneman’s
_Thinking, Fast and Slow_ (FSG, 2011). In some cases, it is startling and
powerful, like the desire to run the heck out of a building when you smell
gas. In more common situations—like removing our running shoes or using
an app—the automatic reactions are less jarring but still guide our behavior.
Our conscious minds don’t really have insight into what goes on within our
automatic response system.


While researchers don’t fully understand this process, we have some
significant clues as to what drives our nonconscious reactions.


_It’s strongly social_


In many ways, we are wired to pay attention to and focus on social

interactions. We intuitively assess whether something is right for us to

do based on whether it’s something that other people like us seem to do.

We are hesitant to take actions that our peers might disapprove of. We

try to be consistent with our social commitments and our sense of

identity, both of which depend on and are shaped by our interactions

with others. Our social connections reach us at a level that’s deeper, less

deliberative, than merely a cost–benefit analysis of expected outcomes.


_It’s linked by similarity_


Our minds quickly assess how we feel about unfamiliar things based on

their similarity to more familiar items (aka the similarity heuristic).

Sometimes those similarities express something essential—like the

genre of a book or movie. But often, the distinctions are based on more

cursory distinctions: shape, color, smell. This is true for fruit and for


people: it’s a root cause of stereotyping, and like all mental shortcuts,

it’s a valuable cognitive tool that can go awry.10


_It’s shaped by familiarity_


The more we’re exposed to something, like an idea or object, the more

we tend to like it (all else being equal). Researchers call this the _mere_

_exposure effect_ .11 For example, advertisers rely on this principle when

they buy ads to show you an image of a brand again and again—just by

seeing the ad, people can come to like the brand more (again, all else

being equal). More generally, our minds confound the easy-to
remember with the true; it just feels right to us when we can think about

it quickly.


_It’s trained by experience_


Our intuitive responses are the ruts cut into the earth of our mind by

frequent passage. Over time, our minds learn associations; the things

that we have enjoyed in the past, we learn to react positively to in the

future ( _operant conditioning_ ); even the things that are associated with

good experiences in the past can make us respond positively ( _classical_

_conditioning_ ).12 And even without formal conditioning, our minds learn

what to expect in a familiar situation. For example, if we’re thinking

about walking up 10 flights of stairs, the last time we took the stairs and

almost had a heart attack will color how we feel about doing it again

(and this can occur _before_ we consciously think about whether or not to

act). Prior experience can also affect us in more immediate ways: if

we’ve become angry, we may interpret an ambiguous situation as more

hostile than if we were in a good mood to start with.13


Remember reference dependence, one of the lessons of behavioral science?
Our experiences help set our reference point. They tell us what to expect in
a situation—and thus even a very good meal at a restaurant could be viewed
negatively because we expected (based on our own experience or what
others had told us in the past) an _excellent_ meal.14


What happens because of this reaction? First, our nonconscious mind can
render a _verdict_ or “gut feeling” about the action: an emotion that colors our
thinking and conscious deliberation, if any. The gut feeling we get doesn’t
necessarily determine our behavior. Our conscious minds can override (or
ignore) what our intuitive system tells us—but it will feel wrong. And it’s
hard to sustain a change in behavior if it intuitively feels wrong.


The reaction may also trigger other memories and ideas: when we start
thinking about one action, we also activate memories and thoughts about
other related concepts. If we’re thinking of a particular need (like hunger),
our minds will search for other possible answers to the need and evaluate
them as well. For example, if I’m looking at the stairs, my mind will
automatically, and without my control, also activate thoughts about using
the elevator or escalator.15 Our web of mental associations may lead us in
an entirely different direction as well, distracting us from the original cue
and task at hand.


And finally, the reaction may directly trigger an _action._ In the case of
habitual behaviors, the reaction might automatically initiate the action,
based on the cue. Let’s say I take the elevator every day. Once I walk in the
building, I may go to the elevator and press the button without conscious
thought.


### **Evaluation**

After the mind is cued to think about a particular action, and assuming it
hasn’t been derailed by its intuitive reaction, then the action may rise to
conscious awareness. This happens especially when we’re facing novel
situations and we don’t have an automatic behavior to trigger. The
conscious mind kicks in and evaluates whether the person should take the
action, given the various costs and benefits.


This stage is the one that we tend to think about first when we’re trying to
change behavior. We try to educate people about the benefits of the action,
increase their motivation with money or other rewards, and reduce the
(perceived) cost of taking the action.


For example, again consider people who have the choice of taking the stairs
to go up a few flights or taking the elevator (Figure 2-1). Let’s say that their
conscious mind is engaged. The common approach to encouraging people
to take the stairs would be to focus on:


_Highlighting benefits_


Taking the stairs will get you in shape and may lengthen your life.


_Minimizing costs_


Taking the stairs will cost you only three more minutes, and if you go

slowly, you won’t sweat.


_Downplaying alternatives_


The elevator is slow and crowded at this time of day.


_Figure 2-1. While the subconscious mind might see the stairs and think “Ugh, that’s work,” the_
_conscious mind thinks of costs and benefits (Benefits: good exercise. Cost: just three minutes. And the_

_elevator is crowded anyway. Done!)_


There is, of course, tremendous complexity behind the deliberations we
make over whether to act. How much do we really know about the costs
and benefits of the action? Where did we get that information, and do we
trust it? Is it worth the effort to seek out more information, or should we
simply use what we have? What motivations weigh upon us most strongly
at the moment we’re deciding?


These are vital questions. For now, though, let’s leave it at this: if we deem
the action worth the effort _and better than the alternatives_, then we’re in
business. The choice to act has been made.


Note that the “thinking” that occurs here may be extremely limited and
rapid. If the action isn’t very important or is familiar, then the conscious
mind may decide to go ahead without much effort. It’s when the action is


unfamiliar, or the mind decides to pay a lot of attention, that more intensive
thinking occurs.


A product that promotes an important action that users “should” take (and
some part of them wants to take) isn’t enough. The product must give users
something they actually want, right now, more than the alternatives. Like
any product, a behavior-changing product must solve a problem for its
users. Otherwise, the rest of this discussion won’t help. If the conscious
mind doesn’t see value that’s worth the effort, it won’t intentionally use the
product or take the action. That value needn’t be purely instrumental—it
can be something social, emotional, or an intrinsic enjoyment of the activity
(we’ll talk more about types of motivation later)—but it needs to be there.


Remember, for habitual behaviors, this conscious awareness and evaluation
usually doesn’t occur at all. But our conscious minds are happy to make up
stories about why we do habitual things. Those stories are just noise and
aren’t real reflections of our actions.16




### **Ability**

Let’s say the choice to act has been made after weighing the costs and
benefits. Is it actually _feasible_ to undertake the action? If you’ve decided to


finally put aside some money for your retirement, can you actually do it,
right now? The individual must be _able_ to immediately take the action; the
ability to act has four dimensions:17


_Action Plan_


The person must generally know what’s required to take action. For

example, they must know that setting up a retirement account requires

going to a particular website, entering information provided by their

employer, and so on.


_Resources_


The person must actually have the resources required to act. For

example, they must have money available and access to a computer to

go to the retirement website and set up an account.


_Skills_


They must have the necessary skills to act. For example, to sign up for a

retirement account online, they must know how to use a computer and

navigate its (too often impenetrable) user interface.


_Belief in success_


No one wants to feel like a failure. The person needs to feel reasonably

sure that they can be successful at the action and not end up looking like

an idiot. That’s known as a feeling of _self-efficacy_ .


If the person doesn’t have a basic plan for how to take action, doesn’t have
the necessary resources for immediate action, or is hesitant because the
action is daunting, those challenges are surmountable. But that means delay.
It means that the person isn’t taking the action _right now._ And that, from the
perspective of behavior change, is a partial failure.


In the research community, we call these moments _decision points_ :18 each
time a person who has already decided to do something needs to stop to
think about the next step in the action plan, gathering the resources to do it,
or whether they personally have what it takes, you’ve created a new
decision point. That decision point may pass smoothly, and after whatever
frictions or obstacles are resolved, the person could take the action later.
That’s _if_ the other preconditions for action are still in place when the person
has the ability to act. However, the situation may change—other
distractions could arise, the cost of action may go up, and so on.


It’s because of these decision points that minor frictions can be so important
to product design. For example, checking a box on a retirement form is, in
itself, a trivial action. The cost is minor, especially in comparison to the
benefits. And yet, we know that defaulting people in (and letting them opt
out so they can express their preferences either way) tremendously boosts
enrollment in retirement plans, in part because it reduces friction. The
friction isn’t important for the cost–benefit _evaluation_ ; rather, it creates a
decision point at which people can become distracted, feel unsure about
their mathematical ability and competence, decide they need to think about
it more later, and so on.


### **Timing**

You have their attention and the action is appealing and feasible. But _when_
should you take the action? Why not do it a bit later? (And why not later,
and later…) That’s a major problem with many “beneficial” actions we
want to take, like exercising, getting control of our finances, or planting a
garden. We can always do them later. Even if we want to take the action, if
our minds feel that there is something that’s likewise desirable but more
urgent, we’re out of luck. We could take the action later. However, as we
saw with ability barriers, if there isn’t a decision that _now_ is the right time
to act, there’s a problem. By the point the person does feel the timing is
right, circumstances may have changed, and the person won’t take the
action for other reasons.


The decision of when to take action (i.e., its timing) can be driven both by a
sense of clear and present urgency and by other, less forceful but still
important factors. Urgency can come from a variety of sources: [19]


_External urgency_


In the US, we really do need to put in our taxes (or file for an extension)

by April 15. Otherwise, the IRS comes after us. That’s a true, external

urgency; bad things happen if we deny the tax man his due.


_Internal urgency_


Changes in behavior may be urgent because we have a biological need

that we can’t ignore (hunger, thirst, etc.). However, these needs just

don’t apply to many actions and products. Negative mental states like

boredom may provide a lesser, but still potent, urgency to act.


Similarly, we can decide that now is the right time to act (even when it
doesn’t feel strictly urgent) for a variety of reasons:


_Specificity_


Think about the two statements “I should save for retirement” versus “I

should set up a retirement account on Thursday at 8 p.m., right after

dinner.” The latter feels more real, right? Simply by putting a specific

time on an action can settle the issue of “when” to act. It also helps us

_remember_ to act then too!


_Consistency_


Another way to help us decide when to act (and to follow through on it)

is to pre-commit to a specific time in the future, especially if we tell

others about our commitment. That moves the action from the domain

of something that we might do some time to an issue of personal

consistency with our word. Our desire to be consistent with our prior


statements means that the right time to act is exactly when we said we’d

act.


The decision to act at a particular time also arises, in part, from our
motivation (emotional and deliberative) to take the action. An action that’s
really exciting and promises to be enjoyable also can feel more urgent and
prompt someone to decide to act now rather than later. I’ve distinguished
between the two concepts to analyze and address them separately, but in
reality, there can be a significant blurring between them when the action is
highly motivating (Figure 2-2).


_Figure 2-2. When is eating chocolate cake urgent? (Top left: When you’re hungry! Top right: When_

_the waiter calls “Last chance for cake!” Bottom left: When it’s New Year’s Eve, and it’s time to_

_indulge a little. Bottom right: When you’ve promised yourself cake after finishing work.)_


### **Experience**

Prior experience is uniquely powerful and important when it comes to
designing for behavior change. We’ve already talked about the role that it
plays in forming one’s intuitive associations and reaction. It also shapes our
understanding of the costs and benefits of the action, removing uncertainty
and calibrating our evaluation to the actual pros and cons for us rather than
the claimed or expected ones because of a company’s marketing efforts. It


helps determine whether we have the self-confidence to attempt the action.
And due to confirmation bias and selective attention, it deeply shapes
whether we pay attention at all.


For example, imagine two people who work at the same company and live
in a stylish part of town that’s a 30-minute walk to the office. One person
might intuitively love the idea of walking to work because it makes them
think about showing off their calves. Another person, in equally good shape
and living in the same neighborhood, might intuitively hate it because they
associate walking to work with growing up in poverty and not having the
money to afford to drive. That’s just how people are: we can look exactly
the same on the surface, but our histories run through us and guide us in
hidden and surprising ways.


I find it useful to call prior experience out as a separate factor in designing
for behavior change to remind ourselves, as practitioners, that prior
experience is fundamentally personal: it varies from user to user. It varies in
ways that we don’t necessarily know or understand. Even before someone
uses our products, we are judged by the experiences each person has had in
similar environments and with similar products. As they use our products,
_history matters_ . Regardless of how awesome the product is now, if we’ve
already taught them that it’s poorly built and designed, that will be difficult
to overcome. Or, if people have previously tried to succeed at their behavior
using your app and hadn’t seen any progress, they’re less likely to try again.




## **The CREATE Action Funnel**

These six mental tests are prerequisites for most conscious action. They are
what we need to _create action_ .


Let’s say you have a hundred people, all of whom are trying to better
organize their email and respond to messages in a timelier manner
(behavior change isn’t always sexy!). All one hundred of them have set a
reminder to go through their old messages and delete or respond to them on
the path to a zero-message inbox. Suppose 75% of them will actually see
and pay attention to the reminder despite their hectic schedules and
clustered home screen (we all know that 75% is really optimistic, but let’s
work with that assumption). Unfortunately, some of them will quickly and
intuitively close it because they don’t want to deal with that annoying task.
But let’s say that 75% have a positive emotional reaction to the thought of
cleaning their inbox (I know, wildly optimistic). The remaining people will
think about it for a second, and 75% of them decide that cleaning up their
inbox really is worthwhile.


Of those who have a favorable evaluation, a few of the remainder will
realize they don’t have enough mental energy and time to do it now and will
postpone. But an impressive 75% of them still preserve. Among those who
are left, an astounding 75% say to themselves, yes, absolutely, this is the
most urgent and important thing I could do right now (the others let it wait
because there are more pressing matters; they postpone). Finally, only 20%
of people had previously failed at cleaning out their inbox and were
discouraged because of that past experience or cleaned it out and it quickly
became cluttered again, killing their enjoyment of it.


In the end, how many people of the one hundred who sincerely wanted to
clean out their inbox actually did it? Just 18. And this is with wildly
optimistic assumptions. Only a handful of the original hundred people
actually respond to the cue and followed all the way through to action.
That’s the intention–action gap at work.


There’s a nice study by Yale’s James Choi and others that measured the
intention–action gap in the context of saving for retirement (sadly it was


before CREATE existed): they found that only 10% of the people who
declaratively committed to saving more actually did so.21 In other words,
looking at what actually happens in practice, and the simple math of the
many barriers that people need to pass to take action:


We shouldn’t be surprised when sincere, motivated people do
nothing.


Another way of thinking about this process is as a leaky funnel: a group of
people start the process and some leak out at each step, leaving only a few
of them who make it all the way (Figure 2-3). The funnel metaphor is a
common one for salespeople, marketers, and product folks focused on
converting potential clients into actual clients on their website.


_Figure 2-3. The CREATE Action Funnel: six stages that a potential action has to pass in order to be_

_undertaken—people can drop out at every step along the way_


Each section of the funnel has two leaky holes in it. On one side, people can
reject the action (or the cue) because it’s not valuable or urgent enough. On
the other side, they can be distracted into doing something else—either


because they think of something else to do with the same effect (like surfing
the Internet to relieve boredom instead of using a meal planning app) or
because they are pulled into something completely different (like answering
the phone).


For habitual actions, there’s a simpler version of the funnel than for
conscious action: Cue-Reaction-Ability. Habits effectively plug potential
leaks in the conscious process, so there is very little drop-off where a
conscious evaluation of the action would otherwise occur (unless the person
is intentionally trying to be aware of their habitual actions and stop them)
and where the assessment of urgency would occur.

### **Each Stage Is Relative**


An important thing to remember about the funnel is that at each stage, the
person only continues on if the action is more effective or _better than the_
_alternatives._ There are always alternatives, including other cues that seek to
grab us, other actions we’re intuitively and consciously assessing, or other
priorities that could be urgent.22


From a product design perspective, that means you should consider not only
how well the product guides the user through these stages but what else is
competing for the individual’s scarce time and mental resources. Removing
distractions is a key part of structuring the individual’s environment, which
we’ll return to in Chapter 9.


It also means thinking about what the user is currently doing with respect to
the action. Let’s say the product seeks to promote dieting in order to lose
weight. What is the person currently doing? Avoiding any thought about
dieting? Trying something and failing? Asking friends for advice, but never
acting? _Whatever the user is currently doing_ - _that’s the main behavioral_
_competition for the product._ One shouldn’t assume that products interact
with a user who’s a blank slate. Rather, the product needs to beat an existing
behavior and do so at each stage of the CREATE Action Funnel. Each stage
is relative to the alternatives.


### **The Stages Can Interact with One Another**

I’ve presented a nice, neat model with six stages of processing. At a high
level, that’s correct. The details are much more complex, of course. One
issue we haven’t talked about much is how these different processes interact
with one another.


While all six factors must be in place at some level for conscious actions,
weakness in one area can be counterbalanced by strength in another area.
For example, things that are really easy to do (like grabbing a bottle of olive
oil out of the cabinet instead of an unhealthy hydrogenated oil blend) don’t
need to have significant conscious benefits (it might make you a little
healthier) or positive intuitive feeling. This is one of the lessons that BJ
Fogg incorporates in his Behavior Model23—in economic terms, the factors
are partial substitutes for one another.


In terms of the ordering, the funnel is a useful way to remember the
activities the mind performs, but it isn’t a perfect representation of sequence
of processes. The first two steps generally come before conscious
awareness, as shown, but sometimes intuitive reactions can occur after (or
as part of) conscious deliberation.24 For the next three, there’s some
evidence that the evaluation of an idea (e.g., value, timing, and ability) is
pursued simultaneously by different parts of the mind,25 and there can be
some interaction between them. These complexities don’t affect the central
lesson, though: intentional actions need to pass all five stages, and there is
often a significant drop-off at each step.



24



25


### **The Funnel Repeats Each Time the Person Acts and** **Each Time Is Different**

People don’t stay in the funnel over time. They drop out somewhere or they
take the action—either way, the moment passes and they’re out. Each time
people think about taking the action, the process repeats: a cue leads them
to think about it, they react intuitively, and so on. Thus, repeated actions
require multiple passes through the CREATE Action Funnel. However, the
funnel is subtly different each time. This is especially true when the person
is deciding whether to take the action a second (or third, etc.) time.


Let’s say you’ve gone to the gym for the first time. Here are some of the
things that change from the first time you planned on going to the second
time you’re thinking about going:


_Your relationship to the action has changed_


You now know how the gym operates, where the equipment is, and so

on. So your cost to use it decreases. But you also know more clearly

whether you like going to the gym or not. So your intuitive reaction and

conscious evaluation change too.


_You’ve changed_


If you did well your first time exercising, you have more confidence

(increasing the perceived feasibility); if you weren’t able to do the

exercises you had hoped, you have less confidence.


_Your environment may have changed_


You may set reminders for yourself to go back to the gym (creating

cues) or set expectations among your family that you will continue


going (creating urgency and increasing benefits). You may have friends

at the gym who expect you to return.


**WHAT’S STOPPING YOUR USERS?**


Here’s another way of thinking about the CREATE Action Funnel and
the six stages that a potential behavior passes through: what _blocks_ your
users from taking action? What are the cognitive and practical barriers
they face?26


_Problems with cues_


The user forgets to act or has limited attention. Nothing in the

environment reminds the user to act.


_Problems with the intuitive reaction_


The user doesn’t trust the product or the company behind it. The

action is unfamiliar and feels foreign.


_Problems with the conscious evaluation_


The user just isn’t very motivated to act. The costs of taking the

action are too high.


_Problems of ability_


The user doesn’t know how to actually do it or doesn’t have what

they need to act. The user fears failure.


_Problems of insufficient urgency_


The user procrastinates and puts off the action until another day,

which never comes. Or, other urgent issues block the user from the

action.


_Problems of prior experience_


Your product reminds the user of a badly designed, difficult-to-use

one they tried in the past. Even out of the gate, your product is

negatively judged.


Whether you look at it from the perspective of what’s required for
action (the CREATE Action Funnel) or from the perspective of barriers
to immediate action, the same factors are required for individuals to
successfully act.

## **A Short Summary of the Ideas**


Here’s what you need to know. For someone to take a conscious action, six
things must happen immediately beforehand:


1. The person responds to a _Cue_ that starts their thinking about the

action.


2. Their intuitive mind automatically _Reacts_ at an intuitive level to

the idea.


3. Their conscious mind _Evaluates_ the idea, especially in terms of

costs and benefits.


4. They check whether they have the _Ability_ to act—if they know

what to do, have what they need, and believe they can succeed.


5. They determine whether the _Timing_ is right for action—especially

whether or not the action is urgent.


6. They aren’t turned off by a prior negative _Experience_ —that

overwhelms the otherwise clear benefits.


These six events can be visualized as a funnel, like a conversion funnel in
ecommerce websites. If the person passes all six stages, then they will act.


A quick way to remember the preconditions for action is the acronym
CREATE: Cue, Reaction, Evaluation, Ability, Timing, Experience. At each
step, people drop off because they fail to see the cue, don’t consider the
action worthwhile, or don’t find it urgent. Each step of the way, they can
also become distracted and diverted into taking other actions.


If the action requires conscious thought (System 2), our minds engage in all
six steps. If it doesn’t require conscious thought (System 1 only), then part
of the process is short-circuited, and the cue, reaction, and ability are most
relevant (CRA).


1 [New York Federal Reserve (2019); Kantrowitz (2018)](https://oreil.ly/ME9bU)


2 This case study derives from phone interview and subsequent email exchange with Kristen

Berman of Irrational Labs.


3 I’m thankful to BJ Fogg for stressing that behavioral prerequisites must occur at the same

time. It’s something he talks about in the Fogg Behavior Model (Fogg 2009a) and that sets his
work apart from other models of behavior and intentional action—which too often focus on the
raw materials of behavior (resources, motivation, etc.) but not the _timing_ required for action.


4 [Service et al. (2014); Michie et al. (2011)](https://oreil.ly/3pe0O)


5 Chabris and Simons (2009)


6 Aka the _cocktail party effect_ . My thanks to Peter Hovard for suggesting its inclusion here.


7 For lack of a better term, I’m using _thinking_ to refer to preconscious sensory processing and

reactions and, later on, conscious thought.


8 I’m indebted to Nir Eyal for reminding me of the importance of internal cues and showing me

how products can move from relying on external cues to internal cues over time.


9 Eyal (2014)


10 [Pomeroy (2013)](https://oreil.ly/OqOhl)


11 Zajonc (1968)


12 For summaries and links to the broad body of research, see Wikipedia’s articles on operant

[conditioning and classical conditioning.](https://oreil.ly/Z3NPr)


13 See Litvak et al. (2010) for a summary.


14 [See contrast effects in psychology; for example, see Cash et al. (1983) for an early study.](https://doi.org/10.1177/0146167283093004)


15 Many thanks to Keri Kettle and Remi Trudel for their feedback on an early draft of this

chapter, and for bringing up the intuitive needs assessment and search for alternatives.


16 See Dean (2013) for a great overview.


17 In this general concept of _ability_, I’m combining disparate elements from the self-efficacy

[literature (Bandura 1977), work on goals and implementation intentions (Gollwitzer 1999), and](https://doi.org/10.1037/0033-295X.84.2.191)
“weak” rational choice models of resource constraints, like the Civic Volunteerism Model
(Verba et al. 1995). You may be familiar with the term “ability” from the Fogg Behavior
Model. I’m using it in a different way here—as the perceived and actual capability of the
individual to take the action. Fogg uses the term for how “easy” or “simple” the action is; i.e.,
[the lack of costs (Fogg 2009a).](https://doi.org/10.1145/1541948.1541999)


18 See Soman (2015) for a nice discussion of this in a business context.


19 Beshears and Milkman (2013). Also, these factors serve as cues as well as urgency. They grab

our attention and provide urgency to act on it now. Hat tip to (h/t) Paul Adams.


20 Many thanks to BJ Fogg for introducing me to the concept of Kairos.


21 Choi et al. (2002)


22 This concept of ever-present competition is found in social marketing (e.g., Grier and Bryant

2005) but is considered in few other behavior change perspectives.


23 Fogg (2009a)


24 There can be an interplay between the deliberative and intuitive minds, as our conscious

attention shifts, potentially intervening in an automatic process, or relinquishing control back
to automatic processes. See Wood and Neal (2007) for a discussion of some of these scenarios.


25 Brass and Haggard (2008)


26 Many thanks to John Beshears and Katy Milkman for presenting the idea of basic cognitive

barriers to action (procrastination, forgetfulness, and a lack of motivation) when they came to
speak at the Action Design Meetup, April 2013 (Beshears and Milkman 2013).


# **Chapter 3. Stopping Negative** **Actions**

Breaking: “FBI Agent Suspected in Hillary Email Leaks Found Dead of
Apparent Murder-Suicide"



_It’s on NPR._ 1 _It’s been talked about all over the internet. It’s also completely_
_fake._


_Such news stories are often really interesting: they excite our emotions,_
_confirm our suspicions, and help us see that other people like us are out_
_there who “get it.” In other words, they build on nondeliberative “fast”_
_thinking from System 1, deploy confirmation bias, and leverage social proof_
_and other behavioral techniques. It’s no wonder that people trust these fake_
_news stories, forward them to others, and start to integrate them into their_
_view of the world._

_What can be done about it?_ 2 _Researchers Sander van der Linden and Jon_
_Roozenbeek developed a psychological vaccine called Get Bad News,_
_building on a body of research known as_ cognitive inoculation theory. _Get_
_Bad News is an online game in which players try to create a fake news_
_website and build a base of loyal followers by using the tactics of actual_
_fake-news purveyors. By experiencing fake news tactics in a controlled_
_environment where participants can see how they work without being duped_
_by them, people can become inoculated against the real thing. In van der_
_Linden and Roozenbeek’s research, they tested the platform with 15,000_
_participants and found that people could better spot (and resist) fake news_
_because of it._ 3



2



3



_Qatar’s B4Development Foundation and Nudge Lebanon partnered with_
_van der Linden and Roozenbeek to apply the same approach to_
_radicalization to help people who might be recruited into terrorist or other_
_extremist organizations recognize the tricks recruiters use and resist them._


_Together, they developed the game Radicalise, in which the participant_
_plays the chief recruitment officer for a fictious extremist organization._
_Players use social media to hook their audience to get them interested in_
_the organization and its narrow interpretation of the world and to start to_
_hate others who oppose them. Individuals have been randomly assigned_
_into a treatment (using the game) and control group (not using it), and the_
_team tested how well participants could identify the manipulativeness of_
_sample WhatsApp posts. While the project is ongoing, it appears that the_
_treatment group is better able to identify manipulative messages and to_
_identify people who might be susceptible to recruitment._


_Radicalise, and the fake news research that it builds on, is a promising_
_example of how behavioral techniques can be used to hinder bad decisions_
_and actions in the future._


Sometimes, users of our products can’t succeed at their goals because they
make a series of bad choices that they wouldn’t otherwise want to make, or
act out previously learned bad habits. In both areas, lessons from behavioral
science could help, starting with an understanding that the same
environment facilitates desirable and undesirable choices alike. For
example, we’re far more likely to overindulge when alcohol is present and
available than when we need to go search for it. Similarly, we need more
self-control and are more likely to falter when others around us are doing
so.4


Often, people think that to resist temptations, they need an iron will.
However, one of the most effective ways to help block rash decisions or
actions is to intentionally design the environment to hinder them.
Researchers call this _situational self-control._ 5 For example, we can help
someone be less subject to peer pressure to overdrink by relocating the
person away from binge drinkers or surrounding the person with more
responsible drinkers.


The process is effectively CREATE in reverse; you can think about it in
four steps:


1. _Identify how CREATE supports the negative behavior._ What Cues

it? What causes the person to have a positive Reaction and
Evaluation? What makes the person Able to act immediately and
prioritize it as Timely over other things?


2. Come up with strategies _to change the environment to create_

_obstacles_ —adding friction, removing cues, etc.—and to lock them
in over time.


3. _Double-check what type of behavior it is._ If it is habitual

(nonconscious, without intention), there are extra techniques you
can use (discussed in “Changing Existing Habits”). If it is an
effortful conscious choice, then special attention should be paid to
supporting the Evaluation.


4. _Set up a feedback loop_ to check in and see if you are being

successful at stopping the behavior. We need feedback loops to
stop behaviors just as we do when we’re starting them because
we’re just not that good at seeing averages and trends in our
behavior over time.


Step 2 in particular deserves extra attention. How do we _create_ obstacles?
We’ve spent our time thus far talking about how to remove them. But the
same logic can work to add them.

## **Using CREATE to Add Obstacles to Action**


Let’s look at each stage of the action funnel to see how to interfere with
problematic actions. Consider someone who checks their phone frequently
and finds themselves ignoring their family and friends. The behavior might
be an automatic habit, or it might not, depending on how long it is
continued in the same context—we’ll start by looking at the nonautomatic
version of phone checking:


_1. Cue_


Just as the secret to getting attention is to put the item in the line of

sight, to avoid attention, _get it out of sight._ For my wife and me, one

way we’ve tried to avoid checking our phones is to remove them from

our room so we have fewer distractions from spending time with each

other.


_2. Reaction, especially our social reaction_


How can we use our innate social sense to help us avoid bad behaviors?

One way is to intentionally surround ourselves (at the moment of

temptation or otherwise) with peers who _don’t_ act that way or actively

disapprove. Another way is to avoid being around friends who _do_

engage in it and trigger us to do so as well. In the context of phone

checking, that means seeking out people who have gone cold-turkey on

their phones, or intentionally spending time with that annoying person

who always gives us a hard time when we’re using our phone in public.


_3. Evaluation_


Think about the consequences of the action and see how to make those

consequences more prominent, or make the benefits of not doing it

more vivid and real. It doesn’t have to be the most important aspects of

the costs and benefits (in the long term)—but rather something you can

focus on and change your framing of it in the moment. For example,

add a timer on the phone that shows how long it’s been since you’ve

unlocked it. You could also significantly increase the cost of action by

_making it more difficult._ On my phone I have the bad practice of

checking the news many times a day. To make it more difficult, I


canceled my online news subscriptions and removed the apps from the

phone.


_4. Ability_


We can also add _small frictions_ that cause pause without fundamentally

changing the big picture costs and benefits of an action. I moved some

of my most distracting apps (those I felt I couldn’t simply delete) to a

folder labeled “distractions.” It only takes a second to overcome, but it

slows me down, giving me more opportunity to think about what I’m

doing. I set a simple password on Amazon Video for the same reason.


_5. Timing_


How can we remove a sense of urgency from the parts of our lives that

distract us from our goals? I’ll admit I struggle with this one greatly,

and I don’t have an answer that has worked for me. I try to increase the

urgency of things that matter to me—like setting a deadline for myself

to write this book—to crowd out other things. That helps, but not as

much as I’d like. Many people have found mindfulness practice helpful

to remove the false urgency from life’s many distractions.


_6. Experience_


If someone wants to hinder a negative behavior (and that’s the only type

of behavior we want to help stop), their prior experience is generally

pretty negative.

## **Changing Existing Habits**


Sometimes helping people take action requires intentionally stopping a
habit. For example, at some point, improving fitness through exercise
means not just exercising more but also sitting less. And that means
overcoming an existing habit. Unfortunately, it can be extraordinarily
difficult to stop habits head-on. Brain damage, surgery, and even
Alzheimer’s disease and dementia sometimes fail to stop habits, even as
other cognitive functions are severely impaired.6 BJ Fogg, for example,
argues that stopping existing habits is the hardest behavioral change task to
undertake.7



6



7



Why are habits so difficult to change? First, remember that habits are
automatic and not conscious. Our conscious minds, the part that would seek
to remove them, are only vaguely aware of their execution;8 we often don’t
notice them when they occur, and we don’t remember doing them
afterward. Across dozens of studies on behavior change interventions,
researchers have found that the conscious mind’s sincere, concerted
intention to change behavior _has little relationship to actual behavior_
_change_ .9



8



9



Second, it’s because habits never truly go away—once a habit is formed
(i.e., the brain is rewired to associate the stimulus and response), it doesn’t
normally un-form. It can remain latent or unused, but under the right
circumstances, that circuitry in the brain can be activated and cause the
habitual behavior to reappear.10


Another way to think of habit cessation is this: if stopping bad habits were
easy, we wouldn’t need so many darned books on everything from stopping
smoking to dieting.11 Nevertheless, we can draw lessons from the literature
on habit formation and change, which can save product teams needless pain
and suffering. There are four main options that product teams can take to
handle an existing habit:


_Attention_


Avoid the cue.


_Reaction_


Replace the routine by hijacking the reaction.


_Evaluation_


Cleverly use consciousness to interfere, including using mindfulness to

avoid acting on the cue.


_Ability_


Crowd out the old habit with new behavior.


In each case, the person doesn’t engage in a direct confrontation to simply
suppress the habit. That takes constant willpower, which is finite and often
unsustainable.

### **Attention: Avoid the Cue**


The cue signals the brain to engage in the problematic behavior; one way to
stop a habit is to avoid the cue. For example, in addiction counseling,
counselors advise addicts to change their environment so that they don’t
encounter the things that remind them to act. If you always stop for a drink
when you see the bar on the way home, then change your route home so
you don’t see the bar anymore.12


Designing a _product_ to help people avoid cues is especially tricky. First of
all, most cues for bad habits are, by definition, outside of the behavior
change product. People use the product in order to change the habit—the
product didn’t cause the bad habit. So, the product must help the person
avoid the cues themselves; it must provide guidance and instruction. And
the individual must first know what the cues are—and be able to
successfully avoid them.


Second, because the routine is outside of the product, the application
usually won’t know if the person has engaged in the behavior. It’s up to the
user to report falling off the wagon—which is doubly difficult. External
monitoring systems are required—like the breathalyzers that alcoholics


install in their cars to avoid driving drunk. Much more is required in the
case of chemical addictions like alcoholism, but we can learn from these
efforts as we design products to stop less intractable habits.


While this route is clearly challenging, there are products that have
[successfully done it. One example is CovenantEyes—software that helps](https://oreil.ly/nV0Bs)
people who are struggling with sexual addiction or want to avoid the
temptation before a habit is formed (see Figure 3-1). It helps users avoid
cues (by filtering out sites with explicit content) and/or automatically
monitors web usage to inform accountability partners of when the person
does access pornography.


_Figure 3-1. CovenantEyes, an application to stop the habit of viewing sexual material online, via_

_filtering and automatic monitoring_


**Reaction: Replace the routine by hijacking the reaction**


The other strategy that products can use to change a bad habit is to
transition an existing cue and reward to a different (more beneficial)
behavior. In _The Power of Habit_ (Random House, 2012), Duhigg describes
two elements that are needed: routine replacement and a real belief that the
habit can change.


Routine replacement works by hijacking the cue and the reward and
inserting a different routine between them. He uses the example of taking a
snack break when you’re not really hungry. The cue may be that you’re


having a down moment at work or watching a commercial on TV. The
reward would be the relief of (momentary) boredom and the pleasant
crunching sensation of the snack. To hijack this process, one needs to:


1. Identify the trigger and the reward (if appropriate).


2. When the trigger occurs, consciously engage in a different routine

that provides a similar reward (like doing a crossword puzzle
during commercials).


3. Continue that conscious switching of routines until the new habit is

instilled.


The process of consciously replacing routines is also known as _competing_
_response training_ . It is used in the treatment of people with Tourette’s
syndrome (involuntary tics) and has shown dramatic results in experimental
testing.13


For especially difficult habits, like smoking and drinking, swapping in a
new routine isn’t enough, though. The new reward is never quite like the
old one. Swapping can handle everyday behavior, but when times are tough,
people can be immensely tempted to “fall off the wagon.” Something else is
needed to get through those dark times and back to the day-to-day
humdrum that they _can_ handle. That something else can be faith that the
hard times will pass. It can be a religious faith, a personal faith in
themselves, or a faith in others that pulls them through. Either way, it’s an
internal narrative that things will get better.


How does routine replacement work in practice? One of two ways. First,
you can ensure that the product itself is present at the moment when the cue
normally occurs. At that moment, it would remind or entice the user to do
the new routine instead of the old one. After the routine is done, it would
reward the user—or encourage them to reward themselves.


The other route is trickier and is needed when the product _isn’t_ present
when the user encounters the cue. As with avoiding the cue, the product
must advise and prepare the individual for the moment of temptation and
[find some way of tracking what action the person took. Changetech has an](http://www.changetech.no/)


intensive program of support and tracking that accomplishes this, with more
than four hundred points of contact with individuals during their smoking
cession program. And its method has shown positive results in randomized
control trials.14


An example of in-the-moment hijacking of habits that we’re all familiar
with is shopping in brick-and-mortar stores with a smartphone:


_1. Cue_


See a camera, computer, or something else you like.


_2. Old routine_


Pick it up, go to the cash register, buy it.


_3. New routine_


Look it up on the phone, compare price (usually lower), and buy it.


_4. Reward_


Feel great about saving money, imagine yourself using the cool camera,

and so on.


This habit hijack is killing brick-and-mortar stores, of course.


**Evaluation: Use conscious interference**


Our big brains are really good at blocking our own autopilot; properly
deployed, they can interfere with habits in progress _without requiring direct_
_willpower to overcome the action_ . Thinking = bad, for a habit at least. In
sports, masters of their game sometimes “choke” because they consciously
cut into a process that normally runs on autopilot, and this happens in any
field of mastery.15 To interfere with a habit, think about it. Look especially
for what triggers it, then closely examine the routine that’s normally
automatic—just by thinking about it (consciously), we can interfere with its
smooth execution.


Products that do this should be present at the time of action and can grab the
user’s conscious attention to their behavior. The Prius is well known for
functioning this way. The car’s consumption monitor provides ongoing,
immediate feedback about the car’s gasoline consumption. This in-themoment feedback can break people out of their existing driving habits by
making them consciously aware of what’s going on, causing them to use
less gasoline, aka _the Prius Effect._


In order for this approach to work, like all habit intervention (and habit
formation) approaches, it must be voluntary. If someone doesn’t care about
mileage or finds the car’s consumption monitor annoying, they won’t listen
to it. It starts with the conscious choice to act.


**Evaluation: Increase attention with mindfulness**


Another, subtle way to overcome bad habits is by employing mindfulness.
Mindfulness is a concept used in Buddhism to refer to awareness of the
present moment and its experiences without judging or trying to control
them. It’s a mental state of openness and acceptance of events and
sensations as they occur. Mindfulness-based therapies are increasingly
popular in the treatment of mental conditions such as acute stress, anxiety,
and depression. Similar to mindfulness meditation in Buddhism, these
therapies entail an intentional focus on the present moment without
interference or judgment.16


By bringing into conscious awareness the cues that trigger habitual
behavior, it’s possible to be aware of the trigger without acting on it. As
someone who personally has practiced this approach, it’s fascinating and
nonintuitive. You don’t fight the habit; instead, by noticing the trigger (and
the urge to respond), you sap the habit of its power. You don’t need to
respond to the habit when you’re being mindful.


Mindfulness has been shown to be powerful in a variety of contexts; for
example, in limiting undesired but habitual binge drinking.17 A number of
[apps such as Headspace and Calm support mindfulness to reduce stress or](https://www.headspace.com/)
increase focus, though do not target habit change in particular.


**Ability: Increase the power of other behaviors**


Another way of approaching habit change is to crowd out the old habit with
new behaviors. In this method, you _focus on doing more of what you want_
_instead of less of what you don’t want_ . The consequence is that you don’t
have the time or energy to do the prior action anymore—the relative ability
decreases.


For example, think about someone who is in bad physical shape, spends lots
of time watching TV, and has bad eating habits. The person starts to go to
the gym to exercise more (creating a new habit). As they go to the gym,
they meet new people and enroll in exercise and cooking classes with them.
Slowly, the amount of time available to watch TV decreases. The person
simply isn’t at home as much, which leads them to avoid the old cues to
watch TV. Also, because of the cooking class and new ways of eating and
cooking, they simply don’t have the hunger and opportunity to use their old
eating habits, which are slowly being replaced.


Naturally there are multiple forces at work in their life, such as changing
self-identity and changing social norms. However, as the structure of their
daily life changes, the old habits fade away—not through a direct assault
but because other things are taking up their time and satisfying their hunger
pangs. This only works if they get far enough down the path of habit change
—and don’t quit going to the gym soon after signing up, as so many people
do. The initial choice to push ahead before the habit is formed is a
conscious one.

## **Rushed Choices and Regrettable Action**


If your users face an important decision that they’re likely to rush or not
properly think through, what obstacles can interfere with that choice and
hasty action? Rushed choices are different than intention–action gaps since
the cue is already there (they are making the decision) and the rush often
comes from the person deciding based on their intuitive reaction instead of
a careful deliberation or evaluation.


Behavioral researchers Soll, Milkman, and Payne put out a guide to
debiasing a few years ago that provides some excellent pointers on how to
do this.18 The core lesson: you either change the person or the environment.
To change the person you’d:


1. Educate them beforehand, so they’ll have the information they

need for the decision ready when the time comes. For example,
teaching people about the risks of assault at campus parties with
heavy drinking.


2. Provide an effective rule of thumb, so they can still make a quick

decision—but it will be based on a rule that gets them to a similar
place as a long thought through deliberation. For example, the rule
that you should never take on a mortgage payment over 28% of
your income.


3. Teach them to use more formal decision-making aids, like a

checklist for the many factors a pilot needs to consider before
landing a plane.


To change the environment you’d:


1. Slow people down—especially with friction. If people are making

a poor intuitive choice, add friction to switch them from System 1
thinking to System 2 thinking (i.e., change the _Ability_ to act
immediately).


2. Lessen the consequences of their biases. For example, a default

contribution rate on a retirement plan both makes it easier to take
the action of contributing (as we’ve discussed earlier) and makes it
easier to make the good choice about how much to save—as long
as the default is appropriate for the person.


In financial services, disclosure rules are meant to slow people down and
give them time to think through a big commitment—like a mortgage.
Unfortunately, people eventually learn to skip over these slow-down
devices. For that reason, stronger slow-downs are sometimes required. In


Denmark there is a 48-hour _cool-off_ period before someone can receive a
payday loan to reduce the incidence of impulsive borrowing.19 There’s
[active debate in the United States on requiring a 24-hour waiting period](https://oreil.ly/7EWHu)
before purchasing a gun.



One of the ways to avoid rushed choices and regrettable action is to try to
change a person’s time perspective. As already mentioned, we can’t focus
on all points in time at once, and we give undue focus to the present and
near-present costs and benefits of an action. That makes perfect sense when
we’re facing a tiger; less so when deciding whether or not to have another
drink or watch another episode. As Seinfeld nicely captured it: when we’re
deciding on that nighttime drink or episode, we’re Night Guy, thinking only
about what’s happening now, and not the suffering Morning Guy will
endure because of our choices.20 And so, making Night Guy (or whenever
the present-tense mind is focused on) connect with the future can help avoid
bad choices.


Finally, another technique is to bring attention to otherwise ignored aspects
of a decision. In an experiment conducted at the Financial Conduct
Authority of the UK, researchers found that a pop-up message of warning
successfully turned participants’ attention to an important detail of the
purchase: the fees they were paying.21 And, in one of my favorite
experiments of all time, Dan Egan at Betterment tested an in-the-moment
intervention to avoid a hasty investment sale. When people intended to sell
an investment, he popped up a box reminding them of the tax consequences
of the sale, slowing them down and having them look at the decision from a
different perspective.22 If there is one thing that people hate more than
losing money on an investment, it’s paying taxes!



21



22


## **A Short Summary of the Ideas**

Users aren’t a blank slate. For example, in order to spend more time with
their families, they often will need to spend _less_ time with their phones. If
they want to eat healthier, _not_ eating a tub of ice cream at a time would
help. And so, often when designing for behavior change, we need to think
about how to stop or hinder existing (negative) actions, as well as starting
new ones.


Here’s what you need to know:


Self-control often isn’t enough on its own—if people want to stop
a negative behavior and struggle, exhorting them to push harder is
likely to be ineffective, condescending, or both.


Instead, we can help people use what’s known as _situational self-_
_control_ ; just as we can shape an environment to encourage action,
we can shape an environment to slow down rash decisions and


interfere with undesirable habits and behaviors. We control the
situation (environment) in order to control behavior.


The process uses the CREATE framework in reverse:


_Identify how CREATE supports the negative behavior._


What Cues it? What causes the person to have a positive

Reaction and Evaluation? Etc.


_Find ways to change the environment to create obstacles_


Add friction, remove cues, etc. For example, add an automated

lock on the phone after a certain amount of screen-time.


_Set up a feedback loop_


To check in and see if you are being successful at stopping the

behavior, and adjust accordingly.


If the behavior is habitual, here are specific techniques to focus on:


_Avoid the cue altogether_


For example, if seeing the bar triggers stopping and getting a

drink, avoid seeing the bar.


_Hijack the cue and trigger a different behavior_


Build up a new (positive) habit that uses the same cue. For

example, see the bar: call spouse and talk about your day.


_Deploy intentional mindfulness_


Acknowledge and be aware of the trigger without overtly

exerting willpower.


While the focus of this chapter and this book is on behavior, there is also
literature on improving the mental process of decision making: to be more
careful, for example, in selecting mortgages or jobs. See Soll et al. (2015)
for a short summary of that research, but major approaches include:


_Educate_ beforehand so people will have the information they need
for the decision ready when the time comes. For example, provide
detailed training on the mortgage process.


_Provide a rule of thumb_ so they can still make a quick decision.
For example, the rule that you should never take on a mortgage
payment over 28% of your income.


Use a _formal decision-making aid_ . That is, train them to use a
mortgage evaluation tool (instead of training them to learn how to
evaluate it themselves).


_Slow people down_ —especially with friction. Time-delayed
disclosures (HUD-1 forms) are an example in the U.S. context.


_Lessen the consequences_ of their biases. For example, by using
regulations to limit the rates and fees that lenders can charge
borrowers, especially uninformed or first-time borrowers.


1 This statement is true but misleading. It is on NPR; it’s just in an article that critiques fake

news.


2 This case study derives from a phone interview and subsequent email exchange with Fadi

Makki and Nabil Saleh, both of B4Development and Nudge Lebanon.


3 [Roozenbeek and van der Linden (2019)](https://oreil.ly/24kS_)


4 Hofmann et al. (2012)


5 Duckworth et al. (2016)


6 [See, for example, Eldridge et al. (2002).](https://doi.org/10.1037/0735-7044.116.4.722)


7 [Fogg (2009b)](https://doi.org/10.1145/1541948.1542001)


8 Dean (2013)


9 Webb and Sheeran (2006)


10 And, in cases of chemical addiction, there are added layers of difficulty that make defeating

addiction beyond the scope of this book. For example, drugs can cause brain’s receptors for
key neurotransmitters to change, requiring additional levels of stimulation to attain the same
experiences that were had before the drug was used. While many of these techniques are also
used for addiction, I don’t try to cover the extensive research on addiction.


11 They’re difficult to change on their own, and, of course, there are also other factors associated

with the habit that make it more difficult to change—like peer pressure, chemical addiction,
etc.


12 Changing circumstances is used widely beyond addiction counseling as well. See Wood et al.

(2005) for research on this method.


13 Piacentini et al. (2010); Dean (2013)


14 Many thanks to Sebastian Deterding for mentioning this example. For more information, see

[Brendryen and Kraft (2008).](http://doi.org/10.1111/j.1360-0443.2007.02119.x)


15 [Baumeister (1984); Gallwey (1997)](https://doi.org/10.1037/0022-3514.46.3.610)


16 Hofman et al. (2010); Shapiro et al. (2006)


17 [Chatzisarantis and Hagger (2007)](https://doi.org/10.1177/0146167206297401)


18 Soll et al. (2015)


19 H/t Paul Adams. Payday loan companies know this would deter people, so they renamed and

[retargeted their products to get around the law (Toft 2017).](https://oreil.ly/d45vv)


20 [See Seinfeld’s discussion with Jay Leno about Night Guy.](https://oreil.ly/iQEWY)


21 Hayes et al. (2018)


22 [See Egan (2017), under “Tax Impact Preview” and prior work on tax avoidance, Sussman and](https://oreil.ly/ZWGCm)

Olivola (2011).


# **Chapter 4. Ethics of Behavioral** **Science**

_Researchers at Princeton developed an automated tool for searching_
_websites for dark patterns: “user interface design choices that benefit an_
_online service by coercing, steering, or deceiving users into making_
_unintended and potentially harmful decisions.” In analyzing 11,000_
_websites, they found 1,841 dark patterns. They even found 22 third-party_
_companies who offer “dark patterns as a turnkey solution”; in other words,_
_digital manipulation as a service._ 1


_[The term dark pattern was coined by UX specialist Harry Brignull, who](http://darkpatterns.org/)_
_categorizes 11 different types, from confirmshaming (guilting the user into_
_opting in) to privacy Zuckering (you can probably guess). He hosts a “Wall_
_of Shame” of companies clearly trying to trick their users and demonstrates_
_how Amazon makes it nearly impossible that someone will discover how to_
_cancel their account, which Brignull nicely calls a “roach motel”: you can_
_enter, but you can never leave._


_Sadly, cases of such deceptive techniques aren’t hard to find in practice. A_
_recent New York Times exposé, for example, detailed how the company_
_thredUP generated fake users to make it look like other people had recently_
_purchased a product and saved money to encourage real customers to make_
_a purchase themselves._ 2


There’s a rightful backlash against the application of psychology and
behavioral techniques in the design of products and marketing campaigns.
Products that seek to manipulate users—to make them buy, get them
addicted to our products, or change something deep and personal about
their lives like emotions—have started to gain the rightful negative scrutiny
they deserve.


In April 2019, Senators Mark Warner of Virginia and Deb Fischer of
Nebraska introduced legislation they called the Deceptive Experiences to
Online Users Reduction (DETOUR) to make it illegal for large online
services to:3


“Design, modify, or manipulate a user interface with the purpose or
substantial effect of obscuring, subverting, or impairing user
autonomy, decision-making, or choice to obtain consent or user
data”


“Subdivide or segment” users into groups for “the purposes of
behavioral or psychological experiments” without informed
consent


Operate without an independent review boards for the approval of
behavioral or psychological experiments


The effort by Senators Warner and Fischer is clearly targeted at social
media, search, and ecommerce companies, which have been some of the
worst offenders in terms of data privacy and tricking individuals into giving
their consent to data usage. But the work on dark patterns, and sadly, the
daily experience of anyone with an email inbox or mobile phone, shows
that the deception and abuse don’t stop there. And we’re kidding ourselves
if we think we’re not part of it.


Thus far in this book, we’ve talked about how to help our users succeed at
their own goals; this chapter takes a different angle and seeks to accomplish
four things:


To show the extent of unethical manipulation of users


To think about where things have gone wrong


To show that each of us is as likely to be unethical as anyone else
given the right circumstances


To look at ways to clean up our act


## **Digital Tools, Especially, Seek to Manipulate** **Their Users**

The Princeton study nicely quantifies how common dark patterns can be—
but their analysis focused specifically on shopping sites in 2019. Is this a
widespread problem? There don’t appear to be other large-scale quantitative
studies (yet), but many government and watchdog groups have analyzed the
practices of major digital companies and found them to be, nearly across the
board, manipulative. For example, in a 2018 report, the Norwegian
Consumer Council analyzed how Facebook, Google, and Windows
discouraged people to exercise their privacy rights. Google is under fire for
obtaining consent for location tracking through deception. ProPublica
shows how Intuit has tricked people into paying for tax filing—even when
it is free. Apple has even changed its App Store guidelines to hinder apps
from tricking people into subscriptions.4


And while these issues have gained prominence recently, they clearly
occurred before. Do you remember when people trusted Facebook, or at
least didn’t think it was evil? One of the initial chinks in their armor came
with an experiment they ran to manipulate user emotions, reported by the
_New York Times_, _Wall Street Journal_, and others.5 The _Times_ story started
with “To Facebook, we are all lab rats,” and went downhill from there:


_Facebook revealed that it had manipulated the news feeds of over half a_
_million randomly selected users to change the number of positive and_
_negative posts they saw. It was part of a psychological study to examine_
_how emotions can be spread on social media…_


_I wonder if Facebook KILLED anyone with their emotion manipulation_
_stunt. At their scale and with depressed people out there, it’s possible,”_
_the privacy activist Lauren Weinstein wrote in a Twitter post._


This study was part of a collaboration with academic researchers and was
widely condemned—even if it was misunderstood and blown out of
proportion.6 After that study came Cambridge Analytica, and many more
high-profile stories of broken trust with Facebook and other major


companies. LinkedIn paid millions of dollars in a class action lawsuit
because of its use of trickery to use people’s contact lists.7



I’d challenge the reader to think of three major digital companies that _don’t_
try to trick you into giving consent to using your data, sign you up for
things you don’t want, or encourage you to binge on their products despite
your better judgment. As the _Financial Times_ nicely summarized, for many
companies “manipulation is the digital business model.”8 And despite the
negative attention recently, the unfortunate revelations continue; for
example, Flo Health’s app reported to Facebook about its users’ intention to
get pregnant and the timing of their periods, without informing users.9


But it’s also important to note that it’s not a problem of “those big
companies over there.” In the broader product development, marketing,
design, and behavioral science communities, we brag quite publicly about
the ways in which we can manipulate users into doing what we want. At
numerous behavioral marketing conferences, for example, speakers talk
about their special expertise at changing user behavior by understanding the
psychological drivers of customers and using that to drive a desired
outcome. They often throw around some behavioral techniques like peer
comparisons and claim a tremendous rate of success for their clients.


Similarly, marketing and design companies tout their ability to change user
purchase behavior, without any concern or discussion about whether the
products being sold are appropriate or wanted by the end user. One example
(among many) from the field is that of System 1 Group, a marketing agency
named after a core psychological (and behavioral) model of decision
making, which advertises on their website how they use “behavioral and
marketing science to help brands and marketers achieve profitable growth.”
As written in their promotional book, _System1 Unlocking Profitable_
_Growth,_ 10 “Designing for System 1 (i.e., avoiding conscious thought
among customers) can also boost the profitability of promotions and pointof-sale materials. To increase rate of sale, shopper marketing must help
people make quicker, easier, more confident decisions.”



8



9


System 1 isn’t, I believe, a particularly egregious example. I personally
know some of the people there and at similar companies in the field; they
are reasonable people who are trying to catch the wave of interest in
psychology (and behavioral science in particular) to do marketing and
advertising more effectively for their clients. That wave of interest—and
manipulative techniques that accompany it—wasn’t something they created.


While it’s easy to find examples of digital companies (or companies in the
digital age that advertise online) doing questionable things, this is not a new
problem. One of the great pioneer researchers in the field, Robert Cialdini,
learned about the strategies and tricks of persuasion by doing field research
with used car salesmen and other in-person persuaders,11 and many
analyses have been written about the physical and psychological designs of
casinos.12 What’s different is that behavioral science is both documenting
and explicitly contributing to these efforts—especially in digital products.



11



12



Researchers and other authors like me have actively spread these
techniques. In our community, we write books on topics such as how to:13


Make games and apps “irresistible” so you can “get users…and
keep them”


Build habit-forming products based on “how products influence
our behavior”


Apply behavioral research to adjust packaging, pricing, and other
factors to create consumption


“Harness the power of applied behavior psychology and behavior
economics to break through these nonconscious filters and drive
purchase behaviors”


I’ve known some of these authors over the years, and they aren’t bad
people; they are sharing techniques that can help product designers make
better products—ones that people enjoy using and want to use. They seek to
develop relevant and engaging marketing campaigns that are tailored to
their audience’s interests. But empirically, the techniques we talk about are
used in many other ways as well, which aren’t so beneficial.14


My own writing—including the first edition of this book—clearly falls into
this category as well. We may want to help users, but we shouldn’t be blind
to what has actually happened.

## **Where Things Have Gone Wrong: Four Types** **of Behavior Change**


In the Preface and throughout this book, we’ve talked about two different
types of behavioral products:


Behavior change is the core value of the product for users


Behavior change is required for users to extract the value they want
from the product effectively


In the first case, products explicitly seek to help users change something
about their lives, like exercise bands, sleep habit apps, and mindfulness
apps. In the second case, products use behavioral techniques so the user can
be more effective at using the product itself; these types of applications and
products vary from making app menus manageable to helping users
customize their displays and focus on what they care about.


Both of them have something clearly in common: they seek to help the user
do something they already wanted to do. That’s the focus of this book:
voluntary and transparent change. There’s another type of behavior change
that hasn’t been our focus thus far, but now must be:


Behavior change is about helping the company achieve something,
and the user doesn’t know about it or doesn’t want it.


From what I’ve seen in the industry, that’s the most common type of all,
and it’s time to call a spade a spade. Our industry uses consumer
psychology, behavioral science, and whatever other techniques it can to
push people into doings they don’t fully realize, and wouldn’t want to do if
they were fully aware. [15]


Facebook’s emotion study? That was about Facebook, not about helping its
users. Marketing campaigns to use psychology to push a product (regardless
of what the product is and who the audience is)? That’s clearly about
helping the business’s profits, without thinking about the user and their
goals and needs. If we refer to the issues that make people uncomfortable
(effective persuasion or coercion, often hidden from users), that study rings
alarm bells on all accounts.


To be fair, there are many cases where unethical use of behavioral
techniques isn’t _intentional_, however, where by accident or through
competitive pressure, firms have adopted an approach that tricks their users
without setting out to do so. Teaser rates are an example: where competitive
pressures and historical practice in the credit card industry lead to
unsustainability low opening interest rates. Such teaser rates are only viable
for a company because they are replaced with much higher rates later (as
sophisticated buyers know, but the unsophisticated fall for), or user
behavior triggers punishingly high rates that make up the difference in
profits. In theory, credit card companies would be better off if they all
ditched teasers and used more transparent pricing, but if any single
company did so without the others, they would lose market share.
Manipulative techniques don’t always signal malice; still, unintended but
obvious manipulation is our responsibility just as intentional manipulation
is.16


So, is the solution simply “don’t do that”? If only it were that easy. Instead,
we have bad actors that poison the water for everyone else, products that
seek to be addictive, and problems of incentives in our industry that lead us
back to problematic uses.

### **Poisoning the Water**


Applied behavioral science has a reputation problem; there’s no easy way
for users to distinguish between “good” and “bad” actors—between
companies that are using behavioral science to help them and those that are
using it to hurt them. And, especially when companies overhype how
effective behavior science is at changing behavior (as marketers often do),


people can assume that behavioral techniques are inherently coercive—that
is, able to make people do things they don’t want. What else should people
expect from titles like _The Persuasion Code: How Neuromarketing Can_
_Help You Persuade Anyone, Anywhere, Anytime_ and _How to Get People to_
_Do Stuff: Master the Art and Science of Persuasion and Motivation_ ?


That’s based on hype, though, and not the real state of the research. The
main issue of impact in the research community is over techniques that
don’t replicate (i.e., that don’t seem to have a real effect at all), that aren’t
clear whether they generalize (i.e., all effects are context specific, and we
don’t fully understand in which contexts a particular technique helps or
not), or that backfire (i.e., something that has a positive effect to help
people in one context but actually makes things worse in another context).
That’s why throughout this book we talk about the importance of
experimentation: behavioral science has an incredible set of tools, but they
aren’t magic wands. The hype in the industry makes it seem like our tools
are magic and that makes us all look bad.


Beyond telling thoughtful companies to simply _stop_ using behavioral
science in ways that users won’t approve of, we have a problem of how to
stop the bad actors who don’t want to stop, or at least differentiate everyone
else.

### **Addictive Products**


In addition to products that go against what users want in the short term,
there’s another highly problematic category of uses:


Behavior change helps the user do something that they currently
want to do, but we know they are likely to regret in the future.


What’s an example of this? Any product that seeks to _addict_ or _hook_ its
users, without their users asking for it, from mobile games to social media.
We can see the backlash and discomfort in the field, from Ian Bogost’s
labeling of cell phones (BlackBerry, at that time) as the “Cigarette of this
[Century” to more recent stories in the](https://oreil.ly/9MB5B) _[New York Times](https://oreil.ly/IN-h3)_, the _Washington_


17



_Post_ [, and on NPR.17 These products can harm users directly (like cigarettes](https://oreil.ly/9MB5B)
harm people’s lungs) or indirectly by dominating what’s known as the
_attention economy_ :18 eating into their users’ time and attention to the point
that they crowd out meaningful interactions with friends, family members,
and others.



18



Now, the term _addict_ is used loosely in the field and often doesn’t refer to
what a medical doctor would call addiction. There’s also healthy debate on
whether technological products are actually as addictive as some
researchers say.19


From the perspective of those of us who design for behavior change, the
point remains, though: if a product or a product designer _tries_ to addict its
users (even if it can’t achieve it in the medical sense), there’s probably
something wrong. The language in the field of designers seeking to hook
people is disturbing—to the extreme of Mixpanel’s congratulatory report
called “Addiction.”20 Digital products seek to hook people on something
they want right now (even if they may not have wanted it before the
advertising campaign or sense of FOMO took root) but hurts them in the
long run. Naturally, the individual user makes a series of choices that lead
to that bad outcome. As a field, we should take responsibility for our
actions; that doesn’t imply that others shouldn’t take responsibility for
theirs as well.


So we could simply say, “Don’t addict people.” And indeed, some brave
voices in the field do, like Matt Wallaert, chief behavioral officer at Clover
Health.21 But even more than products that explicitly go against their users’
wishes, this is a hard one to tackle. There’s an easy path to self-justification,
and the business incentives are huge: products that really could hook their
users would be immensely profitable.


That brings us to the question of _incentives_ . Simply put, would a company
avoid designing for behavior change if that means hurting their business?
When we would objectively see an action as ethically dubious, would the
product managers, designers, and researchers working on the project see it
as such _in the moment of action_ ?22 It appears that, in many cases, the


answer to these questions is no. To understand and address these challenges,
let’s take a short detour from the ethics of behavioral science into the
behavioral science of ethics.

## **The Behavioral Science of Ethics**


There is significant research literature on how ethical behavior is influenced
by our environment, both explicitly in behavioral science and in the older
social psychology research tradition.


Researchers find that our environment impacts not only everyday behavior
but also _moral_ behavior. There is a long history of work showing how
factors in our environment shape whether we act responsibly or not; for
example:23


When people hear the cries of someone having an epileptic seizure
in another room, the more people who hear, the less likely that
anyone responds.


People are more likely to help others when the person gives a
meaningless reason for requesting help, instead of simply asking
for help without a reason.


People are more likely to cheat on a test when they can’t be caught,
when they see others cheat, and when they can rationalize it as
helping someone else.


My personal favorite is the story of the seminary students.24 In that study,
researchers had seminary students do an activity, at the end of which they
had to go to another building (not knowing that the travel to the other
building was, in fact, the key part of the study itself). The researchers varied
the degree of urgency with which the students were asked to move and
varied the activity the students undertook before traveling to the other
building. In one version of the pretravel activity, the students prepared to
discuss seminary jobs; in another, they prepared to discuss the story of the
Good Samaritan. The requests to travel had one of three levels of urgency.


In each case, the seminary students passed by a man slumped in an
alleyway. He moaned and coughed, and the researchers had observers
record whether the seminary students would stop and help the individual.


The level of urgency mattered—the more urgently the student was supposed
to reach the other building, the less likely they stopped. The pretravel
activity (thinking about the Good Samaritan story) did not. The
ineffectiveness of thinking about the Good Samaritan story makes the
research more dramatic and interesting, but the truly important finding was
how simply being asked to hurry changed the behavior of presumably moral
and helpful people. In particular:


In the least-urgent situation, 63% of the people helped the man
slumped in an alley.


In the medium-urgency situation, 45% stopped and helped.


In the highest-urgency situation, 10% did.


A temporary and, in the grand scheme of things, largely unimportant detail
(whether the person was asked to hurry or not) had a massive effect on the
person’s behavior. To put it bluntly, these things _shouldn’t_ matter—not if
we’re good and thoughtful people, right? But yet they do. And as much as
we might condemn the students in this famous study, I’m sure we can all
remember similar times in our lives as well—when we had something on
our minds and didn’t take the opportunity to help someone in need.


The research on moral behavior and how it’s shaped by our environment
ranges from the comical to the truly troubling. It raises serious concerns:
how can people be ethical in one situation but unethical in another situation
that is only slightly different?


It also raises questions about what it means to be a good or moral person.
Gil Hamms comes to this conclusion about avoiding the evil within: “we
should seek out situations in which we will be good and shun those in
which we won’t,” or as Kwame Appiah puts it:


_A compassionate person can be helped by this research, by using it to_
_provide a “perceptual correction” on how we see the world, and using_
_them to reinforce the good in our behavior and avoid the bad.25_

## **We’ll Follow the Money Too**


What does this literature tell us? The first lesson from the literature is that
good intentions aren’t enough; people’s environments affect ethical
behavior just as they affect other areas. And, “people” includes us (heck,
most of us aren’t as ethical as seminary students to begin with). Thinking
otherwise requires a potent combination of arrogance and self-deception.


What environment are _we_ in? Our environment, in which we apply
behavioral science, by and large, is not directed to help individuals flourish
and prosper. Many companies sincerely would want their users to be happy
and successful, but their first priority in applying behavioral science is to
increase profits, either for themselves directly or by serving as consultants
and providers to other firms. The most money is to be made either using
behavioral science to increase the profitability of products (regardless of the
user’s interests and needs) or hooking users on products that look
interesting in the short run but can cause significant downsides in the long
run.


It’s neither a new discovery nor necessarily a negative thing that companies
want to increase their profits; both good and bad come from our system.
There is a problem, however, when those of us in the product, design, and
research communities ignore the fact that we are affected by our
environment. We should expect ourselves to follow the money just like
anyone else and to use behavioral science in unethical or questionable
ways. We shouldn’t be naïve about how our _behavior_ will diverge from our
_intentions_ .


The second lesson is much more hopeful, though. Despite our impressive
ability to self-deceive and the many ways in which our environment can
nudge us to act unethically, we can also design our environment to


_encourage_ ethical behavior—that is, to turn our intentions to act ethically
into action.

## **A Path Forward: Using Behavioral Science** **on Ourselves**


How might a company or individual change their environment to support
ethical uses of behavioral science? We can find many such techniques once
we start to think about the problem as a behavioral one; in particular, as a
gap between our intentions and our subsequent actions.

### **Assess Intention**


As with any intention–action gap, the first question we should answer is
whether we intend and prioritize helping users succeed. In other words, is
the company actually concerned with the ethical behavioral science as
we’ve defined it here; that is, does the company want to help the end user
change behavior in a transparent and voluntary way?


This isn’t a glib question, nor one where the opposing side is evil or full of
bad people. Many companies find their true north in accomplishing
something that’s never been done before or in providing stable jobs for their
employees. Similarly, most consulting companies are first and foremost
concerned with providing value to their clients and not in judging what that
means for the end user. These aren’t inherently bad companies; they are just
companies for which the rest of this section won’t be relevant. Behavior
change, even within our own companies, should be _voluntary_ and
_transparent_ .

### **Assess Behavioral Barriers**


Your company might already be applying behavioral science, and you might
have a sense of where trouble could be in the future (or present). If the
challenge is one of not taking a particular ethical action, debug it with the
CREATE Action Funnel we’ve used throughout this book. If the challenge


is one of existing and problematic habits, look to the cues of those habits
and disrupt them. Above all, check the core incentives. Despite all of the
nuance that behavioral science can provide about how people’s decisions
are shaped by social cues and other factors, often the simplest economic
reason is the best place to start: we do what we’re paid to do. If your
company hasn’t started applying behavioral science, but you’re concerned
about where things might go in the future, again, basic incentives (not
intentions) are often the best place to start.


The specific barrier or challenge matters: there isn’t a magic wand here any
more than there is in any other part of behavior change work. That being
said, we can point to some techniques that might help, depending on the
particular behavioral barriers you face in your company.

### **Remind Ourselves with an Ethics Checklist**


A simple way to keep ethical uses of applied behavioral science front and
center is to remind ourselves, such as with a humble checklist. What do you
consider important in a project? Write it out. Condense it into a few
questions to evaluate each project. That’s something we’ve done on my
team at Morningstar. Then, with that checklist or set of questions, print it
out, post it prominently, and if possible, set up a process where other people
outside of the team review it.


As with other behaviors, often we simply fail to take action in the way we
desire because we get distracted by other things and lose focus or forget; a
checklist helps fix that.


Several groups in the field have drawn up ethical guidelines, from the
Behavioral Scientist’s Ethics Checklist by Jon Jachimowicz and colleagues
to the Dutch Authority for Financial Markets’ Principles Regarding Choice
Architecture.26


Here are some rules that I find useful for this purpose:


_Don’t try to addict people to your product._ This should be obvious,
but clearly needs to be reiterated.


_Don’t harm your users._ The phrase I use with the team is to always
keep our work “neutral to good” either explicitly helping or doing
something that users don’t mind and won’t cause harm. It can be
difficult to know for sure that you’re helping the user, but if even
your own team doesn’t think it will help or if people wonder if it
might be harming users, that’s a big warning sign.


_Be transparent: tell users what you’re doing._ Directly telling the
user what you’re doing shouldn’t cause a problem and is a good,
simple check on excess. A related technique is to imagine that your
work becomes front page news—would your users be upset?
Would your company survive? This technique is useful, but it’s
hypothetical. Even better is to tell them up front.27


_Make sure the action is voluntary._ The user should be able to
decide whether or not to participate in the product or service. For
example, an app that’s required at work to monitor employee
productivity isn’t optional; the job may be “optional,” but the app
isn’t.


_Ask yourself_ whether you’d want someone else to encourage you to
use the product. Is this product really designed to help you? Would
you encourage your child or parents to use it?


_Ask others_, especially strangers, if _they_ would trust the application.

### **Create a Review Body**


Checklists are great, but not very valuable if you don’t use them or you get
into the habit of marking off all the questions by rote. Having an external
review body—external to your team, or even external to your company—
can help here. In the academic community, the Institutional Review Board
(IRB) serves this function, with an independent board that reviews the
ethical considerations of any research study.


Most private companies do not work with the IRB or other external body.
But they can create an internal one without much difficulty. However,


remember the research in self-deception: the more closely aligned the
review body is to the people being reviewed (the more the reviewers see the
reviewed as friends or colleagues to support), the less valuable it is. In other
words, it helps to have strangers on the review body. Or, if strangers can’t
be found, try adding a few jerks!

### **Remove the Fudge Factor**


One of the key lessons in the self-deception research of Ariely, Mazar, and
others is that self-deception relies on a “fudge factor”: the capacity to bend
the rules a bit and still see ourselves as honest people.28 That fudge factor is
largest in ambiguous situations (where it isn’t clear whether you really are
bending the rules or not) and in situations where it’s easy to rationalize the
rule-bending (when you’re helping others or when you see others bend the
rules—as previously mentioned).


To limit self-deception, we should try to limit the fudge factor, especially
ambiguity and rationalization. To remove ambiguity, we can make the rules
crystal clear with a plain-language internal policy, or we can create
feedback processes to frequently check whether we’ve strayed from our
internal rules. To remove rationalization, we can intentionally set an ethical
reference group that is the best of the best; we can ensure that senior leaders
set the tone not only that unethical behavior won’t be tolerated, but that it
won’t help the company or other employees in the long run.

### **Raise the Stakes: Use Social Power to Change** **Incentives**


Another technique we can use is to intentionally raise the stakes against
straying from an ethical path by telling others about our commitments. In
other words, don’t just set a checklist: tell your customers, your employees,
and your friends and family, that you’ve made a particular commitment.
Tell them the rules you’ll follow for designing products and applying
behavioral science.


If your company has a reputation for honesty (which ideally yours does),
this means using that reputation to help keep yourself in line; it’s at risk if
you stray. As part of this technique, welcome attention—being transparent
about how you’re applying behavioral science is good in its own right, but
it also helps raise the stakes to not stray. If it fits your company culture, you
can also be a bit preachy: call out the abuses of other groups in the field. In
addition to perhaps helping clean up our field, it has another effect: because
people really dislike hypocrites, this approach makes it very risky to stray.

### **Remember the Fundamental Attribution Bias**


Working on behavior change in a company adds the extra layer of
complexity: within the company there can be a thoughtful range of opinions
and priorities. They may not like your approach to improving ethical
behavior—thinking it unnecessary or actually counterproductive. And when
they don’t like it, it’s simply easy to see them as naïve, deceived, or
unethical themselves. In other words, that there’s something wrong with
them. I find that, as a behavioral scientist, it’s valuable to start with the
assumption that we’re all wrong; that the other person seeks to do good, but
is just as imperfect as I am.29 It’s a small step to try to counter the
fundamental attribution bias: to assume that other people’s “bad behavior”
is because they are bad people, while ours we excuse away.

### **Use Legal and Economic Incentives as Well**


Behavioral science provides a great set of tools to close the gap between
intention and action. Sometimes, though, there really are bad actors who
have no intention to doing right by their customers, their employees, or
others.30 And in these situations, we shouldn’t be afraid of more traditional
techniques to regulate abusive practices (legal penalties and economic
incentives). Legal approaches can include the proposed DETOUR Act,
which, at the time of writing this, is imperfect but could be revised and
restructured to provide thoughtful legal oversight and penalties where they
are lacking. Economic incentives might include taxes on the use and
transfer of personal data (making some deceptive practices less lucrative).


## **Why Designing for Behavior Change Is** **Especially Sensitive**

Thus far, we’re talked about abuses in the field and how to potentially
counter them. However, are these abuses particular to behavioral science?
I’d argue that they really aren’t. We shouldn’t design products that addict
people—whether we use behavioral science or not. We shouldn’t trick users
into buying things they don’t want, nor into giving uninformed
“permission” to hawk their data.


Behavioral science offers a set of ideas for design (what to change) and
measurement (how to know if it worked). Where the idea for a design
comes from shouldn’t matter as much as whether the targeted change (the
ends) and how you do it (the means) are themselves ethical. In other words,
the simplest answer to the question “When is it ethical to use behavioral
science to try to change user behavior?” is this: “in the same situations
where it’s ethical use non-behavioral techniques to try to change user
behavior.” Unethical efforts shouldn’t be tolerated either way, and ethical
designs should be fine with or without a layer of behavioral science.


While theoretically correct, that answer isn’t terribly helpful. There _is_
something different about behavioral science in product design that makes
people uncomfortable. We can think about and understand why. From the
perspective of a user, four factors are likely at work:


_Persuasion_


It’s inherently unsettling to think that any product is trying to “make” us

do something.


_Effectiveness_


It’s especially unsettling when is a technique appears to be universally

effective; that is, that it compels us to act or do something and we have

no control over it.


_Transparency_


It’s worse when the technique is hidden; we never know it’s happening

or know only after the fact (and thus feel tricked).


_Attention_


Behavioral science has the word _behavioral_ in it and talks explicitly

about trying to change behavior. That draws our attention to it, whereas

in another case, we might not know about it.


The first three factors—persuasion, effectiveness, and transparency—aren’t
really issues of behavioral science at all. We should always be concerned
about them; doing something against someone’s will (effective coercion),
especially without their knowledge (i.e., lacking transparency), should raise
hard questions.


In terms of attention, though, behavioral science is special; people pay more
attention to, and thus are more unsettled by, sketchy uses of behavioral
science. In the design and research community, we should embrace that
critical attention. Rather than try to dismiss it as behavioral science being
treated unfairly, let’s use this attention to have an honest conversation about
persuasion, effectiveness, and transparency.


If there’s something that we’re doing that relies on people not paying
attention, that’s a pretty clear sign we shouldn’t be doing it. And yes, there
are absolutely such cases—because of behavioral techniques or not—
people are rightfully upset once they become aware of how products were
designed and function. In other words, let’s apply behavioral science to
ourselves to welcome the attention and scrutiny and special attention our
field gets to raise the stakes to unethical conduct. Because sadly, we need it.


## **A Short Summary of the Ideas**


Here’s what you need to know:


While there are always gray areas, ethical behavior change is not a
subjective, squishy thing. There are manipulative, shady practices
in our industry, and they are rightfully being called out by
journalists and regulators. We need to clean up our act.


Other disciplines also have manipulative practices—Cialdini, for
example, learned from used cars salesmen—but designing
behavior change is drawing particular scrutiny because we do so
intentionally and at massive scale. We should welcome that
scrutiny; obscurity is never a solid ethical defense.


We do need guidelines for our work. For example:


Don’t try to addict people to your product.


Only apply behavioral techniques where the individual
will benefit.


Tell users what you’re doing.


Make sure the action is optional.


Ask yourself and others if they’d want to use the product.


We’re all human though, and guidelines aren’t enough. We will
fudge things and stretch the rules just like anyone else. Applying
behavioral science on ourselves means:


_Fix the incentives_


If you’re paid to drive sales, you’re going to drive sales. If

there aren’t clear goals or incentives to ensure clients will

benefit from the product or service, then it’s too easy to fall

into murky territory.


_Draw bright lines_


Ensure that whatever guidelines you set are straightforward and

clear so any reasonable observer can talk whether they are

being violated or not.


_Set up independent review_


Is there a third party, not on your team, who reviews the

applications of behavioral science in your work?


_Support regulation_


Yes, I said it. While bills like DETOUR are flawed, some

regulation is coming, and it’s better that we make it thoughtful

and effective. Like it or not, the best way to align incentives,

draw bright lines, support independent review, etc., is to hold

our organizations legally liable for not doing so. Regulation

and penalties force attention to the issue.


Avoiding coercion doesn’t mean that you encourage users to do anything
they want to do. Your company will have, and must have, a stance on the
behaviors it wants to encourage. “Dieting” and “eating everything you
want” aren’t two equally valid options for weight loss. One works
(sometimes) and the other doesn’t. You can talk about and be up front about
that stance. If you’re helping people diet, don’t be ashamed about it. Do it,
and do it proudly, but be transparent and make participation optional.


Many types of products, even those that are explicitly coercive, can be good
and useful. The ankle bracelets used for home detentions probably fall into
that category. On net, society is better off because of their use. But that’s a
different type of product than we aim to develop here, and they deserve
scrutiny and thought. Here, my goal is to spur ideas about products that
enable voluntary behavior change so that we are clear about what we’re
doing and the means we’re using to affect user behavior.


Talking about product ethics may be an unusual topic for a book aimed at
practitioners. But we can’t outsource ethics. We should feel proud of our
work. Part of that means double-checking that the product is truly
voluntary, is up front about the behaviors it tries to change, and seeks to
make a beneficial change for its users.


1 Mathur et al. (2019)


2 [Valentino-DeVries (2019)](https://oreil.ly/M9dgE)


3 [These quotes come from Reuters (2019) and GovTrack (2019.](https://oreil.ly/6ARpC)


4 [Norwegian Consumer Council: Forbrukerrådet (2018); Google: Meyer (2018); Intuit: Elliot](https://oreil.ly/Wj0ZP)

[and Waldron (2019); Apple: Lanaria (2019)](https://oreil.ly/_jTa4)


5 [Goel (2014); Albergotti (2014)](https://oreil.ly/EaxaF)


6 Kramer et al. (2014); My thanks to Ethan Pew for pointing out that the effect size was much

smaller than was represented in the media.


7 [Roberts (2015)](https://oreil.ly/MhDyd)


8 [Murgia (2019)](https://oreil.ly/skPIF)


9 [Schechner and Secada (2019); h/t Anne-Marie Léger](https://oreil.ly/Vt_Rg)


10 Kearon et al. (2017)


11 Cialdini (2008)


12 See Schüll (2014), for example.


13 These quotes come from the Amazon book descriptions for Lewis (2014), Eyal (2014), Alba

(2011), and Leach (2018), respectively, as of June 2019.


14 Nir Eyal’s book provides perhaps the clearest example. As one author puts it in describing his

book: “the well-known book by user experience expert Nir Eyal was a hit because it showed
developers exactly how to create addictions. Yet readers often forget that Eyal gave ethical
[guidelines for using this ‘superpower,’” Gabriel (2016).](https://oreil.ly/899Pr)


15 [In addition to Brignull’s Dark Patterns site mentioned earlier, an examination of how (usually](http://darkpatterns.org/)

unintentional) bad design can harm users can be found in _Tragic Design_ by Savard Shariat
(2019); h/t Anne-Marie Léger.


16 [See Gabaix and Laibson’s (2005) shrouded attributes model; h/t Paul Adams.](http://doi.org/10.3386/w11755)


17 Bogost (2012); see Alter (2018) for a book-length analysis of addictive products and their

repercussions.


18 Thanks to Florent Buisson for the suggestion of including the attention economy here.


19 [Gonzalez (2018)](https://oreil.ly/r1_iF)


20 This report has been removed from Mixpanel’s website, but was up when I last accessed it in

June 2019, tauting the benefits of addicting your users.


21 Wallaert (2019)


22 Or hide behind either intentional ignorance or a cynical take on the mantra that “no design is

neutral” and therefore all designs are permissible?


23 See Appiah (2008) for a summary. These examples come from Latané and Darley (1970),

Langer et al. (1978), and Ariely (2013); the last study also provides a nice summary of how
self-deception operates in daily life, what exacerbates it (ambiguity, cheating to help others,
seeing others cheat), and what minimizes it (clear feedback on what dishonesty is,
supervision/surveillance).


24 [Darley and Batson (1977)](https://doi.org/10.1037/h0034449)


25 Appiah (2008)


26 [Jachimowicz et al. (2017), Dutch Authority for the Financial Markets (2019); h/t Julián](https://oreil.ly/qQkfx)

Arango


27 Telling people what you’re doing doesn’t necessarily mean to have a big banner saying,

“Look here, we’re testing the impact of this button color on speed of response.” That creates an
annoying experience for the user and an unrealistic environment for measuring the impact of
an intervention (see Chapter 13 on experiments). Rather, it means being clear that you’re
running tests and what you’re trying to accomplish overall; h/t Fumi Honda for raising the
issue.


28 See Ariely (2013) for a summary.


29 Aka, Hanlon’s Razor: “Never attribute to malice that which can be adequately explained by

[stupidity”; h/t Paul Adams. See Wikipedia for a brief history of this aphorism.](https://oreil.ly/_Lwok)


30 Thanks to Clay Delk for stressing the need for tools to handle _intentional_ bad actors. While

there are variety of frameworks out there for organizing the tools for regulating behavior and
society, my favorite framework comes from Lawrence Lessig’s _Code_ (Basic Books, 1999):
law, market, architecture, norms. Behavioral science tends to focus on architecture and norms;
we should never forget the power of the law and market.


# **Part II. A Blueprint for Behavior** **Change**


# **Chapter 5. A Summary of the** **Process**

_The Applied Behavioral Science team at Walmart and Sam’s Club_
_understands how the mind works and that there is often a gap between mind_
_and action. For example, even customers who are interested in their_
_products may not return to the store in the future. They also know that_
_theory isn’t enough: to put these ideas into practice, they need a step-by-_
_step and repeatable process._


_Min Gong, head of Applied Behavioral Science at Walmart and Sam’s Club,_
_refers to their process as “the 4-D’s”:_


_Define the business case and problem._


_Diagnose the status quo and opportunities for change._


_Design and test the proposed solution to the problem._


_Decide on whether to scale up and implement the solution more_
_broadly._


_For example, the team was recently asked to help drive in-store trips and_
_membership renewal at Sam’s Club. First, they worked with their business_
_partners to more tightly define the problem and constraints. Together, they_
_found that what was really needed was a marketing strategy that was cost-_
_effective, helped address behavioral biases among customers, and_
_supported membership renewal._


_The team studied current engagement and renewal decisions among Sam’s_
_Club members to diagnose gaps between current and desired behaviors,_
_and identified strategies to build habits that led to tangible business impact._
_They designed 20 different RCTs (randomized control trials, or A/B tests)_
_across six rounds of testing based on this understanding. As Min says about_


_their efforts, “Often we spend 70% of the time iterating on the solution; it’s_
_not something you should expect to get right immediately.”_


_The winning idea was a progressive-incentive program to reward members_
_as they returned to the store over time and it supported long-term_
_relationship and habit building. Given its demonstrated impact, and low_
_cost, they’ve decided to implement it across Sam’s Clubs. Their clear,_
_repeatable process allows the team to focus on translating insights into_
_practical, field-tested interventions._

## **Understanding Isn’t Enough: We Need** **Process**


Thus far, we’ve covered the easy part: how the mind works. We’ve also
started learning how to _intervene_ in the process of decision making and
action to help people do better. There’s a problem, though. These
interventions are unlikely to work. Or, more accurately, they are unlikely to
work in a given situation without forethought, adaptation, and learning in
the field. That’s because _all_ new products and features, whether informed
by behavioral science or not, are unlikely to have a meaningful effect on
their users’ lives without tuning them to a particular environment and target
audience.


Behavioral science helps us understand how our environments profoundly
shape our decisions and our behavior. It shouldn’t come as a surprise that a
technique that was tested in one setting (like a research laboratory) doesn’t
affect people in the same way in a real life. To be effective at designing for
behavior change, we need more than to understand the mind; we need a
process that helps us find the right intervention, the right technique, for a
specific audience and situation.


What does this process look like? I like to think about it as six steps, which
we can remember with the acronym _DECIDE_ : that’s how we decide on the
right behavior-changing interventions in our products and
communications. [1]


First, _Define_ the problem. Who’s the audience, and what is the outcome
we’re trying to drive? Second, _Explore_ the context. Gather qualitative and
quantitative data about the audience and their environment. If possible,
reimagine the action to make it more feasible and more palatable for the
user before we build anything _._


From there, _Craft_ an intervention—a behavior-changing feature of the
product or communication. We craft both the conceptual design (figuring
out what the product should do) and the interface design (figuring out how
the product should look). As we prepare to _Implement_ the intervention, we
consider both the ethical implications and how to instrument the product to
track outcomes.


Finally, test the new design in the field to _Determine_ its impact: did it move
the needle or did it flop? Based on that assessment, _Evaluate_ what to do
next. Is it good enough? Since nothing is perfect the first time, we’ll often
need to iteratively refine it.


In shorthand:


1. _Define_ the problem


2. _Explore_ the context


3. _Craft_ the intervention


4. _Implement_ within the product


5. _Determine_ the impact


6. _Evaluate_ what to do next


**TALKING ABOUT PRODUCTS**


The process of designing for behavior change is used in many
situations: developing new products or features, refining existing ones,
or developing marketing and communications. For ease of reading, I
generally refer to all of these as developing a “product.” Where the
differences between working with an entire product versus a feature or
a communication are important, I call that out in the text. Otherwise,
product is used in the general sense of something we build that can
change behavior.


It’s important to emphasize that the process is inherently iterative. That’s
because _human behavior is complicated,_ and thus, stuff is hard! If you
could simply wave a magic wand and other people would act differently, we
wouldn’t need a detailed process for designing for behavior change (and
would be very disturbing). Instead, there’s a cyclical process of learning
about our users and their needs and our efforts to address them if they miss
the mark. The most overlooked yet most essential part of the process isn’t
great ideas and nifty behavioral science tricks; it’s careful measurement of
where our efforts go awry and having both the willingness and the
necessary tools to learn from those mistakes. You can see this illustrated in
Figure 5-1.


_Figure 5-1. DECIDE: A six-stage process for applying behavioral science to intentionally change_

_user behavior_


The first part of the book laid the foundation: understanding how the mind
makes decisions. DECIDE takes that foundation and builds real, impactful
products on top of it. However, let’s not overclaim its uniqueness.


## **The Process Is a Common One**

The field has now matured to a state in which a range of approaches are
available for applying behavioral science to products and communications.
When _Designing for Behavior Change_ was first written, groups like the
Behavioural Insights Team in the UK and ideas42 in the US were starting to
do this work, but their underlying design processes weren’t widespread nor
fully solidified. There were (and still are) lots of books about biases and
nudges; _Designing for Behavior Change_ was one of the first public manuals
on the _process_ of how to do this stuff.

That’s changed. ideas42 has a published process;2 Dilip Soman’s book _The_
_Last Mile_ (Rotman-UTP Publishing, 2017) outlines how to “engineer for
behavior change”; Clover Health’s Matt Wallaert recently published a book
on his Intervention Design Process ( _Start at the End_, Portfolio, 2019). And
to be frank, they all look pretty much the same. I’d like to think that’s
because everyone else copied _Designing for Behavior Change_ ’s process,
but that’s not true. Rather, we all copied common sense and the scientific
method.


At a high level, we all settled on some similar ideas. That’s because, in
retrospect, they are simply what’s needed to do this work effectively. We
need a base of knowledge about human behavior. In Chapters 1 through 3 I
cover the foundation you need before designing for behavior change;
others, like ideas42 and Soman, similarly have it as a precondition. We need
to study the details of a particular situation and the problem at hand
(“Define & Diagnose” in ideas42’s terms; a “Behavioral Diagnosis” in
Irrational Lab’s terms). We need to come up with a proposed solution and
implement it (Soman’s “Select Nudges and Levers”). We then need to see if
it works, and iterate if not. Got it. As a field, we now have a blueprint for
behavioral design—the details of what we call each step differ, as do some
of the particular substeps along the way, but at a high level, it’s a shared
blueprint. And indeed, in many ways it is a shared blueprint with the design
community as well; many similar design and problem-solving frameworks
exist. Originally launched in 2004, the Design Council’s (2019) Double


Diamond is one prominent example; it’s a nonlinear approach to the design
process, and problem-solving overall.


So if you don’t choose to use my process, I won’t be at all offended. If
you’re using any other well-baked and thorough process, you’re following a
similar path. What really matters are the details: how you actually do it in
practice, what tools you have to carefully diagnose behavioral obstacles,
and how you select among interventions. To use a common term in design,
it’s the _artifacts_ you generate and the specific process you use to generate
them that matter. That’s what we turn to next. I hope the detailed tools and
artifacts that the rest of the book covers will be valuable for your work to
make designing for behavior change real in your organization.3

## **The Details Do Matter**


To make things concrete, Figure 5-2 shows how the six DECIDE stages of
designing for behavior change can be applied, and their specific
deliverables (or artifacts). It shows you the specific outputs that the team
will generate within each stage of the process.


_Figure 5-2. The outputs of Designing for Behavior Change at each stage of the process_


Let’s assume that a company (or NGO, government body, or individual
entrepreneur; I use “company” as a convenient shorthand for any individual
and organization making behavior change products) is developing a new
product.


To start things off, the company gains an understanding of how we make
decisions and how our cognitive mechanisms can support (or hinder)


behavior change. The two main topics to cover are the prerequisites for
action, which are summarized in the CREATE Action Funnel. From there,
we move to DECIDE. Here is how the DECIDE process works, and the
outputs the team will generate at each stage:


1. _Define_


With that knowledge in hand, it clarifies what, specifically,
the company wants to accomplish with the product and for
whom: the _outcome_ . Perhaps the company seeks a world
full of (newly) healthy people. The company then
identifies the particular group it wants to make healthier
(let’s say, office workers) and the action it generally _thinks_
will help (let’s say, walking more); that’s the _actor_ and
_action_ . If the company is working with an existing
program, then the action may be where there appears to be
a current bottleneck (like office workers with an existing
walking program, where people don’t show up regularly).


2. _Explore_


With these goals in hand, it’s time to get out in the field
and see if those goals are, in fact, realistic and wise. How
does the target audience think about the action? What
alternative actions could we take, and how do we evaluate
them? Exploration is about gathering the _data_ we need to
better _diagnose_ the behavioral obstacles users face, and
inform a thoughtful design.


3. _Craft_


The company crafts an _intervention_ or series of
interventions that will help overcome the obstacle, and
writes it up as a behavioral hypothesis, a story about how
the user will interact with the product. The interventions


are incrementally built up by changing the _action_ itself, the
_environment_, and the _user’s preparation_ to act.


4. _Implement_


Next, it’s time to actually build _the product_ . We take a step
back and perform a final _ethical review_ of the proposed
product. If everything checks out, we proceed to
development. Some engineering compromises and tradeoffs naturally occur, and the team reviews them as well for
their behavioral impact.


5. _Determine impact_


Once a version of the product is ready for field testing, the
team starts to gather quantitative and qualitative data about
user behavior to form an initial _impact assessment_ of how
the product is doing.


6. _Evaluate next steps_


A careful, structured analysis of that data leads to _insight_
_and ideas_ for improving the product. That could lead the
team members to revise their underlying concept of whom
they are helping and how, and generate a new behavioral
map and interventions accordingly. The process continues
inward until the desired level of impact is achieved. With
each revision, the team makes _changes and measurements_
of how those changes impacted user behavior.


If the company already has an existing product and wants to refine it, the
process is similar but often is shorter and more focused. It too starts with a
problem, an existing challenge or bottleneck in the product. But, unlike the
more speculative work of new product development, companies will likely
have empirical data on the actual behavioral patterns of users—to help


identify obstacles and their causes. There will be strong in-house views
about what needs to be done, which is both a blessing and a curse. That
makes analysis easier, but also makes it harder to see alternative
interpretations (i.e., confirmation bias sets in). For that reason, we
intentionally set aside time to reimagine the “obvious” solution in the
exploration phase. We may discover new avenues and opportunities, in
which case the rest of the process becomes more like new product
development work.

## **Since We’re Human Too: Practical Guidelines** **and Worksheets**


Earlier, I mentioned that _understanding_ how to change behavior isn’t
enough because our interventions require adaptation and targeting to a
specific audience and situation. That’s certainly true, and that’s one reason
we need a _process_ for designing for behavior change. But there’s another
one too: we’re just as human as anyone else. We’re unlikely to put the ideas
from the previous chapters into practice. A collection of stories about our
biases may entertain us, it may even inspire us to design products
differently, but that’s not the same thing as effectively changing _our_
behavior.


Instead, we should apply the lens of behavior science on ourselves as
product managers, designers, and researchers to think about and overcome
_our own_ obstacles to designing for behavior change. One of the best ways
to do that is to have a written process to follow, with checklists and
worksheets, so we don’t need to rely on our own overtaxed System 2 to
figure things out in the middle of a project. At the end of most of the
subsequent chapters, I offer exercises from worksheets that you can use.
[These are collected in a complete start-to-finish workbook, giving you](https://oreil.ly/behavior-change-wkbk)
practical tools to design for behavior change in your work.


I think about it like this: Chapters 1–3 are what most people want and
expect from a book about designing for behavior change. The rest of the
book is what I sincerely believe is actually needed to do it effectively. So


please stick with me. We’re going to talk about processes, checklists, and
experimental design, not because they are exciting or popular; instead,
because they’ll help you succeed.

## **Putting It into Practice**


Now that we have a good understanding of the theory behind applied
behavioral science from Part I, it’s time to put these ideas into practice.
Applied behavioral science has settled on a certain blueprint for behavioral
design; many teams have independently come up with a similar process on
how to be successful. This chapter introduces our take on that shared
process: DECIDE. As we dig into each step in the process in what’s to
come in Part II, you’ll find a “Putting It into Practice” section at the end of
each chapter. It includes both a summary of the key lessons and a set of
exercises you can use to apply these techniques yourself.


Here’s what you need to do. While different teams use different names, we
can summarize this process as DECIDE:


1. _Define_ the problem—identify the people you’re working with

(actor), what you and they are trying to accomplish (outcome), and
how you plan to drive that outcome (action).


2. _Explore_ the context—learn more about the context in which your

users live and act, and align your initial plan for action with what is
realistic and helpful to the user.


3. _Craft_ the intervention—a new screen, feature, product,

communication, etc., that helps someone overcome the obstacles
they face.


4. _Implement_ within the product—build the new intervention into

your product, feature, or communication, and include metrics and
behavioral tracking as a core part of the product itself.


5. _Determine_ the impact—by gauging their reaction and checking

whether it is having the effect you’re looking for.


6. _Evaluate_ what to do next—by learning how to further improve its

impact and judge whether those additional iterations are warranted.


The DECIDE process is fundamentally about problem-solving: because
applied behavioral science at its best is about helping your users overcome
obstacles to the choices and the actions they want in their lives. It’s a
process shared with user-centered design and many other communities.


Where designing for behavior change differs from a general problemsolving process is in the specific tools you use along the way; for example,
with a particular process for identifying behavioral obstacles—which we’ll
call a _behavioral map_ . With an understanding of the many ways one can
misinterpret changes in user behavior and thus the tools for rigorous
objective measurement. With a set of specific behavioral techniques that
researchers have discovered over the years—from temptation bundling to
implementation intentions. It’s these specific tools that’ll be our focus for
most of the remainder of the book.


### **Workbook Exercises**

Check out the worksheets at the end of each chapter in the rest of Part II for
tools to help you apply the techniques from that chapter.


[You can download the full workbook, which collects all of the worksheets](https://oreil.ly/behavior-change-wkbk)
in one place for you to use.


1 For those of you who read the first edition of this book, you’ll notice that this structure looks

different. I took three phases from the first edition (discovery-design-refine) and broke them
into two sections each—to better outline the specific steps you take. The core idea is quite
similar, but the structure is different and I’ve added new details and tips along the way.


2 [They adapt it to different domains of application, but the core is similar. See Darling (2017)](https://oreil.ly/i16qH)

for an example. Irrational Labs has a toolkit by Dan Ariely, Jason Hreha, and Kristen Berman,
_Hacking Human Nature for Good_ (2014).


3 There are a range of similarities between the detailed process and that of other authors. I’ll

cite them along the way. We’ve each tried to solve the same fundamental problem. I think this
book brings together a more holistic and detailed toolset than most, but if you disagree, that’s
perfectly fine. In the end, what matters is what helps you and your team do good by your users.
Use what works for you!


# **Chapter 6. Defining the Problem**

_If you currently save for the future, what’s your goal? I know it sounds_
_strange, but if I were to ask you in a few hours, the answer might be_
_different. That’s because we tend to respond to questions like this with what_
_comes easily to mind, either because it’s something we think about_
_frequently or we were recently exposed to._


_If I asked you right after you’d gone through an expensive neighborhood,_
_you might answer that you wanted to save up to afford a nice house and_
_lifestyle. If you’d just spoken to your father who was recovering from an_
_illness in the hospital, you might answer that you wanted to have what you_
_needed to pay for medical expenses in the future. But in reality, both are_
_true, and it would be hard to tell which was more important._


_At Morningstar, my team thought this might be a problem among everyday_
_Americans—we’d found research documenting it in particular_
_circumstances, such as MBA students not providing stable answers about_
_their goals for a summer internship and major executives not giving stable_
_answers on the goals of their company.1 If so, it would represent a real_
_challenge to how we encourage people to save and invest, since knowing_
_why people save is key to helping them commit to, and follow through on,_
_their savings goals over time._


_We decided to assess the problem among two populations: a nationally_
_representative sample of working Americans over 18, and a subsample_
_specifically of investors. We wanted to determine whether goal instability_
_was in fact a problem worth solving, and if so, test a potential action that_
_would help: using a_ master list _of goals to prompt people to think more_
_broadly._


_With an outcome in mind (reducing goal instability), an action (master list),_
_and two target populations, we could design a specific intervention: an_
_online tool to help people analyze their own goals. Indeed, we found that it_
_both seemed to be a major problem and that we could address it. In a_
_randomized control trial, testing different ways of asking people about their_
_goals, we found that when presented with our tool, nearly three-quarters of_
_the participants reevaluated and changed one of the top three goals they’d_
_initially reported, and an amazing 24% changed their top-priority goal._


_Overall, the participants’ new goals were longer-term, and more specific,_
_than their initial responses. We published the results and implemented the_
_concept in a software tool for our clients. This was possible because we_
_started with a clear understanding of the problem, the_ outcome _we sought_
_to drive, and a specific behavioral_ action _that a behavioral_ actor _would_
_undertake._ 2

## **When Product Teams Don’t Have a Clear** **Problem Definition**


I fear that we’ve all been there: six months into a two-month project, with
no end in sight. At the beginning, someone thought everything was obvious
and charged ahead. Of course we know what we’re doing, let’s get on with
building it! Six months later, you look back and wonder where all the time
has gone and why the product is still off course.


In my experience, the root cause of many bad designs—when designing for
behavior change or otherwise—comes from a lack of clarity from the start.
It comes from a researcher or product manager who had a great idea about


how to fix something and rushed to implement it without thinking through
what was really needed. It comes from a product team taking orders from
an executive to “just build this” and never really getting the opportunity to
learn _why_ that was being built or questioning whether it was the right way
to do it. And so you end up with a mess—or a misaligned product. Or, as
Yogi Berra once put it, “If you don’t know where you are going, you might
wind up somewhere else.”3


The problem isn’t unique to designing for behavior change, of course, and
there are good tools for problem definition throughout the business world
and in the design community. Here, we’re going to take a particularly
behavioral approach to this age-old problem. For us, Defining the problem
centers on:


_The target outcome_


_What_ is the product supposed to accomplish? What will be different

about the real world when the product is successful? For example, users

should have less back and neck pain, with 50% fewer doctor’s visits and

physical therapy sessions over the next six months.


_The target actor_


_Who_ do we envision using the product? Who will do something

differently in their lives and thus accomplish the target outcome? For

example, sedentary white-collar office workers who don’t exercise

regularly.


_The target action_


_How_ will the actor do it (to the best of our knowledge)? What behavior

will the person actually undertake (or stop taking)? For example, users

should go to the gym twice a week, for 30 minutes each time.


**AN ONGOING EXAMPLE: FLASH**


In this chapter, and many of the following ones, we’ll show how
designing for behavior change works with a running example: an
exercise app. Imagine that you work at a B2B company that offers
wellness programs to employees of your clients. You already have a
number of programs in place, but now your company wants to develop
a new product to help people became more physically fit through
exercise—especially by going to the gym. You can think of it as Fitbitstyle app for a B2B context. The tentative name is _Flash_ (to evoke
images of rapid, positive change in the user’s life).


Your company has seen a suite of wearable computing devices fail in
the market and has decided to try something simpler (and less
expensive to develop): an app on the employee’s mobile phone. In
particular, this is the problem definition you’re given:


_Target outcome_


Have less back and neck pain, with 50% fewer doctor’s visits and

physical therapy sessions over the next six months.


_Target actor_


Sedentary white-collar workers (employees of client companies),

who don’t exercise regularly


_Target action_


Users should go to the gym twice a week for at least 30 minutes at a

time.


We’ll flesh out this example over time, Exploring the context, Crafting
the intervention, etc.—going through the full DECIDE process. As
you’ll see, this is a _difficult_ problem and one that is difficult to build a
successful app around. We’ll use the example to show the challenges of


designing for behavior change, as well as the process. Along the way,
we’ll also use other examples to show a range of situations in which
these techniques can be applied, and just to keep things more
interesting.


Throughout the book, we’ll use those three terms, outcome, actor, and
action, to Define the problem we’re looking to solve. We’ll use them first to
express the initial _intentions_ of the company—the intended target audience,
behavior, and outcome. The real world isn’t so simple, however. As we
learn more about the realities of our users and their situations, we often
discover that our intentions aren’t realistic. And so, we’ll evaluate and
refine these three ideas until key stakeholders are on the same page, and
potential problems have been identified and resolved. We’ll build a clearer
and more impactful problem definition over time, centered on these three
concepts.


Here’s what we’ll cover in this chapter, to clearly define the (behavioral)
problem:


1. Clarify the overall behavioral vision of the product.


2. Identify who we are trying to serve—the users.


3. Identify the user outcomes sought.


4. Document our (initial) target action.


5. Define success and failure according to that action.


Your company may already have completed some of the initial stages of the
problem definition process. If so, you should feel free to jump ahead to the
part that’s relevant. However, you may find it useful to quickly scan the
earlier parts to see if there’s anything you missed. At the end of this chapter,
I introduce a worksheet that helps with problem definition (“Worksheet:
The Behavioral Project Brief”). If you can’t complete the worksheet, check
back for the relevant section on how to handle it.


## **Start with the Product’s Vision**

Inspiration for a product or a new feature can come anywhere, from a client
request to inspiration that strikes while taking a shower. Either way, you
start the problem definition by simply getting the vision of the product
down on paper. The vision can be general and somewhat vague—that’s fine.
It allows us to start the conversation about the more specific, concrete
impacts that the product should have—the target outcome.


As an example, let’s start with a product vision rooted in the mission of an
[organization. For example, the Sunlight Foundation, a nonprofit that works](https://oreil.ly/6n0Z1)
toward government transparency, gives its mission statement:


_Our Mission: The Sunlight Foundation is a national, nonpartisan,_
_nonprofit organization that uses civic technologies, open data, policy_
_analysis and journalism to make our government and politics more_
_accountable and transparent to all._


The vision for each of its products clearly follows from this organizational
mission. For example, its Web Integrity Project “monitor(s) changes to
government websites, holding our government accountable by revealing
shifts in public information and access to Web resources.”


For a company developing health and wellness programs, the product vision
might be to “help people take control of their weight and health.”

## **Nail Down the Target Outcome**


After you’ve recorded your general vision for the product, ask, What should
be different about the world when the product is successful? What’s the
specific, concrete change that should occur because of the product? What
could a third party see, hear, or touch? What meaningful thing in the real
world _changes_ because you’ve done your job?


The answer to these questions is the product’s (or feature’s) desired
_outcome_ . It’s the tangible thing that the company _seeks to accomplish_ with
the product (remember, I use “company” as shorthand for corporation,


nonprofit, or government agency). You might call it a goal, but I like the
word _outcome_ rather than _goal_ because it feels more concrete—it focuses
attention on something changing in the world.


Write down that desired outcome (or outcomes).

### **Clarify the Outcome**


Next, let’s refine your target outcome with some probing questions. We’ll
use the example of an environmental cleanup program, in which we move
from a vague outcome (decreasing pollution) to one that is clear and more
precise. Specifically, we ask:


_Which type?_


Does the product ultimately seek to change something about the

environment (e.g., clean water) or about people?


_Where?_


What is the geographic scope of the impact (e.g., Chesapeake Bay)?


_What?_


What is the actual change to the environment or person (e.g., decrease

nitrogen pollution)?


_When?_


At what point should the product have an impact? We’re looking for the

order of magnitude. Unlike the others, this doesn’t need to be precise at

this point—“in a few months” or “in five years” is fine.


_Figure 6-1. How to turn a vague outcome into a specific, measurable one_


Write down the answers to these questions with a simple, clear statement
that summarizes them. For example, “This product should cause a decrease
in nitrogen levels, an environmental pollutant, in the Chesapeake Bay over
the next five years.” The new, clearer outcome statement is displayed in
Figure 6-1.


Based on that statement of the desired outcome, define a metric that you
can use to gauge whether the product is successful or not—nitrogen levels
in the water or an employee’s weight, for example. You don’t need to settle
on the exact measurement yet—but if you can’t define one at all, then the
outcome isn’t concrete enough.


Here’s an example of clear outcomes that are readily measurable and ones
that aren’t:


_Clear, measurable outcomes_


Employees with a BMI over 25 will lose 10 pounds. Teenagers in San

Jose won’t smoke.


_Unclear, difficult to measure outcomes_


Users will gain experience with exercise. Users will understand the

dangers of smoking.


Having a clear outcome in mind doesn’t mean that you’re omniscient or that
you’re locking your company into a strict path for the next few years.
Instead, it’s a solid point of reference. As problems arise, you can settle
disagreements of fact (does this design work or not?) by measuring against
the outcome. And, you can settle disagreements of vision (is this the right
goal for the product or not?) by redefining the target outcome when needed

- _as long as the new outcome is also clearly defined_ .


**That and nothing else**


One of my favorite techniques to refine a team’s desired outcome is to ask,
“If you got exactly what you asked for (the outcome you’ve identified thus
far), and absolutely nothing else, would you be satisfied?” For example,
imagine a team that’s working to reduce teen pregnancies and had
developed an educational program. They decide that their target outcome is
that teens are aware of how pregnancy could disrupt their schooling and
future career path. If the teens were educated but didn’t care (and did
nothing differently), would the team consider that a success? Certainly not.
The team would then refine the target outcome to be concrete: they want to
decrease teen pregnancy. Education is simply one of the tactics that they
_believe_ will lead to that outcome.


Vanity metrics—metrics that make a company feel good but don’t give an
accurate sense of whether the product and company are on the right track—
fail on these criteria. For example, consider page views—the stereotypical
vanity metric. Let’s say a company had _zero_ revenue from its flagship
consumer product but had lots of page views on the product’s website. That
usually wouldn’t be considered a success. And, vice versa: if the product
brought in lots of revenue, but for some reason it had few page views, that
_would_ be considered a success.


**Avoid states of mind**


The teen pregnancy example illustrates a common problem that many
companies face as they define the product’s target outcome: they want to
talk about something within their user’s heads. Education. Confidence. Skill
at doing something. There are two reasons why states of mind are
problematic.


First, they are difficult to measure in a consistent and unambiguous way.
States of mind can be measured with surveys, but the results of those
surveys are highly dependent on how questions are framing, the question
order, when and how they are administered, and more. _Highly dependent_
means open to debate, misunderstanding, and argument. That’s exactly what
we’re trying to avoid.


Perhaps more importantly, though, states of mind probably _aren’t what the_
_company actually wants_ . Consider an NGO that trains low-income people
in developing countries to be entrepreneurs; do they want the people to
know what it takes to be an entrepreneur, or do they actually want the
people to start new, successful businesses? If the clients knew how to be
entrepreneurs but never actually started businesses, would the NGO
consider the program a success? Probably not.


Instead, we want the outcome to be something observable, outside of the
individual’s head, absolutely unambiguous (to avoid arguments within the
company about whether something is successful or not), and easy to
measure (so you can gauge success quickly). _The target outcome will define_
_the success (or failure) of the product_ . Avoiding states of mind as the
outcome doesn’t mean that states of mind aren’t important; a particular
perspective (like wanting to have a bright future without having a baby as a
teenager) may be absolutely necessary.4 However, it’s just not enough.


**Prioritize and combine**


If you’re stuck with more than one outcome, that’s fine. Multiple outcomes
need extra work, though. First, they need to be organized. If there’s a clear,
top-priority outcome, excellent. If not, get the stakeholders together and see
if there is a majority opinion on what’s most important. Or, take the list of
desired outcomes and ask for each one: would the product still be
“successful” if this did not occur? Drop them, one by one.


If winnowing down the list isn’t feasible, there is another, more challenging
route. Create an aggregate outcome that combines the contenders for top
priority. To do this, you need to get very specific and define a formula that
combines them in a way that can get everyone on the same page. This
formula is a formal definition of success for the product.


For example, say the two _highest priority_ outcomes are “employees will
have lower blood pressure” and “employees will lose 10 pounds” A
definition of success that combines them both would be “the success of the
product is defined as one point for every decrease in average blood pressure
across the target population and two points for every decrease in weight, in
pounds.”


Unfortunately, most companies just don’t have enough information to
understand the complex impacts of the product across related behaviors
before the product has been built. Personally, I’d avoid making up a


formula that combines multiple outcomes and settle on one outcome as the
top priority.


**Avoid stating how the product (might) do it**


You may have noticed that there’s an important question I didn’t suggest
asking at this point: how?


For now, try to avoid delving into how the product works its magic (i.e.,
what action it encourages users to take to make the outcome happen). We’ll
get to that shortly, after we’re armed with additional information.


We focus on outcomes instead of actions for three reasons: first, because
there may be many ways to accomplish the action, and the “best” one may
not be what comes to mind easily. Second, the link between any behavior
and the outcome is uncertain, so we keep our eyes on what really matters:
the outcome. And finally, because of “compensatory behaviors.” Human
behavior is a complex web of checks and balances, not something you just
change with a clear effect. A well-known example is moral licensing:
sometimes when people exercise, they feel so good about what they’ve
done, they go out and eat unhealthy food. They nullify any benefit that the
exercise might have had on their weight.5


**Why go through the trouble?**


Why do we need to define the desired outcomes so carefully and clearly?
We want to _pull problems into the present_ and resolve them. If the team has
a mess of conflicting objectives, or something that can’t be measured, then
there are problems lurking in the future. The team is likely to argue over
what the product should look like as each member tries to meet conflicting,
unstated objectives. The head of the company may think the product isn’t
successful, but the engineers do. The grant funding agency (for NGOs)
might cut off funding because it had implicit assumptions that aren’t met
about what the product would do.


A clear statement of measurable outcomes, which key stakeholders sign on
to at the beginning of the project, can resolve many of these problems early.


And, just as with any product development process, finding and resolving
problems early on is much cheaper than trying to fix things later.


In addition, a clear outcome statement is essential for future revisions to the
product to improve its impact. It forms the basis for measuring the product’s
success, finding problem areas, and gauging whether proposed changes to
the product are worth their salt.


**What if no one can agree on the product’s intended outcome?**


One possible result of this process is that there simply isn’t a clearly defined
outcome for the product to achieve. Either the stakeholders fundamentally
don’t agree or the product was poorly conceived and doesn’t have realworld outcomes. In that case, the product shouldn’t proceed in its current
form. In the spirit of failing fast, that’s a really good outcome—and should
be embraced, painful as it is.


That doesn’t mean the team needs to have _consensus_ about what the ideal
product should do; few companies operate that way. But everyone should
know what to expect and sign on to the goal once the decision has been
made about the product’s intended outcomes. If there are still deep divisions
in the team, then problems lie ahead. The team should move on to other
interesting products, or change its membership, rather than argue for
months over a product that’s ultimately doomed.

### **Define the Metric to Measure Outcomes**


Next, you define your outcome _metric_ . The metric is what tells you, as
unambiguously as possible, whether the target outcome has occurred, and at
what level. The outcome metric should flow directly from the target
outcome itself. It’s how you determine if the outcome is there or not. You
should define and write down a formula, even a dirt simple one, which says
how the outcome is measured. Here are some easy ones:


_Company income_


Money received from client companies over the course of a month


_User weight_


Body weight without shoes, measured in the morning after breakfast


And here’s one that is a bit more complex:6


_Neighborhood connectivity_


Number of times users attend social gatherings with their neighbors

over the course of a month


Ideally, the metric should be:7


_Accurate_


It actually measures the outcome you want to measure.


_Reliable_


If you measure the exact same thing more than once, you’ll get the

exact same result.


_Rapid_


You can quickly tell what the value of the metric is. Rapidness

encourages repeated measurement and makes it easier to see if a _change_

in the product was effective.


_Responsive_


The metric should quickly reflect changes in user behavior. If you have

to wait a month until you can measure the impact of a change (even if it

only takes a minute to measure it; i.e., even if it is rapid), that’s 29 days

wasted that you could have been learning and improving the product.


_Sensitive_


You can tell when small changes in the outcome and behavior have

occurred. For the developers among you: floating-point values are great;

Booleans are not.


_Cheap_


Measuring the outcome _multiple times_ shouldn’t be costly for the

organization or it will shy away from measuring the impact of

individual changes to the product and have difficulty improving it.8


Quite a lot there, right? Yes, but that doesn’t mean you need to obsess over
the perfect metric. What we’re really looking for is a quick check of
sufficiency. Treat this like a checklist—for a given outcome metric, ask: is
it specific enough that there won’t be too much disagreement when it’s
measured? Is it reliable enough that it won’t fool the team into thinking the
product is working when it actually isn’t?

### **Working with Company-Centric Goals**


Thus far, we’ve talked about a product development process that’s focused
primarily on the user and what the product can do for them. But I’ve found
that companies sometimes take two very different approaches to behavior
change. They can either:


Focus on how the product will _benefit the user_, which in turn helps
the company’s bottom line


Focus on how the product will _benefit the company_, by way of
providing value to the user


This difference is in how companies think about the _value_ of changing
behavior; it isn’t related to the behavior itself. The target behavior could be
inside the product or outside the product, socially important or trivial; that
doesn’t matter as much.9


In the first case, which we’ll call a _user-centric approach_, the company
might have a vision of improving financial wellness (like Acorns or Mint)
and need to figure out what actions users can reasonably take that will best
make that happen. In the second case, a _company-centric approach_, a
company might have a purely self-interested goal, like increasing customer
renewals, but needs to provide real value to the user in order for that to
succeed. The second approach includes red-blooded capitalists as well as
NGOs that need to make their case to their funders. There’s nothing wrong
with that approach—as long as the companies build products that people
like. But it does mean that the process is different.


In the user-centric approach, the process of Defining the behavioral
problem is this:


_Product Vision (for the User) → User Outcome → Actor → Action_


In the company-centric approach, we add another step:


_Product Vision (for the Company) → Company Objectives → User_
_Outcome → Actor → Action_


The product vision is _why the product is being developed_, at a high level;
and the company objectives are _what the company seeks to achieve_, for
itself, by building that product.


Since the previous section highlighted examples of the user-centric
approach, let’s now walk through the company-centric process (you can
safely skip this if you’re using a user-centric approach).


**State the vision**


As before, the Definition process starts by writing down the high-level
vision the company has for the product. That vision, however, should
answer how the product will generally benefit the company. For example,
this product should:


Expand the company’s appeal into new markets.


Increase revenue.


Demonstrate the expertise and capacity of the organization to take
on new projects, to support new grant funding.


Increase public awareness and interest (or brand prestige) of the
organization.


**State the company’s objectives**


With the company’s vision for the product in mind, translate that vision into
one or more specific, measurable objectives that benefit the company. For
example, ask:


How will the product be judged a success or failure at fulfilling the
company’s vision? How will success be measured?


What would a third party observe about the company that’s
different because of the product? Increased retention of customers?
Increased upsell? More referrals of new customers?


The company’s objective might be to win 35% of the wellness program
market among technology companies in the next year. Or it might be to win
at least one million dollars of additional grant funding for the next year.
Write down that initial company objective.


Based on that initial statement of the company’s objectives, fine-tune it by
asking who, what, when, and where the outcome occurs (as we did in the
previous section).


**Define the user outcomes**


Building your business or establishing your expertise to funders is great, but
your users probably don’t care. Sorry. You need to deliver something of
value to them. Without that value, you can’t meet your business objectives.


So, putting aside the financial (or other self-interested) goals of the product
for a moment, what does the product mean for users? We want to define the
measurable changes in the world that are caused by the product _that the_
_user would care about_ .


Here are some questions to help draw out those outcomes:


What does the product deliver? What’s its core value proposition
as the user would see it and measure it?


After users have used the product, what’s different about the
world?


What tangible thing would a user look at (or hear or see), sometime
after using the product, and say, “Hey, I want to use that product
again”? (The product itself doesn’t count, sorry.)


How would you know that your users have gained the maximum
value from your product?


What do the users _do_ because of the company’s increased brand
awareness?


For example, consider the company objective of winning 35% of the
wellness program market among technology companies in the next year.
The specific user outcome might be what we identified above for our _Flash_
app: the product helps the user decrease doctor and physical therapy visits
by 50% over six months. Or the product might help the user drop two waist
sizes.


In the previous section, we discussed a set of rules and tips for clarifying
target outcomes. All of them apply for company-centric goals as well: avoid
states of mind, make sure the outcome is measurable, find disagreements
early, and don’t obsess about _how_ the product will achieve these outcomes
yet.

### **A Quick Checklist**


In summary, this is what makes a good outcome, both for the user-centric
and for company-centric goals:


The outcome is _what will be different_ in the real world when the
product is successful.


The outcome should be something _tangible_, and not something in
the user’s head. Often the user’s head is just a proxy for what the
company really cares about—a tangible outcome that occurs
because the user’s knowledge or emotions have changed. For
example, lower BMI, or pounds lost, instead of knowledge about
the importance of exercise and maintaining one’s weight.


The outcome should be something _unambiguously measurable_ . For
example, say your product is supposed to “decrease government
corruption.” What is corruption, exactly, and how is it measured?


The outcome should be able to _signal success_ . If you can say,
“Well, if X didn’t happen, the product would still be a success,”
then X is not the outcome we’re looking for.


The outcome should be able to _signal failure_ . You must be able to
think of a plausible case in which the outcome would indicate that
the product is failing.

## **Who Takes Action?**


Usually the company’s business goals and market research specify who a
product is supposed to serve: the people who buy the product (private
company) or the people who they are tasked with helping (NGOs and
government agencies). Here, we need to dig a bit deeper. We want to know
not just who the product will serve, but who is it that will take action?
Whose behavior are we seeking to change?


Often the person being served and the person taking action are the same:
user = actor. But that’s not always the case. The user may influence another
person, who then does the real work. This is common in situations like B2B
sales (where the user is a different person than the buyer) and with
advocacy websites that try to influence policymakers to change regulations
(like on the cost of gasoline), which then change behavior in society to
drive outcomes (like lower greenhouse gas emissions).10 For the sake of


simplicity, though, and to use language people are familiar with, I’ll assume
they are the same for this discussion.


Write down the target actor as specifically as possible: age, gender,
location, number of people, and so on. It can also help to write down who is
_not_ being targeted; for example, people without smartphones, the wealthy,
or expats.


In all likelihood, some target actors aren’t a good fit for the product, and
you’d waste your time trying to target them. True. For now, we want to
know the _potential_ actors you should investigate further. You may end up
targeting only a subset of them.


If the company has no idea who it is trying to serve and who needs to take
action, then it’s back to the basics. A behavioral product, like any product,
must serve a user need. It can only help people change their behavior to the
extent that they care about the product at all. To get a handle on the unmet
user need, you need a traditional market research or (non-behavioral)
product discovery process. That’s beyond the scope of this book; from here
on, I’ll assume you have a sense of the target user already.

## **Document Your Initial Idea of the Action**


Thus far, we’ve intentionally not talked about how your actors would
accomplish the outcome. That’s to help us separate and clearly think about
the outcome, without assuming a particular way to accomplish it. But, of
course, we have ideas about what action the person should take. We need to
record that idea. It won’t necessarily be correct—but by writing it out, we’ll
better be able to evaluate and refine it.


What defines an action? I think about it as two blanks you want to fill out in
this sentence:


_Our product will help the user [start/stop] doing [describe action]._


For most companies, especially those with existing products on the shelf,
the universe of possible user actions is tightly constrained by the company’s


business model, product strategy, and internal culture. At HelloWallet, for
example, we looked for actions that would be appropriate for a wide range
of users and weren’t being well covered by existing products, that fit our
company mission. So job-hunting tools were out, as were mortgage finders
and pure lead-gen tools.


Next, ask specifically, “How does the action cause the target outcome?”
The action should directly and clearly cause the target outcome. If the
current action doesn’t do that, is there another, later action that _does_ cause
(or is a missing piece that’s required to cause) the outcome? If so, focus on
that one instead. We want to target a behavior that directly supports the
outcome.


For example, let’s assume we want to drive community volunteerism. The
action “Go to a seminar about the importance of community engagement”
_might_ lead people to get more involved in their communities. The direct
link between the action (go to seminar) and outcome (community members
volunteer) is a bit tenuous though. What if the person doesn’t pay attention?
What if they’ve been forced by their spouse to attend such events in the
past? A better, more immediate action is “Volunteer at a local soup
kitchen.” That’s the real point of the seminar and has a direct link to the
outcome we care about. A seminar might be a useful tactic along the way,
but it’s only a tactic to support action—it’s not the target action itself.

### **Clarify the Action**


As we did for the company’s target outcome, we’re looking for a concrete,
specific definition. A physical, measurable action someone will take. Avoid
actions that just affect the person’s mental states (reading educational
material) and dig deeper into what the person does with their new education
that causes them to _do_ something differently and achieve the outcome.


For example:


_Outcome sought_


People don’t get lung disease.


_Vague action_


Users avoid cigarettes. (Does that mean they cut down on smoking? Go

cold turkey?)


_Action that’s too far removed from the outcome_


Users attend a seminar about the dangers of smoking (OK, but do we

care if they attend? Or that they actually stop smoking?).


_Clear action_


Users don’t buy cigarettes at all.


You’ll notice that the action doesn’t specify how exactly the product will
help the user not buy cigarettes. It could be by helping them avoid stores
where cigarettes are sold, or by decreasing the desire to smoke with nicotine
patches.


Like the target outcome, the target action isn’t written in stone. It should be
clearly defined so that it can be built into the product and clearly measured.
The definition, and measurement, will help with fine-tuning the product.
They’ll also help with revisiting and revising the target action itself, if the
need arises.

### **A Metric for Action**


As we did with the outcome, we want to translate the target action into a
specific metric that will assess whether people are taking action. The action
metric tells you whether (and to what degree) the user is taking the target
action, the action that is supposed to drive the desired outcome. If the
desired outcome is a specific level of weight loss and the action is exercise,
a sample metric would be “How much is the user exercising, and how
often?” A good action metric must pass the same tests as the outcome
metric: accurate, reliable, rapid, responsive, etc.


The action metric covers _what_ is measured, _how_ it is measured, and for _how_
_long_ . For example, one way to define purchase behavior for a particular
product is: money spent (not flexible future commitments) through product
sales and subscriptions over a 30-day period.


It also needs to be specific, because if the value changes over time,
specificity helps us determine if it changed because of your product. If the
definition is unclear, a change in the data may be caused by a change in
how people interpret or measure it.


Here are two examples of action metrics:


Action: “the user exercises”


_Bad metric_


User exercises = how much the user reports exercising each

day. This is a bad metric because (a) the user may not know

how hard they are exercising without the help of a timer, heart

rate monitor, or other tracker and (b) the user may stretch the

truth.


_Good metric_


User exercises = how long and how hard a heart rate monitor

automatically tracks the user exercising each day.


Action: “the user studies a new language”


_Bad metric_


User studies = an expert evaluation of language proficiency on a

lengthy written exam. This metric is problematic because it

focuses on the intended _outcome_ rather than on the _activity_ that


we assume, rightly or wrongly, leads to that outcome. It also

takes a long time to measure and can’t be measured frequently

(without annoying the users!).


_Good metric_


User studies = time spent within the application, or number of

exercises completed with a minimal level of accuracy.


Clearly there are trade-offs when creating action metrics. The most accurate
metric may take too long to gather, or the cheapest metric may not be
reliable. Again, there’s no need to obsess over it—we’re looking for an
action metric that is sensitive enough to quickly show when there’s a
problem and accurate enough to not mislead the team.

### **Look for the Minimum Viable Action**


The _minimum viable action_ (MVA) is the shortest, simplest version of the
target action that users absolutely must take to so that you can test whether
your product idea (and its assumed impact on behavior) works.11 It builds
on the Lean start-up concept of the minimum viable product: the smallest
set of features that allows the product to be deployed and tested in the field.


How do you find the MVA? Look over the action you’ve proposed. I think
of the minimum viable action as something that you arrive at by cutting
back on what naturally came to mind the first time. Cut back from the
obvious until only the necessary remains:


1. _Cut repeated actions down to the first action._ If you have a

repeated action, can you start by supporting a one-time action?
One-time actions are easier for users to perform and engineering
teams to build than repeated ones, all else being equal. And they
still provide valuable insight into whether the software works at
supporting the behavior. For example, if you want to help people


lose weight by getting them to run two miles twice a week, see if
they will run or jog _at all_ before trying to change their regular
routine.


2. _Cut big actions down to simpler ones_ . Even if the target outcome

won’t be achieved initially, can you cut the action down into
something smaller and shorter but still fundamentally the same
basic task? The goal is to test the core premise, as with a minimum
viable product (i.e., instead of asking people to run frequently, can
they start with a group jog?)


3. _Drop steps in the sequence altogether._ Can you identify the high
risk, most uncertain aspects of the action (i.e., having people feel
comfortable running alone in a new place) and either remove them
altogether from the target action (e.g., run at work with colleagues)
or field test them before developing the lower-risk aspects?
Similarly, are there steps that are just nice to have and can be
removed?


I find that people don’t naturally think about the smallest possible action to
change behavior. We like to think big. That’s fine. It’s useful, good, and
most natural (i.e., easiest) to express that big vision first. That provides a
blueprint that the team can go back to and draw upon as the product
develops.


However, once those big behavior change thoughts are up on a board, and
we see all of the pain we’re thinking of putting our downtrodden users
through, then reality should hit—the more work that users have to do, the
less they are likely to do it (with some important exceptions I’ll cover later).
Hence, the MVA.


To demonstrate the idea, let’s use an example of helping users learn
Spanish. Here are actions that the team might target:


Complete an online training course.


Visit Spain for a few weeks to be immersed in the language.


Label each item in the household with their Spanish names.


With simpler MVAs, you can test the core assumptions of the approach and
its impact more quickly:


Complete a single module of an online training program.


Get a Spanish-language conversation partner who is committed to
only speaking Spanish with the user.


Label a few items in daily use with their Spanish names.


OK, we have a rough idea of the potential action that users might take. The
next chapter will dig deeper into exactly who the users are and whether that
action is realistic for them to take.

## **A Hypothesis for Behavior Change**


You now have all the things you need to determine what success and failure
would mean for your product _before you build it_ . You know who the
product is supposed to serve. You know what real-world outcome that
action is supposed to cause. You have an initial sense of the action you want
to drive in order to accomplish that outcome. You don’t have all of the
details, of course, but that’s OK. At this stage, you have the rough outlines
you need.


Write down a sentence that says what the product is supposed to be doing,
and for whom. For example:


_By helping overly sedentary white-collar workers (actor) to go to the gym_
_(action), our product will cause them to have less back and neck pain and_
_go to the doctor and physical therapist 50% less often (outcome)._


As other authors have thoughtfully noted, we can think about this as our
_hypothesis for behavior change_ .12 The general format is:


_By helping the [actor] [start/stop] doing [describe action], we will_
_accomplish [outcome]._


It’s a nice way to structure the outcome-action-actor, and it reminds us that
everything we plan to do is just a plan. It’s full of assumptions about the
real world, and calling it a hypothesis (which it is) helps us remember that
it’s something we need to test to see if, in fact, we’re right and we’ll have
the effect we hope.


Now, from your user research about what’s feasible for users to accomplish
and from your market research about what will differentiate and sell the
product, you should be able to add in specifics about the proposed product
and its impact on your business. For example:


_By helping 25 to 35-year-old white-collar employees of tech companies_
_in urban areas (actor) to go to the gym twice a week for at least 30_
_minutes (action) the product will cause them to decrease their doctor and_
_physical therapy visits for back or neck pain to 50% less than they_
_otherwise would have had over the following six months (outcome)._
_When successful, it should double our current revenue (company_
_objective)._


In this statement, the team is saying: if this happens, the product will be a
success; if not, it will be a (complete or partial) failure. Later on, we’ll
translate this statement into a set of metrics to gauge whether the product
actually succeeded or failed at its goals.


Our goal isn’t to create a false sense of security by thinking we can forecast
the future and how the product will actually play out. There are lots of
assumptions built into this definition of outcome, actor, and action. We
want to draw out those assumptions, to get something that can be explicitly
tested and then revised as lessons are learned. Once they’re on paper, we
can review and improve them—through pre-mortems, thinking-hat reviews,
and such.13 And, perhaps most importantly, it helps us fail fast—to make
sure that the key stakeholders in the company are on the same page before
building the product. If they aren’t, now’s the time to fix it.


Defining success and failure ahead of time doesn’t mean that we can’t
change the goalposts now and then. As we learn more about the market,
product, and the company’s other opportunities, our understanding of


what’s “good enough” will change. But make sure the team knows about
the change and understands the rationale. No one likes a moving target—
especially when that means making the job harder for the team midstream
and without explanation (raising the standard) or it seems like accepting
failure (lowering the standard).

## **Examples from Various Domains**


Desired outcomes and target actions can be a bit abstract, especially given
the tremendous range of possible products that can affect user behavior. So
let’s look at some concrete examples (Tables 6-1 and 6-2). Since the
approach is somewhat different for user-centric versus company-centric
products, I’ve broken them up into two different tables. I’ve started both
tables off with our sample product—the Flash running app—to show how
the analysis would proceed from each perspective.


_Table 6-1. User-centric examples_


**Example 1** **Example 2** **Example 3**



Product Flash, an exercise app Financial wellness app
(Acorns)



Cigarette Cessation



Outcome Less back and neck

pain (fewer doctor and
physical therapy visits)


Action Go to the gym twice a
week for at least 30
minutes





Users automatically
transfer money to
savings account each
month





Americans have
sufficient emergency
savings



Cigarette smokers stop smoking







Smokers switch from cigarettes
to vaporizers and decrease total
nicotine intake by 50%


_Table 6-2. Company-centric examples_


**Example 1** **Example 2** **Example 3**



Product Flash, an exercise
app



Breathalyzer





Company
objectives



Increase revenue
from corporate
wellness program
clients



Grocery store
website


Double number
of upscale
buyers



Attain 25% market share in three newly
entered states











Actor White-collar
technology
company
employees



Upper-income
Denverites
commuting
from the
suburbs





Drivers in the targeted states, who have
had a suspended license, a ticket,
and/or an accident from a DUI in the
past




## **Reminder: Action != Outcome**

Despite our best efforts, there may be a big leap between the outcome and
the action. Will transferring small amounts of money into a savings account
(when the user can choose to transfer it back or spend it) really solve the
broad lack of emergency savings in the United States? That’s a tough
question to ask. The purpose of this chapter was to provide a clear direction
for the product development process, uncover hidden assumptions, and,
sometimes, determine that a pivot is needed, and a different approach or
behavior should be targeted.


Sometimes the outcome that’s important is, in fact, an action that the user
takes. The first example could easily have had “users exercise” as the
outcome, as well as the action. This occurs when the action itself has an
unambiguous, real-world outcome (like exercise). However, I argue that
companies should avoid equating the two in most cases. It’s an easy way to
hide assumptions about why the action is important and thus to potentially
choose the wrong action.

## **Putting It into Practice**


This chapter started off the DECIDE process by Defining the problem; in
particular, with the outcome we’re seeking to achieve, for whom, and our
initial idea of how (an action). Here we summarize the key lessons and
show you how to use the exercise in the workbook.


Here’s what you need to do:


Define the real-world outcome that the product should have. Avoid
states of mind—focus on measurable outcomes that define the
success or failure of the product.


Translate company-specific goals (e.g., increased profit) into realworld outcomes that the user actually cares about.


How you’ll know there’s trouble:


The company can’t agree on the intended outcome of the product.


The company knows what it wants but doesn’t offer something that
users care about.


Deliverables:


The behavioral project brief: a clearly defined outcome, a clearly
defined target population (actor), and an initial idea for the action
the actor will take. You can bring all of these together into a
_hypothesis for behavior change_ .


Learning about a technique often isn’t enough on its own. Perhaps the
biggest obstacle readers faced with the first edition of _Designing for_
_Behavior Change_ was that they were unclear on how exactly to act on it,
and that kept them from getting the most out of the book.


For Defining the problem and each of the other steps in DECIDE, we have
exercises your team can go through to implement the process. For all of the
exercises, we’ll use a consistent example throughout: the Flash app
introduced in the sidebar at the beginning of this chapter. In this example,
your company provides wellness software to employers, who then provide
it to their employees. You’re working on a mobile wellness app to help
people exercise—it’ll be a new product for your company, and you’re just
starting on the project.

## **Worksheet: The Behavioral Project Brief**


_Goal: Understand and articulate the aims of your team’s new product—the outcome, action, and_
_actor it should target._


Project: Flash app


☑ New product, feature, or communication?


☐ Change to existing product, feature, or communication?


Vision: Briefly describe _why_ you want to change behavior and how this product fits in. Flash will
help employees take control of their health.


Outcome: What do you hope to achieve with the product? Consider both the company’s objective,
as well as the real world, measurable change users will see and value. Then, drill down and define
a rough metric your team can use to evaluate the product and an idea of what success looks like in
numbers.


Company objective: Increase revenue from corporate wellness program clients.


Real-world outcome: Less pain (back, neck, etc.)


Performance metric: Doctor and physical therapy visits


Definition of success: 50% decrease in doctor/PT visits


_Actor: Who is the specific user (or person involved in the product) who causes the outcome?_


Who is the actor? Sedentary white-collar workers


_Action: What does the actor do/stop doing to accomplish the outcome? This an initial idea; we’ll_
_refine it later._


What is the action? Go to the gym twice per week


A Hypothesis for Behavior Change: Alternatively, you can write out this information as an
explicit hypothesis to remind the team that nothing is for certain, and you’ll need to test that
hypothesis in practice through the product:


By helping [actor] sedentary white-collar workers ☑ Start ☐ Stop doing [action] go to
the gym twice per week, starting with 30 minutes per session, we will accomplish

[outcome] decreased pain and a 50% decrease in doctor or PT visits over six months..


1 Bond, Carlson, and Keeney (2008); Bond, Carlson, and Keeney (2010)


2 Detailed results from this study can be found in Sin, Murphy, and Lamas (2018).


3 Yogi Berra was a professional baseball player and coach, known for his (mal)aphorisms. For

example, see _[“Yogi Berra Dies at 90”](https://oreil.ly/H6Md3)_ in the _LA Times_ .


4 My thanks to Brian Merlob for pointing this out.


5 Again, h/t to Brian Merlob for this one.


6 Originally inspired by the (now-closed) community connections start-up, Neighborsations.


7 There are a variety of perspectives on what makes a good metric but no generally accepted

and applied definition. These are characteristics that I’ve found to be important.


8 It may take an up-front investment (that isn’t cheap) to make recurring measurement cheap.

We want to set up data collection that will be cheap and easy to check whenever there is a
change to the application. Survey data, for example, is often “cheap” to measure the first time,
but the cost usually remains the same with each iteration (and survey data is plagued with
biases, as we discuss in “Figure Out How to Measure the Outcome and Action by Hook or by
Crook (Not by Survey)”). Ideally, we want automatically gathered administrative data—
collected from the original source without human intervention or extra costs. Asking people
what they spend money on is a survey. Their actual credit card transactions are administrative
data.


9 In other words, this is a different distinction than the one I made in the Preface about behavior

change affecting a behavior _within a product_ or _outside of it_ . In either case, a company could
start with the benefit for the user or the benefit for the company.


10 My thanks to the folks at ForumOne for pointing this out.


11 In the context of habits, BJ Fogg has a similar idea in his new book, _Tiny Habits_ (Fogg 2020).


12 My thanks to Rajesh Nerlikar for first introducing me to the idea. Matt Wallaert has a similar

idea in his book, _Start at the End_ (Wallaert, 2019).


13 On pre-mortems, see Klein (2007)—h/t Paul Adams. On thinking hats, see De Bono (2006).

There are also many assumption-mapping techniques to draw out (and question) assumptions
[in a decision or process. As discussed in Booth (2019), Shopify has a fun one called the](https://oreil.ly/OPNxs)
_assumption-slam_ —h/t Anne-Marie Léger.


# **Chapter 7. Exploring the** **Context**

_Clover Health’s Behavioral Science Team shows how we can combine_
_qualitative and quantitative research to Explore the context of our users’_
_lives. From survey data, the team knew that some members reported_
_difficulty getting the care they needed. So, the team tried to understand the_
_underlying causes._ 1


_After talking with clients and checking the data, they found that people in_
_lower income neighborhoods especially reported not getting quality care._
_The team hypothesized: perhaps lower income neighborhoods attracted_
_lower quality doctors, making it essentially an issue of access?_


_However, the data showed this simply wasn’t true: low-income_
_neighborhoods had high-quality doctors and enough to serve Clover’s_
_members there. Members simply weren’t finding their way to those doctors._
_But why?_


_In interviewing members, they learned that the problem wasn’t access but_
_learned behavior. Because many of these members had faced a lifetime of_
_medical racism, they simply no longer believed that good doctors existed—_
_and so they didn’t look for them. In a self-fulfilling prophecy, the very_


_inequity they’d faced in the past led them to face continued inequity in the_
_present. They took whichever doctor they found. If they happened to get a_
_good doctor, they received good care. But if they ended up with a bad_
_doctor, they simply ascribed it to an unjust system and continued to see_
_them._


_With this understanding of the context of people’s lives, the behavioral_
_science team developed a number of interventions, from providing an_
_annotated map of good doctors in the area to calling members and_
_introducing them to better doctors in their neighborhoods.2 Overall, more_
_than 80% of targeted members were redirected to high-quality, equitable_
_care._


Each of us has different routines, experiences, and ways that we respond to
the world. To design for behavior change, we need to discover the right
action for your users based on this complex terrain of routines, experiences,
and responses. The action must be effective at helping them achieve their
goals. And, at the same time, you must balance user needs against the needs
of the company building the product—to generate revenue and to costeffectively deploy design and engineering resources.


In Chapter 6, we clarified what the company sought to accomplish with the
product (the _target outcome_, like people having less back and neck pain)
and identified a potential action that users could take to make that happen
(such as going to the gym or going on a diet). These steps helped us identify
what _we_ want to accomplish. If only the world would oblige and make
people’s behavior conform to our plan. Naturally, it doesn’t.


Now it’s time to confront our assumptions and goals with real users. We’ll
revisit the outcome, actor, and action and evaluate them according to
company and user needs. Along the way, we’ll also gather vital information
about the target users for designing the product itself. The end result is a
refined problem definition, especially of the _action_ we want to target and a
_diagnosis_ that captures why we believe that action isn’t currently occurring.


Here’s how we’ll do it:


1. Get to know your users and how they feel about the target outcome

and action.


2. Generate a list of other possible actions they could take.


3. Evaluate the list of possible actions and select the best one.


4. Express that big action as a series of micro-steps.


5. Diagnose why the action isn’t occurring currently.

## **What Do You Know About Your Users?**


Clover Health’s example of underserved patients and medical racism
illustrates the importance of learning about your users—their real lives and
circumstances, their desires and interests, and especially how they relate to
the behavior you’re seeking to change. We need to gather data, both
qualitative and quantitative, to better target our interventions and find
realistic solutions for our users’ lives.

### **How Do They Behave in Daily Life?**


First the team should seek to understand where users are starting from. In
particular, what are they currently doing?


I’ll use an example from my past life as a microtargeter (someone who
analyzes data about large numbers of individuals to identify people who are
likely to take action and what will appeal to them). One of my company’s
clients was an advocacy organization, which I’ll call ActMore so they don’t
feel obliged to sue me. ActMore is an environmental NGO and wanted to
help its constituents become more deeply involved in ActMore’s
community of like-minded environmentalists. They had a large number of
people who had signed up for their email list and newsletter and had said
they wanted to do more but hadn’t yet really gotten involved. First ActMore
needed the basics—information about age, location, income level, race,
gender, political interests, and so on. My company used data that the


organization already had to fill in most of the basics. We could use that to
target the appeal and provide guidance on the website.


That type of analysis is all standard stuff and is well covered in any book on
product development or assessing market opportunities (as well as in
political advocacy books, in ActMore’s case). We then started on the more
interesting part, though, focusing on behavior. We wanted to understand
how strong the members’ interest would be in a specific event the
organization was putting together—a rally on Earth Day. We were looking
specifically for divisions within the member base: groups of people that
would respond differently to appeals to join the rally. Each group would get
its own personalized appeal that made sense given its background and level
of experience. The product we were shaping was an outreach campaign and
associated website (and, as I remember, there was a phone-calling
component as well). So, we started digging into the data available about the
members to understand who the product would need to serve.


With ActMore and other organizations I’ve worked with, I’ve found the
following questions most relevant to learn about the user base from a
behavior-changing perspective:


_Prior experience with the action_


Do the users have experience taking the target actions? (For ActMore—

have they been to other, similar rallies?) How do they think about the

action? Are there strong emotional associations, or is this fresh ground?

It’s much easier to increase an action than to start a new one. Existing

_habits_ around the goals are especially important.


_Prior experience with similar products and channels_


If the product employs email and a website, do some users have regular

access to a computer (and know how to use it) and others don’t?


_Relationship with the company or organization_


To put it bluntly: do users trust you? You’ll have a harder time making

your case, and need a different set of appeals, for the people who don’t

trust you versus those who already know you and love you.


_Existing motivation_


Why would users want to achieve the outcome, completely separate

from what the product offers them? In other words, what can the

company build upon so it doesn’t need to do all of the work itself? One

especially powerful aspect of motivation is social motivation (positive

or negative). What will users’ friends and family think if/when they take

each of the actions on the list? Will they face a community of support,

ridicule, or simple apathy?


_Physical, psychological, or economic impediments to action_


This isn’t as common, but sometimes arises. Are there groups of users

for whom the action is especially difficult? For example, users who are

homebound or don’t have the money to travel to the rally (we faced this

with ActMore, in fact).


These five things make up the behavioral profile of the users. To gather this
information, you can use the standard tools of market research and product
development—look for existing quantitative data on user demographics,
deploy field surveys, and conduct qualitative research with users in focus
groups and one-on-one interviews.3 If at all possible, _include some direct_
_observation in the field_ —see how people actually act (and not merely what
they say they do). If you’re just exploring the idea for a product informally
or if no direct contact is possible with the user base (if business or privacy
restrictions make it infeasible), then talk to people who have had contact
with the target users and glean what you can from them.


This approach obviously builds on existing tools and techniques. The
innovation here is in adding questions directly focused on the target action,
not how people feel about the product or their “user needs” per se, but their
actual experiences, motivations, and problems vis-à-vis the company’s
target outcome and target action.


As you observe your users, you may witness or think up completely new
ideas about what behaviors to change. For example, for the Flash exercise
app, you may have thought about having users go to the gym, but after
observing them, you realize that eating healthier food (enabled by shopping
at a different grocery store) could be much more effective at controlling
weight and decreasing back pain. Add that idea to the list and evaluate it
along with the others. You may also realize that one (or more!) of the ideas
just doesn’t make sense. But if you know at this point without a doubt that
one of your early ideas isn’t feasible, save yourself time and cross it off the
list.


Along the way, the team might also identify particular terms and concepts
that resonate with the users; that’s not the focus now, but it’s still useful—
put them aside to inform the UX design later on.


### **How Do They Behave in the Application?**

If your company or organization already has an existing application or
product, great. It can be used to understand the diverse groups of users you
have and how they will respond to the new product or feature being
considered. If you don’t already have a product serving these users, you can
safely skip this step.


In my personal example, we couldn’t work with ActMore’s previous
products to learn about users, so I’ll stretch my example a bit. Assume that
ActMore already had a mobile and web platform for facilitating political
action called “ActMore Now!” In studying an existing product like
ActMore Now!, start with standard questions from the user testing arena:
how do users feel about the application, what features are they lacking,
what different types of people use the product, who is most active in the
system and why, etc. Then add new questions focused on behavior:


_Prior experience with the action_


What features of the existing application are similar to the targeted

action? Have the users built up existing habits that can be leveraged for

the new targeted action?


_Prior experience with the product_


Which features were unsuccessful? What did those failures reveal about

the characteristics of the users (particularly low attention space,

impatience, or lack of background knowledge about a topic)?


_Relationship with the company or organization_


Are they showing that they trust you with their current usage of the

application?


_Existing motivation_


What motivations or interests are underlying the most successful

features of the application? How does using the current application

interact with users’ daily lives, and especially their social lives? Are

there communities built around using the application?


As you can see, the questions are very similar to those asked when
analyzing users outside the context of the product: motivation, prior
experience, and trust. But the answers are all the more valuable as a guide
because they relate to user behavior in the context of the product itself.


Practically, this process means watching, interviewing, and/or surveying
existing users to understand their views of the application, their frustrations,
and their joys. Make sure to include some direct observation of people as
they go about their lives and use the application.5 It also means analyzing
existing usage patterns within the application to see what parts of the
application have been successful at catching users’ attention. Especially
important is measuring the behaviors of users on tasks related to the


application’s top-level goal and analyzing how the population has
responded to existing interventions.

### **Behavioral Personas**


Next, you can use the information you’ve gathered to identify broad groups
of (potential) users within your target population. I know the term is a bit
loaded, but I like to generate formal user personas—short descriptions of
archetypal users with a simple background statement about a sample user’s
life. (You can accomplish the same thing in your own way, without the lifestories part, as long as you get a clear idea of the groups of users within the
population.) Since designing for behavior change entails changing nittygritty details of people’s lives, it’s valuable to keep in mind vivid, realistic,
specific personas—not an amorphous vague concept of “our users.”


Unlike traditional user personas, these personas are all about behavior:
groups of users who are likely to interact with the application differently
and who are likely _to respond differently to behavioral interventions_ . Each
persona should have information about the topics discussed; Table 7-1 gives
one way to organize them. The examples are inspired by my work at
HelloWallet and Morningstar, where the target action is saving money for
emergencies among a population that hasn’t used online savings tools
before.


_Table 7-1. Two behavioral personas on saving money for emergencies_


**Frugals** **Spendthrifts**



Experience
with similar
actions


Relationship
to the
company



Always keeps emergency savings. No real experience saving for
emergencies.







None. None.









Hard
barriers to
action



N/A Doesn’t have excess money to save
currently







Here are three approaches to synthesizing behavioral personas. First, you
can use the four questions (experience with similar actions, experience with
similar products, etc.) to spur ideas for personas in an open-ended way. For
example, is there a group of users that is clearly more experienced taking
this action than others? What are they like? Who would be an archetypal
example of that group?


Second, you can use the four questions in a more formal way to generate a
fixed set of options to explore. For example, take the four questions and
consider them each as a simple yes or no question. Look at each possible
combination of answers to the questions (there are 16 of them). On a first
pass, you can eliminate most of the resulting options as not relevant to your


population (e.g., physical impediments may not be relevant to your product;
that cuts the options down in half immediately). After that quick pass
through the options, you can ask whether you really have any users who fit
those criteria and what they are like as a group. Each remaining option
gives you a persona.


Third, when you have historical data available about your users and their
behavior, you can build them using statistical or machine learning
techniques, looking for which users’ characteristics best segment the
population in terms of outcomes. A decision tree (random forest, etc.) or a
simple regression can accomplish this. We use this approach at Morningstar.


My preference is the data-driven approach. When historical data isn’t
available, however, the more formal second method, odd as it may appear,
completely covers the range of possible users. It makes you think about
each “type” and decide whether or not it’s relevant. Ideally, your personas
should be _exhaustive and mutually exclusive_ ; that is, every person in the
target population _best_ fits into one and only one persona. You also can do
this by drawing a simple box that represents your entire user population
(Figure 7-1). Each line marks off another segment of the population, until
you’ve covered everyone.


_Figure 7-1. A sample population breakdown to generate personas (this is from a start-up that_

_encouraged people to use a new software package their employer purchased for them)_


For each persona, mark it off as a portion of the box, with a rough estimate
of the group’s size. If personas overlap—or one is part of another—that’s
OK. Look at each overlapping piece as a separate group of people. As
you’re running out of ideas, ask, “Who isn’t in one of these groups? What
are they like?” Label each group and see if some of them are redundant
from a behavioral perspective (i.e., you expect them to respond to the
product’s appeal to change behavior in the same way). Then, use those
informal groups to come up with more detailed personas.


As we study our users, to understand (behaviorally) diverse segments
within the population, we also start to understand the context in which they
act. What does it really mean for someone to sign up for our service? It
seems like a simple straightforward thing: just sign up! But what’s simple to
us isn’t simple to them. We discover that, and the real obstacles our users
face, by digging into the micro-behaviors on the path to action.

## **The Behavioral Map: What Micro-Behaviors** **Lead to Action?**


Barack Obama was in the midst of the struggle over the Affordable Care
Act (aka Obamacare). His team wanted to mobilize supporters to call into
radio programs in support of the legislation. In the last election cycle, they
had built an impressive set of online tools to onboard potential supporters
and get them involved in the campaign—from calling potential voters to
making campaign contributions themselves.


But calling into a radio show? That was a particularly nasty challenge, and
something that most American’s aren’t familiar with doing, especially about
a piece of new, complex legislation.6


How did the campaign do it? Figure 7-2 gives a screenshot from the
campaign’s online mobilization platform. They intelligently structured the
action into something volunteers could reasonably do. They broke the
action down into three manageable chunks. They automated parts of the
process, such as figuring out what number to call. They simplified and
provided defaults for other parts of the process, with a script of discussion
points to mention during the call. They gave clear instructions. They
provided positive encouragement.


_[Figure 7-2. Image from barackobama.com; snapshot taken by The Political Guide in February 2010](http://barackobama.com/)_

### **Building the Behavioral Map**


You know what you want to do (help volunteers call a radio show on behalf
of your cause). You know something about your users (they are interested
volunteers, but most have never called a radio program as part of an
advocacy campaign). Now what?


Well, in order to call into a radio program, the volunteer will need to:


1. Find a quiet time and place with a radio and a phone.


2. Identify the radio program.


3. Listen to the radio program for an appropriate time to call.


4. Get the number to call.


5. Work up the gumption to actually call.


6. Call the program.


7. Convince the person screening calls that the volunteer has

something interesting (and not crazy) to say.


8. Say something intelligible on the radio show itself.


9. Tell the volunteer HQ that the call was made so other volunteers

can spread out their efforts to other shows.


That’s a heck of a lot to do. Imagine if your product simply told users to
find a radio program and call them about this issue. Each person would
have to plan out the long list of things required, find the confidence to try
this new strange thing, and not get distracted by other concerns along the
way. They would also need to do some serious prior planning—planning
ahead to find the program, find time in the day to call with having access to
a radio, thinking about what to say, and so on.


Good luck. In fact, only a fraction of Americans has _ever_ called into a talk
show, and an even smaller subset has called in a premeditated, advocacyoriented way.7


To use another example, for someone to take up running as exercise, there’s
a lot more required than simply walking out the front door and starting to


run. Some of the prior steps include (a) getting running shoes, (b)
identifying a route and reasonable distance, (c) finding the time to do it, (d)
remembering to do it, (e) making sure you haven’t eaten heavily
beforehand, and more. Again, a heck of a lot to do.


That’s why we have products that can help people take action and make
unwieldy tasks like these feasible. The process starts by writing out the
obvious steps a user would normally take to complete the action. Make it
detailed. List each physical and mental piece of work that’s required, like
the radio program example. When we’re seeking to _stop_ a behavior, the
behavioral map outlines all of the micro-steps that the person takes leading
up to engaging in the behavior. Each of those steps provides an opportunity
for intervention—to help the person change. It’s the same idea—break the
big action into micro-behaviors.


Now that you have a basic list of steps, let’s flesh it out into a full
behavioral map.

### **Write or Draw It Out, and Add Behavioral Detail**


The behavioral map is a depiction of the individual steps users take from
whatever they are doing now, all the way through using the product and
completing the target action (or for stopping an action, what they do that
leads up to the action to be stopped). Some of those steps will occur within
the product, and some require behavior that is completely outside of it. The
map examines, at each step of the way, what’s going on with users and _why_
they would continue to the next step.


For those in the UX world, this should sound familiar, and intentionally so.
You can express the behavioral map with a variety of design tools. I’m
partial to customer experience maps like the one depicted in Figure 7-3.
They not only can include the stages of the individual experience, but they
can also draw out the “customer types” (similar to our personas), areas of
frustration and delight, and user emotions along the way. Related tools
include a touch-point inventory and map, empathy maps, and journey
maps. [8]


_[Figure 7-3. Part of a customer experience map from Mel Edwards at desonance](http://desonance.wordpress.com/)_


I don’t have a graphic design background, so I’ve used much simpler tools
to accomplish the same thing:


The humble flowchart with notes in a sidebar


A written narrative describing the user’s experience and mental
state at each step


A hierarchical outline where each top-level point is a step in the
user journey and under each point is a description of what’s
happening with the user during that step


No matter which tool you use to express it, developing the initial behavioral
map is a bit different than a normal customer experience map process (if
you’re familiar with that process; if not, don’t worry). Namely, make sure
you cover the following points:


1. Write/draw out the rough sequence of steps in the real world—not

just in your product—that a user must take to complete the action.
(That’s what we did in the previous section, listing the nine steps
that person would have to take to call into a radio program.)


a. To be successful, you’ll usually need to plan for how the

product indirectly affects those other steps. [9]


2. Label each of the steps as follows:


a. Something the user must do _within the product_


b. Something _the product should do_ in response to the user


c. All of the other things that need to be accomplished “in

the real world” (outside of the product) on the behavioral
map


3. Look for missing steps, especially for new users.


a. Take the perspective of a completely new user—one who

has never interacted with your product. Are there
additional steps required in the beginning (e.g.,
registration)?


4. Look for one-time steps.


a. Take the perspective of an experienced user—one that has

often interacted with your product. Are there steps that
can be skipped for experienced folks?


For example, in the case of the Obama campaign, with volunteers calling in
to radio programs, some of the steps clearly had to occur outside of the
product, such as “Find a quiet time and place with a radio and a phone” and
“Listen to the radio program for an appropriate time to call.” Most of the
rest could be done within the app. Repeat-callers might need to do steps 2
or 4 (“Identify the radio program” and “Get the number to call”).


That’s the initial behavioral map. Nothing too fancy. Now let’s figure out
where to focus our attention.


### **New Products or Features Versus Existing Ones**

The behavioral map provides the series of micro-behaviors that lead up to
the target action. For an existing product, the map is _descriptive_, like the
volunteer radio program system’s, which describes what people currently
need to do. We use the data we’ve gathered from the existing product and
about people’s real lives interacting with the product to carefully trace out
the micro-behaviors.


For new products (and features), the behavioral map is necessarily more
speculative. It helps us make that hypothetical future user interaction more
real by tracing through in detail what will really be required to use the
product or feature.


In both cases, we usually find that the reality—what people do (or will do)
—is far more complicated than we think. And that there are numerous steps
along the way where people could get stuck. As you’ll see, the behavioral
map will help diagnose behavioral challenges—whether existing challenges
in existing products, or challenges down the road, waiting for us in the
products and features we plan to build, if we don’t think them through and
eliminate them now.

### **The Behavioral Map for Stopping Behaviors**


What does it really take for someone to quit smoking? Often smoking
cessation is presented as a command, such as, “Just stop! Don’t light up (or
vape)!” But the reality is more complex. There’s a social and physical path
that leads up to each instance of smoking or vaping. There are the
colleagues who also smoke. There’s the box of cigarettes or Juul cartridge
easily at hand. And of course, there’s the internal dependency and strength
of habit. As with starting an action, stopping an action isn’t simply about
that moment. Rather, it’s a series of moments and micro-behaviors that lead
up to a fateful choice or behavior.


Just as these micro-behaviors present potential frictions to beneficial action,
they also present opportunities to hinder negative ones. When creating the
behavioral map to stop an action, pay close attention to the micro-behaviors
that lead up to the final act and look for _vulnerable_ or easily disrupted
ones.10 It may be far easier to block one of the micro-behaviors that lead up
to smoking than to stop the urge to smoke in the moment when there is a
cigarette in front of you.


For example, if the cigarette weren’t there cuing the person, or the
colleagues at work weren’t asking the person to hang out, the fateful
decision of “smoke or not smoke” wouldn’t even occur. The behavioral map
helps us find those creative opportunities for intervention rather than taking
on the hardest point in the process (usually the final step).

## **Is There a Better Action for Them to Take?**


You can think about the behavioral map as helping us understand where to
intervene—which micro-behavior leading up to the action really needs our
attention. The behavioral map can also show us just how hard it would be to
intervene at all: How hard it will be to change behavior.


Sometimes the wisest choice to make isn’t to plow through, but rather to
rethink the plan altogether. To see if there is a better action to target—one
that can meet the goals outlined in Chapter 6, but in a more efficient and
effective way. Let’s look at how to thoughtfully reevaluate our core
assumption about the action a user should take.


### **Techniques for Generating Ideas**

How can you figure out the actions that people could take? What types of
actions would make the target outcome happen?


There are lots of brainstorming and creative thinking techniques out there. I
cut my teeth reading Edward de Bono, who popularized the term _lateral_
_thinking_,11 but you can use whatever works for you. Either way, don’t stop
until you have at least five different actions.


If you don’t know where to start, here are some approaches that can help:


What does someone do right before the outcome occurs?


What’s unique about the company? What user actions are easier to
facilitate because of those unique aspects of the company
(specialized skills, a special relationship with the users, etc.)?


What do users already do that’s similar?


Why aren’t people making the outcome happen?


Why would users want to make the outcome happen? What action
is most natural for them to take if they are motivated?


Observe your users in practice. People find creative ways to
change their own behavior all the time. Watch them for inspiration
on what the product can do.


Draw from a list of random words (yes, I really mean random—
this is a technique from Edward de Bono). How is the word related
to the outcome? How would a person act based on that word, in
support of the outcome?


If possible, start small. Go with the bite-sized, easy things that the person
could do to accomplish the outcome. That will make it faster to test and can
be expanded upon later if needed. Look for the existing skills and habits of
the users wherever possible and build on them. Try some crazy ideas. At
this stage, don’t self-censor and limit actions that seem impossible.


The action doesn’t need to be something that the user would do while using
the product itself—dieting is a great example. People don’t (usually) eat
while they are logged in to a dieting app on their computer or phone.
Dieting occurs when people make choices about what to eat and how much.
Many dieting applications are designed to help inform and prepare
individuals so that when they _are_ making food and eating choices, they
avoid temptation and make better choices for themselves. There’s a danger
there, though—the further removed the product is from the action itself, the
less likely it will be that it causes people to take action.


As you think of actions, there’s necessarily a leap that occurs between the
action and the outcome—the assumption that the action will actually work
and produce the outcome the user and company seeks. We’ll draw out that
assumption and judge how risky it is a bit later. For now, I suggest focusing
on coming up with some cool new ideas, even if some of them are
uncertain.

### **The Obvious Is Our Enemy**


These techniques for generating alternative actions are useful when you’ve
hit a dead end; when you’ve explored the context of your users’ lives,
mapped out the micro-behaviors that would lead up to action, and figured
out that it’s just too hard. Then you go back to the drawing board.


Personally, I try to use these techniques from the beginning, not just when
we hit a dead end. When I’m first approached with a behavior change idea
or problem and asked how to support a target action, I try to put on the
brakes. I try—I certainly don’t always succeed—to question the action itself
that we’re looking to support.


For any long-standing and difficult problem, there’s usually an “obvious”
action for their users to take. The challenge is that for long-standing and
difficult problems, the _obvious is our enemy_ . Once we starting thinking
about the problem, a solution will often pop into our heads. It will
intuitively feel right and we’ll want to move on it. It’s a cognitive mirage.
Our minds have the nasty habit of conflating the ease of thought with truth;


that’s our availability heuristic at work. But if a problem is difficult, what
comes to mind quickly has probably already been tried _and failed_ .


For example, let’s say you’ve defined your target outcome as helping users
put more money into savings. The obvious answer is to set a budget and
spend less on something. It’s obvious but it’s also a really hard action for
most users to undertake (at least, head-on). Other, less obvious actions
might work better (e.g., automatically deducting the money from your
paycheck so it’s never in your checking account to tempt you). Similarly, in
the case of retirement, when people don’t save for retirement, the obvious
answer is financial literacy. If people just knew about retirement, they
would save. Unfortunately, the facts just don’t show that.12


And so, when you’re faced with a difficult problem, I encourage you to
look for the nonobvious. Write down the obvious answer and then force
yourself to come up with five other, unrelated solution. Use random word
association. Use lateral thinking. Use whatever get you beyond your
intuitive sense of a solution that _feels right_ .


That said, we don’t always need the big guns. For easy problems the
obvious is obvious because it’s actually the right approach to take. You just
need to take that obvious path and follow through. In the first edition of the
book, I placed this section front and center—pushing everyone to think of
alternative actions as part of the initial problem definition phase. It’s now
here and optional to save you time and energy when this level of effort just
isn’t needed.

### **Select the Ideal Target Action**


Once you’ve generated a list of alternative actions, what do you do with it?
Combine them, and narrow down the list.


Before getting too fancy, first remove actions that are directly blocked by
known impediments, especially if similar actions were tried but weren’t
successful in the past. Next, take each action and score it along the
following criteria, ranking it _low, middle_, or _high_ . To make the process more


concrete, imagine that the target outcome is to help users learn a new
language:13


_Impact (on outcome)_


How effectively would it achieve the outcome?


In other words, assume that every user does the action, without
reservation—how much would it help? When learning a new language,
the action of repeating one word is not very effective and gets a “low”;
practicing some sentences might be “middle”; immersing yourself in a
foreign country gets “high.”


_Motivation (for user)_


What motivation do users have to perform the action?


Draw upon the data about the users’ existing motivations and their
social interactions around the product. Users may be really excited to
travel to a foreign country or make new friends by practicing their
language skills in person (those two options get a “high” rating). They
may have little interest (and negative associations) with rote
memorization (that’s a “low”).


_Ease (for user)_


How similar is this action to things that the users already do in their
daily lives (including their interaction with the existing product)?


Immersion in a foreign country to learn a language would (usually) be
“low.” Repeating words or practicing sentences could be medium or
high, depending on what you’ve learned about your users. Existing
habits always get a “high” rating. Actions that require users to _stop_
existing habits always get a “low” rating (see Chapter 3). This process
may require subject matter experts to gauge the likely impact of the
action on users.


_Cost (for company)_


How easy would it be for the company to implement a solution around
the action?


True language immersion would be “low” for online products. Live
conversation with native speakers could be a “medium,” depending on
the existing resources and capabilities of the company. Providing scripts
for users to repeat would be easy. This rating may require a lead
engineer to assess potential resource costs.


With these ratings in hand, look for obvious outliers. If there’s a standout
winner, great. If not, remove any hands down losers. If this doesn’t narrow
down the list enough, make a judgment call about what’s most important
and feasible for the company, given their business strategy. If resources are
tight, then the cost of implementation naturally becomes rather important!


Behavioral economics can be useful here—certain behaviors and ways of
thinking are inherently more difficult for (most) users, and we covered
some of the high-level lessons in Chapter 1. For example, behaviors that
require extensive mental calculations are difficult and often avoided.
Actions that focus on long-term gains over short-term losses are also
contrary to much of our cognitive machinery (losses are more painful than
gains are good, short-term gains are valued more highly than long-term
ones).


Beyond that, there’s not more guidance to give here, unfortunately. Keep
narrowing down the list until one top choice remains or there are two neckand-neck options that can be tested in practice.


With the new action in hand, update the problem definition. Write out the
new action and fill in these details: whether it requires starting or stopping,
who does it, and the micro-behaviors that lead up to it.

### **Updating the Behavioral Personas**


If and when the team decides to change the target action, we must revisit
the behavioral personas and see if they need updating. In other words,
quickly look over each of the five questions (experience with similar


actions, experience with similar products, etc.) and generate additional
personas as needed for our new user action. Often, the resulting personas
may be the same across various actions, but be prepared for them to be
different. Remember that unlike normal UX personas, again, behavioral
personas are _relative to and defined by a particular target action_ : since the
goal is to create a set of personas that are likely to respond differently to the
product’s attempts to change behavior.

## **Diagnosing the Problem with CREATE**


Now that we know what micro-behaviors individuals need to take in order
to succeed, we can look more tactically at the changes we want to make to
the environment. For that, we return to the CREATE Action Funnel from
Chapters 2 and 3 both to help people take positive action and to hinder
negative ones.


**BEHAVIOR IS ALWAYS CONTEXTUAL**


Action always occurs in a given moment. While preparation can occur
over time, any _specific action_ only occurs in the moment. While this
may seem obvious, it’s a surprisingly difficult lesson to internalize and
understand the ramifications of. It means that even if someone thinks
about the action (or product) often, it doesn’t matter if they don’t think
about it in the specific moment that matters. Similarly, if people are
generally motivated to act, but demotivated for whatever reason at a
particular point in time that matters—no action.

### **Diagnosing Why People Don’t Start**


I’ve worked with many individuals and companies over the years to write
out their behavioral maps. Often, when participants have mapped out a
behavior they want to support, they say two things:


Wow, there are lots of steps! What we’re asking our users to do is
just much more complicated than we thought!


I know what do to!


Simply by exploring the problem in a more structured, focused way, the
solution might become clear and straightforward. When it’s not, we can use
the CREATE funnel to help us _diagnose_ the core behavioral challenge (and
then work to fix it).


To see how this works, let’s continue the previous example of helping
political volunteers call a radio program. We outlined nine distinct steps,
from finding a quiet time to make the call to telling the volunteer
coordinator afterward. With this behavioral map in hand and our data about
our users and their situation, we ask, “Where are the problems?”


For existing products, where are people dropping off? At which
stage are they stopping? Naturally, some people will falter at
different stages, but we’re looking for where the largest group gets
stuck.


For new products, the analysis is more hypothetical, but similar.
Given what you understand about your users, where are they likely
to struggle in this series of micro-behaviors?


For existing products and features, this analysis is based on the empirical
data you’ve gathered about your users. Figure 7-4 is an example from
_Improving Employee Benefits_, a book I wrote for Human Resources
professionals on behavior change in the context of retirement plans, health
and wellness programs, etc.


_Figure 7-4. An easy way to visualize where employees are dropping off, with a conversion funnel_


Once we’ve identified a problematic step, we use CREATE. During that
specific step, and in that specific moment of potential action, is there a cue
in place to take the action? (And is it sufficient?) What emotional or
intuitive reaction does the person have toward that action? Is the action
motivating, and do the benefits outweigh the costs? And so on. Whenever
the answer is no, that’s a behavioral obstacle. That’s where we’ll focus our
attention in the design process.


In the case of the radio-program example, an obvious problematic step
would be “actually making the call”—that is, overcoming the fear and
uncertainty (an emotional reaction) of undertaking this new and unusual
action.


Diagnosis is thus a three-part process:


First, we identify the micro-behavior that stops people (or for new
products, are likely to stop people). That’s our behavioral map.


Second, we check which micro-behavior seems to be a problem.
Where are people dropping off (or likely to drop off)?


Third, we use the CREATE Action Funnel to determine the likely
behavioral cause.


With these three in hand (a map, a point—or points—in the map that’s a
problem, and a cause for that problem), we have our diagnosis. We have
what we need to start designing a solution.


That’s for _starting_ an action. Let’s look at the similar, but slightly different,
case of _stopping_ an action.

### **Diagnosing Why People Don’t Stop**


The good news about stopping an action is _diagnosing_ the problem is easier
—even if solving it isn’t. Each of the CREATE factors must be in place for
the person to take the (negative) action. Diagnosis entails outlining what
those factors currently are. What’s the cue that triggers people to take the
action? What’s the intuitive or emotional reaction they have? And so on.


When you’re helping the user stop an action, it is essential to know if the
action is habitual; that is, whether it is something the person consciously
thinks about or not. That’s because, as we talked about in Chapter 2, habits
work differently than conscious behaviors. In a habit, the Evaluation,
Timing, and Experience steps are largely skipped (or they are hardwired
internally). A Cue triggers a Reaction, assuming the person has the Ability


to take action. We focus on the C-R-A part of CREATE, rather than the
whole step.


Here’s an example of diagnosing the point of intervention with a common
habit: binge watching online TV. What are the microactions that lead up
binge watching?


Picking up the computer or phone.


Logging into the Netflix app or site.


Selecting a movie or series.


Watching it.


Letting autoplay load up the next episode.


Continue watching it, etc.


At each step, there are either habitual elements (C-R-A) or conscious
choices (CREATE). Picking up the phone is often habitual. What’s the Cue?
It’s the sight of the phone (external cue) or a moment of boredom (internal
cue).


The diagnosis for a behavior you want to stop entails:


Identifying the micro-behaviors that lead up to action—the
behavioral map.


At each micro-behavior, determine if it’s habitual or conscious
(often if the final action is habitual, so will the lead up to it, but not
necessarily).


Use CREATE for conscious actions and C-R-A for habitual actions
to map out the current enabling factors for each micro-behavior.


The behavioral map, our understanding of the nature of the behavior, and
list of enabling CR(E)A(TE) factors is just what we need for designing a
solution.


To give you a preview: we’ve all heard the advice to avoid distractions by
leaving one’s phone somewhere you can’t see or hear it. That’s an example
of intervening at the first microaction (and, specifically, intervening in the
Cue stage of the CREATE Action Funnel). Let’s say that isn’t possible, and
you can’t stop the person from having the computer or phone handy. But
you can make changes to how the person logs in (changing the password to
something that isn’t memorizable!) or to the autoplay process (changing the
settings so autoplay doesn’t occur).


The behavioral problem with autoplay is that it is cheating: it takes the
burden of work from the individual and places it with the software. We can
counter that by undoing that clever design and bringing the burden of work
back to the individual. In other words, turn off autoplay. When _hindering_ an
action, we’ll use this behavioral map and list of enabling factors to look for
a micro-behavior that is both essential to the subsequent process and
feasible to change. Then we use CR(E)A(TE) to identify where to _create_ a
behavioral obstacle.

## **Putting It into Practice**


This chapter is all about checking your assumptions about your users and
their situation so you can refine our vision what they’ll do and diagnose the
specific behavioral obstacle(s) they face.


Here’s what you need to do:


Research and document the characteristics of your users, especially
around prior experience with the action, prior experience with the
product, existing motivations to act, their relationship with the
company (trust), and barriers to action.


Generate behavioral personas—groups of users that you expect
will respond differently to your product’s attempts to change
behavior.


Develop a behavioral map showing the sequence of steps the actor
takes to go from their current state to taking action.


Rate alternative actions for users to take in terms of their
effectiveness, cost, motivation, and feasibility for the user.


Select the ideal target action, based on these criteria.


How you’ll know there’s trouble:


It looks like all of the users are alike—they usually aren’t. You
probably haven’t dug deeply enough into their existing experiences
and behaviors.


When rating potential actions, all of the actions are rated similarly,
or all of them are too expensive to the company or infeasible for
the user to be realistic (sorry, go back and think up more user
actions).


Deliverables:


Detailed observations about your users.


A set of user personas, indicating the main groups of users (or
potential users) of your application and their characteristics.


A behavioral map outlining the microactions the person takes.


On that behavioral map, the particular obstacle(s) you believe your
users face or will face—a diagnosis.


A potentially updated project brief, with the target outcome, actor,
and action.

## **Worksheet: The Behavioral Map**


_Describe each micro-behavior the user needs to take to move from inaction to action. Then ask_
_whether the six CREATE preconditions for action are in place at each step. Check existing_
_preconditions off the list and describe them briefly, for reference. Where one is missing, think_
_about how you can restructure the action, change the environment, or educate the user to help_
_move him or her through the process._


What Is the User’s Initial State? Sedentary, does not normally exercise


What Does the User Do First? Opens email inviting him or her to download the app


☑ Cue: Email from employer


☑ Reaction: Neutral, receives various emails from employer


☑ Evaluation: Low cost to open, generally important


☑ Ability: Easy


☑ Timing: Emails from the company should be opened quickly


☑ Experience: Neutral


What Does the User Do Next? Installs the app using employee ID and unique password


☑ C: Call to action in email


☑ R: Ug. Another app


☑ E: Could help me get in shape


☑ A: Doesn’t have employee id handy


☑ T: Sitting at home anyway, nothing pressing


☑ E: Neutral


What Does the User Do Next? Goes to a class at the gym!


…and so on for each micro action. Look for the first major obstacle: that’s
your behavioral diagnosis. There may be subsequent problems, but if they


don’t get past here, they aren’t relevant.


In the case of our exercise app, we find two problems early on in the
process: the user’s negative emotional reaction to downloading another app,
and the inability to log in to create an account.

## **Worksheet: Refining the Actor and Action**


_For some products, especially existing ones, the actor and action are obvious and not in doubt. In_
_that case, skip this exercise. However, as you Explore the context, you may learn more about your_
_users and their situation and realize that your initial assumptions were incorrect. If you think the_
_product might appeal to or help another group, or that your team is offering the same tired_
_solutions that haven’t worked in the past, this worksheet can help you revisit and refine them._


_Action: Brainstorm four very different actions that people can take to achieve your target_
_outcome because of your product or communication. When thinking through possible actions,_
_keep these points in mind:_


_The obstacles people currently face to achieving the outcome_
_What needs to happen right before the outcome_
_How your company is uniquely positioned to help people achieve the outcome_
_What people who currently achieve the action are doing_


Action 1: Solo run twice per week, starting with two miles.


Action 2: Write down exercise goals.


Action 3: Get a personal trainer at the gym.


Action 4: Participate in an in-person workplace fitness program.


For the sake of argument, let’s assume that for our Flash exercise app, the
company has locked in on the action (going to the gym) and the target user
(white-collar relatively sedentary employees), and we’ll continue with those


[targets throughout the rest of the process. In the workbook, you’ll find an](https://oreil.ly/behavior-change-wkbk)
additional exercise you can use to brainstorm different types of actors and
evaluate among possible actors and actions..


1 This case study is based on an interview and subsequent email exchange with Matt Wallaert.


2 They assessed doctor quality via a combination of self-reported patient satisfaction, patient

outcomes, cost, and availability.


3 Since we were doing microtargeting, the end result of this process was a set of machine

learning models of the propensity of ActMore’s members to respond to different product
features, which we then field tested before rolling out the product for real. We used quantitative
data from the organization and from third-party providers. But the core concept is the same in a
less quantitative-data-heavy environment. Who are the users, and how will they respond
differently to appeals to change their behavior?


4 My thanks to Darrin Henein for highlighting our shared base of techniques.


5 Thanks to Jim Burke for highlighting the importance of direct observation.


6 This tactic isn’t unique to the Obama campaign and was somewhat controversial for trying to

generate a sense of (extraordinary) support on the ground for the legislation. But it’s a darn
good example of helping people voluntarily take an action they wouldn’t otherwise take.


7 There doesn’t appear to be much data on the topic, but even when radio was more popular, a

1993 Times Mirror Center for the People and the Press (predecessor of the Pew Research
Center) survey estimated the percent of Americans ever calling into a talk show at any point in
their lives at 11%, and roughly half of them had actually been on air. See Pease and Dennis
(1995).


8 See Kolko (2011) for various examples of journey maps, touchpoints, and concept maps.

[Xplane developed the empathy map; take a look at an interactive example. You can use tools](https://oreil.ly/s5EJq)
[like the Touchpoint Dashboard, but a whiteboard or some sticky notes work well too.](https://oreil.ly/48aQ-)


9 The reason I start with the real world is that for many behaviors (e.g., controlling finances,

exercising, getting politically active, decreasing energy usage), the product only interacts with
part of the story, but all of it determines whether users will actually change their behavior.


10 My thanks to Clay Delk for highlighting this point.


11 De Bono (1973)


12 [Fernandes, Neydermeyer, and Lynch (2014)](https://doi.org/10.1287/mnsc.2013.1849)


13 This technique of rating potential actions is inspired by BJ Fogg’s method _Priority Mapping_,

in which he rates behaviors on ease of implementation and effectiveness. Also, there’s
certainly a science to teaching people new languages, and I won’t go into those methods here;
this is just a stereotyped example.


# **Chapter 8. Understanding Our** **Efforts: A Brief Story About a** **Fish**

_Imagine that you’re walking along a beach. You see a fish stranded in the_
_sand, flopping around a few feet away from the water. Let’s further imagine_
_that you’re feeling more helpful than hungry. What do you do?_


_Do you walk up to the fish and yell, “What’s wrong with you? Don’t know_
_how important it is to be in the water? If you just understood the value of_
_water like I do, you’d get into the water!”_


_Or do you calmly and thoughtfully try to teach the fish, “Let me explain to_
_you how your gills work. Your gills extract dissolved oxygen in the water_
_and put it in your bloodstream, where the rest of your body can use it. If you_
_aren’t in the water, you can’t get dissolved oxygen, and you’ll soon die.”_


_No. That’s obviously foolish. The fish isn’t lying in the sand because it lacks_
_motivation, nor because it lacks understanding. Maybe it doesn’t know the_
_details, but it “knows” the most important part: it needs to get back into the_
_water._


_Instead, there are really four things you can do in that moment._


_First, you could pick up the fish, hold it in your hands, and walk it over to_
_the water where you drop it in. All the fish needs to do is stay put and not_
_flop around too much in your hands—it’s not trivial, but it’s a whole lot_
_easier for the fish than to get back into the water on its own._


_Second, there might even be a way you could take care of everything. You’d_
_somehow put the fish to sleep, transport it to the water, and then wake it up_
_again. The fish wouldn’t have to do anything at all (it wouldn’t even need to_
_resist the urge to flop around)._


_But if you aren’t in the mood to get your hands slimy holding the fish, you_
_could dig a channel of water in the sand, leading from the fish, down to the_
_water. You could then take some water and pour it over the fish. That would_
_make it easier for the fish to do what it already wants to do: follow the_
_water back to safety. That’s our third option._


_And, fourth, if you had had the luxury of spending time beforehand to train_
_the fish how to flop better, that training might have been useful. But when_
_the problem is acute, you usually don’t have that luxury._


_Either way, yelling, educating, or relying on the fish to rescue itself aren’t_
_great ideas._


When designing for behavior change, our first instinct is to yell: to try to
motivate someone to do something. Or, we try to ram facts and figures
down their throats, thinking that if they just understood the problem as well
as we did, they’d act. Neither is very helpful. Our users (who aren’t
anything like fish, but at least the story get the point across) are the ones
with the problem; they may not know all the details of the situation, but
they usually understand the basics already.1


Instead, where we should start is by taking a hard look at the action itself,
the thing that people are struggling with. Is there an easier way to
accomplish the same end? Something that is more natural for the person to
accomplish?


We should (1) _change the action_ to make it easier. The most extreme
version of changing the action is to completely take the burden of the work


onto ourselves, or (2) _do it for them_ so the person doesn’t have to do
anything at all. Alternatively, we might look to (3) _change the environment_
to make it more likely for the person to take action. Finally, if we have the
time and ability, we might (4) _change the person_ to help prepare them for
the moment of action (see Figure 8-1).


_Figure 8-1. The four approaches to behavior change: do it for them, change the person, change the_

_action, or change the environment_


Each of these options shapes the context of action. Each is designed to
increase the likelihood of a good outcome; they are the four main ways we
intervene in a situation to engender behavior change.


The purpose of the design process is to _craft a context_ that facilitates (or
hinders) action. Crafting a better context rarely entails yelling at a fish.


Let’s look briefly at the extreme case of changing the action: doing it for
them. That’s when we _cheat_ at designing for behavior change and do
whatever is needed on their behalf. It’s great when we can take this magic
solution, and we should always look for it, but we shouldn’t count on it
being available. Afterward, the next few chapters look at the details of
changing the action, environment, or person.

## **Do It for Them When You Can**


While you can make an action rewarding, easy, familiar, socially
acceptable, or any of the other things we talked about in Chapter 2, the
activity still involves work for the user. Ideally, the company could find
ways to shift the user’s burden onto the product by identifying clever ways
to make active participation unnecessary beyond informed consent. That’s
what I call cheating—substituting the user’s nasty problem with a much
simpler one: deciding whether they want to let something else (the product)
take the action for them. As you’ll see, this strategy is only available in
certain cases, but when it is feasible, it is immensely powerful.


Exactly how a company can “cheat” depends on whether the target action is
undertaken once or infrequently (like buying running shoes) or repeatedly
(like going running each morning). I’ll talk about each of these two
situations in turn.

### **Strategies to Cheat at One-Time Actions**


To cheat at a one-time action, either you can take care of the action yourself
directly, by automating it, or you can make it a side effect of another action.
Let’s look at both in more detail.


**Automate it**


To automate an action, the company first finds a way to take the action on
the user’s behalf. Then, usually the company combines it with another
work-saving technique: defaults. They give the user a choice about whether
the product should take the action on their behalf, where the default answer
is “yes.” The user can say “no” if they so choose.


Most automation is invisible—you don’t even think about it as automation;
it just happens. In fact, we’re not used to seeing the automation that’s all
around us, so we rarely think of it as a solution. To that point, the most
common reaction I get to proposing automation is, “That’s great, but there’s
no way that will work here. You can’t automate this behavior.” Well,
maybe. Here are some examples to show how automation works in real life:


_Behavior change sought: have users save for the future_


Two of the greatest success stories in recent history in helping users
save money are 401(k) autoenrollment and autoescalation.2 (For nonUS readers, 401(k)s are retirement savings plans provided by an
employer to employees.) Under autoenrollment, individuals who are
eligible to participate in their company’s 401(k) plan are defaulted into
contributing to the plan but are given the option to not contribute if they
wish. Contributions are then automatically routed to their 401(k).
Similarly, autoescalation increases the contribution rate over time, but
the individual can opt out at any time.


The initial action users take is often quite minimal; for example, signing
their name on a package of new-employee documents. Afterward,
contributions to the 401(k) plan are automatically deducted from their
paychecks and placed into their retirement account on their behalf.
Instead of requiring that an individual choose to contribute to the
retirement plan each month (or choose to find the HR representative
with the necessary paperwork required to enroll in the plan), this
process effectively removes the work required by the user.


401(k) autoenrollment is a powerful example of increasing savings, but
it also can skirt the line between _voluntary_ behavior change and
trickery. Some employers strive to inform employees about their
retirement plans and default contributions. In other cases, the employees
don’t know about their accounts until they leave their job and get a
check—which they quickly spend on non-retirement needs, since they
weren’t informed and invested in the process in the first place.


_Impact of automation and defaults_


It’s significant in this case: autoenrolled, defaulted-in plans have
nearly _twice_ the participation of non-defaulted plans.3


_Behavior change sought: have users take high-quality photos rather than_
_crappy ones_


High-end camera manufacturers have a problem: many consumers want
lots of features, but those same features make the camera sensitive to
user mistakes and result in bad pictures.


Good cameras have a simple solution that help people take quality
pictures, but still provide power options (and a premium price): the
cameras have powerful built-in features that can handle much of the
work for the user. These features (like autofocus or red-eye reduction)
are defaulted on, making the camera dirt simple to use and providing a
good picture in most scenarios. In addition, the cameras have all of the
fancy bells and whistles that make the product more attractive and
expensive than a bargain-basement camera.


Similar combinations of automation and defaults are common in
computer software (“Would you like the standard install or the scary
customized one?”)—the options are there, but the software makers have
provided intelligent defaults so most people don’t have to worry about
them and install the software without getting themselves in trouble.


_Impact of the automation and defaults_


Apparently, cameras still can’t help us take _interesting_ pictures.
More seriously, though: do any mass market cameras _exist_ anymore
that don’t have intelligent defaults for things like contrast, white
balance, and F-stop?


**Make it incidental**


If the action can’t simply be defaulted away, there’s another clever option—
have the action come along for the ride with something else that users are
going to do anyway. In other words, don’t have them think about doing the
action at all. Make the action happen automatically when the user does
something else—something that is inherently more interesting or engaging
—but leave the option for the user to decline the action if they so choose.
Here are two examples:


_Behavior change sought: improve people’s intake of vital vitamins and_
_minerals_


OK, before I go into the solution, what’s the most effective way to
improve the amount of vitamins and minerals people get? Convince
them of the benefits? Pay them to eat well? Run a public campaign with
celebrities endorsing vital minerals? How about this: put it in the food
people already eat—with their consent, and without removing other
food options. For example, put iodine in salt.



Iodine deficiency is the leading preventable cause of mental
retardation.4 It causes stunted growth, infant mortality, lower IQ, goiter
(big lumps in the neck), and more.5 Two billion people suffer from
insufficient iodine. Iodine costs virtually nothing to produce and add to
salt.



4



5



The story of iodized salt also shows that defaulting can’t be allowed to
turn into coercion, either practically or ethically. At various times,
people around the world have objected to iodine being added to their
salt without their consent, causing these iodization campaigns to fail
(and iodine deficiency to continue). When there is no way to opt out
(non-iodized salt) and no consent, it’s not “defaulting”—it’s just an
ethically problematic mandate. There must be consent among the
population _first_ .


_Impact of making iodine incidental_


In many of the places where iodized salt has been used (with
consent), the problem of iodine deficiency simply ceases to exist;
that’s the ideal outcome of any behavior change strategy. In the
United States, iodine deficiency is rarely an issue anymore, except
where it hasn’t been made incidental.


_Behavior change sought: have people (voluntarily) contribute money to_
_savings_


One solution in this case is a savings lottery, aka prize-linked savings
accounts. A prize-linked savings account is like a lottery in that people
can “buy” multiple tickets.6 Each ticket is a contribution to their savings
account. Like any lottery, there’s a jackpot—a big pool of money that
one (or more) winners get. Unlike a normal lottery, the participant
doesn’t lose the cost of their ticket; it’s just deposited into their savings
account.7 There’s a significant upside, but little downside, to
participating.


For users who enjoy playing lotteries, the _savings_ part is incidental: they
would spend money on the lottery anyway;8 the fact that they don’t lose
the ticket money is a nice added bonus, but not the primary reason for
them to participate.


_Impact of making it incidental_



6



7



For users who enjoy playing lotteries, the _savings_ part is incidental: they
would spend money on the lottery anyway;8 the fact that they don’t lose
the ticket money is a nice added bonus, but not the primary reason for
them to participate.



Prized-linked savings programs have been highly popular around
the world for centuries, starting in Britain.9 They have recently
gained traction in the US through the tireless work of
Commonwealth, a Massachusetts-based NGO.10, 11



9



10, 11



And there are many more examples that we rarely think about in our daily
lives. If you want your toddler to take a pill, you crush the pill up and put it
in some juice they like. The toddler doesn’t care or know (and if they don’t
know, they can’t complain) about the pill; it’s incidental. The juice is what
matters.


Even when behavior change is a _side effect_ of the product, the same ethical
rules should apply as when the user directly takes action.12 Is the side effect
something that is truly beneficial for the user? Would they be surprised or
upset if they learned about the side effect? Or, even better, have you told
your users that it’s occurring?

### **Strategies to Cheat at Repeated Actions**


You can also use these two approaches, defaults and making the action
incidental, with repeated actions. For example, with prize-linked savings
programs, the savings lottery can be repeated each month to encourage
sustained savings contributions. Each time the person acts, savings are
incidental. Similarly, each time the person uses an application, they can
encounter the same (configurable) defaults.


In addition to these two approaches, another becomes possible with
repeated actions: you can turn the repeated action into a one-time action by
_automating the act of repetition._


**Automate the act of repetition**


Taking an action repeatedly is inherently more difficult than taking that
action once, even when the person learns how to do it better over time. So,
why not turn a repeated action into a one-time action?


In this scenario, the individual takes a one-time action to set up or accept
the automated process, and then the rest is handled without their
intervention by the product itself. The principle is simple and is very similar
to defaulting a one-time action: use behind-the-scenes magic to shift the
work from the user to the product.


_Figure 8-2. Runkeeper, an app with automated exercise tracking (image by Runkeeper)_


Some great examples of automating repeated behaviors in the health space
are exercise trackers that people carry with them throughout the day. These
include bands from Garmin and Fitbit and apps (e.g., Runkeeper) that use
GPS or a phone’s accelerometer to accomplish this without a separate
device (see Figure 8-2). These apps and devices automatically log and
compare exercise against a user’s target. They’ve successfully taken
something that is annoying but beneficial (logging exercise in a journal,
comparing it to one’s daily goals) and made the work magically disappear.
Once _exercise tracking_ was automated away, companies could focus on
more interesting (and user-beneficial) target actions—like helping users
_exercise more_ .


Another example of automating behavior comes from the personal finance
space, with software that automatically categorizes transactions and tracks
spending—such as Acorns, Mint, and numerous bank websites. In the “old”
days (i.e., the 1980s), if you wanted to know how much you had in your
checking account, you had to track your spending and balance your
checkbook (remember checks?). When ATMs became popular in the 1990s,
you also had to track your cash withdrawals. If you had a credit card, it
would send you a monthly statement, but before that arrived, you were out
of luck.


With personal finance applications, tracking expenses can happen
automatically. Each individual transaction is automatically logged,
categorized, and, where relevant, compared against a goal or budget item.
As with many other forms of automation, once the action is automated for
the user, the product team is then free to focus on more interesting and
difficult-to-change behaviors, like helping users stay within their budget.
But that wouldn’t be feasible for most users if they are wasting their time
tracking their spending first.


The most powerful combination of all is to combine automation with
defaulting—automation makes it a one-time action, and defaulting makes it
little more than an acceptance of that automation. I didn’t go into detail
about this earlier, but 401(k) auto-enrollment is such an example—the
savings contributions are automatically deducted, and the default is to enroll
in the program.

### **But Isn’t Cheating, Well, Cheating?**


Before I move on to other behavior change strategies, I’d like to confront an
implicit assumption that I’ve seen in many do-good products—that doing
good requires making our users work hard. If we, as people designing for
behavior change, want to help people take an action, we should be pushing
people to climb that hill! We know it’s hard, they know it’s hard, and that’s
what makes it worthwhile, right?


Well, no.


If the goal is to make people healthier, the action is consistent with that goal
(say, by making the food that people already eat magically become healthier
but taste and cost the same), and automation doesn’t have nasty side effects,
does it inherently matter if the user doesn’t have to work hard for it? I just
can hear my own inner do-gooder say, “Well, that misses the point—we
want people to make wise choices, learn about the wonders of nutrition, be
grateful for all the energy we put in to help them,” etc. Sometimes, when
we design for behavior change, we secretly want more than to simply _help_
our users: we also want them to be a certain type of _virtuous person_ . We
want them to learn all the important things we know, we want them to care
about the things we care about, we want them to exert real effort toward
their goal—to demonstrate their determination and commitment. However,
these desires are about the behavioral designer, not about the user and what
helps the user succeed.13


That’s why it’s vital to be clear about the _end goal_ of the product. For
example, teaching people what we know about healthy eating is a laudable
goal. But do we really only want to teach people? Or, do we teach in order
to help people change their eating habits, which then makes them healthier
in the long term? If we could jump ahead, solve this _very particular_
_problem_ and move on to something else, wouldn’t that be a good thing?
Maybe making food healthier helps with the goal of decreasing vitamin
deficiencies, but it doesn’t solve the issue of cardiovascular disease. Great
—once the food solution is in place, then you can devote your energies to
the next problem: helping people decrease cardiovascular disease.


Any product will have multiple aims. But there should be one clear thing
that you gauge its success against—a final outcome or goal (that one thing
can be a composite of multiple smaller things). We covered how to identify
and fine-tune the product’s goal in Chapters 6 and 7; let’s assume you’ve
already done that. When you’re clear about what exactly is being sought, go
for it, even if it feels like cheating because it doesn’t make people suffer.
There are no martyrs in beneficial behavior change. The point of making
work magically disappear is that you can move on and help your users with
other, more intractable problems.


There’s good behavioral science behind this point too. In short, our selfconceptions are constantly adapting based on our own behavior. We often
forget or ignore the reasons why we do things and develop a story of who
we are based on what we observe about our own behavior.14 For example,
if we successfully contribute money to a retirement plan, even if we were
defaulted into it, we suddenly feel that that’s something we can do—we’re
savers! The pride that people feel at saving money through automatic
enrollment is real and should not be discounted. That self-conception as a
saver then has knock-on effects for other related behaviors—we’re prepped
for future action.

A classic study in this field is by Freedman and Fraser,15 in which the
researchers started by asking homeowners to put a small sticker in their
window encouraging safe driving. Weeks later, this randomly selected
group was far more likely to accept a large lawn sign about safe driving
than other homeowners; a whopping 76% of them accepted the large sign,
compared to 17% who hadn’t been asked to show the small sticker. In other
studies, homeowners were also more likely to accept other non-drivingrelated lawn signs. The homeowners started to see themselves as people
active in their community, which had broad effects on their behavior.


There are cases when this doesn’t work, of course. When people don’t
know the action occurred at all, then the self-conception doesn’t change—
but in that case it isn’t a voluntary behavior change at all; it’s behind-thescenes trickery.

### **Cheating at the Action Funnel**


Remember the CREATE Action Funnel—Figure 2-3? It’s difficult for a user
to pass all of the way through the funnel from the initial cue to a conscious
choice to act with sufficient urgency. The _cheating_ strategy takes the funnel
and changes its meaning. With a conscious choice to take a hard action,
success occurs when the user passes through the funnel. When the product
cheats, success occurs when the user agrees to the action occurring but
_doesn’t_ pass through the funnel to stop it from occurring.


## **When You Can’t Do It for Them, You CREATE**

When you have the ability to perform magic, you should: magically make
the user’s behavioral challenge go away (while giving the user the option to
say no). Sadly, magic isn’t as common as we’d like. And so, the next two
chapters walk you through the details of crafting an intervention—how you
specifically change the action, environment, and person to help facilitate (or
hinder) action. The solutions—interventions—are intimately tied to the
behavioral diagnosis from Chapter 7. Solutions, like behavioral problems,
employ the CREATE Action Funnel.


As you move into developing a solution, here are some additional lessons
from behavioral science about the philosophy or approach to designing for
behavior change:


Remember to look beyond the user’s motivations


Remember to look beyond the screen

### **Look Beyond Motivation**


As we saw in the opening story, the fish had all the motivation it needed to
get back in the water—its problems lay elsewhere. That part is meant to
encourage us to look beyond the user’s motivation when designing for
behavior change, and it warrants a bit more attention. That’s because one of
the first places that designers and product managers look to change
behavior is to increase motivation. In my experience, this is the tactic that
most of us think of when we’re asked how we can encourage people to do
X. The problem is, extra motivation is often not what’s really needed, or at
least, not on its own.


Here’s a real-life example: the financial rewards of investing in a retirement
plan when your employer contributes money (i.e., a matching contribution)
are tremendous. We’re talking about free money that grows for decades, tax
free, with the magic of compound interest. Employees need to personally
contribute some of their own money to get the match, but that’s something
they know they need to do anyway in order to enjoy their retirement (and


not live in their kids’ basement when they’re 70). But up to 50% of people
won’t do it unless something more is done to encourage behavior change16
—like automating the process (automatic enrollment) or forcing people to
make a choice (a strong trigger to act).


To make this point another way, think about this: what is the most effective
way to earn gads of money? That is, how can you receive the most financial
reward? For most of us, we simply have _no idea_, and we don’t waste our
time looking for that “optimal-money-producing” answer. We’ve picked the
best career path among those presented to us through a mix of what we’re
aware of, what seems feasible, the diverse set of motivations and options
that fit our personal stories, and prior experiences. Money, as with any other
type of motivation, is only part of the story.


Here are some challenges that arise when focusing too much on motivation:


When a product is helping a person take an action they already
want to do, the person by definition already has some motivation.
For most “good” behaviors, like exercising, everyone has already
told that person how important it is—another voice in the choir
isn’t going to add much. (Though sometimes the motivation is too
far in the future, as mentioned earlier.)


There are _always_ competing motivations to do other things.
Understanding which exact action we take, why, and when, is the
kicker. The answer is often not “the most motivating one.”


This isn’t to say that making people more motivated isn’t important—it is.
It’s just not enough. Tactics to increase motivation (like highlighting the
user’s existing reasons to act, or experimenting to find the right motivator
for your users) work best when carefully executed along with other parts of
the CREATE Action Funnel from Chapter 2. More motivation improves the
chances that a person will successfully pass the intuitive reaction and
conscious evaluation components of the funnel. But don’t forget that there’s
other work to be done as well!


Let’s say you offer a badge of recognition when users complete an action,
which is a tactic to increase motivation. That’s useful but needs to be
combined with the rest of the CREATE Action Funnel. For example, for the
users to benefit from that extra motivation and eventually take action, they
first need to be aware of the reward. In other words, they need to be _cued_ to
think about it. The target action must also _out-compete_ (be relatively more
motivating, more urgent, etc.) other potential actions the user could take.
Those two tactics—cueing and blocking the competition—are coming next.

### **The Value and Limitations of Educating Your Users**


Educating users in a behavior change context is all about giving them the
information they need and then hoping that when the time comes to act,
they will make a well-informed choice.


Focusing on information is a noncontroversial and common approach to
behavior change. We think that everyone would believe like we do if only
they had access to the same information and training. This has been an
approach taken by many of my otherwise favorite NGOs and government
agencies.


Unfortunately, information doesn’t equalize us and doesn’t make us behave
the same. As we saw in Chapter 1, conscious information might have
nothing to do with action at all—the action might be habitual or based on
intuitive reactions. Or, when it does have an impact, it might be filtered
through all of the rest of our experiences and information.


Providing users with information can be immensely powerful. But we
should be thoughtful about how and when it’s applied. Education efforts
falter when:


The action that people will take isn’t consciously thought through
at all—it’s habitual or otherwise automatic.


People are overwhelmed with too much information.


The information comes too long before (or after) the decision
needs to be made. We rapidly forget unconnected, unused facts.


An example of an education-only approach that clearly didn’t work is
mortgage disclosures in the United States. Mortgage lenders are required to
provide reams of documentation on everything from how the loan works to
the fact that most older homes have lead paint in them. This is important
information—and rarely read. It’s too much to take in, not structured to
demand attention, and isn’t clearly actionable. The only “action” the
mortgagee can take by the time they get all of the disclosure documents is
to walk away, with no house, and no certainty about where the escrow
money goes.


To better understand when education can be effective, let’s use a common
example: educating people about the importance of saving for retirement
with financial literacy seminars. In the 1990s, there was a significant
increase in the use of retirement planning seminars as employers shifted
from pension plans to 401(k) plans that individuals directly contributed to
and managed. These seminars, and other financial literacy programs in high
schools and beyond, have been the subject of quite a lot of controversy,
with numerous researchers questioning their impact.17


Consider three different approaches that a retirement education product
could take. It could educate people about _why_ an action is important, _how_
the action works and the raw data needed for a good decision, or _what to do_
to take the action:


_Why_


By and large, we already know that saving for retirement is important.

No one wants to die in poverty. However, for other beneficial actions,

users of the product may not honestly know the importance of the

action; for example, I didn’t know that skin cancer screening was

important for (relatively) young people until recently.


_How_


We don’t understand the inner workings of 401(k) plans and score

poorly on financial literacy questions about basic topics like compound

interest.18 And there’s evidence that this knowledge helps us make good

financial choices.19 But if the information is delivered too far in

advance from a moment of decision, as many financial literacy

programs are, we simply forget it.


_What to do_


We don’t know what to do when confronted with dozens of 401(k)

options—in fact, we often take a naïve strategy of putting an equal

amount into each fund we’re faced with. A simple heuristic for easy

diversification—use a stock market index fund or a target date fund—

can simplify and shape that decision to users’ benefit.


Which type(s) of education is best depends on the particular situation. With
voluntary behavior change, we assume that the user already has some
motivation to act. Information about _how_ a system works can be fascinating
for those already in the know, but overwhelming and too removed from the
actual decision for those who aren’t. Logistical information ( _what_ to do) can
provide clear actionable guidance and increase the user’s ability to act
immediately, a key component in the CREATE Action Funnel.

### **Reach Out of the Screen**


Part of the philosophy of designing for behavior change is that we’re not
limited to actions within our products. Or, to come back to the story of the
fish: even if your product isn’t on the beach at that moment, you can still
help change the context of action via the type of action being asked, the
environment it’s done in, and the preparation of the user.


The context consists of two things:


_The product itself_


For software applications, the primary environment enveloping the user

is the product—particularly, the web pages where the user takes action

or the tiny progress screen on the Fitbit One tracker.


_The rest of the user’s local environment_


While using your application, the user is also embedded in a physical

environment (trying to use your application while on the subway, with a

spotty Internet connection) and a social environment outside of the

application (a set of expectations from friends on the “right” behaviors).


You have the most control over steps that occur within the product itself, of
course. But you can also use the product to _reach out of screen and touch_
_the user’s daily life_ . For example, guidelines given within the product, and
even the marketing materials that surround the product, define the action for
the user. They shape how the users think about the action and what it is they
try to accomplish in their daily lives outside of the product. The basic
definition of what behavior is being changed (and how) can and should be
tailored to fit the user base.

## **Putting It into Practice**


It’s easy to get excited about our products and how they can solve our
users’ problem. We assume our users will be just as excited about our
solution as we are; we just need to help them understand how absolutely
awesome it is. But when they don’t immediately “get it,” we want to yell at
them. We want to scream about the benefits. We want to beat them over the
head about _their_ problem and how we’re solving it for them.


If you’ve been in product development or marketing for a while, you’ve
likely been in meetings where everyone is convinced there’s something


basically wrong with the user, and we just need to educate/motivate them,
and they’ll use our solution. It’s because of those painful meetings that I
developed the Story of the Fish. To remind ourselves, in a cutesy story, that
usually there isn’t anything wrong with our users. Rather, that there’s
something wrong with the _context_ . _Designing for Behavior Change_ is about
changing that context, usually in one of four ways: 20


Do it for them by magically taking away all of the burden of work
from the user


Structure the action to make it feasible (or, in reverse, more
difficult) for the user


Construct the environment to support (or block) the action


Prepare the user to take (or resist) the action


The first one is really a special case: great when you can find it, but not
something you should count on.


Here’s what you need to do:


Ask whether you can fully automate the action (i.e., remove the
need for the person to do anything at all).


Look in particular for defaults (automatically setting reasonable
options where the user has to make a choice), making it incidental
(bundling a beneficial side effect with something else the user
does, like enriching bread with vitamins), or automating repetition
after the user has made an initial choice (like automatic deposits to
savings, once the user sets up the transfer).


Don’t force your users to suffer and work through the action
because “it’s good for them.” If you can help them achieve the
outcome, do it—and save the noble suffering for more difficult
problems.


How you’ll know there’s trouble:


The user can’t stop you from taking action on their behalf, or can’t
do so in an easy and obvious way. That’s not designing for
behavior change, that’s simply coercion.


Deliverables:


Where possible, a magic solution—you do it for them.

### **Exercise: Review the Map**


Look over your behavioral map from “Worksheet: The Behavioral Map”
and the obstacle you diagnosed as the most likely problem. Is it possible to
simply remove that obstacle altogether—to skip that step or to take the
burden of work from the user and unto your product? If so, excellent—look
for the next behavioral obstacle in the map, if any, and try to do the same. If
there aren’t additional obstacles, skip the next few chapters and go straight
to implementing the solution (Chapter 12).


In the case of our exercise app, one of the obstacles we identified is that the
user doesn’t have their employee ID on hand when they receive the
invitation email: an Ability obstacle. We can skip that step by embedding it
in the invitation email itself. Unfortunately, there’s still another obstacle
remaining: a negative Reaction to the idea of downloading and using
another app. So we move on to crafting an intervention to overcome it.


1 If they think there’s a problem to be solved or don’t think it’s important despite being aware

of the problem, we shouldn’t be involved in the first place—that’s persuasion or coercion.


2 For many Americans, the behavior change isn’t what our policymakers and companies

intended—it’s become a short-term savings vehicle. But the impact on savings is still amazing.
See Fellowes (2013) for a discussion of the downsides of autoenrollment and autoescalation.


3 Nessmith et al. (2007)


4 [McNeil (2006). Though, to be fair, I found that citation from Wikipedia.](https://oreil.ly/EmZdB)


5 [American Thyroid Association (2020)](https://oreil.ly/DdXEW)


6 Legally, prize-linked savings is usually structured as a sweepstakes in the US; no need to get

into the legal definitions here, though.


7 Tufano (2008)


8 Filiz-Ozbay et al. (2013)


9 Murphy (2005)


10 One could also point to state lotteries as examples of making a behavior, contributing money

to schools, incidental. In California alone, they have funneled $24 billion to “education
[funding” since 1985 (Strauss 2012). But state lotteries are also a great example of how](https://oreil.ly/_Das-)
different the mind is from a conscious budgetary process. In our minds, school contributions
are a side effect of our lottery purchases. No extra work. In reality, state budgeters consciously
know that a dollar is a dollar and move the money around from one budget category (schools)
to another. Changing _lottery participant_ behavior doesn’t mean that you’re also changing the
behavior of accountants!


11 Another great example of making savings behavior incidental comes from the IDEO/Bank of

[America “Keep the Change” program. The program rounds up purchases made on debt cards](https://oreil.ly/OGr0g)
to the nearest dollar and takes the difference between original cost and the rounded version and
automatically deposits it into the person’s savings account. The person does nothing differently
—savings are incidental.


12 My thanks to Peter Hovard for highlighting the ethical concerns with behavior change as a

side effect.


13 This image of a virtuous person is modeled after ourselves (the behavioral designers), of

course. When we try to make our users more like us, it’s like a form of self-affirmation. And
sadly, yes, I’ve seen this in my own and many others’ work.


14 Wilson (2011). The related tendency to create consistent (non-dissonant) stories about our

own behavior has been in everything from North Korean gulags to the “foot in the door”
technique of successive commitments in sales. See Cialdini (2008).


15 [Freedman and Fraser (1966)](https://doi.org/10.1037/h0023552)


16 Nessmith et al. (2007)


17 Bayer et al. (2009); Mandell and Klein (2009); Lyons et al. (2006); Fernandes et al. (2014)


18 Lusardi and Mitchell (2007)


19 Hilgert et al. (2003)


20 This process of changing the context of action has similarities to Sebastian Deterding’s

[descriptions of game design (Deterding 2010) and differentiates it from a traditional UX](https://oreil.ly/c7e_2)
process, where only the product (tool) itself is designed.


# **Chapter 9. Crafting the** **Intervention: Cue, Reaction,** **Evaluation**

_One of the earliest and most powerful demonstrations of behavioral science_
_in government came from the UK’s Behavioural Insights Team. They_
_communicated with people who had tax debts and shared with them the fact_
_that most people do in fact pay their taxes. That encouraged people who_
_hadn’t paid to do so themselves. In other words, they used_ descriptive
norms. _The results were clear and powerful: a 5.1 percentage point_
_increase in the payment of liabilities within 23 days._ 1


_Since then tax compliance, not surprisingly, has been a popular area for_
_applied behavioral science among governments around the world. These_
_efforts are often very low cost and have a long history of success._


_One such effort comes from the small, underdeveloped country of Kosovo,_
_where the World Bank’s Mind, Behavior, and Development Unit (eMBeD)_
_and the German Development Agency GIZ helped the country’s tax_
_authority design, implement and evaluate three experimental trials to_
_improve tax reporting and collection._ 2 _In the US, many Americans grumble_


_about our taxes and how the government doesn’t need them; in places like_
_Kosovo, low tax revenue means the government struggles to provide basic_
_services to their citizens._


_The team tested messages meant to encourage residents to report their tax_
_liabilities—using SMS, email, and physical mail. Within the_
_communications, they employed:_


_A social norms approach: “7 out of 10 firms submit their_
_declaration on time. Don’t wait, be part of the MAJORITY!”_


_An appeal to citizenship: “Not paying your taxes places an unfair_
_burden on your fellow Kosovo citizens. Please don’t be an_
_irresponsible citizen.”_


_A focus on benefits: “Did you know that your VAT contribution is_
_invested in your city?”_


_And reframing non-payment as an active (intentional) choice,_
_instead of inaction: “If you do not declare now, we will consider it_
_to be your active choice…”_


_Overall, they were able to successfully increase tax reporting; the physical_
_letters, for example, increased reporting by 73% among all intended_
_recipients (companies and individuals), with a tremendous 431% increase_
_among individual tax payers who successfully received the letter._ 3 _Like_
_many behavioral studies, tax compliance studies show how low-cost,_
_straightforward marketing and communications can deliver outsized results._


We’ve arrived at the fun part: crafting the intervention itself. What should
our products and communications _actually do_ to facilitate or hinder action?
We defined the problem in Chapter 6. We explored the context and
diagnosed the behavioral problem in Chapter 7. We quickly checked
whether there was a way to magically make the problem go away and do
everything on the user’s behalf in Chapter 8. Let’s say there’s no magic
solution, and it’s time to solve the problem directly.


Thankfully, solutions follow directly from our diagnosis of the problem.
Sometimes they are easy and straightforward as well. If your diagnosis
shows that your users don’t know about your new feature (the Cue is
lacking), well, the solution is obvious: show them the new feature. When
it’s not so obvious what to do, we can draw upon the many research studies
conducted in behavioral science. These studies can be grouped into ways to
encourage beneficial action and ways to hinder negative actions. We’ll start
with encouraging beneficial ones.


As you saw in Chapter 7, we diagnose why users don’t take action in terms
of one or more behavioral obstacles: a missing Cue, a negative emotional
Reaction, and so on. We use the CREATE Action Funnel. For each
CREATE obstacle, behavioral scientists have developed a set of
interventions to help overcome that obstacle.4

Without further ado, let’s introduce the interventions.5


Table 9-1 offers two dozen tactics you can use to facilitate action, organized
by the part of the CREATE Action Funnel that they affect most strongly.
The following sections describe each of these cognitive mechanisms and
how you can deploy them to the user’s advantage. Many of the tactics listed
here have been briefly mentioned earlier in the book, when we first
introduced how the mind works. In those cases, we’ll focus on how that
tactic can be employed in practice. The goal of this section is to provide a
quick reference to each of the major tactics you can use to craft your
interventions all in one place.


_Table 9-1. Tactics to support action_


**Component** **To Do This** **Try This**


Cue Create a cue Tell the user what the action is


Relabel something as a cue


Use reminders


Increase power of cue Make it clear where to act


Remove distractions


Target a cue Go where the attention is


Align with people’s time


Reaction Elicit positive feeling Narrate the past


Associate with the positive


Increase social motivation Deploy social proof


Use peer comparisons


Increase trust Display strong authority


Be authentic and personal


Make it professional and beautiful


Evaluation Economics 101 Make sure the incentives are right







Avoid direct payments


Test out different types of motivators


Increase motivation Leverage loss aversion


Use Commitment Contracts


Pull future motivations into the
present


Use competition


Support conscious decision making Make sure it’s understandable


Avoid cognitive overhead


Avoid choice overload


Ability Remove Friction Remove unnecessary decision points


Remove Friction Default everything


Elicit implementation intentions


**Component** **To Do This** **Try This**



Increase sense of feasibility (selfefficacy)



Deploy (positive) peer comparisons


Help them know they’ll succeed



Remove physical barriers Look for physical barriers


Timing Increase urgency Frame text to avoid temporal myopia


Increase urgency Remind of prior commitment to act


Make commitments to friends


Make a reward scarce


Experience Break free of the past Use Fresh Starts


Break free of the past Use Story Editing


Use slow-down techniques


Avoid the past Make it intentionally unfamiliar


Keep up with changing experiences Check back in with users


So let’s look at each of them in turn. Afterward, we’ll return to the other
behavioral challenge: hindering negative action.

## **Cueing the User to Act**


The sight of the overgrown grass prompts you to mow the lawn. A TV
commercial for steak reminds you that you’re hungry. For many behaviors,
the motivation is often present, but it’s in the background. Something needs
to cue you to think about it _now_ rather than later: that cue is the first step in
the CREATE Action Funnel we talked about in Chapter 2.


Cues, wisely placed, are essential for behavior change. This is true for
nonconscious habits—a cue in the environment starts a habitual routine—
and for conscious decisions to act.

### **Ask Them**


One simple way to cue people to act is just to ask them. Yes, it’s obvious.
Yes, it’s simple. And yet, we forget to do it—because our products are so


awesome and we assume people are already thinking about using them.


I know, you can’t imagine that anyone would make such an obvious
mistake. But we all do all the time. Do you include a link to your website at
the bottom of your emails? If so, do you actually ask people to look at your
site, or do you hope it’s obvious? Do you post your Twitter handle on your
messages or blog posts, hoping people will follow you? Readers could
figure out the action we intend (view website, follow on Twitter), sure. But
the more mental leaps that are required between what we see (Twitter name)
and the action, the less likely is it that the action will cross our minds before
we’re distracted by something else.


Dustin Curtis ran a set of experiments on how he presented his Twitter
handle to readers of his blog.6 He started with a simple informative
statement: “I’m on Twitter,” in which “Twitter” was a link to his page. 4.7%
of readers clicked. Then, he did the obvious—which apparently isn’t so
obvious to the rest of us—he told people what the action was. “Follow me
on Twitter.” Boom—7.31% of users clicked. And, even clearer: “You
should follow me on Twitter here”—12.81% of users clicked. There are
multiple effects at work in the last statement (a personal request, specificity,
etc.), but the effect of requesting the action is undeniable. One lesson is
simple: _directly, and unabashedly, ask people to take action_ .


If you do it nicely and don’t ask too often, asking rarely leads to less action
than not asking. Asking for action within a software product has three
distinct effects:


_Cueing (attention)_


Not only are people busy, but their attention is extraordinarily limited.

Dean Karlan (among others) shows that increasing mere attention to an

issue is a key factor in driving behavior—especially if the person

already has the motivation to act.7


_Obligation_


It’s uncomfortable to say no to a reasonable request. If the company

(and especially, a particular _person_ who the product personifies) can be

seen as a friendly, anthropomorphized presence, then this can help spur

action.


_Immediacy/urgency_


Most “good” actions, like saving money, exercising more, or smoking

less, are things that a person can do at any time, and therefore can be put

off. Asking people to do it _now_ (with some reason for the urgency)

helps people get over the “I’ll do it later” hump.


It doesn’t take much to ask users to act. Emails. Text messages. Big honkin’
Act Now buttons. These are obvious and effective ways to trigger action.8
Don’t waste time on complex psychological approaches to help people to
act if you haven’t already tried the obvious ones.

### **Relabel Something as a Cue**


Another way to cue action is to help users reinterpret an existing feature of
their environment as a cue. Let them specify something that they see or hear
normally in their lives—like the morning show on their favorite radio
station. Then have them associate an action with that cue (e.g., “Once the
morning show finishes, go running” or, “On Thursday, when I exit from the
metro, I’ll go buy my running shoes”).


Simple if/then rules like this have been used for thousands of years—and
your product can help people use them by building an association between
something they’ll see, and something they want to do. More recently,
researchers have experimentally established the impact of _implementation_
_intentions_, in which people make specific plans for action in the future.9
Implementation intentions are a way to tell the mind to do X whenever Y
happens. They pull the burden of thinking from the future to the present,


allowing the person to invest time in setting up the plan to act now, and
simply executing it automatically when the environment cues action in the
future.


Here’s a personal example of how setting up a concrete plan establishes a
cue to act in the future. To write this book, I used a simple online program
by Anna Tulchinskaya that encourages writers to write regularly. Figure 9-1
shows what I filled out when I first signed up. I set a plan to write every
day, at a certain time of day, in a certain place. So when I saw the clock,
that became my cue for action.


_Figure 9-1. My plan to write each night_

### **Make It Clear Where to Act**


We scan, we don’t read. Don’t expect users to read lots of text on your
page. The two-second rule is a good test—if you don’t get the gist in a twosecond glance at the page, you risk losing the reader’s attention. Krug’s
_Don’t Make Me Think_ (New Riders, 2006) gives a great overview and
practical examples, and Johnson’s _Designing with the Mind in Mind_


(Morgan Kaufmann, 2010) talks about the visual perception system and
related psychology.


Some of the key things that we quickly recognize are the ways in which we
can interact with a page ( _affordances_ per Norman’s classic _The Design of_
_Everyday Things_, Basic Books, 1988)—what looks like it is clickable,
doable, or can otherwise get you off this page and quickly on to the next
one. The lesson is simple: make buttons look like buttons, and make
anywhere else people are expected to take action clearly a place where they
_can_ take action.

### **Remove Distractions: Knock Out the Competition**


There’s a flip side to encouraging a behavior that hasn’t received nearly as
much attention in the behavior change world. Namely, each distinct type of
behavior is in competition with (almost) every other type10—competing to
grab the user’s very limited attention (i.e., competing triggers), to claim the
user’s time (i.e., competing to be easier and faster), and to be the most
motivating. One can draw out these competing or blocking factors with a
series of questions:


What in the environment already has the user’s attention and thus
_crowds out awareness of your action_ ?


Similarly, is the environment crowded with other actions that are
already _easy or simple_ to take?


What in the environment _demotivates_ the individual or, more
subtly, _motivates the individual to do other things_ and thus crowds
out the target action?


When faced with serious competition, here are three strategies to counteract
it.


First, if the competing factors are within the application, the product team
needs to make hard choices and potentially decrease the
attention/motivation/ease provided for other behaviors. Often you really


don’t need to change all of them—just focus on pulling the users’ attention
to one thing at a time. If you have their attention at the time they are doing
what they need to do, it doesn’t matter (as much) that the application
motivates them to do other things at other times. One straightforward way
to minimize competing attention-getters is to simplify: remove other calls to
action, remove distracting text, and take out anything else that isn’t
essential from the page. Put those other actions in another part of the
application that is clearly, conceptually different from the current one.


Since users are scanning a screen and trying to save work, they’ll all too
likely just to click on the first thing that looks clickable. So make a single,
clear call to action if your goal is to get the person to keep moving through
the screen. Remove extra links and buttons, or place them in a distinctly
lower level in the screen’s hierarchy.


Second, you can use competing factors to your advantage. If the user is
really engaged in something else, look for a clever way to connect it to your
target action. Wherever the user’s attention already is, that’s the best place
to be. That’s why many applications are built for Facebook—that’s where
users are already putting their attention.


Third, there’s the brute-force approach—shout louder for attention, be more
motivating, and make using the product easier than breathing. I don’t
recommend this. If the user is doing something (else) there’s (a) probably a
good reason, and (b) it takes more than a slightly better behavior to
overcome an entrenched one. There are real costs to switching behaviors;
for example, we’ve already discussed the challenges of changing habits.
However, if you can’t directly dampen the other actions or find a clever
way to use them to your advantage, this may be your only option. Over
time, you can build up competing habits and experiences within the
application that crowd out those other actions. Or, you can go back to the
drawing board and find a different target action that doesn’t compete so
strongly with other existing behaviors.

### **Go Where the Attention Is**


Where’s the easiest place to get someone’s attention? Where their attention
already is. That’s the logic behind marketing swag at conferences.
Pharmaceutical salespeople are well known (and rightfully critiqued) for
giving away tons of “free” pens, clipboards, stickers, and such to doctors,
all with their logo on them, so that when the doctors are prescribing
medicine, they’ll be reminded of the particular company’s products.


The same logic underlies many wearables for a far more laudable purpose.
If someone wants to exercise but keeps forgetting, what do you do? You
could devote a significant ad budget to signage, video testimonials from
athletes, etc. Or, you could simply give them an exercise band that doubles
as a watch (or, increasingly, a watch that doubles as an exercise band). They
wear it on their wrist because it performs a key function and, in the process,
are frequently cued to think about exercise.


If you want to get someone’s attention to a recurring activity—like taking
time out of their day to meditate—you could try having them install an app
on their phone that triggers a reminder message, since their attention is
often on their phone. Or, you could give them a calendar invite that sets up
a recurring appointment—since again, their attention is often on their
calendar.

### **Align with When People Have Spare Time**


In my research, I’ve found that the single most powerful factor in whether
someone pays attention to your cue is when you cue them; that is, whether
or not you align with when they have bandwidth to pay attention.


Over the years, I’ve run over a hundred studies of time-of-day and day-ofweek effects on different populations and regularly see changes in response
by three times within the exact same population and with the exact same
content. Figure 9-2 illustrates results from one set of those tests. This
particular study entailed emailing employees at a large manufacturing
company in the United States—we found that by far the best time to contact
them was during the start of the workday on Tuesday.


Before you set all of your marketing campaigns and product launches to
occur on Tuesday morning, there’s an important caveat. Each group of
people, and indeed each person, has a different _structure of attention_ : a
different rhythm to their days and weeks. People working the night shift
will be able to pay attention to your cues at different times than those on the
day shift. In addition to the manufacturing population in Figure 9-2, we ran
a similar set of experiments with other groups—including a large minimum
wage population in the service sector. Many of them worked two jobs, and
weekdays were absolutely terrible times to reach them. Instead, it turned out
that Sunday evenings and holidays were by far the best time to gain their
attention—on the order of a two to three times improvement.


_Figure 9-2. Aligning when you contact people with when they have attention to spare can have a_

_tremendous effect on response rates_


So when you try to interact with people is tremendously important. But
there’s no simple rule: it comes from your understanding of your population
and their structure of attention.

### **Use Reminders**


We all forget things in our daily lives—even things that are important to us.
Yet we often don’t consider simple forgetfulness as a cause of inaction
among our users.


Researchers indeed find that people don’t follow through on an action they
want to take simply because they failed to remember it.11 Reminders don’t
need to be fancy or complicated; an email, text message, call, in-app
message, etc. can be enough. Don’t assume that because the action is
important people will remember. We all have busy lives—and so do your
users. In some of my own research studies using email to reach diverse
populations, I’ve generally found that two follow-up reminders lead to a
roughly 50% increase in response relative to the first communication. It’s
not an iron-clad rule, of course, and it helps when those reminders occur at
different times—in case you didn’t align with people’s spare time.

### **Bonus Tactic: Blinking Text**


Blinking text is a really great cue. It never fails to catch our attention. And
it’s also darned annoying, because it catches our attention and won’t let go.
If possible, use blinking _scrolling_ text. Right across the top of the screen.


OK, please don’t do it. Seriously.

## **The Intuitive Reaction**


Once a cue catches the user’s attention, the mind reacts—often in the blink
of an eye. Regardless of the overall merits of the action (and product), that
reaction can cause the user to shut down. Here are some techniques to
address that problem.

### **Narrate the Past to Support Future Action**


Our self-narrative is how we label ourselves and how we describe our
behavior in the past; products can help people see themselves differently.
The goal, from a behavior change perspective, is to _help people see_
_themselves as someone for whom the action is a natural, normal extension_
_of who they are._


In other words, if you want to help people begin exercising (like Fitbit’s app
does), help them see themselves as people who have already been


exercising in small ways and just need to do more (e.g., first-time Fitbit
users may be surprised to find out how far they normally walk each day).12
An easy way to support this process is by merely asking people about things
they’ve done in the past that are related. And congratulate them for the
work they’ve already accomplished.



Essential to a supportive self-narrative is the belief that one can actually
succeed in the action (i.e., users need to feel that the action is under their
control and that they have the skills and resources to—potentially—make it
happen). That’s the sense of self-efficacy discussed in “Ability”.13
Reminding people about their prior successes at related tasks can help build
that sense of self-efficacy; so can the “small wins” and positive feedback
described in the last two chapters.14



13



14


### **Bring Success Top of Mind**

Similar to renarrating the past to shape someone’s self-conception, a related
technique is to redirect someone’s current attention to prior successes. We
all each have frames of reference with which we interpret and respond to
the world. Those frames of reference are selectively activated, based on our
(very) recent experiences.


If you’re asking someone to commit to running once a week, get the person
thinking about previous times they’ve run first (as long as that experience
was positive)! When you ask them to commit to running, the benefits of
running will be clearer and more salient in their minds.

### **Associate with the Positive and the Familiar**


Chapters 1 and 2 talked about how, for many of our choices in life, we
intuitively know whether taking an action feels right or not to us. A big part
of that is our prior _associations_ —our learned experience that buying a fancy
pair of shoes is going to make us feel great when we walk out of the store
with them, at least for a few days.


Products can build these associations to help a person change behavior. In
Chapter 8, we talked about changing the _action_ itself so that it leverages


prior experiences. Here, the _product_ can be changed so that it helps users
make the mental connection between the action they want to take and their
prior experiences. I call this a _behavioral bridge_, because it helps the user
cross from one type of behavior to another by making it less “new” and
difficult. The bridge connects past experience with future actions.


Here’s an example: Jive Voice is a conference-calling application that
allows people to switch from using a dial-in number and long PIN code to
using a simple link in a URL. Dial-in numbers and PINs are frequently
misplaced and annoying to enter. When a user clicks the URL, Jive Voice
calls them and patches them into the conference line. The challenge is that
using a URL is new and strange. In the product, the company highlights the
new and unique aspects (ease of use, etc.) but is also careful to leave a
behavioral bridge in place—a comforting bit of information about how
users can treat it like a normal conference call if they need to, since the
underlying technology is a conference line with a dial-in number and access
code.

### **Deploy Social Proof**


If we see that other people are taking an action, we’re more likely to feel
that the action is valuable and worthwhile. It’s a quick gut check—if that
person does it, it must be OK, right? This is one of the major ways that our
minds save work and quickly make decisions in uncertain situations.


Using social proof is a key tactic in sales and persuasion with a long
research tradition behind it.15 You can convey the fact that other people are
taking the same action by using people’s faces or short testimonials.
Different genres of social proof include user or expert testimony
testimonials (often on a product page), celebrity endorsements (in movies or
TV ads),16 or online reviewers (think Amazon). In addition to having as
long research tradition, it is used and abused extensively in marketing
campaigns, from paid testimonials by fake experts to comments supporting
a product by people who look like everyday users but are actually trained
actors.17 For more information on this topic, see Chapter 1.



15



16



17


**NO MAGIC WANDS**


Throughout this book, I provide the tools you need to find the
behavioral processes and product features that work in your particular
context, and verify their impact with your specific set of users.


What I can’t do is give you the secret behavioral tricks that will always
change user behavior in predictable ways. That’s because such magical
formulas simply don’t exist (run away from people who tell you they
do!). All behavior change interventions interact with an individual’s
desires, prior experiences, personality, and knowledge to produce their
unique impact on that person. There is just too much variation across
people for any approach to always work.


Most of the approaches and lessons that I talk about here have been
tested either in a researcher’s laboratory or in a specific product setting.
In most cases, I’ve also observed these techniques in practice in my
own work or through the dozens of companies I’ve interviewed and
learned from. Unfortunately though, there are very few studies out there
that apply and rigorously test theories of behavior change in ways that
can be generalized to lots of other products. That’s something we strive
for on my team—but even then, it’s difficult to make the case that what
works for us, in helping people take control of their finances, is going to
work the same way for someone else’s dieting software.


We are all still in the early stages of learning how to use products to
help people change their behavior. So in Chapters 12–14, I provide
some guidelines on how to test specific interventions in your product,
and help you move the field forward at the same time. I encourage you
to contribute your findings to the broader community so we can all
learn and develop our skills together.

### **Use Peer Comparisons**


Being told about, and compared to, the actions of our peers can be
immensely powerful. It’s a specific form of social influence, like social
proof. Our behavior frequently conforms to what we believe our peers do
(i.e., _descriptive norms_ ), compounded by the usually false belief that our
peers are watching our behavior and judging it ( _spotlight effect_ ). This effect
has been shown in everything from energy usage to voting.18


For behavioral products, the implications of peer comparisons are
tremendous. Social norms are an incredibly powerful part of our
microenvironments and can encourage (or discourage) action. The same is
true within the context of each individual screen that the user interacts with.


To use this technique, compare the user’s performance to a reference group
that they care about (their friends, colleagues in a similar job), and try to
ensure that the reference group you choose is doing _better_ than the user. A
note of warning, however: peer comparisons encourage people to move
toward the norm (the average for the reference group). So if you tell them
they are already going better than most people, they may just relax and
don’t work so hard. That negative effect can be counteracted with an
explicit social approval (Great job!) for exceeding the norm.19 Figure 9-3
shows one of our studies at HelloWallet that encouraged people to save.


_Figure 9-3. A peer comparison I helped develop to encourage people to save_

### **Display Strong Authority on the Subject**


People are more likely to trust those who they see as an authority on the
subject. If you’re telling your users that they have to do action X in order to
build up to their goal of Y (and it’s true), then speak with authority. Don’t
write wishy-washy text. Make sure your credentials can be seen without
beating your users over the head with them.


There are great studies on how people wearing suits, or with professional
titles, are simply assumed to be more credible and trustworthy. The use of
(perceived) authority is also a favorite tactic in sales and persuasion. See
Cialdini’s discussion of the underlying research (2008).

### **Be Authentic and Personal**


People pay more attention to personal appeals to act than to impersonal
ones. If you receive a letter with a handwritten envelope, how likely are you
to open it? How about one with a standard machine-printed address? The
reasons are manifold, but we are more likely to ignore machine-generated,
impersonal appeals than tailored, personal ones.20 We have an almost


automatic response of “this is spam” for any email or letter from impersonal
sources.


Here’s a great example of using personalization and authenticity to cut
through the noise and get people’s attention. In Oregon, there’s a lottery for
free healthcare for people who can’t afford it. But some of the people who
sign up for and end up winning the lottery don’t open the letters notifying
them that they’ve won. And so, they miss their chance at free healthcare.


ideas42, the leading behavioral economics consultancy in the United States,
devised a simple outreach campaign to the winners of the Oregon
healthcare lottery. They notify people that they’ve won with a postcard
featuring the smiling faces of the people at Providence Health in Oregon
that will help them sign up for their healthcare. The recipient’s name and
address are handwritten on the postcard. Figure 9-4 shows a sample.


_Figure 9-4. A postcard developed by ideas42 to help winners of the Oregon healthcare lottery get_
_past their automatic rejection of form letters and read enough to see that they’ve won free healthcare_


Remember, we’ve been conditioned to reject impersonal and computergenerated appeals. Most of us have an intuitive reaction against them. To
avoid that intuitive reaction, our products need to do something different,
something that’s good practice anyway: be authentic and personal.

### **Make the Site Professional and Beautiful**


And finally, let’s not forget the basics. We rarely consider unprofessionallooking websites and apps to be credible.21 If you’re trying to help someone
take an action, don’t make them have an intuitive reaction of distrust. That’s
unnecessary friction on the action. Like it or not, we assume that scammers


make bad websites and apps. We even find it easier to _use_ clean, welldesigned products.22 Even if your app is created to help people, it has to
look good.


People really do judge a book by its cover. You could try to argue with the
shallowness of people’s intuitive reactions all day long. Or, you could just
design a nicer cover. After they open the book—i.e., start using your app—
then they can discover how beautiful it is on the inside, too.

## **The Conscious Evaluation**


A person’s conscious evaluation is similar to the stereotypical view most
people have of decision making: do the benefits outweigh the costs? What
are the alternatives, and how does this action stack up against them? While
similar, it certainly isn’t a perfect cost–benefit analysis: because people are
often distracted, they may not carefully think about all of a particular
action’s benefits (or costs!). They may have limited information. And even
when they do think carefully and have the necessary information, they may
be overly focused on the present (present bias) or miscalculate costs or
benefits (e.g., exponential growth bias).


Because of these imperfections, we should ask once again: what are ethical
ways to design for behavior change? The core costs and benefits of an
action are obviously very important; if the costs outweigh the benefit, the
user shouldn’t do it. Changing the core incentives to make it more valuable
for the person, decreasing cost or increasing the benefits, seems appropriate
and ethical. And there’s no particular magic or mystery here, so we’ll only
touch upon that briefly.


While there are certainly gray areas, hiding the costs of an action sounds
and likely is manipulative and dishonest. Highlighting existing (but
unattended to or miscalculated) benefits seems generally permissible—
though each case of designing for behavior change should be still reviewed,
as noted in Chapter 4.


Thus, in this section, we’ll focus on these three options: increasing benefits,
decreasing costs, or highlighting existing benefits. In terms of the costs,
we’ll look at substantive changes, and not minor ones. Minor costs are
surprisingly important—many of the early examples in behavioral science
involved tweaking form fields, defaults, and such. Small changes can lead
to outsized effects. However, these effects are not (primarily) because of the
conscious calculation that people make—an extra form field shouldn’t
affect a conscious cost–benefit analysis at all. Rather, they cause us to pause
and face a decision point (a concept we introduced in “Ability” and will
show in more detail as we craft interventions to increase their Ability in the
next chapter).23


That said, let’s start with the most basic of all: incentives.

### **Make Sure the Incentives Are Right**


Behavioral economics, and with it the broader field of behavioral science,
in large part arose as an extension to or even a correction to traditional
economics. Traditional economics focuses on a person’s preferences and the
optimal route to fulfill those preferences. In many economic models, this
boils down to the simple observation, “People want to be paid, so pay them
and they’ll do stuff. Pay them more, and they’ll do more.” Behavioral
economics shows that this isn’t always the case, and people have many
motivations above and beyond receiving something in return.24 People are
motivated by altruism, by a sense of self-esteem, etc. That’s all true, but we
should never lose sight of this simple fact: people really are motivated by
getting stuff, especially by getting money.


If the behavioral obstacle that a user faces is one of Evaluation—they don’t
see the benefits outweighing the cost—then we should fix that first. Make
sure it really is in the users’ narrowly defined interest to take the action. If it
isn’t, (a) it’s likely very difficult to overcome that basic problem of
incentives, or (b) it’s likely going to involve trickery.


So if you’re product isn’t very good and doesn’t benefit your user enough to
justify the cost—from their perspective, not yours—designing for behavior


change isn’t going to help you. Fix the product first. It must solve a user
need in a way that the user feels is worth the cost. That may require
lowering your price. It may mean building a better product. Either way, it’s
not something you can avoid. And yes, this is actually something I’ve had
to say many times when people ask me how to promote a product that their
target audience doesn’t want. Yep.


OK, let’s assume you’ve covered Economics 101. Now for the more
interesting stuff.

### **Leverage Existing Motivations Before Adding New Ones**


Does your product need to add a new motivation for users to act, highlight
existing ones, or both? First, understand what currently motivates users to
act. Use the information you learned about your users in Chapters 6 and 7,
about why they want to take the action. Maybe their doctor has told them to
exercise more; maybe they really enjoy running but can’t seem to fit it into
their schedule. Since we’re often distracted and thinking about other things,
simply reminding people of their existing motivation at the moment of
action can be powerful. And _it’s really cheap to remind people of what they_
_already care about; it’s much more costly to add a new motivation._


If you’re not sure what currently motivates your users, you can do some
simple field tests—check how important particular motivations are versus
other things in the person’s life. A good way to gather that information is to
present a series of trade-offs—ask which of two things the person wants
more (e.g., as motivations for exercise: “living five years longer” versus
“going on a date next month”). It’s less ideal to simply ask people, “How
important is this to you?” because we often don’t have a real baseline
against which to answer that question, and it engages a different part of our
minds than the one that usually makes the actual decision to act.


Another reason the existing motivations are important has to do with
extrinsic versus intrinsic motivation.25 _Intrinsic motivation_ comes from the
inherent enjoyment of the activity itself, without considering any external
pressure or reward. _Extrinsic motivation_ is the desire to achieve a particular


outcome, such as receiving a reward for it (like money or winning a
competition).


Your users can have preexisting intrinsic _and_ extrinsic motivations, and
your product can leverage both to drive behavior. But when the product
_adds_ a new motivation to act, the source of that motivation is almost
always, by definition, outside of the user and outcome-oriented, or
extrinsic. For example, people using the Fitbit One often have both a
preexisting intrinsic motivation and a new extrinsic motivation: an inherent
enjoyment from exercising and using one’s muscles, as well as the desire to
reach a particular goal and be congratulated for it by the product.


Intrinsic motivations can keep people going when the product isn’t directly
involved in their lives. New extrinsic motivations, provided by the product,
can’t do that. They are effective only when the product is directly involved:
when they stop, so do the users. If your product adds extrinsic motivations,
it can also crowd out people’s existing intrinsic motivations—meaning they
lose the joy of doing something for its own sake if they start being paid to
do it.26


However, that doesn’t mean new extrinsic motivations are always a bad
thing; they just have to be used judiciously:


_When the person doesn’t have a strong existing motivation for a particular_
_step in the sequence of actions_


For example, someone really wants to get healthy, but doesn’t see how

regular blood pressure checks are important. A little boost can help.


_For one-time actions where crowding out intrinsic motivation is irrelevant_


For example, someone really wants to exercise but has no motivation to

go buy gym clothes. An incentive can get them past that barrier and

closer to their goal.


_To help users transition from extrinsic to intrinsic motivation—to get people_
_started as they find the joy of the activity itself_


For example, conversation clubs can use a small incentive (free dinner)

to get together people who are learning a new language for the first

time. While they are there, they experience the intrinsic joys of being

immersed in the language, which pulls them forward for future

learning.27

### **Avoid Direct Payments**


In line with our discussion about leveraging existing motivations before
adding new ones, you could just pay people to click on your button. But I
don’t recommend it. If you need to pay people to do something that’s
supposed to be a voluntary behavior change, you’re probably not
connecting that small action with the reason they want to change their
behavior in the first place.



There is extensive evidence that financial incentives induce individuals to
undertake behaviors that they would not undertake.28 People are motivated
by money. No great surprise, right? However, when a person is already
inclined to take the action, financial incentives can backfire by decreasing
preexisting internal (intrinsic) motivations; the individual is more likely to
stop the behavior after the incentive is removed.29 Similarly, other social
motivations are crowded out when we start thinking about our behavior in
terms of being paid to act.30 Direct payments are less likely to cause
problems with one-off behaviors, like signing up for the gym. But they can
undermine long-term intrinsic motivation, like actually going to the gym
over time!



28



29



30



So, bringing together the various points thus far about the user’s conscious
Evaluation: you do want the basic incentives to be aligned. That is, it should
be in people’s interest to take the action. But if you find yourself adding
additional payment on top of that, to make the action “more motivating,” it
may not have actually been in their interest in the first place (incentives
were off) or you’re not connecting with and leveraging the existing intrinsic
motivation the person has (and risk crowding them out).


### **Leverage Loss Aversion**

People respond much more strongly to losses than to gains—they are
“averse” to losses. In fact, in many scenarios people will be willing to
forfeit twice as much money to keep an item that they already have (and
have no other personal attachment to) than they are willing to pay to
purchase an otherwise identical item. There’s a detailed literature on special
cases of loss aversion, but that general rule holds true in many cases: _losses_
_are roughly twice as motivating as gains_ .31


Loss aversion is a very powerful tool to help people change their behavior.
By selectively framing the presentation of a desired action as _avoiding loss_
_rather than gaining benefits_, the application can trigger a strong gut
reaction to act. For example, it can be much more persuasive to tell
someone they’ll lose sexual potency unless they get in shape, rather than
telling them they’ll gain more attractive abs.32


When leveraging loss aversion, though, remember that your users can just
stop using your product to avoid loss and the negative emotions that come
with it. The product must be seen as worthwhile and enjoyable overall—
loss aversion should be used only on the margins.

### **Use Commitment Contracts and Commitment Devices**


Loss aversion, when used too often or people actually have to experience
the loss (instead of merely the prospect of it), has an obvious downside: you
can end up _punishing your users_ . If you give people a consistently bad
experience, in most cases, they will stop using your product and do
something else with their time. If you could hypothetically force people to
endure your punishment, that might be effective. But you can’t, and the user
has the option to ignore or avoid you.


Not punishing your users doesn’t mean completely avoiding the _threat_ of
properly selected punishments. One powerful type of threat is a _commitment_
_contract_, in which people pre-commit to taking an action, and they forfeit
something they care about if they fail to follow through.33 For example,
[stickK.com employs commitment contracts to generate creative, personal](http://stickk.com/)


punishments, like automatically donating money to an NGO you hate if you
fail to lose weight. Importantly, their punishments are self-imposed and
self-calibrated; people choose their own punishment. We react much more
negatively to externally imposed punishments than we do to self-imposed
ones.


Overall, the trick is to carefully use the threat of punishment (and ideally, a
self-imposed one) to motivate action without actually punishing people and
driving them away.


Another, related technique is to use a _commitment device_, in which people
lock in their choice to not act in a certain way in the future. It is like a
commitment contract, but it’s more extreme: the future action is closed off,
instead of threatening a punishment. Taking disulfiram before a night of
potential drinking is one such device; it makes the person who doesn’t want
to drink feel sick if they cross the line and do.34

### **Test Different Types of Motivators**


As humans, we don’t lack for things that could motivate us. Money. Food.
Control. Esteem. Researchers have tried to make sense of our motivations
for decades,35 from Maslow’s hierarchy of needs (we address deficiencies
in a successive set of needs, from basic comfort to self-actualization) to von
Neumann and Morgenstern’s expected utility theory (we should do what
provides us the most benefit). I won’t try to argue which motivations are
most important for all of humanity but rather will make an observation. The
most important form of motivation is the one _that’s actually compelling for_
_your users, given their life circumstances_ . Identifying that motivation is part
of getting to know your users and what resonates with them.36 It may also
entail experimentation—trying out a cash payment or public acclaim or
providing a sense of mastery. Three big areas you can explore with your
product are:



35



36



Quasi-monetary rewards like points redeemable for cash (while
being wary of crowding out other motivations and of needing cash
because the product is fundamentally misaligned with user needs)


Progress and achievement rewards (including badges and other
gamification techniques)


Social motivations, like status or esteem of peers


Intrinsic benefits like exploring something new (the product can
accent the intrinsic rewards that users already receive)


Also, try varying the motivation over time—we become satiated in any
single area, at least in the short term and start looking for new rewards.
That’s obvious with food (if you’re no longer hungry, more food just isn’t
that motivating), but it also applies to other forms of reward (if you’ve won
a competition against your friends 10 times in a row, winning again isn’t
that interesting).

### **Use Competition**


To call out one of the existing social motivations people have: competition,
judicially used, can be quite powerful. We all have a natural competitive
side—though it’s much stronger in some people than others. Usually, you’d
build a competition into the overall product, but it can be deployed at a page
level too. For example, imagine a page that has people match Spanish
words to their English meanings to help the users learn Spanish. The page
could include a counter of how many correct answers the individual has
versus others on the page at the same time.

### **Pull Future Motivations into the Present**


We like stuff now, rather than later. We’re far more motivated by current
goods and experiences than in future ones, even after accounting for
inflation, uncertainty, and so on. This _temporal myopia_ (focusing on the
present even to our own detriment), aka _present bias_, is deeply ingrained
and something that too many behavioral change programs forget.


For most people, most of the time, “a few years from now” doesn’t exist.
It’s not real, and whatever happens _then_ isn’t motivating _now_ .


And that presents a serious problem. Let’s say we sincerely want to slim
down our weight to avoid heart disease, or we may really think that saving
for retirement is important. But if the threat of heart disease or the need for
retirement money is still many years off, it just isn’t real to us.37 Daniel
Goldstein refers to this as the struggle between the present and future self.
We have noble long-term goals but are tempted to do other things in the
present.



37



38



How can we make that future motivation affect our near-term behavior? We
can use moments of strength (when we are actually thinking about the
future) to lock in that motivation. Commitment devices—described in an
earlier section—are one option. An extreme version of them, called the
Ulysses contract, was described in Homer’s _Odyssey_ : Ulysses had the crew
members on his ship tie him to the mast so that he was physically unable to
respond to the alluring call of the mythical (and deadly) sirens. In a Ulysses
contract, people make binding commitments that restrict what they can do
in the future.


Another method is to try to bring the future into our current awareness. For
example, researchers have used photo imaging techniques to help people
visualize what they will look like in the future and act according to their
future self’s motivations.39


Dan Ariely tells a personal story about how he turned a long-term
motivation into something meaningful and useful in the present with
“reward substitution.”40 He needed to take a highly unpleasant, painful
medication for over a year that had a long-term benefit (beating a disease).
But that long-term benefit wasn’t enough to overcome the temptation to
stop taking the medication. So, he linked taking the medication to
something that he enjoyed in the near-term—in this case, watching movies.
He’d only watch movies right before taking the medication, effectively
substituting one motivation (beating the disease) for another one (enjoying
the movie).


If these don’t work, we can forget about the long-term motivation altogether
and simply look for a completely different motivator that isn’t far off in the


future. For example, instead of talking about the long-term health benefits
of getting in shape, highlight the immediate benefits it will have on
someone’s love life.



Each of these is a technique to make the action motivating now, when it
otherwise would be far in the future. Just remember: when we ask people to
just think about what a wonderful retirement they’ll have in 20 years or all
the things they’ll be able to do after they lose three hundred pounds, we’re
asking them to do something that’s deeply foreign to how our brains are
wired.41

## **A Few Notes on Decision Making**


In this chapter, and indeed in most of the book, we focus on facilitating (or
hindering) action. As we briefly talked about in Chapters 1 and 3, there’s
another body of work in behavioral science around how to make better
decisions: how to help people slow down and make the choice they’d make
if they really thought it through. Here are some techniques that can help
there, which are similar to the Evaluation stage of the CREATE funnel.

### **Avoid Cognitive Overhead**


One way to think about the mental cost of your target action is _cognitive_
_overhead_, or “how many logical connections or jumps your brain has to
make in order to understand or contextualize the thing you’re looking at.”42
Figuring out what to do shouldn’t be guesswork for the user. That may
mean making the action slightly more _difficult_ to undertake in order for it to
be easy to understand.43


David Lieb gives a great example of product that is physically easy to use
but still is costly to the user because of cognitive overhead.44 Here’s his
hypothetical user thinking through a QR code, “So it’s a barcode? No? It’s a
website? OK. But I open websites with my web browser, not my camera. So
I take a picture of it? No, I take a picture of it with an app? Which app?”45
Forcing your users to think about what to do should be reserved for cases



42



43



44



45


where their input is important and will shape their outcomes; don’t force
your users to expend energy because the product is confusing.


Make it straightforward and clear what the user needs to do each time the
user has to make a logical leap from, “Oh, if I do this, then this will
probably happen, but I’m not sure,” that’s costly. It takes time and energy
away from the task at hand.

### **Make Sure Instructions Are Understandable**


This one is relatively straightforward. Look at the behavioral map and
specifically micro-behaviors where the user is told what to do next. Write
down how those parts would be described to a prospective user in at most
two sentences. Thinking about the behavioral personas identified in
Chapter 7, would those users understand the description? As needed, run it
by some sample users.

### **Avoid Choice Overload**


A growing body of work demonstrates the difficulties individuals face when
confronted with too many choices. Despite the common wisdom that “more
choices are better,” two problems arise. First, people may refuse to make
any decision at all. Second, people may regret the choices they made in an
impossible search for the optimal choice.46


For example, an often-cited study by Iyengar and Lepper placed two
different displays of jam in a grocery store: one with 24 jams, and one with
6.47 The 24-jam display attracted 60% of customers, but only 3% of those
shoppers ended up buying any of them. The 6-jam display attracted 40% of
customers, but 30% of them bought one. Subsequent studies have also
shown that satisfaction with one’s choice, _whatever it is_, decreases with the
number of options one had to choose among.


There is an obvious implication here when constructing individual pages in
an app—avoid situations in which the user has to choose among a large
number of options (if you want the user to make a choice and be happy with
it). There is also a less obvious lesson: be wary of users (and fellow


employees) who say they would really like more options. The person is
probably telling the truth, at least from the perspective of their conscious
deliberative self, but that doesn’t mean providing more options is the right
thing to do.

### **Slow Them Down**


Avoiding overhead, ensuring clarity, and avoiding choice overload all seek
to decrease the effort that the conscious mind needs to exert—to help
people focus on what matters in a decision and not put it off because of its
complexity. What if people aren’t making a conscious evaluation at all?
Here, we look to the techniques in the broader judgment and decisionmaking literature, in particular, intentionally adding friction to the process
so that it is difficult to act on an intuitive reaction. You can try to require a
waiting period before making a decision, make the problem intentionally
more onerous, or even make the text more difficult to read. Check back in
“Rushed Choices and Regrettable Action” for more information on this
topic.

## **Putting It into Practice**


There are a great variety of approaches to choose from when crafting
interventions to support action. In this chapter, we reviewed those for the
first three behavioral obstacles in CREATE: Cue, Reaction, and Evaluation.
Let’s take a look at the crib notes.


Here’s what you need to do:


Behavioral solutions often follow directly from a clear diagnosis of
the problem. If you don’t have your users’ attention to a new
feature, well, get their attention. If they dislike how your product
looks, change it. Spending enough time on the diagnosis can make
crafting the intervention really straightforward.


When the solution isn’t obvious, however, we have many
techniques to draw upon. These include removing competition for


the user’s attention, social proof, loss aversion, and commitment
contracts.


How you’ll know there’s trouble:


When you’re not clear which obstacle users face (go back to
Chapter 7 to diagnose it).


When increasing the users’ motivation seems like the obvious and
only solution (go back to Chapter 8).


Deliverables:


One or more intervention to try with your users, to see if it helps
them take action and overcome their obstacles.

## **Worksheet: Evaluating Multiple** **Interventions with CREATE**


_When your team is evaluating alternative interventions for a particular micro-behavior or step on_
_the behavioral map, you can quickly assess the strengths and weaknesses (from a behavioral_
_perspective) of each using a checklist like this:_


**Intervention**
**1: Tout**
**benefits of**
**app** **Intervention 2: Social proof**



**Condition**


_Cue_ to think
about taking
action



**Current state**
**for step:**
**Installs app**



☑ ☑ ☑







☑



Conscious
_Evaluation_
of costs and
benefits



☑ ☑


Increases
motivation, but
that’s not the
primary
problem









_Timing_ and
urgency to
act



☑ ☑ ☑



1 For a summary of this and other international studies in tax compliance, see Hallsworth et al.

(2017). For more information on the BIT’s work in this area, and their many other
groundbreaking projects, see and Halpern (2015).


2 My thanks to Abby Dalton at eMBeD for suggesting this study, among the many the World

Bank has implemented. This writeup is based on their report, “Promoting Tax Compliance in


Kosovo with Behavioral Insights” (Hernandez et al. 2019), and subsequent email exchanges
with Abby Dalton.


3 That is, on the treated population of individual taxpayers. The prior figure, 73%, was for the

intent-to-treat population of both individual and corporate taxpayers. There was a significant
problem of nondelivery because of bad contact information.


4 CREATE is my framework for organizing the myriad behavioral findings out there; the

original researchers did not use this framework—in the behavioral literature, there often isn’t
any discussion of organizing principles like this. Instead, each paper studies each behavioral
mechanism on its own. Dan Lockton provides a good (and unfortunately rare) example of
systematically organizing these tactics—he discusses them as eight “lenses” for thinking about
behavior change (2013).


5 This presentation in table form is inspired by a conversation with Nir Eyal and ideas42’s

Behavioral Map.


6 Curtis (2009)


7 Karlan et al. (2011)


8 By effective, I mean they engender more action that than not using them. This technique is

really obvious, but there are actually experimental studies that show that they work. See
[guessthetest.com for some examples of optimizing these simple calls to action.](http://guessthetest.com/)


9 Gollwitzer (1999)


10 We talked about this briefly in Chapter 2—that at each stage of the CREATE Action Funnel,

the action must be _relatively_ better than the other potential actions the person is thinking about
undertaking.


11 Guynn et al. (1998)


12 [Clear (2012) expands on this concept further in his Layers of Behavior Change model. He](https://oreil.ly/MGDMd)

describes three layers of progressively increasing power over behavior: appearance,
performance, and identity.


13 [Bandura (1977)](https://doi.org/10.1037/0033-295X.84.2.191)


14 On the other extreme, generating a supportive self-narrative might require overcoming

_learned helplessness_ (Maier and Seligman 1976). If people have failed repeatedly and believe
they had no control over the outcome, they can simply stop trying. For example, a student who
has repeatedly failed at math despite hard work may shut down and think they simply aren’t
smart enough to handle it. Learned helplessness is difficult to overcome; products have to find
creative ways to reinterpret past events and have users develop other ways of explaining future
ones. Show that the person does have control over their future and that the causes of past
failures don’t apply to the present situation.


15 Cialdini (2008)


16 [And sometimes of celebrities making fools of themselves doing so.](https://oreil.ly/Y420a)


17 [A few of the many examples.](https://oreil.ly/WsDhJ)


18 Energy usage: Cialdini et al. (1991); voting: Gerber and Rogers (2009)


19 Schultz et al. (2007)


20 See, for example, Garner (2005); Noar et al. (2007).


21 Fogg et al. (2001)


22 See Anderson (2011) for examples.


23 Thank you to Emiliano Díaz Del Valle at IMEC for raising questions about the ethical basis of

designing for behavior change when the person does not feel motivated to act.


24 And, to be clear: traditional economics does not solely focus on monetary incentives nor that

preferences are limited to money. It’s rather that many economic arguments and models take
this simple form.


25 Deci and Ryan (1985); Ryan and Deci (2000)


26 Deci et al. (1999). While there are various forms of extrinsic motivation, there is always an

element of external control; we feel intrinsically motivating things are things we _want to do,_
and extrinsically motivating things are things that we _need_ to do, even if it is to get a reward
that we want and choose. When a “want to” is turned into a “need to” by adding extrinsic
motivation, it’s hard to go back to feeling that it’s something we want to do. The destructive
sense of external control is lessened when the outcome we seek (the extrinsic motivation) is
aligned with our other goals and desires. Such integrated motivations are less likely to
undermine intrinsic motivations.


27 An activity can move from relying on an extrinsic motivation to an intrinsic one over time in

stages. For example, consider a kid who plays the piano under the watchful eye of a parent.
Over time, the kid can internalize the parent’s wishes and hear their parent’s nagging voice in
their head (an _introjected motivation_ ; Ryan and Deci (2000), with thanks to Sebastian
Deterding). Later, the kid might learn to really enjoy playing the piano—making it an intrinsic
motivation.


28 Jenkins et al. (1998)


29 Gneezy et al. (2011)


30 Ariely (2009)


31 Kahneman and Tversky (1984)


32 Kolotkin et al. (2006)


33 They leverage loss aversion, the cognitive quirk in which we work much harder to retain the

things we own (or otherwise feel to already belong to us) rather than to earn something of
equivalent value.


34 See Rogers et al. (2014) for a summary of commitment devices in health, for example.


35 Millennia, really. For example, Plato saw desires coming from three parts of the soul

(Blackson 2020).


36 Understanding your users’ landscape of motivations also allows for clever techniques like

temptation bundling (Milkman et al. 2013)—in which you make something people really like,
such as reading _The_ _Hunger Games_, conditional on something people like but aren’t as keenly


motivated by, such as exercising at the gym. That doesn’t mean you can hold the things that
people love hostage to something they hate. Instead, the researchers focused on intentional,
voluntary bundling—allowing people the option to get the book and exercise at the same time.


37 In economic terms, we “discount,” or place less value on, things that are in the future. The

further in the future they are, the less we value them.


38 Goldstein (2011)


39 Hershfield et al. (2011)


40 Ariely (2009)


41 See, for example, Laibson (1997), Kirby (1997).


42 [Demaree (2011)](https://oreil.ly/YDxBG)


43 [Lieb (2013)](https://oreil.ly/eXo8c)


44 Ibid.


45 Ibid.


46 See Iyengar (2010); Schwartz (2004)


47 Iyengar and Lepper (2000)


# **Chapter 10. Crafting the** **Intervention: Ability, Timing,** **Experience**

_My wife has a Fitbit—a small exercise tracker that hooks onto her clothing,_
_displays progress on a screen, and sends over detailed information to a_
_computer or smartphone._


_The Fitbit does many things right to help encourage exercise. It automates_
_two very annoying (and therefore action-inhibiting) parts of the exercise_
_process: it automates the process of tracking how much exercise the person_
_has had, and it automates uploading that information onto a computer or_
_phone. Those are examples by shifting the burden of work from the user to_
_the product (aka “cheating”)._


_The device also uses a number of other behavioral techniques to help_
_people exercise. For example:_


_It reminds people to exercise. It gives random Chatter messages on_
_the screen; I still smile as I remember when I first saw the message_
_Walk Me; that is, it provides a (funny) cue._


_It provides immediate and meaningful feedback. Shortly after my_
_wife got it, I remember her looking at the screen and seeing she’d_
_walked something like 9,945 steps. She just started running around_
_the room, to break the 10,000-step threshold. That is, it creates_
_urgency (Timing) by establishing a near-term goal—even if it’s_
_arbitrary. Even though the benefits of exercise are long term and_
_abstract, a 10,000-step goal is immediate and real in the present._


In the previous chapter, we covered interventions to use when encouraging
an action that’s blocked by a Cue, Reaction, or Evaluation. Here, we’ll
cover the second half of CREATE: Ability, Timing, and Experience.

## **The User’s Ability to Act**


Ability is most obviously the physical means to do something: having shoes
to go running, having healthy food to eat. From the perspective of
behavioral obstacles, we can also think about it as the means to act without
further thought and without fear of failure. Every time your user stops to
think about what to do next, there is an opportunity to be distracted. Each
micro-behavior in the behavioral map can become an obstacle simply
because it requires an extra iota of thought, effort, and confidence. Your
user might really want to study a new language and was about to download
the next lesson, but during the moment it took to look up the website and
download it…the phone rang. Your user might really want to apply for a
new job, but that line about needing to present in front of others terrifies
him.


In this section, we’ll look at each of these types of Ability: the physical
ability to act for each micro-behavior, the sense of self-confidence it takes
to proceed, and the mental ability to follow through from step to step
without stopping to think and needing to concentrate on what to do next.

### **Remove Friction and Channel Factors**


Small frictions play an outsized role in behavioral science; much of the
initial work in the field looked at how simple form fields and minor hassles
blocked people from following through.


We’ve talked earlier about the importance of automation: when you can
take the burden of work from a user (e.g., manually making a 401(k)
transfer), it’s more likely to get done! Automation is often combined with a
default: the user, by default, transfers work to the product unless they opt
out. Both of these techniques, however, are powerful on their own. Let’s
look at setting defaults, separate from the issue of automation.


An early (and startling) example of this comes from the realm of organ
donations. Organ donations are an ethically important subject. We literally
have the potential to save someone’s life. There are huge variations in
participation in organ donation programs across countries, with many
countries either having 98%–99% of the population agreeing to donate their
organs upon death, while in others, only 0%–10% plan to do so. Even
neighboring countries with similar histories and cultures—like Germany
and Austria—show these variations. Germany has a 12% rate; Austria has a
99% rate.


The reason for these differences isn’t because of a deep-seated ethical or
religious understanding of organ donation. It’s likely because Austria
defaults people _into_ their organ donation program and lets them readily exit
if they choose. Germany defaults people _out_ and lets them readily enter if
they choose. It seems that what matters is the simple act of checking (or
unchecking) a box on a form. That’s the incredible power of a small friction
(merely checking or unchecking a box) and the default presented to
people.1


What can we learn from this? Obviously, set _appropriate defaults_ . But more
generally, look for ways to _remove these small frictions_ .


**Remove unnecessary decision points**


Removing the need for users to do extra work is a high-level behavior
change strategy (cheat), and it should be used within particular interactions


as well. If you don’t need to ask a question of the user, don’t. If you can
save the user from scrolling down the page, excellent. That’s just another
small but frictionful activity that the user needs to take on their path to
action. Removing these frictions can slightly decrease the cost of action, all
else constant, but most importantly, removing such frictions removes
intermediate decision points and opportunities to be distracted. If the person
has chosen to do something, let them go ahead and do it—the more times
you stop them, the more often they can be derailed.


That isn’t to say that users can’t do work. There may be really important
information below the fold, and the user really does need to read or act on
it. However, if there is a choice between accomplishing the same task with
or without additional form fields and user work, choose the route with less
work.


**Set appropriate defaults**


Even if there isn’t a big choice you can default in your product—like organ
donation—look for the small choices as well. For example, keep in mind
the individual input fields within an application. Assume that many users
will stick with whatever default value you give them. This occurs because
people are in a hurry and don’t fully read the questions posed to them,
because they are unsure of what the question means or because they simply
do not have a strongly held preference. Thus, defaults matter not only
because they create decision points (and hence distraction, etc.), they also
change outcomes for the person.


Default values can be immensely useful (a) where the default response can
move the individual closer to action, (b) where power users can fine-tune
their responses, and (c) where everyone else can breeze past the defaulted
values. However, default values should be used only where nonresponse is
acceptable; it shouldn’t use used where essential information is gathered.
And, since users will make up fake answers (or simply disengage) when
forced to answer questions that they can’t really answer, it is better to
altogether remove questions that users don’t have answers to and can’t be


defaulted. When default values are provided, the answers should be
interpreted as one-part truth and one-part nonresponse.


For example, let’s say your application asks users if they have kids. If
there’s special advice that’s only relevant for people with kids, then default
the answer to “no kids.” Let those users who do have kids, and are paying
enough attention, indicate it to receive the special content.

### **Elicit Implementation Intentions**


As you may recall, implementation intentions are specific plans that people
make on how to act in the future.2 They are a form of behavioral
automation, telling the mind to do X whenever Y happens. The person does
the work of thinking through what needs to be done _now_, and then when the
action is actually needed, there’s no need to think and no logistical barrier
to action—the person just executes the action. Implementation intentions
should include the event that triggers action, the context for that action, and
the physical things the person should do. For example: “On Friday at work,
if my supervisor yells at me about the project, I’ll leave the room and take a
short break rather than yelling back.”


You can encourage the user to create a future action plan (implementation
intentions) wherever the user is committing to take some future action,
_especially_ when that action is outside of the application. Making a specific,
concrete plan of attack can help the person follow through with the action,
even when the product isn’t there to remind them.


For behavioral products, deploying implementation intentions can mean
adding text boxes where the user describes how they’ll take the action. The
key is to make people think consciously about the concrete actions, and, if
possible, visualize undertaking those actions. The challenge is that
implementation intentions are a friction; they slow people down and make
them do additional work.3 As we talked about in the previous section, that’s
not such a good idea on its own. Rather, you can think about it like this: if
an unimpeded path (removing friction) doesn’t get people over an obstacle
on their own, you need to prepare them for that obstacle (with


implementation intentions or other such techniques) to get over it when they
reach it.

### **Peer Comparisons Can Help Here Too**


We talked about peer comparisons in the context of the person’s emotional
reaction: knowing that other people are spending less money on electricity
than you, or voting more often than you, can trigger a strong intuitive
response. In addition, peer comparisons can have an effect on our sense of
ability. I think about peer comparisons as having both a “yes you can”
(Ability) dimension, as well as the “yes you should” (Reaction) side.


If we think a task isn’t achievable, we have better things to do with our
time. On your pages, make sure not only that the person _can_ do what’s
needed but that they know they can do it, too. One way to accomplish that
is through the peer comparisons described earlier; show the user that other
people are successfully taking the action. Then they know, yes, it’s probably
something they can do as well.


Remember, however, that peer comparisons are complex. If the peer group
is too far ahead of the individual, that can be demotivating (I’ll never catch
up), and if the peer group is behind the individual, that can also be
demotivating (ach, I can just relax a bit—I’m doing better than everyone
else already).

### **The Other Side of the Wall: Knowing You’ll Succeed**


In the last week, how many times have you tried something that you were
pretty sure you would fail at? Something important, where other people
would know that you failed and likely judge you about it? I’m guessing not
many times at all. That’s because our minds prune these options from the
tree; we don’t really think through how to do improbable actions (beyond
daydreaming—here I’m talking about intentional action).


If you think you aren’t going to be able to do something, you’re less likely
to even try. The underlying research comes again from Bandura’s concept


of self-efficacy. The belief that you yourself can be effective at the task with
similar lessons comes from research on goal completion.


Helping your users know that they’ll succeed can be as complicated as an
in-depth training program and building up their expertise and confidence
for a hard action. It can also be as simple as reframing the action to make it
feel more familiar and feasible. Figure 10-1 shows one such simple
experiment I reported on with John Balz in a previous paper.4



_Figure 10-1. Simple changes in wording to help people know what they’re getting into (and whether_



_5_



_they’ll be able to complete it)_


### **Look for “Real” Obstacles**

The obstacles we’ve talked about thus far under Ability are in some sense
psychological—from a strictly rational, cost–benefit perspective, they
shouldn’t be obstacles. But people do face real obstacles of course to using
a particular product or service, like not having their password or an internet
connection to use your app. It’s always obvious in hindsight, but I’ve
certainly fallen prey to missing these obstacles myself. In one study I ran a
while back, we emailed a call to action to our users, using email addresses
they didn’t have passwords for…and sat wondering why no one responded.
So this one is a simple reminder: look at your usage data and do qualitative
research with your users to make sure you didn’t miss simple stuff while
you searched for more fancy behavioral obstacles.

## **Getting the Timing Right**


Ideally, the action is inherently time-sensitive: people need to take the
action immediately because of some existing, external rationale—like taxes


on April 15. However, when that’s not possible, there are a few other tactics
that you can use.

### **Frame Text to Avoid Temporal Myopia**


We’re wired to value the present far more than the future—that’s our
temporal myopia. We talked about that earlier, when we looked at ways to
motivate the user with immediate rather than future rewards. Well, what if
you’re stuck, and the basic structure of the application and its core
motivation are already fixed? You can still avoid the curse of temporal
myopia by crafting the descriptions you provide to the user.


When designing for behavior change, this means being very careful about
the framing of time. Look for ways to frame benefits in terms of immediate
or near-term gains; in the exercise example, reference how the person will
feel and look better _almost immediately._ The opposite is true for _pain and_
_effort_ : effort that occurs sometime in the future is much easier to commit to
than effort right now. So if the pain and effort need to be discussed at all,
put it in the future as much as possible. Benartzi and Thaler do this
beautifully with their Save More Tomorrow plan—people commit now to
saving (i.e., _pain_ ) at a future date.6

### **Remind of a Prior Commitment to Act**


We don’t like to be inconsistent with our past behavior. It’s very
uncomfortable, and we have a tendency to either act according to our prior
beliefs or change our beliefs so that they are in line with our actions.7 One
way to achieve this is to have the user impose urgency on themselves—
promise to take the action at a specific time, then come back to them and
remind them at that point. In addition to their other reasons to act, that will
spur them to follow through, to avoid feeling inconsistent.

### **Make Commitments to Friends**


Another way to create urgency to act is to make specific promises to do so
to your friends. Social accountability is a powerful force—we don’t want to


let our friends down or lose esteem in their eyes. The next sidebar illustrates
that point with a personal story from my friend Justin Thorp.


**OUR FRIENDS HOLD US ACCOUNTABLE**


I’ve always been a big guy. Back in the fall of 2009, I was clocking in
around 280 and was getting fed up with being winded when I ran up a
few flights of stairs. I knew it was time to do something different.


So I decided to get into running. That was a daunting task for me. I
could barely run down the block. Being a nerd, my first thought was…
what’s better than exercising? It’s exercising with technology. So I
perused the app store and got Runkeeper—an app that used my phone’s
GPS to track how far, how fast, and where I ran. I was instantly hooked.
It allowed me to see my progress throughout my running journey.


After a while, I noticed little Facebook and Twitter share buttons at the
bottom of the Runkeeper report. With the press of the button, I could
share my runs with my friends. I was like “what the hell” and hit the
button not really thinking much of it.


A few days passed and all of a sudden my friends and coworkers started
noticing my runs. They were commenting on my Facebook posts. They
were cheering me on via social media. When I wouldn’t run, my boss
would ask, “Justin, why didn’t you go running today?”


When I got up in the morning and didn’t want to go running, I’d hear
the voices of my friends and supporters in my head. I didn’t want to let
them down. They believed in me and believed that I could do it.


And I did. I lost 50 lbs. I ran the Cherry Blossom 10 Mile Race. I
gained a ton of confidence. And I still run regularly. It’s become a great
way for me to get exercise and clear my head.


—Justin @thorpus


Our friends have a wide range of effects on our behavior, as we’ve talked
about previously under the power of social proof and descriptive norms.


But telling our friends what we’re doing has a particular power to push us
to act when we say we will. It’s not just the action by which they judge us
but whether we kept our word overall—and that includes timing.


Of course, it all depends on who we look to for support and accountability.
If we turn to people who really don’t care about us or who don’t value the
activity we’re trying to undertake, then their disinterest can sap us of
motivation. Products can mitigate this by explicitly asking people to
identify friends and colleagues who will support them or by matching up
the person with other users who are seeking to change the same behavior or
have experience providing support (i.e., products can construct a local
network of peers who _will_ [push us to succeed). Coach.me does something](https://www.coach.me/)
akin to that.

### **Make a Reward Scarce**


You can make a reward for the action scarce (“the names of the first
hundred people losing one hundred pounds will be featured on our
website”) or artificially time-sensitive (“act in the next five minutes and
you’ll get another 10 points”). This is another favorite sales and marketing
tactic.8 It’s best for one-off actions and not repeated behavior. If you try to
repeatedly push for a behavior with scarcity people will stop believing you.
Also, you run the risk of desensitizing the person to normal scenarios that
aren’t artificially scarce or time-sensitive.


This technique has been abused in the field, however, by creating scarcity
for the benefit of the company that is disingenuous and hurts the customer.
thredUP, which we talked about in Chapter 4 on ethics, is one such
[example; hotel booking sites like Expedia, Hotels.com, and Booking.com](http://hotels.com/)
are additional negative examples that have rightly been called out by
regulators.9

## **Handling Prior Experience**


People’s prior experiences shape their reactions in ways that can be difficult
to foresee and even comprehend. Our intuitive reactions, knowledge about
the costs and benefits of an action, and our sense of self-efficacy are all
guided by the associations and information we’ve built up over time. The
previous sections on obstacles arising from Cue, Reaction, Evaluation, etc.,
all speak to common challenges that people face because of how our minds
are wired, or even because people generally have some similar experiences
in life. This one, Experience, is the wildcard. It’s a reminder that no matter
what general lessons we glean in the research community about behavioral
obstacles people face, and the tools to help overcome them, all are
dependent on the particular experiences of an individual.


For example, loss aversion is certainly powerful in general. However,
someone who was raised with the constant threat of loss may be especially
sensitive to it or may have learned to intuitively reject it. People who
actively practice Buddhism may be less responsive to most of the
techniques discussed under the Evaluation phase if they are able to release
the hold of material desires on their lives more effectively than the rest of
us.


On a more day-to-day level, people who have seen disingenuous and
manipulative ads for bad products that employ social proof (expert
testimonials and the like) may reject any appeal that uses that technique.
And finally, people may rightfully distrust anything you say if they had a
bad experience with a prior version of your product or service, which had
hyped up, inaccurate claims about its benefits.


So, what can we do when someone’s prior experience creates an obstacle to
something they would otherwise want to do? While there is less research in
this area, here are a few ideas and approaches.

### **Use Fresh Starts**


Fresh starts are special times in our lives when we feel a new opportunity to
change something about ourselves.10 Research by Hengchen Dai, Katherine
Milkman, and Jason Riis at the University of Pennsylvania about fresh


starts finds this: _people are disproportionately likely to make major life_
_commitments during times of transition._ 11 For example, these scientists
looked at how people are more likely to make commitments like exercising
more or eating better over New Year’s (New Year’s resolutions), birthdays,
and marital changes.


The behavioral logic is this: when we’ve struggled to do something in the
past, fresh starts give us a reason to hope things will be different this time
around. We mentally separate out our experiences from before the fresh
start and label them as irrelevant or outdated (“That was _last_ year!”). The
time after the fresh start has a newness free of our historical baggage that
lets us try something different or recommit ourselves to a prior goal we’ve
failed to achieve.


If there’s something your users tried to do in the past but struggled with,
like exercising regularly, then these special fresh start moments can help
them reset the clock, to have renewed vigor and a sense of hope that they
otherwise would not have, given their prior experience. New Year’s
resolutions are the stereotypical example, but these fresh starts can center
on other events as well—moving house or changing job, for example. Many
religious traditions have “fresh start” periods as well, such as Lent; websites
[like FaithGateway send out emails and change their web design during Lent](https://oreil.ly/-aI22)
to highlight the special time for users to recommit to and re-invigorate their
spiritual path.


A Fresh Start can make the action and context feel special and allows
people to put their past experiences in a separate historical category that
doesn’t doom them to repeating those mistakes again: _the future can be_
_different, if you make it so._

### **Use Story Editing**


In “Reaction” we talked about Tim Wilson’s research on the self-narrative:
the story we tell ourselves about who we are, based on our past experiences
and our understanding of our future path. There, we focused on bringing
together related past experiences—especially successes—to make a new


action feel more familiar and natural. Wilson also discusses a related
technique: story editing (helping people “edit” their self-narrative to
reinterpret negative past experiences).


One of the best studies I’ve ever seen on behavior change was one Wilson’s
on story editing. He and his coauthor, Gilbert, took a group of first-year
college students who were struggling—they weren’t doing well in school
and were worried about their future—and randomly assigned the students
into one of two groups: one group received a short, 30-minute intervention;
the other received nothing special.12


Wilson was concerned that the students saw themselves as failures. His
intervention entailed giving the students information about potential
_interpretations_ of their bad performance in school:


_We gave them some facts and some testimonials from other students that_
_suggested that their problems might have a different cause…namely, that_
_it’s hard to learn the ropes in college at first, but that people do better as_
_the college years go on, when they learn to adjust and to study differently_
_than they did in high school…13_


The randomly selected group that reinterpreted their bad grades got better
grades in the future. They got better grades _all the way to their final year in_
_college_ ; they also were less likely to drop out of college. While the study
did not track their full academic performance over time, we can posit that
the effects were not immediate. Rather, it appears that students would have
slowly changed how they saw themselves and gradually changed the
amount of effort they put into their studying after this initial push.


A 30-minute intervention that changed performance for years? Impressive.


Wilson is a leading proponent of the idea of story editing more broadly; like
the students in his experiment, we can reinterpret what’s happened to us in
the past by changing the story we tell ourselves about it—our selfnarratives.14 That reinterpretation then affects our future behavior. When
we change our behavior, we also change the experiences we’ll have in the
future, making them marginally more likely to support our self-narratives.


And with each new experience, our internal story of who we are changes a
bit more, spurring a new cycle of behavior change.


For the students, it would have worked like this: Wilson helped half of them
interpret their performance differently. Those who saw themselves as going
through a temporary tough spot (and not as failures) would be slightly more
likely to work harder and perform better on the next test. They would then
look back at that (improved) performance and reinforce their understanding
of themselves as students who _could_ study and could overcome the
challenges of first-year life. They would then work even harder on the next
test, perform better, and so forth. With time, the internal stories, or selfnarratives, of the two groups diverged, thanks to a small push from the
initial intervention.


We interpret and reinterpret our experiences every day of our lives and thus
shape our self-narratives and our future behavior. These cycles of
interpretation and behavior can clearly support beneficial changes, like
studying more. They can also lead to negative ones, like when someone
feels like a failure and doesn’t put in effort to try to change that. It depends
on how we use our past experiences and whether we see ourselves in
control of the outcomes of our lives.

### **Use Techniques to Support Better Decisions**


If a person has a strongly negative emotional reaction to an action, based on
their prior experience, or similarly obsesses about a single facet of an
action’s costs, it may help to treat it as a decision-making problem, rather
than a problem of action. We covered this body of literature in Chapter 3 in
the context of helping people make more careful conscious decisions.15
Here are some of the key points:


Slow thinking allows for more careful thinking.


Add friction to slow people down by adding cognitive overhead
and adding the number of steps required for action.


Direct attention to important but ignored facets of the issue.


### **Make It Intentionally Unfamiliar**

While I haven’t seen a research study specifically test this idea in the field,
another technique comes to mind that is inspired by existing work. If prior
experience with a familiar (same or similar looking) product or
communication causes a negative reaction that blocks action, you could
intentionally change the look and feel to no longer trigger that reaction.
This is appropriate only when someone faces a reaction they themselves
would want not to have—i.e., in calmer moments, that they would want to
take the action.


It’s a technique that has clearly been used by many an unscrupulous
company as well. When my wife and I were on a vacation in the Caribbean,
we came across a travel service that looked wonderful. It offered great
discounts on vacations in the future, at what seemed like a reasonable (but
not unbelievably low) price. I checked out the company online, and
everything looked OK. Only a few weeks later did we find out that the
company had repeatedly changed names—whenever bad reviews and
lawsuits caught up with it, it simply changed names and marketing
campaigns. Same company, same (bad) service, but new skin. They kept
bringing in customers by making their brand intentionally unfamiliar.
You’ve probably come across companies on Amazon that have done the
same—they change the name of their product or of their company—to
avoid people’s prior bad experiences with them and their negative reviews.


Thankfully, we can envision more beneficial uses as well. Think of
someone who has struggled with weight loss in the past and doesn’t think
they’ll ever succeed. Intentionally creating a service that looks and feels
different than a standard offering in the market (that didn’t work out for
them), like a meal-delivery service or a meal planner, could help them give
it another try. Even though the service itself is the same, the environment
around the individual may have changed, and they could be successful now
—if only they could get past their prior negative experiences. Which raises
the final point for this section—remember that people change.


### **Check In Again: You’re Not Interacting with the Same** **Person**

Not only are people’s experiences different from one person to the next, but
every day, your users are changing and adapting—in both universal ways
(aging) and idiosyncratic ways (getting married, having children, etc.). The
person you emailed six months ago is different from the person you’re
communicating with now. Through your user research, you can _check back_
_in with them_ and gain insight into how your user base is changing over time.
If the company has had a retirement workshop in the time since the last
retirement communication, build on that, especially if you can segment the
communication to target those who attended.

## **Putting It into Practice**


In this chapter, we walked through interventions you can use for the second
set of behavioral obstacles in CREATE: Ability, Timing, and Experience.
Let’s take a look at the crib notes.


Here’s what you need to do:


Ideally, once a user has made the decision to act, they can flow
from one micro-behavior to another on the path to the final action.
Unfortunately, large and small Ability barriers get in their way, in
which they are lacking physical resources (having a password),
lacking a sense of self-confidence, or needing extra time and
thought to proceed.


To remove physical barriers, the solution is usually pretty obvious:
if we’re careful to watch for each micro-behavior along the path
and notice them. To remove barriers of self-confidence, we look to
peer comparisons, and removing uncertainty about what’s ahead.
To remove frictionful pauses (decision points) we use defaults and
simplify interactions.


People are naturally focused on immediate tasks and needs—so
activities that benefit us in the long term are easily lost. To counter
that, we reframe how we talk about the benefits, create current
scarcity, or focus people’s attention on action now through
personal and social commitments.


Negative prior experiences can cause them to lose sight of the
broader benefits of an action, and each person’s experiences are
idiosyncratic. To help people move past those negative
experiences, we can use the concept of fresh starts (birthdays,
major life events, and such) to reset the clock, story editing to
reimagine what those experiences portend for the future. We can
also avoid intuitive associations and invoke deliberative System 2
thinking by _adding_ friction and slowing the person down. Or, we
could simply avoid those prior experiences by making the action
look and feel like something unfamiliar.


How you’ll know there’s trouble:


When the product is simply hard to use—behavioral techniques
can help smooth minor frictions and challenges; it can’t fix a
broken product.


When we’re using behavioral techniques to cover for prior failings
of the product: we’re trying to avoid prior bad experiences people
have had with our own products and convince them they should
spend more money on it, etc., when it hasn’t really improved.


Deliverables:


One or more interventions to try with your users to see if it helps
them take action and overcome their obstacles.

### **Exercise**


You’ll continue to use “Worksheet: Evaluating Multiple Interventions with
CREATE” for obstacles related to Ability, Timing, and Experience. In


addition, the table of suggested interventions to support action is
reproduced in the workbook for your ease of use.


1 Johnson and Goldstein (2003). Technically speaking, this analysis shows the marginal impact

of a default, given automation that is already in place—since no one can remove their own
organs after death, with or without a default. But the point is the same: defaults can be
logically separated from automation and have powerful marginal effects.


2 Gollwitzer (1999)


3 Thanks to Paul Adams for the tip.


4 Balz and Wendel (2014)


5 Wendel and Balz (2014)


6 [Benartzi and Thaler (2004)](https://doi.org/10.1086/380085)


7 See Festinger (1957)


8 Cialdini (2008); Alba (2011)


9 [See Monaghan (2019) for a story on how the UK’s Competition and Markets Authority has](https://oreil.ly/BoQwW)

clamped down on these techniques. Once more, I am indebted to Paul Adams for the tip!


10 This section draws from Wendel (2019).


11 [Dai et al. (2014)](http://dx.doi.org/10.1287/mnsc.2014.1901)


12 We discussed this study briefly in Chapter 1, as an introduction to the idea of _self-concepts_ or

_self-narratives_ .


13 [Gilbert and Wilson (2011)](https://oreil.ly/LVulI)


14 Wilson (2011)


15 See Soll et al. (2015) in particular.


# **Chapter 11. Crafting the** **Intervention: Advanced Topics**

_New Moms is a small nonprofit in Chicago serving young mothers at risk of_
_homelessness with a range of programs—from low-income housing to_
_doulas and parent education. Their job training program, however, faced_
_many challenges: mothers were interested, but few people actually made it_
_into the program. In marketing terms, their conversion funnel faced steep_
_drop-offs at each stage of the process._


_Unlike most small nonprofits, however, New Moms has long studied_
_behavioral and brain science. “We’re big fans of ideas42 here,”1 says CEO_
_Laura Zumdahl. Under the direction of Dana Emanuel, their Director of_
_Learning and Innovation, they partnered with the behavioral science team_
_at MDRC to identify obstacles facing young mothers in the program. And,_
_as is often the case with any program or product, there were many. Here’s_
_what they found:_


_Their marketing materials talked about the long-term benefits of_
_the job training program, in technical terms (who doesn’t get_
_excited about “job skills”?). In their behavioral analysis, they_
_realized that the young mothers were strongly present biased and_


_rightfully focused on near-term goals like feeding their kids. So the_
_team changed the materials to “message to the mothers’_
_motivations,” as Dana described it. In other words, money for_
_their family and a flexible schedule. It’s a lesson that many “good_
_for you in the long run” products would benefit from learning_
_too…_


_In order to sign up for the program, the mothers had to fill out_
_multiple pages of forms and meet multiple requirements. Most of it_
_was simply unnecessary, they realized, and created unnecessary_
_barriers to entry (i.e., hassle factors). So they simplified the sign-_
_up process considerably._


_Once new mothers were in the program, the organization asked_
_them to set quarterly to six-month to one-year goals. Many of the_
_mothers had never worked, and long-term job goals were simply_
_abstract ideas. Those goals didn’t help them, and they got_
_discouraged. So New Moms worked with them to set a series of_
_more immediate and manageable one-week and daily goals, which_
_laddered up to a bigger transformation. These small wins helped_
_the mothers see their progress and keep them on track over time._


_From small nonprofits to international technology companies, the problems_
_our users face are remarkably similar because they arise from how our_
_minds are wired and how we develop products and services without_
_understanding that mental machinery. And, as with many products and_
_services, New Moms found that there wasn’t a single barrier, but rather_
_many that mothers faced over a multi-step process. Their thoughtful_
_analysis uncovered what obstacles were at work in each case and how to_
_overcome them to better serve their users._


The behavioral solutions we discussed in Chapters 9 and 10 are about pointin-time interventions to support action: ways to facilitate action at a
particular point in a behavioral map. In this chapter, we look at three
extensions: working with multi-step interventions over time, building
habits, and crafting interventions to hinder negative action.


## **Multi-Step Interventions**

For some products—and many communications—the behavioral map is
straightforward and simple, or there is a single point of failure that needs
attention. Here we take a step back and look at cases where the process is
more complex and you need to address the behavioral map’s series of
micro-behaviors as a whole to make the process more feasible for users
overall. In particular, we’ll look at how to simplify the map, how to make it
easier, how to provide feedback along the way, and how to build habits.

### **Combine Where Possible**


Each step in the sequence should represent the _largest_ possible chunk of the
work that is still understandable and feasible. Look for ways to combine
multiple steps into one. _Largest?_ Yes. There is a tension between breaking
the action into steps to make each one more manageable and having so
many steps that it overwhelms the user. There’s no hard-and-fast rule, but
keep this in mind especially when you see any sequence that’s more than a
dozen individual steps!

### **Again, Cheat If You Can**


See how to shift the burden of work at each step from the user to the
product—that is, use the “cheating” strategy within each of the individual
steps the user has to take. Look over the behavioral map. Is it possible to
automate away the whole action? If not the whole action, is it possible to
cheat at any of the individual steps along the way?


With the radio program from Chapter 7 (in which Obama’s campaign
sought to encourage people to call into a radio program to voice their
support), complete automation wasn’t feasible. But certain parts of it could
easily be automated or defaulted. For example, the platform could:


Automatically match the user up with a call-in radio program and
provide the necessary phone number to call, saving the user the
need to research relevant radio shows.


Make finding a radio unnecessary (incidental to using the
software), by streaming the call-in program through the app itself.


Provide intelligent defaults for what to say while on the air (e.g., a
simple script that the user can edit and personalize as needed).


By simplifying the process, automating, defaulting, or making steps
incidental, you remove unnecessary work for the user. In terms of the
CREATE Action Funnel from Chapter 2, that means decreasing the costs of
action (part of the mind’s conscious evaluation) and increasing the basic
physical ability to take action. This simplification process allows you to
focus attention on more intractable behaviors or more exciting (to the user)
parts of the application. Another way to accomplish this is to build habits
over time—something we’ll return to shortly.

### **Provide “Small Wins”**


In addition to being _easy_, each step should be _meaningful_ enough that the
user can feel a sense of accomplishment afterward. It’s up to the product to
help users feel that accomplishment (often by presenting it as progress
toward the target action), but the step itself needs to support it. In the
research literature, this is called “small wins”—if, after each small step,
people feel they’ve done something and they’re closer to finishing their
goal, they are then more likely to continue.


For example, in my prior work at HelloWallet, we had a tricky problem
when we designed our guidance—how much should you encourage people
to commit to save each month? Authors such as Jean Chatzky tell their
readers to save about $10 a day.2 That is simple and clean, but either way
too easy or too hard for many users. We have users who struggle to put
aside $10 each week, let alone each day; we also have users to whom $10 is
a rounding error, and a laughable goal. So, we constructed a meaningful
step on the path to greater savings that provided small wins, regardless of
their financial means—we calculated the target amount as a percentage of
income (and then rounded to the nearest clean, simple number that people
would remember).


For an action to provide a small win, it needs another characteristic—it
must be clear to the user that the step has actually been completed. In other
words, there must be a clear definition of success or failure and feedback
about whether that has occurred. Weight loss applications are a great
example—they set a specific, unambiguous weight target, and encourage
people to change their weight. An example of an unclear target would be a
step that tells users to cut down on smoking. It doesn’t allow users to know
if they are succeeding; if users have to wonder whether they’ve done it right
or not, they are distracted, and you lose them.

### **Generate a Feedback Loop**


Multi-step, and especially quickly repeated, actions provide another
opportunity for behavior change: by enabling users to adjust course over
time, to better meet their goals.


The current crop of wearable computing products, like the Apple Watch,
Fitbit Versa, and BodyMedia CORE, are built to provide feedback to users
about their exercise and sleep habits. For example, my wife’s Fitbit
provides constant feedback on how much exercise she’s gotten. When she
makes an adjustment in her routine, it’s quickly reflected in the tracker, and
she can see how she’s doing. That feedback loop allows her to adjust her
behavior throughout the day to meet her goals.3


For feedback to be effective at actually helping people change their
behavior, it should be:


_Timely_


Ideally, the feedback should occur while the action is being undertaken

so the user can make live adjustments and see the impact.


_Clear_


The user must understand what the information means.


_Actionable_


The user must know how to act on the information.


In addition, and this may seem obvious, the user must _care_ enough about
the feedback to change behavior. Being intrigued and entertained by
feedback is not enough. The user must want to, and be able to make the
adjustments necessary to, improve performance. The user must also be
paying attention. In this combination of motivation, attention, and the
ability to act, we find many of the same issues we’ve already discussed
about designing for behavior change.

### **Common Mistakes**


Here are two of the common mistakes I’ve seen at this stage.


**It is easy!**


The first common mistake is to be satisfied when it’s easy for _you_ to do.
Too often, especially in my prior political advocacy work, I’ve seen
campaigns that expected people to come to a night-long vigil, write a letter
to their representatives from scratch about an issue the author knew little
about, or organize a local group of activists on their own. These are each
daunting, complex tasks to someone who has never done them before—
though relatively straightforward to those who have already built up the
expertise.


It’s quite difficult to step outside of your own experience (if only because
once you think of the action, your System 1 immediately activates the
relevant prior experiences, and it really does _feel_ easy on an intuitive level).
If there’s any doubt, though, run the proposal by someone who has never
taken the action before.


**Hard work builds commitment**


Another common mistake is to believe that work makes commitment and to
allow the user’s tasks to be difficult _on purpose_ . This view is half-right,
half-wrong. Effort can build commitment to a product and can build a


commitment to continue what you’ve started. People who complete difficult
tasks (successfully and without undue grief) are more committed to
continuing further. In psychology and economics, there’s the well-known
mental blip called the _sunk cost effect_ : the more work you put into
something, the less willing you are to let go of it—even when it is not in
your economic interest.


If users see the target action as a difficult, substantial task—great. _After_ the
action is completed, they will be committed. The product’s job is to get as
many people as possible across the finish line. The “make ’em work hard”
approach leads to very committed people who finish—but those committed
people are only a small subset of the people who could have completed the
task; that creates the illusion of effectiveness—because everyone else has
already been filtered out!


So building commitment doesn’t mean that each step needs to be a pain in
the butt or that we should _design_ an application to be difficult. For any
“hard” behavior (exercising, learning a language, etc.), there will be things
that the product can make easier and things that it can’t. Make the things
that can be made easier easy—and then build up the excitement on the
remaining tasks that are hard. Provide users with a sense of accomplishment
for the tasks that are truly difficult—and not just badly designed.4

## **Creating Habits**


Chapter 1 described the two basic types of habits: habits created out of
simple repetition (cue-routine, cue-routine, etc.), and habits that have the
added feature of a reward at the end (cue-routine-reward) that drives the
person to repeat the behavior. Your product’s users could form habits by
simple repetition, but then the burden of work and willpower is all on their
side. When designing for behavior change, add a reward at the end to help
bring people back while the habit is forming.


Either way, though, habits form when the mind takes a repeated action and
automates it. In each early iteration, all of the CREATE factors are
important; it builds on conscious action, and we need to keep in mind all of


the behavior obstacles that can arise. In time, however, as the behavior
becomes automated, the Cue, Reaction (the Routine), and Ability (to
actually take the action) are the most important.


Repetition isn’t the only aspect that’s important, however. To build habits
with a product, here is a straightforward recipe:


1. Identify an action that should be repeated dozens of times, without

significant variation or thought each time. This is commonly
known as a _routine_ in the habit literature. For example, maybe your
behavioral map includes “run each morning for 30 minutes.” That
is a candidate for a habit.


2. Make sure there is a strong and immediate benefit, especially that

triggers a strong and positive intuitive Reaction or conscious
Evaluation. This is known as the “reward” in the habit literature.
An example is receiving congratulations from the app or from a
friend.


3. Identify a clear, unambiguous, and single-purpose cue in a person’s

daily life or in the product itself (an email, an alert, etc.). An
example is a notification from the product at the right time of day
that it’s time to run.


4. Make sure the user knows about the cue, routine, and especially,

the reward.5


5. Make sure the user wants to and can undertake the routine using

the rest of the CREATE framework.


6. Deploy the cue.


7. Track whether the routine occurs.


8. Have the product _immediately_ reward the user once the routine has

occurred. That allows dopamine in the brain to reinforce neurons
associated with the cue and routine before the memory fades.


9. Repeat steps 6–8, tracking completion times and rates and adapting

the process until it’s right.


There’s a lot of nuance there, of course.


First, the _cue_ really needs to be single-purpose and unambiguous (i.e., after
the habit is formed, the cue is linked to the specific routine and nothing
else), because you want to avoid the mind having to think about what to do
when the cue occurs. Fogg and Hreha (2010) argue that the triggers (i.e.,
cues) can be:


Directly tied to another event (e.g., looking at the bathroom mirror
first thing in the morning is connected to picking up your
toothbrush)


At a specific time of day every day or every week


The trigger/cue can be internal (boredom or hunger) or external (seeing the
clock first thing in the morning or getting an angry email). Internal triggers
are great, since they are inherent in the human condition; however, lots of
other things in one’s life compete for the same triggers (which makes them
not single-purpose and thus ambiguous). External triggers can be just as
effective, if wisely constructed.


Second, while the _routine_ must be structured so that it can occur effectively
without thought. It need not be “stupid” or “simple.” Good driving, for most
people, is a (complex, impressive) habit. Remember how hard it was to
learn to drive? Remember all of the thought that was required just to start
the car and get it going? Yet, after learning, we avoid getting too close to
other cars while on the road, we coordinate what our eyes see with what our
hands do to steer, and so on. The reason is that driving uses a set of
hierarchical habits—large, complex habits built out of thousands of small,
routinized behaviors that are cued from the environment and linked to one
another in succession. Each piece is structured so that it can be consistently
executed after the cue without conscious thought.


**KEEPING HABITS OVER TIME**


Habits are tremendously powerful once formed, but they can also be
fragile. They depend on having a stable cue, in a stable context to
trigger. For an app on a phone, that cue might be the sight of the app on
the home screen or a push notification. If that cue is lost, like when the
person changes phones and hasn’t installed the app, the habit no longer
triggers.


I use a popular and free app called YouVersion to read the Bible on my
phone. YouVersion knows that their users might get a new phone
around the Christmas holidays, so they send out an email reminding
people to install the app on their new phone—and thus support their
habits of spiritual reading. Figure 11-1 shows the email I received at the
end of December last year.


_Figure 11-1. An email I received to reinstall the YouVersion app on my new phone—a smart way_

_to ensure that once a habit is formed, the Cue isn’t disrupted_


Routines that can be made into a habit often will have a strong and clear
feedback loop (i.e., after the action is taken, the reward is immediate and
unambiguously tied to the success). Habit formation is not a conscious
event, though we can consciously put ourselves in situations where we’ll
learn them.


Third, the _reward_ need not be offered every time, as long as it is still clearly
tied to the routine. Random rewards are quite powerful in some
circumstances. In the operant conditioning literature, habits with random
reinforcement take the longest to _form_ but also take the longest time to
_extinguish_ once the reward is no longer given. Gambling provides the
ultimate random reward—and once you have the bug, it’s difficult as all
heck to get rid of. One reason that random reinforcement is so powerful is


that our brains don’t really believe in randomness. We look for patterns
everywhere. So part of the desire driving a random reward is our brains
trying to find a pattern (ever talk to a gambler who has “a system”?).6


Finally, a key part of using products to build habits is experimentation and
fine-tuning. Your product is probably going to get it wrong the first time—
the cue won’t be clear or won’t grab the user’s attention, the user may stop
caring about the reward, or the context for the routine might change and
conscious thought is required.7


The cue-routine-reward process used for _forming_ habits is depicted in
Figure 11-2 (remember the reward is optional, but useful). For example,
seeing the scale in the morning triggers the exercise routine. The immediate
reward is a pleasant muscle burn.Charles Duhigg popularized the process in
the _Power of Habit_ (Random House, 2012), building on an old tradition in
applied behavioral analysis.8


_Figure 11-2. The cue-routine-reward process described by Duhigg (2012)_

## **Hindering Action**


Believe it or not, we’ve already covered most of the information we need to
hinder action, back in Chapters 3 and 7. That’s because hindering an action
is far simpler, conceptually, than enabling it. In our diagnosis, we identified
how CREATE supports the negative behavior: what is the current cue?
What causes the person to have a positive Reaction and Evaluation? What
makes the person Able to act immediately and prioritize it as Timely over
other things? And in Chapter 3, we looked at specific ways to hinder habits.


In short, we can add an obstacle at any relevant point in the CREATE
funnel. We start by asking the question (as we did in the initial diagnosis, in
Chapter 7): is the behavioral habitual? If it is habitual, then we can focus on
the Cue, Reaction, and Ability (C-R-A). If it isn’t, then we use the full
CREATE. The practice of _creating_ obstacles is less researched in behavioral
science than the practice of removing them, but often we can find simple
solutions that are the opposite of what we’ve covered already.

### **Habitual Actions**


While stopping a negative behavior in general isn’t well researched,
stopping habits is. When we first took a look at negative actions in
Chapter 3, we discussed many of the core interventions one can use to
shape them. Here’s a reminder:


1. Cue: Avoid the cue. Since habits are automated, learned behavior

triggered by a cue, the most straightforward simplest way to stop
them is to avoid the cue—hide it (like a phone), avoid places where
one would see (like avoiding bars for drinkers).


2. Reaction: Replace the routine by hijacking the reaction. Old habits

don’t go away, but another routine can be triggered faster. For
example, when boredom in line strikes, load up Duolingo instead
of Twitter.


3. Ability: crowd out the old habit with new behaviors. While one can

directly attack the routine, the time and ability to act on it can be
crowded out indirectly by filling that time with other activities.
And, one obviously can’t smoke if they don’t have (e-)cigarettes—
but that isn’t designing for behavior change; that is (probably
warranted and useful) coercion.


4. In addition, while habits run off of Cue, Reaction, and Ability,

there’s been success with a conscious approach.


5. Evaluation: Cleverly use consciousness to interfere, including

using mindfulness to avoid acting on the cue. While it’s frustrating


and tiring to consciously override habits, mindfulness practice has
been shown to teach people how to notice, but let pass, the urge to
respond to the cue.

### **Ideas for Hindering Other Actions**


Table 11-1 shows our list of techniques to enable action from Chapters 9
and 10, reenvisioned to _hinder_ action, after removing some items that aren’t
relevant in this context.


_Table 11-1. Techniques to hinder action_


**Component** **To Start** **To Stop**



**Cue** Relabel
something as a
cue



Unlink the action from other behaviors that flow into it



Use reminders Remove reminders



Make it clear
where to act



Make the cue more difficult to see or notice







Align with
people’s time



Move the cue to a time the person is busy, or make the person
busy at the existing time







Associate with
the positive



Associate with action with negative things the person doesn’t
like







Use peer
comparisons



Use negative peer comparisons (show that most other people
resist it, don’t do it)





Make it
professional
and beautiful


Leverage
existing
motivations


Leverage loss
aversion



Make the appeal to stop professional and beautiful, _or_ make
the context of taking the negative action ugly or
unprofessional





Unlink the action from existing motivations





Leverage loss aversion


**Component** **To Start** **To Stop**







Pull future
motivations
into the present



Pull future motivations to stop into the present







Avoid
cognitive
overhead



Add to cognitive overhead







**Ability** Remove
unnecessary
decision points



Add small pauses and frictions







Elicit
implementation
intentions



Elicit implementation intentions (on how to avoid temping
situations)







Help them
know they’ll
succeed



Help them know they’ll succeed (same!)







**Timing** Frame text to
avoid temporal
myopia



Frame text to avoid temporal myopia (same—for benefits of
stopping)






**Component** **To Start** **To Stop**



Make
commitments
to friends



Make commitments to friends (same, to stop)



Experience Use fresh starts Use fresh Starts



Use story
editing



Use story editing







Since stopping a behavior usually means stopping a repeated behavior (why
try to stop a behavior in the past that won’t recur?), feedback loops are
especially important. As we discussed in “Multi-Step Interventions”, we
want feedback loops to be Timely (feedback is given as quickly as possible
after the negative action), Clear (it’s unambiguous that the person is off the
mark), and Actionable (they can do something about it, right then, and
know how to).


Sadly, there are many examples of companies and governments seeking to
stop behaviors against the person’s wishes or explicitly to harm them.
_Nudge_ coauthor Richard Thaler refers to the misuse of nudges for ill as
“sludge”: applying _friction_ with _ill intent_ .9 From decreasing voter
participating by de-registering people to offering rebates on products and
then making it difficult to receive them (requiring that someone complete
an onerous rebate process), they aren’t hard to find. Many of the techniques
listed here can (and indeed are) used in sludge settings; whether a
behavioral technique is positive or not depends on the person and their
desires, more than the technique itself. As Thaler notes “the goal…is to
help people make better choices ‘as judged by themselves.’”10 Thus, when
seeking to stop a behavior, the same ethical rules apply as for any other
behavioral technique, as we looked at Chapter 4: are you being transparent?
Is it voluntary? Is it something the person has asked for or wants?



9



10


## **Putting It into Practice**


In this chapter, we covered three different advanced issues in crafting
behavioral interventions: working with multi-step actions, building habits,
and hindering unwanted actions. Let’s look at the lessons for each in turn.


For stopping action, here’s what you need to do:


For habitual actions, avoid the cue, replace the routine by hijacking
the reaction, crowd out the old habit with new behaviors. See
Chapter 3 for more information.


For non-habitual actions, look to create friction, decrease benefits,
or remove attention: that is, to use CREATE in reverse.


How you’ll know there’s trouble:


When you’re seeking to hinder an action that people want to take


When you don’t know if the action is habitual or not


Deliverables:


A set of interventions to hinder negative behavior


And for multi-stage actions, here’s what you need to do:


Break the target action into discrete steps that the user needs to
complete. These pieces should be:


Simple and straightforward (easy to understand)


Easy to complete (both appearing easy to the user and
being easy in practice to execute)


“Small” (so that the user sees clear progress after each
step)


Meaningful enough to reward after completion


Straightforward to see when they are complete (so they
the user will clearly know if the action was successful or
not, immediately after making an attempt)


How you’ll know there’s trouble:


When team members can’t clearly and simply convey what the
user is supposed to do


When no one outside the company has been asked how difficult the
action is


Deliverables:


An updated behavioral map, with simplified, more feasible microbehaviors

### **Exercises**


You’ll continue to use “Worksheet: Evaluating Multiple Interventions with
CREATE” for hindering action. In that case, however, you’re looking to
_add_ obstacles. In addition, the table of suggested interventions is
reproduced in the workbook for your ease of use.


1 ideas42 is a large nonprofit behavioral science organization, based in New York City.


2 Chatzky (2009)


3 [The quantified-self movement has brought rightful attention to feedback loops and their](http://quantifiedself.com/)

power to both inform and change behavior.


4 When automation of the whole process is possible—something I strongly recommend—then

commitment to the action is a real issue. For example, people who are automatically enrolled
in a 401(k) without their real commitment are likely to cash out the money and use it for
something else. But if your product isn’t doing automation and you can still make _everything_
that the user needs to do easy, that’s a nice, high-class problem to have.


5 In studies of classical conditioning with animals, you actually don’t need to link the cue,

routine, and reward beforehand. You can build a habit around simple trial and error. However,
with us humans, and especially with _voluntary_ behavior change, you can skip the trial-anderror part and tell people what’s going on.


6 But where we expect a strong pattern, and don’t get it, we’re angry. Would you be happy if

you went to Starbucks for your morning coffee and some days the coffee was terrible and other
days it was great? That would be random reinforcement.


7 There’s much more that one could say about designing habits, but my goal is not to

exhaustively cover them here. Numerous books have been written about forming and breaking


habits in different contexts; Duhigg (2012), Dean (2013), and Eyal (2014) are three good
places to start. In addition, BJ Fogg has developed a hands-on approach to creating habits in
[your own life; see Tiny Habits and Fogg (2020). For now, though, my goal is to give enough of](http://tinyhabits.com/)
a foundation that a product team can make a solid product plan and then learn what really
works for them in their particular context.


8 This cue-routine-reward is a clearer presentation of the antecedent-behavior-consequent

(ABC) model used in rational emotive behavior therapy and applied behavioral analysis. See
Miltenberger (2011) for one application of the ABC model.


9 See, for example, Thaler (2018): “Nudge, not Sludge.”


10 Ibid.


# **Chapter 12. Implementing** **Within the Product**

_Safaricom is the largest telecommunications provider in Kenya, with a_
_diverse range of products—from phone service to mobile money to music_
_streaming. They hired the Busara Center, a behavioral economics_
_consultancy based in Nairobi, Kenya, and with projects across the_
_developing world, to help them explore a new education insurance product._
_The product would help students and their families prepare for school costs_
_—both by saving for it and by ensuring that school fees would be paid even_
_if disaster struck, such as the death of the parent. After talking with_
_Safaricom and conducting qualitative research in the field, they identified_
_the key obstacles and developed a suite of potential interventions._


_Often behavioral teams may have multiple interventions they want to test_
_and aren’t sure if any will be effective and profitable enough to warrant a_
_full-scale rollout. Busara handled this problem by iteratively developing the_
_product over time, starting with a series of low-cost tests in their lab using_
_members of the target audience. They “built” the product first as a set of_
_wireframes and product marketing materials and tested the audience’s_
_willingness to use them. In this low-cost format, they could test multiple_


_interventions: how the product was framed, how often people contributed,_
_how much they contributed, and whether other features were offered. From_
_day one, they built metrics of success into the process to ensure they_
_received accurate data to drive future iterations._


_They then built a “dummy product” that offered key features of the_
_education savings product, but did so in a domain where it’s easier to get_
_immediate feedback: insurance against extra education costs due to rain (a_
_frequent problem in Nairobi). They deployed the simple, but real, product in_
_the field and had impressive interest and take-up, allowing them to more_
_accurately calculate the true interest and impact of the full product. With_
_these results in hand, they have begun to iterate on a minimal viable_
_product that can address the user’s core needs and drive uptake._


Designing for behavior change doesn’t require or benefit from a
fundamentally new process to implementing your intervention in the
product. The action, as it were, is all in preparing the behavioral maps and
diagnosis, in designing the intervention, and after it is built, in measuring
the real impact on people’s behavior and outcomes. Many companies use an
iterative product development process, as Busara did in this example, to derisk the process and assess real market interest. That iterative process
allows teams to assess the impact of different interventions along the way as
well, which is quite valuable. It is not essential, though. Others use a
waterfall process, in which case the product, and its behavioral
interventions, are all implemented and rolled out in the field in one big
bang.


Regardless of the process used to implement the product itself, there are a
few pointers along the way that can help the behavioral aspects of the
project. In particular, it’s important at this stage to double-check that your
incentives and intervention plan are ethically sound, plan to track user
behavior and results from the outset, and ensure that thoughtful planning
doesn’t get in the way of creative solutions. Let’s look at each of those in
turn.


## **Run the Ethical Review**

Once you’ve determined your intervention(s), the final step before building
it and deploying it with real users should be an ethical review. While you
should consider ethics from the beginning—asking how a particular
behavioral design will benefit the user, and whether they _want_ that help—
it’s only when the intervention has been selected that the full ramifications
become clear. In other words, yes, be ethical throughout, but make sure
there’s also a final review.


The process of the review matters as much as the guidelines themselves. As
we discussed in Chapter 4, we all have the temptation and the tendency to
blur the lines under the right circumstances. So we should apply behavioral
science to our own decision-making environment to make it harder to do so.
That starts with ensuring our own incentives are clear and aligned with the
user’s benefit, that we have an independent review body checking our
plans, and that the guidelines, whatever they are, are clear and difficult to
misinterpret. For more on the theory, check Chapter 4. For a practical
worksheet to help with the process, see “Putting It into Practice”.

## **Leave Space for the Creative Process**


The behavioral interventions we developed over the past few chapters are
fundamentally _functional_ specifications; that is, they are ideas or
approaches to solving a user’s behavioral obstacle. They may come with
associated tips on how those ideas might be implemented in practice, but
behavioral science just doesn’t offer mockups or graphic design. It doesn’t
offer over the best page layout or information architecture. And it certainly
doesn’t offer the right programming language, the right software
engineering pattern, or deployment architecture.


I’ve seen behavioral designers, myself included at times, try to weigh in on
these issues, to take expertise in one area and try to port it over into another.
There’s a natural tendency to over-specify behavioral interventions, to try to
dictate how the product should look and operate, in addition to what it


should do. In reality, most of the behavioral research to date hasn’t
validated a specific look and feel—and it certainly hasn’t validated a
specific look and feel that translates and is effective across diverse contexts
and user experiences. Instead, our research tests underlying concepts that
inform those designs; it helps us inform the design process (UX, UI,
graphic design, etc.), but it isn’t the same thing as that process.


Part of the challenge is that there’s an inherent tension between structured
analyses of behavioral obstacles and creative design. Thus far, we’ve used a
rather planning-heavy process—thinking through what the user should do to
accomplish the goal, what the context of action is, and how to shape that
context. It’s just too tempting to think that the _things we want_ users to do,
and the _way we want_ them to behave, is how they’ll _actually_ behave, when,
clearly, there’s a lot more required.


Users have to want to change their behavior. When there’s a product
helping them change, that means they have to want to use the product. The
product must not turn them away; no product can be effective at changing
behavior if people never use it. The desire to change won’t pull most people
through an ugly, uninteresting product. Developing a product that people
enjoy using takes more than a top-down behavioral map, diagnosis, and
intervention—it takes creativity, and it takes the team’s development and
design expertise.


So, how can you integrate planning and creativity? Part of the solution is
philosophical: remembering that everything we’ve done so far has specified
desired functionality, and not how the product should accomplish it.
Another, subtle, part of the solution is to avoid a strong reference point by
intentionally separating behavioral design from the process of designing the
interface or communication. The goal is to avoid using the behavioral map
and intervention as an implicit, unintentional starting point for what it
should look like: one that would strongly shape what the final design looks
like.


How can you open up the design process and avoid getting a cookie-cutter
product? Don’t try to push an interface design under the cover of behavioral


science and behavioral interventions. Keep them focused on the what, and
not the how. Then, let the design team (or members of the product team
who are fleshing out the requirements) put aside the behavioral diagnosis
and intervention for a bit, and brainstorm ideas on how the product might
look; sketch them out. Prototype them. The design process should be
honored and given the space it needs.


People on the team may wear more than one hat—a product manager may
also be a behavioralist; it’s the same with the designer. The key is to take off
the behavioral hat when seeking creative designs.

### **A Cautionary Tale: My Exercise Band**


A few years ago, a new piece of wearable technology hit the market. The
product combined exercise and sleep tracking with a band you wear at night
and one you wear during the day. It sounded great, and I preordered mine—
I received it right before Christmas. The product turned out to be an
excellent example of what happens when a company makes something that
is strongly focused on behavior change but forgets to build a good product.
(I won’t mention their name, since the company is continuing to revise and
improve its products, and it isn’t the only company to build an exercise
band that had problems in the early stages!)


My wife and I made the product into a twofer gift: I would use the exercise
band and she would use the sleep tracker. So, on Christmas day, I installed
the app and started trying out the exercise band.


The product did a lot of things right from a behavioral perspective. It
automatically tracked sleep and exercise, which are difficult to do by hand.
It had a simple, clean user interface. It helped me set reasonable goals to
start with and then provided constant feedback and nice rewards (little icons
on the screen) as progress was made.


The next day I went into the office. After a long day of sitting on my duff, I
checked how much exercise I’d had. I saw the screen shown in Figure 12-1.


_Figure 12-1. My daily exercise—while sitting at the computer_


Believe it or not, I didn’t walk 38 miles that day while sitting at my desk. I
wish I had. Disappointment number one: clearly a bug in the tracking
system.


As I got ready to go home, I put on my jacket. The wristband came off. The
small magnetic clasp that held it together wasn’t strong enough. It
accidentally fell off multiple times over the following days; I’m lucky I
didn’t lose it. Disappointment number two: industrial design problem.


The next day, I forgot it on the counter of my desk. Shortly after lunch, I
saw the screen shown in Figure 12-2.


_Figure 12-2. A little judgmental, aren’t we?_


Not the best experience. If the product had been absolutely correct and I
had been inactive, maybe I would have taken the message better. But from
its lack of knowledge about me, it inferred that zero data meant a problem
in my behavior rather than in its knowledge. A good interaction designer
should have caught this.


Ah well. I returned it quickly. I’m still excited about the concept and look
forward to new wearable technology as it comes out. But for now, this is a
cautionary tale about what happens when you focus exclusively on behavior
change and not enough on building a good product first. Remember that
behaviorally effective products must _also_ be interesting and usable.

## **Build in Behavioral Metrics from Day One**


While applied behavioral science doesn’t specify how a product should be
built, it does very strongly indicate one of the elements that must be
included: metrics of success. These are not an afterthought, something to be
added after the product is built. I’ve tried that route across many products


and marketing campaigns, and I know many others have as well. It’ll really
difficult to retrofit metrics into a product or campaign that’s already
launched—it’s difficult technically and it’s difficult psychologically, since
the team has already moved on to thinking about other things. Instead,
behavioral metrics are part of the product itself, not an add-on for later.


To do this well, you need to make sure those metrics are well-defined and
that they’re easy to gather in the product.

### **What You Should Already Have**


The first step in measuring the impact of your product is to be absolutely
clear on the impact you care about (i.e., the intended outcome of the
product). That should have been established in Chapter 6 (and refined in
Chapter 7). In particular, you should have:


A clearly defined, tangible, and measurable outcome that you seek,
with a metric (way to measure it)


A clearly defined, tangible, and measurable action that drives that
outcome, with a metric


A threshold for each metric that defines success and failure


If you don’t have this in hand, please go back. If you don’t know how your
product or campaign is going to be judged then, by definition, _it’s not going_
_to succeed_ .

### **Implementing Behavioral Tracking**


You know what you want to measure. Now, you need to measure it by
instrumenting the product or otherwise gathering data about your users’
behavior and the target outcome. How you gather this data depends on the
type of product and behavior change you’re working with, whether the
target behavior is within, or outside, of the product.


**Measuring behaviors and outcomes within the product**


If your behaviors and outcomes are part of the product itself, you’re in luck.
There are tools to help you gather the data. For example, let’s say your
application aggregates user contacts and helps users keep in touch with
[them regularly, like Contactually. The behavior change problem entails](https://oreil.ly/Aetmu)
helping your users figure out how to best organize their contacts within the
app.


You can code your product to automatically record the actions that users
take (organizing contacts) to see if they are successful. In that case, you can
code your product to automatically record the action and outcome or push
[events out to a third-party platform like Kissmetrics or Mixpanel](https://oreil.ly/p3sk8)
(Contactually has used them, for example). That’s the ideal. When your
product is online, you can even gather the data in real time and see what’s
going on immediately.


**Measuring behaviors and outcomes outside of the product**


It can be much more challenging if the behavior change problem is outside
of the product. First, look for ways to pull in existing real-world data. At
HelloWallet, one of our primary goals was to help people save money for
the future. But they couldn’t actually do that within our application—they
moved money into their savings accounts through their bank. Early on in
our product development, we realized that we needed to ask our users for
read-only access to their bank account information. With the bank account
information, we could provide them with better guidance, and, very
importantly, we could tell if our guidance was actually working or not.


You’ll need to be creative and search for datasets you can pull in. Oracle’s
Opower, described at the beginning of Chapter 13, is a piece of paper—a
physical mailer sent to utility customers. There’s no way to reliably
measure people’s real-world behavior with that mailer. But they have built
relationships with the utility companies to access utility records on how
much energy people actually use. And, with that data, they can reliably tell
what impact their mailers are having on behavior.


Your company may need to _consider adding functionality to the app to_
_make real-world measurement possible_ . Let’s say you have an app that


helps people eat healthier. It provides meal plans for easy and healthy home
cooking, so users don’t need to eat out as much. That’s great, but how do
you know if the product is successful? Creating a meal plan isn’t enough.
You need to know if people are actually acting on that advice. One way to
measure behavior outside of the product (actual use of the meal plan) would
be to add a feature to link to the person’s grocery store loyalty card. The
grocery store knows what the user is buying and has a financial incentive to
have people buy more there, instead of eating out. Users can be rewarded
for following the meal plan and get greater insight into what they are
eating.1 There’s a benefit for the user, for the grocery store, and for you—
since you’ll be able to measure impact.


Sometimes, however, there simply isn’t a dataset you can draw upon, or the
dataset is too imperfect or infrequent to use. For example, let’s say your
application encourages people to vote. The act of voting is outside of the
product, and it takes months to get official data on whether someone voted
or not.


In such cases, where you really don’t have a way to regularly gather realworld data, there’s a three-part strategy for benchmarking your product’s
impact:


1. Benchmark the impact your product has on an intermediate user

behavior that you can measure regularly, even though it isn’t the
final real-world outcome you really care about.


2. Determine how to accurately measure the real-world outcome _at_

_least once_ .


3. Build a bridge between the intermediate user behavior you measure

regularly and the real-world outcome you care about.


The bridge is basically a _second_ benchmark—connecting the regularly
measured behavior (usually in the app) and the irregularly measured realworld outcome. We’ll discuss this option in more detail in Chapter 14.

### **Implementing A/B Testing and Experiments**


In the next chapter, on Determining impact, we’re going to talk in detail
about experiments and other ways to determine the impact of your product
based on the metrics you’ve just implemented. Here’s the short version:
experiments are your best route to determining whether you’ve had the
impact you seek, when they are possible. So just like the metrics
themselves, you should plan to implement the _ability_ to run experiments as
part of the product or communication itself. Otherwise, you’ll have a hard
time retrofitting them.


If you’re not familiar with them, A/B tests take a randomly selected group
of users and show them one version of the product (version A), and show
another randomly selected group another version (version B). The
mechanics of A/B testing and multivariate testing are discussed in the next
chapter; let’s look now at what you’ll need to implement in the product,
though, to make that possible.

### **Tools for Behavioral Tracking and Experiments**


To measure your product’s impact, you’ll need to look beyond basic tools
that track page views and conversions. Often the impact you’re looking for
isn’t just a simple event in the application, like a page view. For example, if
your product helps users form the habit of updating their budget each
month, measuring the habit means more than the pages they’ve seen.
Second, you’ll need access to raw, per-person data for statistical modeling.
Third, in order to assess changes in impact, you’ll probably need to run A/B
tests.


Most behavioral tracking tools for websites and applications provide
aggregate information by default: what segments of people are doing or
how many people are following a particular path through your app. Google
Analytics, for example, is in this vein; it’s really useful to figuring out
what’s going on in your app, but it doesn’t tell you what individual people
are doing and thus doesn’t allow you to do more fine-grained analyses and
experimental tests.


Getting individual-level data—what each person is doing in the system—
requires more horsepower; the basic version of Google Analytics doesn’t
provide that. As of the publication of this book, the Google Analytics 360
package _does_ provide individual-level data, as do Heap, Adobe Analytics,
and other packages like it via API calls or export files. Heap is currently my
personal favorite because it does some wonderful magic behind the scenes
to track most activities in a Heap-enabled program, even before you specify
what you’re looking for (in GA and other tools, you have to specify what
you’re looking for before it starts tracking). Once you request that activity,
it provides historical data all the way back to when Heap started in the app
—which is immensely useful.


There’s an open source version of Google Analytics that does what GA
does (though a few versions behind) and provides that individual-level data:
[Matamo. It can be a bit clunky, but it gets the job done if you know how to](https://matomo.org/)
analyze the raw database records.


When working with email, you’ll get behavioral tracking out of the box for
almost all modern email packages—as long as you use a commercial tool
and don’t send through your Outlook or Gmail account, basically. It’s the
same thing for mass text message (SMS, WhatsApp, etc.) software like
[Twilio, Bandwidth, and Vonage.](https://oreil.ly/vWRRK)


Tools that support A/B testing or its cousin, multivariate testing, will
advertise that fact. There are a variety of tools that can handle the A/B
testing for you. As of this writing, tools for app- or web-based testing
include Google Optimize 360, Adobe Target, Optimizely, VWO, and
Mixpanel. Many support mobile, as do specially targeted ones like
[Apptimize (now part of Airship). In the text message world, A/B testing is](https://apptimize.com/)
[also supported out of the box for big providers. And again, in mass email,](https://oreil.ly/PAJVY)
don’t even think of using an email package that doesn’t support A/B testing
(if you can find one!).


The economics of third-party trackers and experiment tools have become so
favorable that it’s unlikely you’ll need to build your own. But, if needed,
companies can also readily implement their own per-person tracking by


pushing the events that occur within the system out to a database for later
analysis. It’s something I had to do many times over the years, but I now
rely on third-party tools.

## **Putting It into Practice**


Applied behavioral science, and the process of designing for behavior
change, doesn’t have a lot to say about the development process or software
architecture you should use to implement your product. However, there are
two areas that are essential, which we’ve covered here: separating
behavioral design from interface design and ensuring that metrics are a core
part of the product itself, and not an afterthought.


Here’s what you need to do:


The behavioral science team (or role) should take a breather
between the planning process (covered in Chapters 6 and 11) and
implementing the product itself, which we cover here. Chapters 6–
11 provide a functional spec—how to help users overcome
behavioral obstacles. They can’t give the team a visual design for
how the product or communication or look or specify exactly how
it should interact with users. That’s a designer’s role. Collaboration
is great, but don’t let behavioral design crowd out visual design


Make metrics part of the _first_ version of the product or
communication. Both behavioral tracking and experiments (A/B
tests) should part of any MVP. It’s a royal pain to retrofit later.


Thankfully, there are many third-party packages you can use to
cover these needs—you rarely need to build it yourself anymore.


How you’ll know there’s trouble:


The behavioral design is being used as an interface design (or
communications design)


You’re building the product, and tracking outcomes isn’t part of
version 1.


Deliverables:


The product, with behavioral metrics built in!


As with all of the “Putting It into Practice” worksheets, we’ll use the
example of an app meant to help people get exercise through running. A
completed worksheet is here, and the blank form is available in the
[accompanying workbook. Some of the fields can be copied directly from](https://oreil.ly/behavior-change-wkbk)
the project brief, or the project brief can be attached for reference.

## **Worksheet: Ethical Checklist**


_If your organization has an IRB or a process modeled on the IRB, then you should use the_
_templates and processes from that review board. If you don’t have an IRB process, here is a_
_worksheet to get you started, modeled on tools we’ve starting using on my team. Some fields can_
_be copied directly from the project brief or the project brief can be attached for reference._


Practitioner: Steve Wendel


Project: Flash app


Date: 1 Jan 2020


Description and Purpose


1. Please describe the product, feature, or communication (henceforth: “product”) to be

developed: Flash app is a mobile app designed to encourage exercise. It is sold to
employers and distributed to employees as a benefits program.
2. What specific behavior (action) does the project seek to change, and does it support or

hinder it? The primary behavioral goal is to encourage users to go to the gym and


exercise.
3. What behavioral intervention(s) does the product use to support that change? The app

uses multiple interventions at different stages of interaction with the product. First, to
encourage downloading the app, it uses testimonials from who uses it (social proof).
Second, within the app it uses a social competition to encourage participation. It also
employs small wins to encourage people to continue using the app and progressing
toward their goals over time.
4. Who is the target population (actor)? White-collar employees of existing clients who

don’t exercise regularly.
5. How, if at all, will this benefit that population (user outcome)? The target outcome is to

help users decrease common sources of pain: back pain, neck pain, joint pain.
6. In what ways might this intervention cause notable harm to the individual, in the short or

long term (e.g., products that seek to addict their users to its use)? There don’t appear to
be serious downsides to these interventions or the product, beyond encouraging
individuals who should not exercise (due to heart conditions, etc.) to exercise: we leave
them free to opt out without penalty from their employer.
7. How will this benefit your organization or team? This will increase revenue from our

corporate wellness program clients.
8. What financial or personal interest do you have in this project succeeding? My career is

at stake—if this doesn’t succeed, I may lose my job or miss out on opportunities for
promotion.


Transparency and Freedom of Choice


1. Does the target population want to accomplish this outcome? Do they want to change

this behavior? Yes, in our qualitive research and in surveys of the population, many
employees want to accomplish the outcome and see the specific action as an appropriate
way to accomplish it.
2. Does the target population know that you are seeking to change their behavior? And, if

not, will they be upset when they become aware of it? Yes, the app is clearly described as
seeking this goal. Users should already be aware.
3. Is the user defaulted-out, defaulted-in, or is it a condition of use for the product to

interact with these interventions? Can the user opt out in a straightforward and
transparent manner? Defaulted out. After choosing to participate, the user can opt out at
any time.
4. What steps will be taken to minimize the possibility of coercion? The main risk of

coercion is that employers (our clients) require use of this program, or penalize nonparticipants with higher medical premiums. We have a clause in our contracts with the
employers barring such penalties and requirements.


Data Handling and Privacy


_If data privacy issues aren’t addressed elsewhere in the company’s standard product development_
_process, this is a good place to cover those issues. If they are covered, skip these._


1. What personal information does this product gather? User email address, first name,

personal exercise goals, and exercise history. Location history is also gathered as the
person uses the app.
2. How is that data handled to ensure privacy of the users? The directly identifiable

information, name and email address, are masked with a salted, one-way hash. All
information is stored on a secured server, following the company’s standard data
handling process.


Final Review


This project has been independently reviewed and approved by: FlashCorp Ethical Standards
Board


Date: 3/3/2020


1 Most of us forget or don’t even think about what we’re eating. See Riet et al. (2011) for a

summary.


# **Chapter 13. Determining Impact** **with A/B Tests and Experiments**

_You should take the approach that you’re wrong. Your goal is to be less_
_wrong._

—Elon Musk


_Opower, an energy-efficiency and customer engagement unit owned by_
_Oracle Utilities, has run some of the largest experiments in the world about_
_how products can change behavior. Millions of people have participated in_
_their studies simply by opening a letter from their utility company or_
_fiddling with their thermostat._


_Opower is best known for delivering monthly reports to utility customers_
_that show them how their energy usage stacks up against their (anonymous)_
_neighbors. It’s a well-studied technique in social psychology called peer_
_comparisons, which we discussed a bit in Chapter 9. Figure 13-1 shows an_
_example of one of its comparisons._


_A host of government, private, and academic publications have shown that_
_Opower’s simple comparisons help consumers cut their energy bills by_
_roughly 2% on average._ 1 _That may seem small, but it adds up to over 2.6_


_terawatt-hours of electricity—enough to power 300,000 homes for a year,_
_or roughly $300 million in consumer savings on energy bills._ 2


_Figure 13-1. An Opower energy report, comparing the reader’s home heating usage to that of their_

_neighbors_


_Opower has repeatedly run experiments to measure their impact and test_
_ways to improve it further. Rigorous measurement and testing have been a_
_key factor in their success._


In designing for behavior change, that unambiguous signal is vital. Our
good intentions—and even our thoughtful statistical analyses—aren’t
enough. Human behavior is so complex and context-dependent that it’s all
too easy to fool ourselves into thinking that our products work as planned.
And there should be no confusion or doubt:


A randomized control trial is simply the most effective and rigorous
tool out there for determining the impact of your product or
communication on behavior. It provides the clearest and most
unambiguous signal of impact.


Randomized control trials aren’t the domain only of world-class
researchers, however. You’ve probably run one type of randomized control
trial yourself: the humble A/B test. You don’t need a big team to do A/B
tests; often, you don’t need anyone else but yourself to measure impact in
this rigorous and highly effective way. And so, this chapter provides a
broader understanding of randomized control trials, including A/B tests, and
how to make sure that your tests are effective, rapid, and clear.




## **The How and Why of Randomized Control** **Trials**

When you want to know whether a product or communication actually does
what it’s supposed to do, randomized control trials are the most trusted and
rigorous tool. In fact, they are the gold standard in science; the same tool is
used to measure how effective medicines are at curing a disease, for
example.

Here’s how they usually work, using the example of an exercise app:3


1. _Write out what you’re trying to do._ Start by writing out three

things, which we’ve already covered in the previous chapters:


a. The _outcome_ you care about (e.g., decreased back, neck

and other joint pain—measured by a decrease in doctors
and physical therapy visits)


b. The _intervention_ that may cause that outcome (e.g., going

to the gym)


c. The _target audience_ (e.g., white collar, sedentary male

workers, aged 35 to 45)


2. _Randomly assign the audience._ Randomly sample enough people

from the target audience, and randomly assign them to two groups,
which we’ll call a _control_ group and a _treatment_ group; for
example, five hundred men assigned to the control group and five
hundred to the treatment.


3. _Deploy the intervention._ Offer the intervention to the treatment

group and not to the control group. For example, give the treatment
group the app and give the control group basic information without
the app’s features. (We discuss how to make this a _double-blind_
study later in this chapter.)


4. _Measure what happens._ After enough time, measure the outcomes

for each group. For example, measure the number of physical


therapy visits for each person in the treatment and control groups.


5. _Calculate the impact._ Use the following simple formula to measure

the difference between the two groups’ outcomes:


Impact of intervention = Average outcome for the
treatment group – Average outcome for the control group


6. _Make a call_ . If the impact is large enough, you can conclude that

your intervention is practically and statistically meaningful. For
example, the app decreases physical therapy visits by 10%, and
that means a real benefit for your users and your company’s
business.


That’s it. There are details we’ll have to examine, especially in terms of
what _enough_ means in each case, but getting the concept down is important.
Assuming the right conditions are met, experiments are simple, powerful,
and highly informative.


Different types of experiments go by many names, such as randomized
control trials (RCTs), split tests, and A/B tests. In the software world, the
most common term is A/B test, and in this chapter we’ll focus on the
particular opportunities (and constraints) of running digital experiments in
software. Another popular technique that we’ll look in more detail at later,
multiarmed bandits, is another type of digital experiment.4 To reinforce the
fact that mathematically they are the same, and for simplicity, we’ll use the
more general term _experiments_ here.

### **Why Experiments Are (Almost) Better Than Sliced Bread**


Let’s say we wanted to know whether our new exercise routine helps people
lose weight. A common, but flawed, approach to answering that question
would be this: compare people who use the exercise routine versus those
who don’t, and see whether those in the first group lose more weight than
the second. The problem is that if we discover that people in the first group
lose more weight, do we really know why that happens? It might be


because of the exercise routine. Or, it might be because people in the group
are simply more motivated to lose weight. Or, people in the first group
might have faster metabolisms.


Instead of comparing the people who use the exercise routine versus those
who don’t, let’s say we ran an experiment in which people were randomly
assigned to each group; that changes everything. The experiment would
remove each of these potential explanations and any other that you might
imagine. We could then say with strong empirical support that people in the
first group lost weight _because_ of the exercise routine.


The way that experiments accomplish this magic is through randomization.
By randomly assigning a set of people into two groups, those two groups
are statistically identical. People’s metabolisms in each group are
statistically the same (the number of people with fast or slow metabolism,
for example, is statistically the same). People’s levels of motivation in the
two groups are statistically the same. And so is their distribution of ages,
incomes, gender, political preferences, and everything else that you might
imagine about the two groups. Most importantly, their likelihood of losing
weight in the future is also statistically identical.


When we take these two statistically identical groups and treat one of them
differently by assigning one group to the exercise routine and the other not
—any resulting difference in the degree to which they lose weight must be
due to that intervention and nothing else. A properly designed experiment
allows us to say, within statistical limits, that an intervention actually _causes_
an outcome. That’s why experiments are awesome.

## **Experimental Design in Detail**


While the concept of experiments is straightforward and easy, the details
really do matter. There are a few rules we need to carefully follow to ensure
that an experiment is designed and executed correctly. The first question
that new experimenters generally ask is: how many people are “enough”? [5]


### **How Many People Are “Enough”?**

When you’re measuring the impact of your product or communication, the
quality of that measurement depends on how many people are in your study.
Here’s a simple example to show why. Let’s say your product is an app that
encourages people to eat less ice cream. You try it with one person. Dang it!
They ignore it and keep binging on ice cream! But you keep going. The
second person cuts back a lot. The third person also does, but not quite as
much, and so on. That’s actually a pretty normal range of variation across
people.


Overall, the product is a success. It helps people cut their (unwanted) ice
cream habit by 50%. If you’d only looked at the first person, though, you’d
have thought it was a failure. If you only looked at the first two people,
you’d be really confused. If you looked at the first four, then the picture
would be clearer—overall, it seems to help, but there are exceptions.
Adding people makes the picture clearer and clearer. At some point, adding
people doesn’t matter; you already have a very good idea of what the
product’s impact is. The number of people you need to have a (statistically)
clear picture is known as the minimum sample size.



You determine the minimum sample size using a function called a _power_
_calculation_ . You can use an online power analysis calculator or any
statistical package like R, Python, G*Power, or Stata. If you don’t know
[where to start, try G*Power,6 which is free and extremely powerful, but](https://oreil.ly/oDECW)
requires some documentation reading. If the product’s outcome can be
expressed as a number (like weight, height, or the number of cigarettes
smoked in the month), then you’ll use a calculator that can handle the
average value for the population. If the product’s outcome can be only one
of two things, like the patient is either alive or dead, then you’ll use a
calculator that handles percentages, proportions, or rates. In R, you can use
the functions power.t.test() when working with average values and
power.prop.test() when dealing with percentages. In Python, you’d use the
[slightly more complicated StatsModel package.7](https://oreil.ly/AQ-cy)



6



7



Here are the specific numbers you’ll need:


The average outcome for people who don’t have the product (or
who don’t have the new feature or communication you want to
test). That’s the _baseline_ . For example, the average weight of the
target audience for a weight-loss app is 245 pounds.


The variance in outcomes (difference from the average) among
people without the product. That’s the _noise_ . Note that for
outcomes that are rates (click rate, etc.), this is built into the
calculation; you don’t need a separate measurement of noise. For
example, the standard deviation of our target audience’s weight is
35 pounds.


The _impact_ you expect from the intervention on the outcome. Be
conservative: ideally the product will have a much _larger_ impact,
but here you want to make a reasonable lower estimate of impact.
For example, we expect a decrease of 10 pounds.


The calculator will also ask for two parameters that indicate how sensitive
the test should be:


Confidence level or, equivalently, an alpha error level (alpha error
level = 1 – the confidence level). Usually the default confidence
level is 95% (alpha of 5%). That means you can expect to
incorrectly say there _is_ an impact when really there _isn’t_ one, 5% of
the time. _That’s a false positive._


Statistical power, or, equivalently, a beta error level (beta error
level = 1 – statistical power). A good default statistical power level
is 90% (beta of 10%); that means you can expect to incorrectly say
there _isn’t_ an impact when really there _is_ one 10% of the time.
_That’s a false negative._


Using these default values for our exercise app, we’d need 258 people per
group—or 516 people total.8


These default parameter values are built around the assumption that you
want to be very careful to avoid claiming that there’s an impact when there


really isn’t (a false positive). In our exercise app example, that means it’s
especially important for us to avoid claiming that the app is successful at
decreasing people’s weight when it isn’t. It’s important, but not as
important, to avoid missing an impact that really is there (a false negative).


Each experiment is different, but those are pretty good assumptions to use
when you’re testing whether your product works or not. It will be very
embarrassing (and costly for the engineering team) to claim you’ve found
an answer, pursue it, and then find out it was a mirage. So, generally, keep
these defaults.


You may also be confronted with a question of whether you want a _one-_
_sided_ or _two-sided_ test. In a two-sided test, you’re looking to see whether
the product causes any change, positive or negative, in outcomes. In a onesided test, you’re assuming that if the product has an effect, it will be
positive (or maybe negative!). If the effect is actually in the opposite
direction, the test won’t work correctly. There’s always debate around this
issue, but I prefer to take the more open-minded route and stick to twosided tests that understand that the product might make things better or
worse.


Once you enter these values into the calculator, it will tell you how many
people you need in the treatment and control groups. If you have more,
that’s great. If you have less, look for more people! If you have just the
number of people it shows but have the _ability_ to collect more, please do so;
there’s a chance that some participants will have invalid data, leave the
process early, and so on.

### **How Long of a Wait Is “Enough”?**


Another common question concerns how long to run the experiment. If you
have a fixed set of people, such as an existing email list, the answer is
straightforward. Run the test for as long as you think the intervention needs
to have its effect (plus a little bit longer, just to be safe).


If you don’t have a fixed set of people and instead have a stream of people
coming to a website or product over time, things become a bit trickier. The


common temptation is to run the experiment until it looks like there’s a
“clear winner.”


Using the ice cream app described earlier, we can quickly see why this is
problematic. Let’s say your app has a steady stream of people signing up for
it and using it. The first few people break their unwanted ice cream habit
very nicely—far better than the control group. However, as more people
sign up for the app that strong initial result seems to fade. After a hundred
users, it looks like it’s not much more effective than the control group after
all. If we had stopped the test after the first few people, we would have
gotten a false signal about the app’s impact. In fact, at _any given moment_,
either the treatment or control will often look like it’s doing better than the
other. That doesn’t mean that it has a meaningful impact; the difference
may be due simply to noise and will fade (or even reverse) over time. If you
constantly check the results of the experiment, waiting for something that
looks promising, you’ll increase the likelihood that you’ll say there’s a
difference between the two groups when there actually isn’t one.9


Many well-meaning product managers have been stung by the rush to call
an experiment “finished” simply because the results look convincing. The
way to avoid this problem is threefold:


1. Run a power calculation, as described earlier, to determine how

many people would be required to detect the effect we expect.


2. Determine how long it will take for that number of people to

interact with the product, given the stream of people over time.
When you expect to reach the target number of people, stop adding
more people.10 Regardless of what we see in the meantime, and
how tempted we are to stop the test early, the end date is when the
test completes. For example, if we need one thousand people for a
website test, and we get two hundred people a day, we keep adding
people for five days.


3. After the test is complete, run a significance test—a procedure that

is related to the power calculation—to determine whether the


results are statistically significant. We’ll talk about statistical
significance a little bit later.

### **Using Business Importance to Determine “Enough”**


Thus far, we’ve talked about the standard academic version of an
experiment: take a reasonable estimate of how much of an impact you
expect, and figure out how many people you needed based on that impact.
In a business environment, there’s another way to approach this problem.
Instead of considering what impact might happen, consider instead what
impact is _important_ . Specifically, the experimenter would follow this
process:


1. Determine the minimum meaningful effect (MME). What is the

smallest change in the outcome that you would consider
meaningful or important to the company or its users? There is no
universal rule for determining this—instead, what matters are a
company’s particular business priorities and opportunity cost.11


2. Calculate the sample size based on that MME. In other words, do

the power calculation described before, but use the MME in the
equation instead of the “expected impact.”


3. If there are plentiful users available all at once, or there’s a

continual stream of people over time from which to draw from,
then the number of people in each version (or “arm”) of the test
should be _at least_ as many people as calculated in step 2.


4. If, instead, there is a fixed and limited number of people available

for an experiment, then:


a. Determine the largest viable effect (LVE). What is the

_largest_ change in the outcome that you’d expect the
intervention to have?


b. Calculate the sample size based on the LVE. In other

words, run a power calculation using the LVE as the


expected impact from the intervention.


c. Use the illustration in Figure 13-2 to determine whether to

run the experiment at all, given the available sample size
available for the test.


_Figure 13-2. Before you run a test, use this table to figure out whether the results will be meaningful_


This approach provides a tremendous benefit to companies with limited
time and resources (i.e., almost all companies!). By focusing on the MME
and using that to determine the sample size of the test, then no matter the
outcome of the test, the company gets a clear signal on what to do next.
Namely:


If the test comes back showing a statistically significant positive
impact: great, full steam ahead.


If the test comes back showing a statistically significant negative
impact: don’t launch the new version of the product or
communication. You’ve just saved yourself lots of pain down the
line.


If the test comes back showing no statistically significant impact at
all: wonderful. It means that there’s no meaningful impact to be
found and no further research is required. If you haven’t finished
building it and deploying it to users, then stop. There’s no business
value there. If you have, it really doesn’t matter if you launch it; it
will have no meaningful business impact.


Thus, all experiments run in this context are meaningful and useful for the
company. They either tell the company that yes, a new product or
communication is impactful, or that it should be abandoned as irrelevant.
There is no wiggle room of “well, maybe another test with more people
would find an impact.” Any such hidden impact is irrelevant to the
business.


From a technical perspective, what’s new here is that the minimum
meaningful effect allows the company to determine a clear plan of action
based on null results. Why doesn’t everyone do that? It’s because
experiments are still primarily used and thought about in an academic
context, where the incentives are different. For academics, the goal is to
publish a paper, and that (usually) means getting statistically significant
results. Thus, academic researchers have a tendency to look for very large
populations that can show a statistical significance even if the expected
impact is laughably small from a practical perspective. Statistical
significance in no way implies practical significance. And businesses care
about practical significance.

### **Points to Remember in Designing an Experiment**


In addition to these basics of experimental design, there are a few other
rules to keep in mind:


_Random selection isn’t always easy_


When people are drawn from the population, they have to be randomly

selected, and not selected based on a convenient (but not truly random)

criteria. For example, in testing the impact of a new product, you can’t


rely on volunteers to be part of the experiment and expect them to

accurately represent the views and outcomes of the overall population.


_You need random assignment as well_


When assigning people into groups, the assignment must be truly

random. For example, if the experimenter has two groups of people and

doesn’t know where the two lists came from, the two groups can’t be

used. Or if a group of people is divided based on something that seems

random like the first letter of their last name, the two resulting groups

are truly random and identical (last names, and their place in the

alphabet, are strongly tied to ethnicity, for example). If you have an

existing list of people and it _looks_ random, it almost never actually is—

there’s some ordering there, but you can’t know how it influences the

results. Use a random number generator, and generate a new number for

each person. As a sanity check, you can verify that the random

assignment process was done correctly by checking whether the two

groups have similar averages on things that the product couldn’t impact

—like age or gender. If so, great. If not, it wasn’t a true random

assignment.


_Check that the groups are drawn from the same population_


For example, a design in which a randomly selected group of men is

compared to randomly selected group of women is not a true RCT;

there’s an obvious difference between the two groups that has nothing to

do with the intervention.


_Make sure you’re only varying one thing_


Only the product (or communication) should vary across the two

groups. Carefully review the experience that each group will face to

ensure that they will see and interact with the exact same things, except

for the desired change and product or communication. “One thing”

doesn’t mean that the change in the product has to be simple; it could be

an entirely new feature or even an entirely new product. “One thing”

means instead there is one conceptual entity that you’re changing and

analyzing (which, again, can range from the text on a button to the

entire functionality of the product).12 Also, you _can_ test multiple

versions of the product at once with an “A/B/C test” or a multivariate

test, as we’ll discuss later.


This section has provided a short introduction to designing an experiment.
In many cases, your email or website targeting package (Eloqua, Marketo,
Optimizely, Google Analytics 360, Adobe Target, etc.) will handle the
mechanics of the experiment itself for you if you need an experiment and
know what to watch out for when using the software. That’s been the goal
here: to arm you with the right questions to ask. However, if you’d like to
learn more about the design of experiments, two good resources are
Shadish, Cook, and Campbell (2001) and List, Sadoff, and Wagner (2010).

## **Analyzing the Results of Experiments**


After you’ve designed a great experiment and deployed it in the field, you’ll
want to look at the results to see whether the intervention you developed in
your product or communication actually had the effect you expected. As
already mentioned, the core idea is quite simple: as long as the effect is
large enough, the intervention’s impact is just the difference in the average
outcomes for the two groups. “Enough” has a very specific meaning—let’s
take a look at how you ensure your analysis is solid.


### **Is the Effect Large “Enough”? Determining Statistical** **Significance**

One of the most common mistakes with digital experiments is that people
look to see if there is a difference between the two groups and don’t look at
whether that difference actually means anything. They can get really
excited about unreliable results, and, most damagingly, they take the wrong
lesson from the experiment and waste time building the wrong thing.


_Always run a test of statistical significance_ . That’s how to save yourself
from that fate. A statistical significance test is the after-test version of a
power-calculation (which is what we run before the test); it tells us, if, in
fact, we have a large enough effect to comment on.


Just as with the power calculation, there are two main versions depending
on how you measure the outcome. If the outcome is only two outcomes per
participant—such as people log into the application or not—then you’ll run
a test on the percentage of people in each group that have the outcome (i.e.,
the rate among each group). If the outcome is a real number (like the
amount someone spends), then you’ll determine statistical significance
based on average outcomes.


In R, you can use the prop.test() function for outcomes with only two
options (i.e., each group has a single rate or “proportion”), and the t.test()
function, or a regression, for real numbers. In Python, you’d use the
StatsModel package for both. If the outcome is ordinal (the possible values
are in order, but the spacing between them may be irregular and they aren’t
directly comparable), things are a bit trickier and a skilled stats person
should be consulted.

### **Other Considerations**


In addition to determining statistical significance, here are a few other rules
that apply to experiments:


_Go double-blind when you can_


In a double-blind experiment, neither the participant nor the

experimenter knows who is in the treatment or control group (in the A

or B arm). If the experimenter knows, it can influence their

interpretation of the data, or the experimenter’s behavior can



(unintentionally or intentionally) affect the behavior of the participant.13



If the participant knows, they’re likely to behave differently. Thankfully,

many A/B tests are double-blind accidentally because the software used

to execute them often doesn’t make it easy for experimenters to identify

and directly interact with participants. Participants receive a seamless

experience as part of the product or website and wouldn’t know what is

being tested.


_Measure the same way_


If the outcome is measured differently across the two groups, then

apparent changes may be because of the product or because of how the

outcomes were measured. To fix this, find a way to measure the

outcome outside of the product consistently (for both groups) or offer a

trimmed-down product (or feature) for the control group that just tracks

the relevant outcome and doesn’t do anything else that should drive.


_Compare results for everyone_


Make sure that when you compare the two groups, you compare all of

the people in each group. In the treatment group, for example, there will

be some people who are offered the product but don’t actually use it.

Count the non-users too; otherwise, the results mix up the effect of the

product with the effect of who chooses to use it or not.


_Generalize outcomes to the same population_


Researchers and product teams shouldn’t assume that the results apply

to everyone after they’ve done a test. For example, after running a test

with college students in the US, you shouldn’t use those results to

comment on the behavior of European pensioners. The results _may_ in

fact generalize well to that population—but it takes more than a single

experiment to determine that. It takes a series of replications of an

experiment that change only the underlying population, to determine the

_structure of portability_ of the results (for whom and under what

conditions the results apply to a different population).

## **Types of Experiments**


Experiments come in many flavors in terms of how they are designed and
executed and in terms of the particular problem or purpose they are meant
to address. Let’s look at some of the options.

### **Other Types of Experiments**


Thus far, we discussed two of the most common types of experiments: one
in which the second group receives nothing (aka a null control), and one in
which the second group receives a different version of the product or
communication (aka an A/B test). There are a few other designs one often
sees in digital experiments. Here’s a more comprehensive list:


_Simultaneous impact_


In these experiments, also known as an A/Null tests, one randomly

selected group receives a new feature or product, and the other group


does not receive it. The result of the experiment tells you the _absolute_

_impact_ of that new feature or product.


_Simultaneous comparison_


Also known as an A/B test, the randomly selected groups receive two

different versions of a product or feature. The result of the experiment

tells you what the _difference_ in outcomes is between those versions. It

makes it easy to compare their impacts.


_Multiarm comparison_


A simple extension of an A/B test looks at more than two versions at the

same time. Each version gets its own randomly assigned and selected

group of participants, all from the same pool of people. This is called an

A/B/C (/D etc.) test, for obvious reasons.


_Staggered rollout_


In a staggered rollout, each group eventually receives the intervention.

However, one randomly selected group receives the intervention _earlier_

than the other. At the moment when the other group receives the

intervention, the experimenter compares the outcome variable for the

two groups. The only difference between those two groups should be

the prior exposure to the intervention. This type of experiment is nice in

that it’s basically a _pilot study_ (something that product companies and

clients are quite used to). By randomly selecting the members of the

pilot, it is a statistically valid experiment with the full power to

determine causal impact.14 A clever way to do a staggered rollout is to

ask for people to pre-commit to buy or receive the product when it’s


released. Then, use a rolling schedule for the release—only make

enough units of the product, or give out enough access credentials, to

supply to a randomly selected subset of the enrollees. Then, later,

supply it to the rest of the people who signed up.


_Attention treatment_


In this version, both groups have access to the intervention at the _same_

_time_ . However, the experimenter has reason to believe that people are

unlikely to find and interact with that intervention on their own; for

example, when the product has many features and users are unlikely to

find a new one on their own. The experimenter draws _attention_ to the

intervention for one of the randomly selected groups. Any difference in

outcomes between the two groups is caused by the difference in

awareness of the intervention and subsequently the use of the

intervention. Attention treatments are appealing because they mean that

no one is denied the intervention—like a new feature within a product.

We can still measure the experimental impact of that feature simply by

drawing selective attention to it.


_Multivariate experiment_


A multivariate experiment entails running multiple simultaneous

experiments at the same time. The key to multivariate experiment is that

each component experiment is independently and randomly assigned. A

simple example of a multivariate experiment would be with a landing

page; the experimenter tests two different versions of the headline and

two different versions of the main image on the page. There are thus


four different versions of the page that people experience: Headline

A/Image A, Headline B/Image A, Headline A/Image B, etc.


_Multiarmed bandit_


In a multiarmed bandit, the percent of people going to each version of

the product (or “arm” of the experiment) changes dynamically based on

how well the arms are performing. The arm that’s performing the best

receives more people. In addition, the arm that the experimenter

believes will be more effective is given more traffic to start. The benefit

of this approach is that if the experimenter is right, the “better” version

receives more traffic, and thus the impact can be identified with a

smaller sample.15 The downside is that if the experimenter guessed

wrong, it takes more observations to find out which treatment is actually

more impactful. The temptation with multiarmed bandits, especially, is

to turn it off once it _looks like_ one arm is the winner—even if

statistically the results are meaningless noise that’s likely to mislead the

team.


As you can see, experimental designs can differ in a variety of dimensions
and still be experiments. The rollout of the new intervention can be
simultaneous or staggered. It can be compared against a null control or
compared against another version of the product or feature. The assignment
can be based on a static ratio between the arms or a dynamic one as in the
multiarmed bandits. None of these changes violates the core rules, and they
can each deliver valid and meaningful experiments.

### **Experimental Optimization**


In many business contexts, the mere idea of running an experiment strikes
many product managers (and marketers) as wasteful since at least one group
of people receives the “wrong” version of the product or communication.
Putting aside the issue that experiments are often the best tool to determine
which version is wrong, there’s an important element of truth in that
concern: that the primary goal for a digital product (or marketing campaign)
in a business context is not to answer a theoretically interesting question,
but rather to increase impact over time.


Companies can structure a series of experiments to _optimize_ that impact
over time. This is especially the case when there are multiple interventions
that the company wants to try.


**How Experimental Optimization Works**


When you do experimental optimization, you deploy interventions in waves
over time (a staggered rollout), with different interventions across each
wave. The lessons from prior waves are applied to subsequent ones, to
optimize the combined package of interventions over time. Step by step, it’s
like this:


1. _Write out the changes_ you want to test. You probably have a pretty

good idea about what you think will improve the impact of the
product. Design your best guess as one coherent version of the
product or feature: that’s the baseline intervention. Then, draw up a
list of the other changes you’re not sure about but probably will
help in order of how impactful you think they’ll be.


2. _Set the threshold_ . Figure out how much of an _improvement_ you

need to see in the intervention’s impact for it to be worthwhile to
re-apply in the field. This process doesn’t seek to prove out small
“nice to have” interventions; it searches for big ones and ignores
everything else. Thus, this target impact is usually greater than the
minimum meaningful effect we discussed before. We’ll call that
impact X.


3. _Chop up the list_ . Calculate the number of participants you need to

distinguish that impact in an experiment. This threshold will often
be much higher than is used in academic studies; thus, it can
radically _decrease_ the required sample size you need. If you have a
predefined list of participants, chop them up. If there’s a stream of
people who interact with the product over time, then automatically
batch up each group of people as they come in. You now have N
groups of people, where each of them is enough to measure an
impact of X.


4. _Test your initial baseline_ . With your first group of people, take

your “best guess” version and test it against no change at all—just
to make sure what you’re starting with isn’t worse than nothing. If
it has _no_ impact, that’s OK—you’ve learned you really need to
optimize more. If the best guess makes things worse, start again.
You now have _N_     - 1 groups. Either way, whichever one wins
becomes your new baseline.


5. _Run a comparison test_ . Starting with change that you believe will

have the next greatest impact, compare it against your current
baseline. Run an experiment with one of the remaining groups. _You_
_can actually run multiple comparisons at once;_ these multivariate
tests can be more efficient, but more complex.


6. _Adapt the intervention_ . If the “new” version was better, update the

baseline intervention to use that lesson for future waves.


7. _Keep doing 5 and 6 until the population is exhausted_ .


To put some numbers around this, imagine that you are doing a very simple
optimization with only two versions of an intervention that leads people to
take action in some important way, like saving for retirement. One of them
leads to 20% of people taking action; with the other only 10% take action.
The problem is you don’t know which one will work best. If you don’t
iteratively test, you can expect either 10% or 20% to take action. A big
difference, and a big risk. If you do iteratively test, using a quarter of the


population in the first wave, you are nearly certain to get 19% of the
population using the system, with almost no risk.


_Figure 13-3. Don’t take chances with your product—optimize_


If you don’t test, you have a 50% probability of picking the “good”
intervention, with 20% uptake, and a 50% probability of the picking the
intervention with 10% uptake. If you do test and you have sufficient sample
size to accurately tell which intervention is “good” based on your first test,
then in the first wave you have 12.5% of the population receiving the
“good” intervention, and 12.5% receiving the “less good” one. In the
second wave, all 75% remaining people receive the good intervention. The
result is an expected uptake of 18.75%. Good job!


When you have more options (changes you think will improve the product),
and more waves, the optimization process further shrinks the risk and
increases the expected impact of the intervention. [16]


On the practical side, in order for this process to work, you’ll need a few
pieces in place:


A large sample size. While we’re looking for big impacts (and thus
smaller sample sizes per test), running many tests still means
having lots of participants.


The ability to rapidly deploy experiments.


The ability to quickly track outcomes and determine the winner—
either with the true outcome of interest or with a reliable _leading_
_indicator_ . For example, someone’s 401(k) contribution rate is a
reliable (if imperfect) leading indicator of how much their 401(k)
balance will grow over time.


The ability to seamlessly adapt the intervention based on those
experiments.


This approach is well suited for optimizing impact where the target
population is large, and a digital context facilitates the necessary data
instrumentation and product adaption. For many digital products and
communications, this is exactly what we have: large numbers of users (or
prospects), a platform for measuring impact, and many ideas about what
could help improve our impact.

### **When and Why to Test**


Most experiments are about impact and determining whether something
works or not. That measurement occurs _after_ the product or communication
is built and provides a final, rigorous assessment. That’s not the only
reason, however; in general, there are four main reasons we do experiments
(and points in the product development cycle when we use them):


_Measuring impact_


First and foremost, experiments measure the real impact of a product or

feature on people’s actual behavior. This is usually after the product is


built and deployed with real users.


_Vetting ideas_


Quick, simple experiments with competing prototypes or product

concepts can vet big ideas at low cost. This is before the product is

built; because you’re interested in large differences, you don’t need

many participants for a statistically valid test.


_Optimizing impact_


You break a product rollup into groups of people to provide real-time

feedback about the product to maximize its impact; we covered that in

“Experimental Optimization”.


_Assessing drift and regression to the mean_


Some interventions work simply because they are new—like reminders

or novel features. You can re-run an initial experiment to check if it’s

lost its effectiveness. It’s better to know than to blindly assume a

product or communication is still works.

## **Putting It into Practice**


Designing for behavior change can and does succeed. In both the
practitioner and academic communities, we have seen impressive successes,
helping people with everything from sleeping better to learning a new
language. But what happens in the aggregate isn’t a good guide to each
individual effort. Most individual efforts have _no effect_ ; our successes are
few, and our failures are many. Thus, at the start of any behavior change
effort _we should assume that we will fail_ . That’s the safest bet, and
empirically, the most accurate one. And so we need a tool that can


accurately, and quickly, tell us when a particular effort has succeeded or
failed, given the tremendous complexity of human behavior.


Whether you’re helping workers save for retirement or encouraging people
who want to exercise more, experiments are the best tool we have to do
that. They are the best measurement tool we have to make our efforts more
effective. Experiments can help you measure the impact of your work, test
assumptions, and better understand what drives client behavior. An
experiment’s power to show a _causal_ impact depends on how it’s designed.
A badly designed experiment can’t tell you anything, but thankfully a good
experimental design doesn’t need to be complex.


Here’s what you need to do:


When you have clearly defined metrics and the technology to
support experiments (covered in Chapters 6 and 12), A/B tests and
other experiments don’t have to be difficult. The key idea is that a
group of randomly selected people receive your behavioral
intervention at the same time that another group of randomly
selected people doesn’t.


Analyzing the results of these straightforward tests requires a
single line of code in most stats packages and is built into many
modern technical tools for marketing and behavioral tracking
(covered in Chapter 12).


Before you run your test, you determine how many people, or how
much time, you need for the experiment. That avoids many
common errors and stopping a test too soon.


It can be helpful to structure an A/B test as a staggered rollout (in
which everyone gets the new feature or communication, but some
people get it earlier than others) or as process of optimization (in
which once you learn what works best, you apply it immediately to
the rest of the population and move on to the next set of tests).


Multiarmed bandits and multivariate tests are just other ways of
structuring experiments—they each have their upside and


downside, but the basic math is the same.


How you’ll know there’s trouble:


The team can’t decide on a reliable, accurate metric of the
product’s outcome or doesn’t define success and failure by that
metric. If that’s the case, return to Chapter 6.


The team is so certain of their new feature or product that they
aren’t willing to measure that impact.


When you don’t have enough users to run a formal test yet—in
which case, you can use weaker statistical methods and gather
quality qualitative feedback in the meantime (covered in the next
chapter).


Deliverables:


An impact measurement: you know if your product works to
change behavior and drive outcomes!

## **Worksheet: Design the Experiment**


_Experiments (e.g., A/B tests) are often the best way to assess whether your product is having the_
_desired effect. This worksheet will walk you through the process of designing one. We’ll use the_
_example of the Flash app, once again. In particular, we’ll examine how to test the effectiveness of_
_two different email campaigns at driving uptake of the app._


Step 1: What’s being tested?


Control:


☑ Do nothing (no email reminding them to sign up for the Flash app)


☐ Existing version


Variation 1: Email reminder focused on creating peer comparison and competition


Variation 2: Email reminder focused on reaching individual goals, investing in yourself


What’s the outcome metric? Number of sign ups for the app (short-term outcome of the email
campaign); Decreased physical therapy visits (long-term outcome of the app)


Is it measured the same way for both versions?


☑ Yes (Continue to Step 2)


☐ No/Not Sure (Stop!)


Step 2: What are the extreme outcomes?


_What’s the baseline value? (What should the control group have?)_


Baseline: 35% of eligible employees are currently signed up for the app based on our existing
outreach efforts.


_What’s the MME? (That is, the smallest change in the outcome that means you’ve been_
_successful.) No idea? Enter the smallest delta seen before._


MME: 2.5% increase in enrollment


_What’s the LVE? (That is, the largest change in the outcome that you’d ever expect to have.) No_
_idea? Enter twice the largest delta seen before._


LVE: 10% increase in enrollment


Step 3: Calculate sample size at the extremes


For the MME and LVE:


Required sample size, MME: 7,768 in each group (23,304 total across three groups)


Required sample size, LVE: 502 in each group (1,506 total)


Step 4: How many people could you include?


Do you have a fixed list of people?


☑ Yes (Use the list size.)


☐ No, I have a stream of people over time (What’s your timeline? Calculate how many
people you’d see by then.)


Number of people available: 30,000


Step 5: How many people should be in each group?


_Divide the number of people you have (step 4) by the number of variations (step 1) to calculate_
_the number of people (sample size) per version_


Sample size: 30,000/3 = 10,000


Step 6: Do you have what you need?


_Refer to Figure 13-2, reproduced here, which shows how to interpret these values._


What do these results mean? The available sample size per group is larger
than both the required amount for the MME and the LVE: _Proceed_ . This
test will tell us:


Whether this particular test has the desired impact, and it will also
tell us


If nothing is found on this test, that it is unlikely that further testing
will find a sufficiently large impact for the business to care.


In other words, either way, no further testing will be needed from a
business perspective, on this intervention after this experiment.


1 See Allcott (2011), for example.


2 Oracle (2020)


3 My thanks to Jesse Dashefsky for spurring me to clarify this section.


4 [See Hopkins et al. (2020) for a nice summary of the different types in practice. Much of what](https://oreil.ly/RgOfq)

we’re talking about here might go under the term “Nimble RCT,” coined by Dean Karlan as a
contrast to long-term impact-focused RCTs. They are all experiments, though.


5 This section and the next draw upon an internal article for Morningstar written by Steve

Wendel. Used with permission.


6 Or just search for “G*Power”—thankfully, it’s an unusual name.


7 [See also the pyDOE2 package for fancier designs to do the same.](https://oreil.ly/llQeD)


8 Values calculated using R’s power.t.test() function.


9 [List et al. (2010). My thanks again to Katya Vasilaky for the reference and description of the](http://doi.org/10.3386/w15701)

problem.


10 If the effect of the intervention is immediate, that’s the end date of the experiment. If it takes

time to have an effect, then the end date is the date at which you stop adding people (because
you have “enough”) plus the time it takes to have its effect.


11 There are criteria in the academic work for identifying whether the size of an effect is

“small,” “medium,” or “large.” These may be good starting points to set your MME if you
don’t have a threshold for your business. For example, the oft-used effect size when comparing
two groups is Cohen’s _d_ . This statistic tells you how many standard deviations (index of a
sample’s spread around its mean) two mean values are from one another. The criterion for a
“small” _d_ is 0.20, or 1/5th of a standard deviation. In our exercise example (the Flash app), if
the standard deviation of our sample is 2.5 physical therapy visits, then a “small” effect would
be a difference of one-half visit (2.5 × .2) between the treatment and the control group. Many
thanks to Stan Treger for adding this section.


12 A test of the full product has a particular meaning: an impact assessment of the combined

package. If the package is effective, then one can follow up with analyses to separate out the
particularly effective components.


13 Thanks to Fumi Honda for highlighting the problem of observer-expectancy.


14 This is also useful when you have a product that your users want and you can’t withhold it

from them. This happens in many international development projects, where the funder
strongly believes in the success of the project before it is tested and feels it would be morally
wrong to withhold the product from potential recipients (see Karlan and Appel 2011).


15 [See Hanov (2012) for an enthusiastic, if a bit too optimistic, description of multiarmed](https://oreil.ly/0VABH)

[bandits. See Gupta (2012) for a nice summary of the pros and cons of A/B testing and](https://oreil.ly/BMjIW)
multiarmed bandits.


16 From a scientific perspective, this process makes a number of assumptions about the

population and the impact of the intervention. These assumptions actually underlie many RCTs
in the field currently, but aren’t explicitly stated. Namely, (a) the experimental results are
generalizable over time, (b) the experimental results are independent of one another, or
additive, and (c) the researchers don’t already, and reliably, know what is “best” (i.e., the
experiments add knowledge and don’t merely document it).


# **Chapter 14. Determining Impact** **When You Can’t Run an A/B** **Test**

_Recently I had the good fortune to attend an event featuring many of the_
_most prominent and prolific behavioral scientists in the world. They had_
_banded together to address one of the frontiers of behavioral science: long-_
_term behavior change._


_The researchers were testing whether they could move the needle on gym_
_attendance. They ran nearly 20 simultaneous studies, with each researcher_
_pursuing their “best guess” of what would work. This event was the first_
_time that everyone in the group would hear the results._


_What happened? Not a single study was effective at long-term behavior_
_change. The best researchers in the world had each taken a shot and had_
_fallen short of their target._


_Something that is often hidden, at least to those outside of the research_
_community, is that in our space the successes are few and the failures are_
_many. That’s normal. That’s expected. It’s because the most interesting_
_applications of behavioral science are often focused on difficult and_


_seemingly intractable problems, like exercise. Even the best researchers in_
_the world try again and again, before they find a breakthrough that_
_generates headlines and a best-selling book._ 1


_The lesson here isn’t merely to “fail fast” (a motto that is deeply engrained_
_in product development, at least in Silicon Valley and similar tech hubs) or_
_that embracing failure means embracing iteration._ 2 _Rather, it’s a bit more_
_nuanced. How did the researchers know that they’d failed? It’s because they_
_looked for failure. In their case, they used randomized control trials to_
_receive an unambiguous signal that things hadn’t turned out as planned,_
_without wiggle room to lie to themselves or try to put a positive spin on the_
_results._


Teams can’t always run experiments, but the need for rigorous
measurement doesn’t go away. The less wiggle room—the less one can
explain away the results or hide from flaws in the product and its ability to
behavior change—the better. We want to find problems early and not let
them turn into expensive messes. So let’s look at other ways to measure
impact.

## **Other Ways to Determine Impact**


Experiments take care of all of the nasty details of figuring out whether the
application, or something else, changed the user’s behavior and outcomes.
The random assignment process, properly done, ensures that nothing is
different between the two groups except for what they want: the product
itself. So any difference in outcomes is caused by the application.


As an academic, I could make the case that experiments are really the only
way to measure _causal impact_ because of these benefits. But in real-world
products, that’s unrealistic and too restrictive. If you aren’t using
experiments, then you have to face the nasty details of estimating the causal
impact of the application head on. It can certainly be done, but it should be
done with open eyes.


The easiest and most common way to look at impact is a pre-post analysis.


### **A Pre-Post Look at Impact**

In a pre-post analysis, you look at user behavior and outcomes before and
after a significant change. For example, if users on average walked 500
steps a day before using your product and 1,500 steps a day after using it
for one month, then the product _might_ have increased their walking by
1,000 steps a day.


In a pre-post analysis, you take the difference you see and try to adjust it for
all the other things that could have caused the change that weren’t part of
your product. This can be done informally or formally. The formal version
requires running a multivariate statistical analysis like estimating a
regression model. The informal version means carefully thinking through
what else could have impacted the users and their behavior.


Personally, while I was trained in the formal, econometric approach, I find
that starting with an informal analysis is immensely valuable (even if you
later do the econometric analysis as well). Also, you’ll probably need a stats
person to handle the econometric analysis, but anyone can do an informal
analysis to help gauge how important further analysis is, and as a reality
check on the stats. So here’s how to run an informal analysis of a pre-post
study.


You have measurements of user behavior and real-world outcomes before
and after a change, either when you gave the users the product for the first
time or added a new feature, etc. Subtract the _pre_ from the _post_ : that’s your
working impact number. You also should have a sense of how big of a
change you need for you to care. If you get people to walk two more steps a
day, is that relevant? No. Maybe you only care if the product can get people
to walk at least a hundred more steps a day—it’s not much, but at least it’s
something to build upon. That “when do I care?” number is your threshold.


Now, look for non-product-related things that would have caused the impact
you’re seeing. With pre-post studies, there are a few very common factors.
I’ll use the example of an exercise tracker to make things concrete:


_Time_


Would the time of year, day of month, day of week, time of day, etc.,

matter for this outcome? For example, if you saw that users were

walking more in the spring than in the dead of winter, would that

surprise you? No. So it’s unlikely that your _product_ would have caused

a change you see in walking between winter and spring.


_Experience_


Let’s say you launched your product last month. You’ve just added a

new feature that puts a smiley face on the tracker when users do well. In

a pre-post study, it will be difficult to know if the smiley face caused

increased exercise or if users just gained experience with the product

from its initial launch and slowly exercised more because of that

experience (rather than the smiley face). _Gradual changes over time_ are

often caused by experience; _sharp changes_ in behavior are more likely

to be caused by a change in the product or another external “event” you

can search for.


_Data availability or quality_


Let’s say that in the new release of the tracker, you added a smiley and

someone in the engineering department fixed some bugs in the analysis

of accelerometer data. Walking is up! Hmm. That could be because of

the smiley or because you’re simply getting better data about the users.

I’ve found that data quality issues in particular are often invisible and

therefore often misleading—someone changed something and didn’t

think it was important or didn’t want to admit the previous problem.

Like product changes, data quality and data availability changes are


sharp, sudden changes, so they are very hard to distinguish in a pre-post

study.


_Composition of the population_


Let’s say that with the new release of the tracker, you’ve added lots of

new features and made a big announcement. You see that average

walking is up! Excellent. But that may be because the product caused

people to walk more, or it may be that the announcement of the new

features caused new users to join who were already walking more—and

the new users brought up the average. This occurs in sudden ways (like

product announcements) or through the slow addition and attrition of

users over time. You should counteract this by looking at a specific

group of people before and after the change.


In each case, you’re looking for a gut check—is this a big deal? Measuring
walking behavior in the dead of winter versus in spring is a big deal.
Measuring it from one Tuesday to the next usually isn’t (barring holidays).
A big deal is anything that looks like it’s going to have a large impact on
behavior _relative to what you’re seeing pre-post_ and _relative to the_
_threshold at which you care_ . If the combination of many small things
pushes the likely impact of your product below the threshold at which you
care, then you can usually stop—and move on to something more
promising.


If the pre-post impact is so large that nothing else seems to explain it other
than the product, excellent. You should check your work with a statistical
model and prepare to be surprised; but if you can’t, at least you’ve gotten an
initial estimate of impact.


This informal analysis feeds into formal statistical modeling. Each of the
factors you identify that might be important become variables in the model
—things that you are trying to control for in order to isolate the unique


impact of your product. You’ll need to identify data that measures them and
run the model itself. That’s beyond the scope of this work—but a good stats
person can help.


Seem complex? It can be. That’s why experiments are useful, because they
remove these complexities. But we can’t always run them or get enough
users into the system to get a solid result. And so we sometimes must use
pre-post analyses. When the product has a big effect, and there aren’t many
other things going on that confuse the result, that’s enough to get a signal
for further product development. Another option is cross-sectional
multivariate analysis, which is up next.

### **A Cross-Sectional or Panel Data Analysis of Impact**


In a cross-sectional analysis, you look for differences among groups of
users at a given point. You want to see how their usage of the product
impacts their behavior and outcomes, after taking into account all of the
other things that might be different about the users. For example, you might
look at the impact among frequent users of the application versus infrequent
users. As with pre-post analyses, I usually start with an informal, logical
analysis and then feed that understanding into a formal statistical or
machine learning model if it looks like there’s enough of an impact from the
product to care.3 Cross-sectional analyses usually pull together diverse
groups of people; in order for the analysis to be valid, you’ll need to control
for all of the factors that make those groups different _other than the_
_product._


As before, there are some common differences you need to take into
account. Most importantly is this: why are some people more frequent users
than others? Age, income, prior experience with the behavior, prior
experience with the product’s medium (mobile versus web), selfconfidence, sufficient free time, etc.—all of these are factors that affect the
users’ behavior above and beyond the product.


If there aren’t obvious candidates that explain the difference in behavior
across users, then take the list of factors you generate and plug them into a


statistical model. Again, it’s beyond the scope of this work, but a good stats
person can help.


In addition to cross-sectional and pre-post analyses, one can (and should)
also look at models that examine changes in behavior and outcomes among
many users over time. These models, using _panel_ datasets (or time-series
cross-sectional datasets with many people, but shorter time frames) provide
a much more fine-grained look at behavior. They can pull out impacts of the
product that pre-post and cross-sectional models can’t because they can
control for other differences across the individuals. However, they require
much more data and statistical knowledge.

### **Unique Actions and Outcomes**


Experiments are the best general-purpose and accurate way to measure the
impact of your product. But there’s an important case in which they aren’t
needed to accurately gauge impact. That’s when there is no conceivable
way that the outcome would occur without the product being there.


For example, imagine a new and highly effective cancer treatment. A team
is developing a product to make people aware of it; the target outcome is for
people to use the new cancer treatment. Without that awareness, no one
would know. There’s no comparison group needed—any impact that occurs
is because of the product.


Similarly, it’s easy to measure the _baseline_ impact of the product when the
action only exists in the product itself—which often occurs where the
behavior change process entails the user learning to use a new product.
That’s the benchmark you can use to compare against future changes. After
that baseline has been established, you’ll still need to run experiments (or
use other means) to gauge the impact of new features and other changes to
the application to distinguish the impact of the feature from that of the
existing functionality.


## **What Happens If the Outcome Isn’t** **Measurable Within the Product?**

You can safely skip this section if users take action directly in your product
and you can easily measure the outcome there.


As we briefly discussed in Chapter 12, sometimes the target outcome, and
even the target action, may not be directly measurable in the product. For
example, think about a website that helps users set up an urban vegetable
garden with video tutorials. The target outcome is more vegetable gardens;
the target action is that users set them up (rather than, for example,
contractors being paid to set them up).


Each person who uses the urban garden site is tracked with a cookie or
authenticated login. Each step in the “how to set up an urban garden”
tutorial is tracked. When users complete the tutorial, are they “done”? Did
they complete the action? No. The action that the company wants to drive is
setting up vegetable gardens, not completing a tutorial about setting up
vegetable gardens. The difference between those two could be slight, or it
could be massive if no one actually follows through. Without further
information, there’s no way the company can know if the product is
successful at driving behavior change. Similarly, it has no way of knowing
that the product has caused more vegetable gardens to be set up than there
otherwise would have been.


So what can a company do? If the action or outcome is not directly
measurable with the product, then a _data bridge_ is needed. A data bridge is
something that convincingly connects the real-world outcome with behavior
within the product. There are two basic strategies for building a data bridge:


_Build it yourself_


Find a reliable way to measure the target action and outcome. Then,

build a model of what behavior in the product relates to that action and

outcome.


_Cheat_


Find an academic researcher who has already established the link

between something you can reliably measure in the application and the

real-world outcome. For example, there are numerous studies that

document “overreporting” (lying) about voting when people actually

don’t vote.4 If there isn’t an existing research paper on the topic, work

with researchers to generate one (ideas on how to partner with

researchers are discussed in Chapter 17).


For the rest of this discussion, I’ll assume that you haven’t been lucky
enough to find an existing research paper or interested researcher to do the
work for you—and so you have to build the data bridge yourself.

### **Figure Out How to Measure the Outcome and Action by** **Hook or by Crook (Not by Survey)**


For our sample company that’s encouraging users to set up urban vegetable
gardens, it will need to measure the number of vegetable gardens, plain and
simple. An obvious route would be to ask the participants with a survey.
Not ideal. Surveys are good for gathering facts when people have an
incentive to actually answer the survey but don’t have an incentive to lie.
Imagine that the vegetable garden company asked users of its website, after
a week, whether they set up a garden. Most people wouldn’t answer—
especially those who didn’t set one up. Some would answer truthfully. And
some would answer with, “What will be truthful when they get around to it”
(i.e., they’ll tell a white lie). The company can’t really know which is
which, at least, not without doing additional field research to verify if
people aren’t telling the truth.


If the company asked users about their _intention_ to set up a garden, that
would be even worse. Users would be sorely tempted just to give the
answer that’s expected of them (“Yes, of course!”); that’s called the social


desirability bias in surveys.5 Or, people might honestly believe that they
will set up a garden, but never get around to it. You can try to reduce this
bias in surveys with carefully worded questions, but it’s difficult to know
the success of that effort without verification.


Direct observation is often the best option: either observing the number of
vegetable gardens themselves or other things that uniquely indicate that the
action was taken, like the number of people buying special vegetable
garden supplies within a city. The company doesn’t need to measure every
single action or every time the outcome changes—it just needs to be able to
measure a few times so it can understand the relationship between the
product, the action, and the outcome. So a small pilot study where an intern
goes out and manually counts the number of vegetable gardens in an area is
fine.6


Building a data bridge follows the same rules as creating a benchmark for
the product, described earlier in this chapter. In this case, you’re looking for
the causal relationship between something easily measurable in the
application and a real-world outcome that’s hard to measure, but what you
really care about. If the real-world outcome is unique to the product (i.e., if
_no one_ normally creates vegetable gardens in the area you care about), then
you can do a simple observation of the real-world outcome, after people use
your product, as your metric. If the real-world outcome has multiple
possible causes, you’ll need to use an experiment, statistical model, or prepost analysis.7


In either case, there are three factors to keep in mind when measuring the
real-world outcome itself. These determine how sturdy the resulting data
bridge will be:


_Representativeness_


You want to observe cases that are representative of what “normally”

happens; if you decide to count vegetable gardens in Portland (very

rainy), and most of your app’s users are in Phoenix (rather dry), that

won’t help you generalize much about vegetable garden creation. The


most solid results come from taking your user base and randomly

selecting some of them to directly observe.


_Getting enough data points_


You need to ensure you have enough information to get a solid signal

about what the real-world outcome really is. For example, if you make

only one observation of whether people make a vegetable garden after

saying they will in the app, that’s not going to tell you much about

whether _other_ people will. You need the general percentage of people

who create gardens when they say they will. So how many observations

are enough? There’s no hard-and-fast rule—it depends how important

the accuracy of the estimate is to the company. For experiments, we

discussed in detail how you compute sample sizes. If you’re not using

experiments, you can use online tools for computing _confidence_

_intervals_,8 which tell you how confident you can be in your estimate; if

you build a statistical model of the relationship, that will also provide

you with confidence intervals.


_Getting a baseline_


Sometimes things happen in the real world that have nothing to do with

your product. I know, it’s hard to believe. Some people will create

vegetable gardens on their own, even without the vegetable garden app.

So when you’re observing your real-world outcome, include some cases

in which people don’t use the app. This is important if you’re doing a

simple model in Microsoft Excel or if you’re running a full experiment

to build your data bridge.


If these options fail, and there’s really no way to measure the product’s realworld outcome, then the rest of this discussion about impact can’t help.
That signal—what’s actually happening in the world—is essential for
keeping the whole process honest.

### **Find Cases Where You Can Connect Product Behavior to** **Real-World Outcomes**


Now you have measurements of actions taken within the product and of
real-world outcomes (though perhaps imperfect measurements). How can
you connect the two? You can connect them at the individual level or at an
aggregated level. At the individual level, for example, the urban gardening
app could ask for users’ names and addresses to connect their behavior in
the product to whether they actually have a vegetable garden (send the
intern to their home and mark it down in the record). Getting data about
individual users is the ideal—as long as the data meets the standards
(representative, sufficient in size, and with a clear baseline).


Alternatively, the action and outcome can be measured as an aggregate, a
known geographic area or a known group of people. If you know that a
certain set of users in the product correspond to the known area or group
(even if you don’t know who is who) and you can measure the actions and
outcomes reliability in that area or group, you’re in business. As we’ll see,
it’ll be more challenging to figure out exactly what is going on, but you can
do it.

### **Build the Data Bridge**


A data bridge brings together something you know and can measure
frequently (user behavior within the application) with something you have
measured only a few times (the impact of the product on the real-world
target outcome). It allows you to estimate how much the target outcome has
probably changed based on behavior within the product. You’ll estimate
that relationship by running a pilot project that gathers both datasets:


1. Take a circumstance in which you can reliably connect user

behavior in the product with the real-world outcome or action, as
we’ve just described.


2. Measure the causal impact of the product on the real-world

outcome or action using an experiment (ideal), statistical model,
pre-post analysis, etc.


3. Analyze the various user behaviors that occur within the

application and identify one or more that is strongly related
(correlated) to the application’s causal impact. If a statistician is
available, use a mediation analysis.


4. When the indicative user behavior occurs within the product, build

a model (in Excel or in a statistical package) of how much that
changes the target outcome. That’s the data bridge.9


5. In the future, whenever you see the behavior in the product, use

your model to estimate the likely impact on the target outcome.


For example, the urban gardening site runs a pilot study where it takes two
sets of randomly selected people and offers its program to one group and
not the other. Some of the people in the first group completed the training
program; some did not. An intern visits the homes of everyone in the study
and measures the truth. The company finds that 65% of people who were
offered the program created a garden, and 90% of those who were offered
the program _and completed their training within the application_ created
gardens. Meanwhile, 15% of those who weren’t offered it nevertheless
created a garden. Those three stats provide a basic understanding of how to
interpret user behavior on the website in the future.


The company would improve the chance that a person will set up a garden
by 50 percentage points (from 15% to 65%) if it _offers_ the person its
training program. It will improve the chance that the person will set up a
garden even more if it can convince them to complete the training
program.10 The company can get a precise estimate of that impact using
what’s known as a mediation analysis on the experiment.


In short, if your target outcome is something outside of the product and not
directly measurable, then you’ll need to build a data bridge. The easiest way
to do that is to find an existing research study that documents the
relationship you’re looking for—like between the intention to plant a
garden and the actual act of doing so. If not, look for a case in which your
team can directly observe the users’ behavior and compare the things they
do or say in the product to what they actually do in the real world. That’s
your data bridge. In the future, you can use that relationship to estimate how
much of an impact you’re having based on what you see in the application
and iteratively improve your product for greater impact.

## **Putting It into Practice**


Here’s what you’ll need to do:


In a pre-post analysis, look for discontinuities in behavior and
outcomes at the moment the new feature or communication was
deployed. The sharper the change and the fewer alternative
explanations there are for that change, the more confidence you
can have that your intervention was the cause.


In a cross-sectional or panel-data analysis, look for other people in
as similar a situation as possible who didn’t receive the
intervention to compare against. Again, the goal is to remove
alternative explanations for any differences you see in behavioral
outcomes.


The text describes the logic behind measuring impact without an
experiment, and if you have a unique action or outcome, that can
be enough. Usually, however, you need a trained stats person to
carefully analyze the data and statistically control for (eliminate)
alternative explanations.


How you’ll know there’s trouble:


There’s no clear definition of success and failure for the product’s
attempt to change behavior. If so, return to Chapter 6.


Many other things changed within your product or user base at the
same time as your new feature or communication—making it
difficult to eliminate alternative explanations for behavioral
outcomes.


You have a complicated environment, no experiment, and no stats
person to analyze the data. Don’t try to wing it and look at bar
charts or line graphs over time—behavior change is just too
complicated.


Deliverables:


A clear measurement of the product’s impact!


1 Now, before you dismiss this experience as one limited to a particular set of studies, a recent

review of research where the authors preregistered (wrote down and published) their
hypotheses before they conducted a study found that over 50% of studies in biomedicine and
psychology did not show the results that researchers expected (Warran 2018). Johnson et al.
(2017) estimate that 90% of research efforts in psychology overall (i.e., including those that
aren’t preregistered) had null or negligible results. And, again, before you dismiss this as a
researcher’s problem, remember that famous researchers like Edison and Dyson iterated
hundreds or thousands of times before generating successful products (e.g., Syed 2015).


2 [Pontefract (2018)](https://oreil.ly/wXBcD)


3 There are often many possible changes to the product you want to analyze—so focusing too

long on features that don’t appear to change behavior in practically significant ways means
you’re wasting time that could be used more valuably elsewhere. This is a difference from
academic social science work in that researchers usually devote a significant amount of time to
a single question; because of a lack of data, they usually don’t have a long list of alternative
questions that can be explored immediately.


4 Silver et al. (1986)


5 Fisher (1993)


6 By the way, if the area is large, I imagine that the best way to do this would be access

government or commercial satellite imagery. Professional geographers have worked out
amazing algorithms to automatically detect vegetation cover, and even the type of vegetation.
The GeoEye satellite that is used by Google Earth, for example, _measures down to increments_
_of 16 inches._


7 To clarify—at this point we’re just talking about how to measure the real-world outcome.

That forms half of the data you need to run an experiment, do a pre-post analysis, or build a
statistical model of the relationship between the real-world outcome and user actions in the
application. That process is what actually creates the data bridge and is covered later. But it
helps to plan ahead for the _type_ of analysis you will be running to ensure you’re gathering the
right data you need when measuring the real-world outcome.


8 For example, you can use for calculating confidence intervals of proportions (percent of

people creating vegetable gardens) and for calculating confidence intervals of quantities
(number of pounds lost after an exercise program). Penn State has a nice summary of the
underlying math.


9 In the simplest case, you might look at the simple linear relationship between the real-world

impact and user behavior in the product. But there’s no reason to limit the analysis to a linear
relationship. You want to build a model that most accurately describes the relationship between
behavior in the product and outcomes in the real world.


10 Exactly how much additional improvement might occur would require additional analysis, to

separate out the self-selection into the program from the program’s causal impact.


# **Chapter 15. Evaluating Next** **Steps**

_Throughout the first decade of the 21st century, microcredit was hailed as a_
_broad solution to poverty worldwide. Low-income people, especially in_
_developing countries, were offered small, often unsecured loans, at rates_
_ranging from a few percentage points to over 100% a year. Many of these_
_programs focused on enabling poor women to become entrepreneurs,_
_providing loans to groups of women at a time who would support and hold_
_each other accountable. The idea was that if motivated but cash-poor_
_women simply had access to capital, they could start or grow their_
_businesses and lift themselves out of poverty._


_[As U2’s Bono said of the microcredit, “Give a man a fish, he’ll eat for a](https://oreil.ly/GrHrp)_
_day. Give a woman microcredit, she, her husband, her children, and her_
_extended family will eat for a lifetime.”_ 1 _One of the most prominent_
_microcredit organizations, Grameen Bank in Bangladesh, and its founder_
_Mohammad Yunus, in fact won the Nobel Prize in large part for their efforts_
_to alleviate poverty through microcredit. In 2008, for example, Grameen_
_Bank had over seven million borrowers, 97% of whom were women, with_
_[over $500 million USD in loans outstanding](https://oreil.ly/8FOvQ)_ .


_When I was in graduate school in 2005, microcredit was a shining example_
_of innovative work for social good: many of my friends went into careers in_
_microfinance (as the broader field is known), as nonprofits, private_
_companies, and governments all around the world were excited about its_
_potential. Microfinance was the place to be if you wanted to devote your life_
_to helping others on a massive scale._


_That picture soon changed._



_A series of studies found that the impact of microcredit was not nearly as_
_universal and transformative as many had hoped. Dean Karlan and Jacob_
_Appel summarize these lessons in their book More Than Good Intentions_
_(Penguin, 2011), citing a study in India, for example, in which “it looked_
_like people were, on the whole, no wealthier than before” and that “the_
_most common reason for borrowing was to pay off other debt.”_ 2 _Karlan_
_and Appel share how the impacts of microcredit were simply much more_
_nuanced than had been portrayed; some people (especially existing_
_business owners) could benefit, but perhaps in nonobvious ways (helping_
_them cut costs, not hire new people); in other cases, people were simply left_
_with debt they couldn’t afford to pay off. “They wound up looking more like_
_characters from a cautionary tale about, say, credit card debt, than the_
_inspiring figures of microcredit literature.”_ 3


_In a highly cited 2015 paper, Banerjee, Karlan, and Zinman presented six_
_randomized control trials on the impact of microcredit and concluded, “We_
_note a consistent pattern of modestly positive, but not transformative,_
_effects.” In that paper and in related writings,_ 4 _they found that while the_
_broad effects were overblown, relatively small changes to microcredit_
_programs could make them far more powerful, like adding flexibility in_
_repayment periods. In other words, they used the power of rigorous_
_measurement not simply to cut down and critique—but to refine._


_If we think about microlending as a product, one that sought to accomplish_
_a specific purpose for its users (lifting them out of poverty, often with the_
_assumption that would occur through debt-financed entrepreneurship), it_
_didn’t hit the mark with its first iteration. However, by digging into the data_



2



3



_In a highly cited 2015 paper, Banerjee, Karlan, and Zinman presented six_
_randomized control trials on the impact of microcredit and concluded, “We_
_note a consistent pattern of modestly positive, but not transformative,_
_effects.” In that paper and in related writings,_ 4 _they found that while the_
_broad effects were overblown, relatively small changes to microcredit_
_programs could make them far more powerful, like adding flexibility in_
_repayment periods. In other words, they used the power of rigorous_
_measurement not simply to cut down and critique—but to refine._


_about who used it, who benefited from it, and under what specific_
_circumstances, we can learn how to better target users and make it more_
_effective overall._


That is what we’ll explore starting in this chapter: how to gather the data
you need, and identify areas to improve, to increase the impact of your
product.


Before we do so, however, one final note: More Than Good Intentions is
one of the three books I recommend to every person who asks me about
exploring behavioral science. Sadly, the promise and perils of microcredit is
just one of many examples the authors give of well-meaning people putting
their hearts and souls into untested products that they thought were
wonderful—until they discovered otherwise. Since I read it many years ago,
it’s served as a haunting reminder that my own intentions to do good simply
aren’t enough. We all need to rigorously measure, to humbly look at our
products, and to ask: how can we do better?

## **Determine What Changes to Implement**


At the end of each cycle of product release and measurement, the team will
have gathered a lot of data about what users are doing in the product and
potential improvements to it. Continued obstacles to behavior change are
only one source of those product improvements. Business considerations
and engineering considerations must also be reviewed. It’s time to collect
the potential changes from these diverse sources and see what can be
applied to the next iteration of the product. I think of it as a three-step
process:


1. _Gather_ lessons learned and potential improvements to the product.


2. _Prioritize_ the potential improvements based on business

considerations and behavioral impact.


3. _Integrate_ potential improvements into the appropriate part of

product development process.


### **Gather**

First, look at what you learned in the two preceding chapters about the
current impact of the product and obstacles to behavior change. What did
users struggle with? Where was there a significant drop-off among users?
Are users returning to the application or only trying it once or twice? Why
does that appear to be happening?


1. Start by picking the low-hanging fruit. List the clear problems with

a crisp follow-up action; for example, no one knows how to use
page Y.


2. Then, write down the lessons that are more amorphous; for

example, users don’t trust the product to help them to change
behavior. Maybe the team has started thinking about potential
solutions, but there’s more work to be done. The next step is to
further investigate what’s going on and settle on a specific solution
to resolve the problem.


3. Next, gather lessons about the core assumptions of the product:


Does the target action actually drive the real-world
outcomes that the company seeks? For example, maybe
walking a bit more each day isn’t enough to reduce heart
disease among the target population, and a stronger
intervention is needed.


Are there other actions that appear to be more effective?
Could the product pivot to a different action that is more
effective?


Are there major obstacles in the user’s life, outside of the
product, that need to be addressed? Looking again at the
causal map, what major factors that are currently outside
of the product’s domain are counteracting the influence of
the product? If exercising more leads the person to also
drink more alcoholic beverages (as a “reward”), is that


defeating the product’s goals? To design for behavior
change, we care about the net impact of the product, not
just the intended consequences. Is there anything the
product can do about that countervailing force, or is it just
a fact of life?


4. Finally, look beyond the specific behavioral obstacles and impact

studied in the previous two chapters. The team has probably
generated numerous ideas for new product features or even new
products. Collect them. Other parts of the company will also
suggest changes to the product as well: changes designed to
increase sales, improve product branding, resolve engineering
challenges, and so on. Behavioral considerations are just one
(vital!) element in the larger review process.


Lessons and proposed improvements can come at different times during the
product development cycle—from early user research to usage analysis
after the product is released. Some lessons will only come at the end, during
a formal sprint review or a product postmortem. I suggest creating a
common repository for them, so that ideas don’t get lost. That can be
someone’s email box, a wiki, or a formal document of lessons. In an agile
development environment, they should be placed in a project backlog.

### **Prioritize**


In any product-development process, there is a point at which the team
needs to decide what to work on in the future. The prioritization process
should estimate the behavioral impact of major changes to the product: how
will the change affect user behavior, and how will that affect the product’s
outcomes in the real world? Since the product is designed for behavior
change, these behavioral impacts will likely have knock-on effects on sales
or the quality of the company brand. Naturally, the prioritization will also
incorporate business considerations (will the change directly drive sales or
company value?), usability considerations (will it make the users happy and


reduce frustrations, hopefully driving future engagement and sales?), and
engineering considerations (how hard will it be to implement the change?).


The team should ground its assessment of behavioral impact in real data;
the drop-off numbers at each step of the user’s progression and the
behavioral map allow the team to make a quick estimate of how large of an
impact a change in the product should have. That helps the team answer:
how big of a problem does this change really address? What _very rough_
change in the target behavior and outcomes do we expect from it? Even if
the proposed change to the application wasn’t driven by a behavioral
concern—for example, if it came from a client request during a sales
conversation—it should be evaluated for its possible behavioral impact. It
may have the added benefit of helping improve user success at the target
behavior, or _it may distract the user and undermine the product’s_
_effectiveness._


The weight of each of these considerations—business, behavioral,
engineering, etc.—in the company’s prioritization will vary, and there’s no
hard-and-fast rule.

### **Integrate**


Your company has a prioritized list of changes to the product (including
open questions that need to be answered) and a sense of how difficult each
piece is to develop. Now, separate out changes that require adjusting core
assumptions about the product and its direction from less fundamental
changes that keep the same direction. If the change entails targeting a
different set of users (actors), a different target action, or, especially, a
different real-world outcome, then those go into the first bucket. If the
change entails a new product or new product feature, where there are major
unknowns, it also goes in the first bucket. Everything else can go into the
second bucket.


Here’s one of the few places I take a strong stand on the productdevelopment process—items in the first group, with changes to core
assumptions or major new features, need to be separately planned out by the


product folks before they are given to the rest of the team. Even in an agile
development process, core product planning shouldn’t be done in parallel
with the rest of the process; that’s the same dictum that Marty Cagan, in
_Inspired_ (SVPG Press, 2008), gives in his analysis of product management.
It’s just too much to determine what to build and how to build it at the same
time.


When designing for behavior change, core changes to the product require
updating the behavioral map. They may also require updating the product’s
outcomes, actions, and actors. In other words, they require another cycle of
the full discovery or design process, starting with Chapter 6 or 7 of this
book. Everything else can go directly into crafting new interventions,
starting with Chapter 9.


Each time the core assumptions—actor, action, and outcome—are changed,
they should be clearly documented, as described in Chapter 6. Then the
behavioral map should be updated. This formalism helps the team pull
problems into the present—rather than let them lurk somewhere in the
future, only to be found after significant resources have been developed.
Making the assumptions and plan clear up front is intended to trigger
disagreements and discussion (if there are any underneath). It’s better to
find those disagreements sooner rather than later.


When a core problem—like a particular step in the sequence of user actions
—is confusing users, there’s a natural tendency to settle on a proposed
solution and just get it done (i.e., a “fix” is often implemented before
vetting and testing the problem). But human psychology is tremendously
complex, and trying to build a product around it is inherently error prone.
There’s no reason to think that the _proposed solution_ is going to be any less
plagued by unexpected problems than the previous solution. The discovery
process—documenting the outcome, action, and actor, and then developing
the behavioral map—is one way to draw out the unexpected and provide
opportunities to test assumptions early. It’ll never be perfect, but it’s a
whole lot better than just shooting from the hip.


## **Measure the Impact of Each Major Change**

Each major change to the product should be tested for its impact on user
behavior; measuring changes in impact should become a reflex for the
team. It’s not always easy to stomach, but it’s necessary. That way, the team
is constantly learning and checking its assumptions about the users and the
product’s direction. As we’ve seen, small changes in wording and the
presentation of concepts can have major impacts on behavior; if we’re not
testing for them, we can easily and unintentionally undermine the
effectiveness of our product. But without a reflex to always test, testing the
marginal impact of changes can raise all sorts of hackles and resistance.


Let’s look at some of the issues that can arise and how to handle them:


_Most tests will (and should) come back showing no impact_


Many people get frustrated at test results that come back with no clear
difference between the versions they’re testing and call that “failing.”
Assuming you designed and ran the test correctly, a “no difference”
result should be celebrated. It tells you that you weren’t changing
something important enough for the test to have found a difference.
Either be happy with what you have, or try something more radical. It
saves you from spending further time on your current approach to
improving the product.


What’s a well-designed test? It’s one where you’ve defined success and
failure beforehand. It’s not one where you go searching for statistical
significance (or a “strong” qualitative signal). For example, let’s say
you have a potential new feature/button color/cat video. How much of
an impact does it need to have before you care? If you improve impact
by 20%, is that your threshold for success? Is it worthwhile to work on
this further if you’re only getting a 2% boost? That definition of success
and failure, along with the amount of noise in the system, determines
how many people you need in the test. If you get a result of “no
difference” from the test, that doesn’t necessarily mean there’s no effect;
it means there’s no effect _that you should care about_ . You can move on.


_A/B tests in particular seem to mean you’re showing some people a “bad”_
_version_


If you have a good UX team, then most of the time, no one really knows
if a _change_ in the app will improve it. You can’t accurately predict
whether the new version will be better or worse. You usually are
showing a “bad” version; the problem is that you don’t know which one
it is! Our seemingly solid hunches are usually random guesses,
especially when we have a good design team. There are two reasons
why.


First, a good UX team will deliver an initial product that is well
designed and will deliver product improvements that are also well
designed. We all make mistakes, but a good design team will get you in
the right ballpark with the first try. By definition, further iterations are
going to have a small impact relative to the initial version of the
product. Don’t be surprised that new versions have similar results
(impact, etc.) to earlier versions—celebrate the fact that the earlier
version was a good first shot.


Second, human behavior is just really confusing. As we’ve seen
repeatedly throughout this book, we just can’t forecast exactly how
people will react to the product. In familiar situations, we can and
should use our intuition about a set of changes to say which one is likely
to be better—like when we’re applying common lessons we’ve learned
in the past. But when you have a good design team, the common lessons
have already been applied. You’re at the cutting edge, and so your
intuition can’t help anymore. That’s why you need to test things, and not
rely (solely) on your intuition.


_Does planning for tests imply you’re not confident in the changes you’re_
_proposing?_


This is another issue I’ve heard, and it’s a really tricky one. You
naturally expect that any changes that you’re planning to make to the
product will improve it. But that’s often not the case (since it’s hard to


make a good product better, and human behavior is inherently
complex).


That sets up a problem of cognitive dissonance, though. It’s very
uncomfortable to think that some of the changes you’ve carefully
planned out, thought about, and _decided will help_ are actually going to
do nothing—and you don’t know which ones those are! It would be like
you’re admitting a lack of confidence in the changes that you’ve already
advocated. So a natural (but dangerous) response is to plow ahead and
decide that testing is not needed.


There’s no simple solution to address this situation—the need to
confidently build something you shouldn’t actually be confident in. The
best approach that I’ve come across is to move the testing process out of
the reach of that cognitive dissonance. Make testing part of the culture
of the organization; make it a habit that’s followed as standard
procedure and not something that the organization agonizes over and
debates each time a new feature is added.


Alrighty. Those are three of the major issues I’ve confronted as teams
explore testing incremental changes to their product. Thankfully, it’s not
difficult to actually measure incremental impact. If you created a
benchmark of the product’s impact in Chapter 12, then all you need to do is
to reapply the same tools here: experiments, pre-post analyses, and
statistical models.

### **Qualitative Tests of Incremental Changes**


I didn’t mention qualitative research in Chapters 13 and 14, when we were
establishing a benchmark of the impact of the product on user behavior and
real-world outcomes. That’s because it’s difficult to generate a repeatable,
reliable ROI metric of real-world impacts using most qualitative methods.
But qualitative research can be quite valuable when you want to quickly
judge how users are responding to a change in the application.


Put the revised application in front of users during user interviews, user
testing (speak out-loud methods), or even focus groups. If you get a clear
signal about whether the change has caused problems, you’ve just saved a
lot of time. You can get feedback and insight in a fraction of the time it
would take to test the product change with an experiment or pre-post
analysis. While I am a big proponent of experiments (and statistical
modeling), the benefit in terms of speed and depth of understanding from
qualitative testing is too much to ignore. Of course, the team should have
already performed a round of qualitative testing on the prototypes before
the change was made to the product itself too.

## **When Is It “Good Enough”?**


Ideally, the outcome of any product development process, especially one
that aims to change behavior, is that the product is doing its job and nothing
more is needed. When the product successfully automates the behavior,
builds a habit, or reliably helps the user make the conscious choice to act,
then the team can move on. There are always other products to build. And,
for commercial companies, there are always other markets to tap. So, how
can the team tell when it is good enough?


Return to the product’s target outcome and try to stop thinking about the
product itself. What’s the target level (or change in the target) that the
company decided would count as success? If the product currently reaches
that threshold, wonderful. Forget the product’s bugs. Forget the warts in the
design. Move on to address other challenges. If the current product doesn’t
yet meet that threshold, what is the best alternative use of the team’s time?
If the alternative is more beneficial to the target outcome and can be
achieved with similar resources, the team should switch its focus.

## **Putting It into Practice**


Here’s what you’ll need to do:


Gather all of the proposed product changes—changes to improve
the behavioral impact of the product and other changes suggested
by sales, marketing, or other parts of the company.


Prioritize the changes based on the company’s and user needs and
their likely impact on the user behavior.


Measure the impact of each major change to the product, using the
same tools outlined in Chapters 13 and 14. Make incremental
measurement part of the culture of the company.


How you’ll know there’s trouble:


Major changes are planned for the product without assessing their
likely impact on user behavior.


The team is afraid to test the new feature, because the tests usually
come back negative or testing would imply a lack of confidence.


Deliverables:


A new and (ideally) improved product!


1 h/t Karlan and Appel (2011) for the quote.


2 [Banerjee et al. (2015)](http://doi.org/10.1257/app.20130533)


3 Ibid. 81.


4 [For example, Karlan et al. (2016).](https://oreil.ly/BIkbY)


# **Part III. Build Your Team and** **Make It Successful**


# **Chapter 16. The State of the** **Field**

_The common spaces are flooded with light and greenery, following_
_behavioral research on well-being. The apartments empower their residents_
_to control their layout and reconfigure them as their needs change. There’s_
_a single switch by the bed that turns off all of the appliances and electronics_
_at once—removing friction and decision points. The shower heads light up_
_after five minutes to remind users of the costs to themselves and the_
_environment. Welcome to the “Paris Nudge Building,” the Bains Douches_
_Castagnary._


_In 2015, Paris’s Mayor Anne Hidalgo announced a new architectural_
_competition to help “Reinvent Paris,” looking for “innovative urban_
_projects to build what the Paris of tomorrow might be.”1 The BVA Nudge_
_Unit partnered with French real-estate firm OGIC, sustainable development_
_firm e-Green, and others to apply behavioral research to redesign an_
_existing apartment building, the Bains Douches Castagnary._


_To design the building, the team drew on a growing body of work on_
_behavioral science and the built environment: how architecture influences_
_our well-being, emotions, and behavior. They interviewed residents of the_
_area to better understand what was important to them—such as being in_
_community, and respecting the environment—and how they sometimes_
_struggled to fulfill these goals. They then designed, field tested, and_
_ultimately implemented these ideas throughout the building._


_In 2019, residents started moving in, and the team is measuring the impact_
_of their interventions over the next decade, to see whether they have been_
_successful or not._


By now, you’ve probably gotten a sense of just how broad the application
of behavioral science has become, from helping young mothers at risk of


homelessness to dark patterns used to manipulate customers in troubling
ways to an entire building designed around behavioral economics principles
to help its occupants live healthy lives. In this chapter, we’ll review scope
of behavioral science around the world—the good and the bad—thanks to a
new survey of behavioral teams.


If you already have a team in place, this chapter can help you learn from
what other likeminded groups are doing. If you don’t have a team in place,
this chapter and the next one are meant to get you started on the career path.
The book thus far has focused on the _process_ of applied behavioral science;
the next two chapters focus on the _organizational structure_ that enables
applied behavioral science.

## **What We Did: A Global Survey of Behavioral** **Teams**


Eight years ago, only a small set of finance, health care, and Silicon Valley
technology companies were applying behavioral science in their work.
Now, the picture is quite different. At least four hundred companies and
nonprofits organizations now have behavioral scientists on staff, in addition
to long-standing groups of traditional psychologists working in the private
sector. These teams are diverse. For example:


A 12-person behavioral analytics and experimentation group at
Uber, which studied the transportation behavior of millions of
people


Two powerhouses of data-driven international development, J-PAL
and IPA, applying behavioral science to the everyday problems of
sanitation and health and safety all around the world


Numerous single-person behavioral consultancies, especially
within the realm of marketing


Google’s People Analytics group, including in-house behavioral
scientists working to improve employee benefits and well-being


To better understand the range of teams out there, and their experiences, I
helped organize the largest known survey of behavioral science teams in the
world. We received detailed responses from more than two hundred distinct
organizations across 54 countries ranging from the United States to Kenya
to Saudi Arabia. In this chapter, we’ll dive into the results to better
understand the current state of the field.


The Behavioral Teams survey was a joint project between two nonprofit
organizations in the field—the Behavioral Science Policy Association
(BSPA) and the Action Design Network (ADN)—and myself. Starting in
June 2019, we drafted the initial survey and then tuned and distributed it in
the field. We promoted it through our own direct contacts, social media, and
email lists in the industry. The survey launched on July 23, 2019; the last
response included here was entered on December 23, 2019. The survey was
written and promoted only in English.


The survey’s target population was people who work on teams applying
behavioral science to the development of products, communications, or
policies, in other words, the same audience as for this book, plus
policymakers.


_[Figure 16-1. The Behavioral Teams home page, inviting people to participate in the international](http://www.behavioralteams.com/)_

_survey_


The survey consisted of three main sections:


Section 1: Contact information and basic information about the
team, to support a public directory of behavioral science teams.
This includes the type of organization (company, nonprofit,
academic, or government organization), the number of people on
the team, their primary location, and their formal training in
behavioral science (if any).


Section 2: Questions on the work of the team, such as the types of
behaviors they seek to change, the techniques they use, their
manner of validating results, and the roles of each member on the
team.


Section 3: Questions about the challenges and successes of each
team.


An archived copy of the survey, and the public directory of teams around
the world, can be found at _[www.behavioralteams.com](http://www.behavioralteams.com/)_ .


After cleaning the data and removing invalid responses, the resulting
dataset provides detailed information about 231 organizations, across 253
individual respondents.2


Currently, there is no exhaustive list of organizations applying behavioral
science to their work. Thus, it’s not feasible to conduct a statistically
representative survey of the field or to know the precise coverage of the
survey relative to the entire field. However, two other, independently
created lists of behavioral science teams can help us estimate that coverage.
Ingrid Melvær Paulin, senior behavioral scientist at Rally Health, and Faisal
Naru, head of strategic management and coordination at the executive
director’s office of the OECD, each maintain a list of organizations,
focusing particularly on private-sector companies and on government
organizations, respectively. We combined the organizations from each list
and found that the resulting directory covered 529 unique organizations,
approximately 44% of whom responded to the detailed Behavioral Teams
survey.3


In the following sections, we’ll offer the most comprehensive look yet at
the scope of the field (based on the directory of organizations) and detailed
look at the makeup, tactics, and operations of these teams (based on the
survey).

## **Who’s Out There?**


Using the directory of behavioral science teams mentioned before, we find
that teams applying behavioral science to the development of products,
communications, and policies are heavily concentrated in three countries
(among the 526 teams with known locations): the United States (217), the
United Kingdom (77), and the Netherlands (30).


Many of these companies are international, with offices all around the
world: for example, Walmart, Coca Cola, and Ipsos all have behavioral
science teams and a global presence. For survey respondents, we asked
them to provide the location of their behavioral science team. Where no
location was given (e.g., for data pulled from other nonsurvey lists of
organizations), we used the company’s headquarters location.


While behavioral science took off in the last two decades in the US and UK,
together they hold only a slim majority of the teams out there. Today, the
range of teams includes:


The Busara Center, based in Kenya and with offices in eight
countries, which combines academic research with consulting for
major companies across the developing world.


Nudge Rio, a small behavioral science unit in the provincial
government of Rio, Brazil.


The Reinsurance Group of America, pioneering a “Behavioral
Approach to Insurance”. [4]


_Figure 16-2. The distribution of behavioral science teams around the world_


What types of teams are there? The majority of behavioral teams are within
companies—333 of them, in fact (64%, _N_ = 520 with known type); 81
different academic institutions have been identified, as well as 60
government institutions and 46 nonprofit organizations.


_Figure 16-3. The proportion of behavioral teams, by type_


Relative to the directory of organizations, the Behavioral Teams survey had
an overrepresentation of US-based teams (43% of respondents, versus 41%
in the directory), an underrepresentation of teams in the UK (8% of
respondents, versus 15% in the directory),5 and an underrepresentation
among private companies (58% of respondents versus 64% in the
directory).


For the rest of the analysis, we will focus on the respondents to the
Behavioral Teams survey since that is where we have detailed data.
However, we should keep in mind that the broader field is at least twice this
size, with a strong concentration in government organizations not covered
here.


This survey best represents behavioral teams in companies and nonprofit
organizations, and unless otherwise noted, we’ll restrict the analysis to the
primary respondent6 at each company or nonprofit organization: 161 out of
the 229 organizations that completed the survey with a known
organizational type. Putting this in the context of the combined worldwide
list, 42% of all known companies or nonprofits with behavioral teams
completed the survey.


## **Where the Interest Lies**

The Behavioral Teams survey focused on dedicated groups of behavioral
scientists (or other behavioral designers) within organizations. That’s an
important segment to understand, but we can see hints that the interest in
and application of behavioral science is actually much broader. Let’s take a
look at these dedicated teams and the potential landscape beyond them in
turn.

### **The Dedicated Teams**


How big are dedicated behavioral teams within companies and nonprofit
organizations? There is a wide variety, but most of the respondents came
from small teams: median team size is four; the largest team was under two


hundred in our survey (N = 153). Well over half (59%) of these
organizations say that behavior change is explicitly part of the
organization’s goals and mission—often because the behavioral change
team _is_ the organization. For example, many small behavioral science[focused consultancies have popped up over the years, from The Behaviorist](https://oreil.ly/knZLv)
[in Canada to Habbitude in Spain.](https://oreil.ly/1P-_w)


How big is the field? The respondents represented teams with 1,216
members and indicated that another 815 individuals applied behavioral
science on other teams within their companies.7 Combining these figures
and assuming that the survey represented 42% of the worldwide total (see
above), we can very roughly estimate the total worldwide employment
within companies and nonprofits. These teams, specifically identified as
applying behavioral science, appear to employ roughly 4,840 people.



That number may feel surprisingly low, given the high-profile teams at
Walmart, Pepsi, and other major brands. However, we should be wary of
generalizing from these teams, if nothing else because of the availability
heuristic. Even within these companies, the teams are generally small.
Further, the largest dedicated behavioral teams in the world, including the
Behavioural Insights Team in the UK and ideas42 in the US, employ fewer
than two hundred people each.8 The largest-known development agencies
focusing on applied behavioral science, the Abdul Latif Jameel Poverty
Action Lab (J-PAL) at MIT and Innovations for Poverty Action (IPA) at
Northwestern and Yale, are not much larger—and many of their staff
members are not directly applying behavioral science in a meaningful way
or are academic professors.9



8



9



Given the newness of the field, this isn’t too surprising. The following
graph shows when each of the behavioral teams started. With the exception
of a few pioneers in the field like Paul Slovic’s Decision Research in
1973,10 the real growth only started in 2013; 2% of teams started before the
year 2000 and 87% started on or after 2013.


_Figure 16-4. Starting date of behavioral teams_


That said, we can expect continued new entrants, and growth among
existing teams. In the next year, the median behavioral team expects to
expand by 25% (average increase is 52%), which if it held true would entail
a growth of 1,208–2,515 roles next year. We should take such projected
hiring with a large dollop of salt, but nevertheless even these optimistic
numbers would result in a larger but generally small field. To put these
numbers in perspective, there are roughly 200,000 psychologists in the US
alone.

### **The Nondedicated Teams**


The dedicated teams covered by the survey should be thought of as a small
portion of the total population of people interested in applying behavioral
science to their work. A few anecdotes can help us make this distinction
between dedicated teams, and broader interested population, clear. The
Action Design Network, a small nonprofit organization that I founded in
2013 to promote behavioral science, has more than 16,000 people signed up
for our events around North America. Similarly, the first edition of
_Designing for Behavior Change_ sold many times more than our estimate of
total employment in the field. And to be frank, this book is for an interested
practitioner audience; it’s not something that a general audience would
normally buy (sadly, for my publisher!). Nir Eyal’s first book, _Hooked_,


which could appeal to a somewhat larger audience but still was squarely
focused on the psychology of product development, was picked up by
approximately 300,000 people.11


It is likely within the broader design, product management, marketing, and
to a lesser extent, human resources communities where the interest lies.
These communities are huge, with over half a million graphic designers
alone.12


There are thus two significant gaps: the number of people actively
interested in applying behavioral science to product and communications
development is much larger than formal employment in the sector.
Similarly, the field of people who could be interested (other designers,
product managers, etc.) is much larger than those who have expressed an
interest (at least according to these anecdotal numbers).


What does this mean for someone looking to enter the field? The short
lesson is that joining an existing, dedicated team will be difficult. Instead,
one should look at either starting a new behavioral practice within a
company or applying these lessons as part of one’s larger work, especially
as a product manager, designer, or marketer.


With that, let’s look at how these teams get started and what we can learn
from them.

## **A Broad Range of Application**


We’re now seeing behavioral science teams around the world and in a wide
range of disciplines. Let’s look next at how these teams are formed, their
business model, placement within their organizations, and the specific
behavioral problems they are looking to solve.

### **Origins**


How do behavioral teams get started? There’s no single path. Our
respondents described a mix of bottom-up and top-down approaches—from


starting a new small company specifically geared toward behavioral science
(29%) to a CEO or department head driving it (22%, 18%) to individual
contributors making it part of their work and growing from there (17%).
What was _uncommon_, however, was someone outside the company
convincing the company to start one (3%); that is, behavioral (organization)
change comes from within.13 That is how it happened in my case, at both
HelloWallet and Morningstar; I was already an employee of each company
and started our teams from within.

### **Business Model**


Among the 161 dedicated teams in companies and nonprofits who filled out
the survey (and among the 379 organizations in the overall directory that we
identified as such, using web searches and prior knowledge), there is a
considerable diversity. Roughly speaking, though, we can divide them into
two big categories: consulting companies (28%) and companies that apply
behavioral approaches to their own products and services (72%). The vast
majority of employment in the field, according to our survey at least, is in
consulting, specifically in consulting companies in the United States, the
United Kingdom, and the Netherlands. Three of the top five largest teams in
the directory are all nonprofit consulting organizations: the UK’s
Behavioural Insights Team, ideas42 (in the US), and the Busara Center
(based in Kenya).

### **Placement**


In terms of where teams are located within the organization, and putting
aside those who are in external consulting (33%), the most common
placement was data science (26%), followed by product (20%), design
(18%), and marketing (14%).


When it comes to the individuals on the team, 52% said that they had a
formal degree in behavioral science ( _N_ = 155). Among the others, 85%
learned through books, 80% on the job, or through formal coursework


(41%) or informal online classes (59%) that did not result in a degree in the
field.

### **Focus Area**


What types of behavior do these teams seek to influence? Some teams are
focused on particular outcomes for the individual—the most common being
financial behavior like saving, spending, and investing (57%), health
behaviors (49%), education (42%), and energy use (36%). Many also spent
time on company-driven outcomes of product usage (60%) and sales (51%).
Respondents selected all that applied to them, and many of the companies
and nonprofits in the sample consult for a range of clients.


The teams use a range of techniques, but at 83%, by far the winner is social
influence (social norms, social proof, etc.). The next most popular item was
directing attention (79%) and shaping the choice set (78%). The oftendiscussed approach of forming habits was used by 62% of respondents(see
Figure 16-5).


In most cases, the target audience for these interventions _did not know_
_about them_ —something that can raise ethical red flags, especially where the
behavior is directed for the organization’s benefit rather than that of the
individual; 40% of respondents said that virtually no users know about the
use of the behavioral interventions, 20% said a few do, and only 20% said
most people did or everyone did (20%) ( _N_ = 143).


_Figure 16-5. Techniques used by behavioral teams (respondents could choose more than one option)_


Respondents reflected upon how important various aspects of their work
were. Direct behavior change, not surprisingly, was consistently most
important, as was sharing the results internally. Most teams did not value
(or perhaps did not have the opportunity) to share their results externally or
to seek to influence policy. Again, this analysis is limited to the companies
and nonprofits in the sample: the picture for academics and government
agencies would be quite different.


_Figure 16-6. How important is each activity to the teams?_

## **The Challenges**


The field is growing rapidly—both in area of application, in geography, and
in the number of organizations with behavioral teams. There are three main
problems facing the field, however: practical problems of setting up and
running a team, replication, and ethics. We already discussed ethical
challenges in detail in Chapter 4. Let’s look at the other two challenges
now.

### **The Practical Challenges of Running a Team**


The single biggest challenge that teams faced was getting their
interventions implemented in practice (43%), or measuring their impact
(41%); generating ideas for interventions was rarely a problem (11%). In
the comments and subsequent interviews for this book, respondents
similarly mentioned that some of their key challenges were implementation
and impact measurements.


The challenges of implementation appear to come from two main sources.
First, I’ve often heard behavioralists who serve as external consultants
complain that after they write their report, they move on to another project
and they doubt that the client ever implements it. And, the same complaint
from internal consultants, except they _know_ their advice wasn’t really taken.
The other reason implementation is a problem, based on conversations with
peers in the field, stems from the normal challenges of product
development: many good ideas simply aren’t put into practice, whether they
are behaviorally informed or not. There isn’t space on the road map, there
isn’t buy-in at the appropriate levels of the company, etc.


Ironically, the opposite problem also occurs: companies rush to implement
without measuring impact. Numerous interviewees among the survey
respondents talked about their clients or their companies acting too quickly.
Once the team had presented an idea, the response was “OK, well, let’s do
to it then—why would we waste time with the test?” This is an issue we’ve
faced at Morningstar as well, and other researchers in the field have written
about it too:14 it’s difficult to simultaneously say that you have a potential
solution to a known problem and that you’re not sure it would work.
Stakeholders simply aren’t using to hearing from their experts that an
approach might not work! The reality is that all solutions, derived from
behavioral science or not, could fail to have an effect or, worse, backfire.
It’s just that behavioral teams are generally more comfortable saying so,
and that can be misinterpreted. These impact measurements are a vital part
of behavioral science and point us to the next problem: the replication
crisis.

### **The Replication Crisis in Science**


Across many fields of science—especially psychology and medicine—we
are experiencing a decade-long crisis of replication. Some of the most
famous early studies in the fields, and many others, have been found not to
replicate—i.e., subsequent researchers attempted to replicate the results of
the initial authors, under the same circumstances, and were unable to. In
many cases, the later researchers found results that were either not


statistically meaningful or significantly smaller than had been previously
reported. John Ioannidis, clinical researcher and meta-scientist (a scientist
who studies science), summed up the problem pointedly and succinctly in
the title of his 2005 paper, “Why Most Published Research Findings Are
False.”


Since then, a wide range of studies from marketing to sports science have
failed to replicate. Behavioral science, which draws heavily on psychology,
is not immune to this problem. Some prominent psychological studies used
in the field that were later undermined include:15


The resource model of willpower (ego-depletion), popularized by
Roy Baumeister, in which engaging in a difficult task would make
you more likely to give in to subsequent temptation.


The use of subtle primes on behavior, studied by Bargh and others.
For example, exposure to words related to old age would
(supposedly) make participants walk more slowly, without their
knowledge.


The power pose associated with researcher Amy Cuddy, in which a
robust stance would increase testosterone and cortisol, and lead to
riskier behavior.


Despite popular TED talks, books on the topics, and literally hundreds of
research studies in these areas alone, follow-up analyses found that they
simply could not be trusted. Estimates vary, but regularly one sees metaanalyses (studies of multiple research studies in the same research domain)
report that 20%–40% of the studies did not replicate as the original authors
had published.


All of this can and should be concerning—not simply to social scientists
and other researchers but to us as we try to apply behavioral research to
product development and to the broader public whose lives and are in many
ways shaped by the results of these studies.


The replication crisis is, however, a healthy and good thing. It is the process
of identifying and removing rot from our base of knowledge, and the


alternative is far worse. The alternative is simply to be blind to our
ignorance.


As a researcher, the failure to replicate so many prominent studies tells us
that to truly advance knowledge is extraordinarily difficult. And, in a
behavioral science context, that behavior change is likewise difficult. It’s
not that researchers design foolish and ineffective interventions (though
some do, certainly)—rather it is that the research process, and especially the
replication process, exposes which interventions are solid and which ones
aren’t. Without that process, we’d still have just as many bad, ineffective
interventions; we just wouldn’t know which ones are which. The history of
medicine is rife with examples of treatments that either did nothing or did
more harm than good (like trepanation and bloodletting), as is international
development (like the example of microfinance in Chapter 15). Without
rigorous measurement and replication, we’d still have these scourges.


And so, what do we do as people applying behavioral science? First, we
look to apply research that is well-founded. That’s what I’ve tried to do
throughout this book, though certainly some interventions we’ve talked
about will later be shown to be less effective than hoped—that’s to be
expected. Second, we measure and test ourselves. We perform our own
replications. Every time we run an A/B test or other rigorous measurement
of impact for an intervention, we replicate the results of others. And more
importantly, we gain confidence that we’ve found something that is
effective for the particular context of our products and our users. This is one
of the reasons why impact measurement isn’t optional when designing for
behavior change: it’s an absolutely essential part of the process, even if it
isn’t as exciting and interesting as the interventions themselves.


Finally, we can also seek to learn from bad research. Where did prominent
studies fail to replicate? Where there were small impacts, small numbers of
people, with incomplete randomization or no experimental control at all,
where null results were ignored or not published, and where the results
appeared to be “too good to be true.”16 We’ve tried to address many of
these issues in Chapter 13 by focusing our attention on impacts that are
practically meaningful, and getting enough people in an impact


measurement to assess that impact; by harping on the power of experiments
versus pre-post tests and other less rigorous techniques; and by setting rules
for when we can use a null result to stop any further analysis.


That brings us back to the Behavioral Teams survey and Chapters 13 and
14, and how behavioralists in the field measure impact. Given the
challenges in implementation and measuring impact, it is noteworthy that
70% of respondents said their teams measured their success in terms of A/B
tests or other forms of RCT. We should be cautious: the median number of
experiments the teams conducted in the last twelve months was only four.
While many of the teams are relatively new, that indicates either that A/B
tests are not as widely spread as the response might indicate or that the
teams have implemented them sparingly.


In addition to RCTs, 71% used pre-post analyses; 50% looked for direct
feedback from users to gauge the effectiveness of behavioral interventions:
two technique that can be immensely valuable to gain understanding about
_why_ an intervention worked or didn’t, but often aren’t up to the task of
measuring the impact itself effectively. Interesting, 25% used statistical or
machine learning techniques (beyond A/B tests). We’ll discuss the
integration of statistical methods and machine learning and behavioral
science in the next chapter, keeping in mind that this combination is still
relatively new and not widespread.

## **Putting It into Practice**


Here’s what you need to know:


The field of applied behavioral science has grown rapidly since
2013: 87% of teams started in the last seven years.


While the US and the UK still hold a majority of teams and jobs,
that is changing rapidly as new teams across the globe are
proliferating.


Much of the action is occurring in consulting companies, both
nonprofit and for-profit.


Current teams especially struggle with implementing their
interventions and measuring impact.


While diverse techniques are used, the most common approach
teams use are social nudges.


If you want to start your own team in a company or nonprofit, look for
places where behavioral science adds to the value of existing roles, and not
where behavioral science would be a role onto itself; the former are far
more common. The roles, often, are in consulting for external clients,
product design and management, research and analytics, and marketing. In
the next chapter, we look in more detail at the types of people and “pitch”
you can use to the start the team.


1 This case study comes from a phone interview and subsequent email exchanges with Scott

Young, head of the BVA Nudge Unit in London. Find more information about the Nudge
Building at Singler (2018).


2 Here is the data cleaning procedure. Respondents were first asked whether their teams fit the

desired criteria and were offered a copy of the resulting report even if they did not meet those
criteria (i.e., removing an incentive to complete the survey with invalid data). Roughly 5% of
respondents filtered themselves out at this stage. Second, responses with fewer than 25 values
(answers to questions or subquestions) were filtered out. Third, multiple responses by the same
individual were grouped and only the most complete set were kept. Finally, multiple responses
by individuals at the same organization were grouped and in sections 1 and 2 above, only the
most senior individual at that company (by title) was included; in section 3, the responses are
about an individual’s perspective, and all valid responses were included. The resulting dataset
had 231 organizations across 253 respondents. On the survey, respondents indicated the type of
organization their team belonged to; we determined that the Other and Independent Research
Organization options were interpreted differently by respondents, and we manually mapped
these responses to the other options: company, nonprofit, government, or academic.


3 From the OECD list, we used the handful of nongovernmental and private organizations

(since the government agencies were often clients of existing teams without a team of their
own), and we manually verified that each had a team.


4 [See also “Behavioral Science and Insurance” by the Reinsurance Group of America.](https://oreil.ly/9Ytlg)


5 While the survey was written in English, it does not appear that there was significantly less

coverage in countries where English is not an official language. In other words, relative to the


directory, survey responses do not appear strongly biased by country. However, the process of
creating the directory itself could have been biased toward English-speaking countries or
groups and there is no clear external standard by which to measure that problem, if it exists.
My thanks the Anne-Marie Léger for raising the issue.


6 See prior footnote on data cleaning. In some cases, multiple respondents from the same

organization completed the survey. Unless otherwise noted, we use the primary respondent.


7 After removing entries that were clearly inaccurate and verified as such manually.


8 [As of October 24, 2019, the UK’s Behavioural Insights Team lists 181 employees, only a](https://oreil.ly/wqtrb)

portion of whom are actually applying behavioral science in their work, and ideas42 lists 126
employees.


9 As of October 24, 2019, the J-PAL listed 294 employees worldwide, including academic

professors, grant writers, and so on.


10 These early pioneers are in fact, real, based on manual verification of the underlying data.


11 Statistic provided by Nir Eyal.


12 [For estimates on the size of the graphic-design community, see this report from IBISWorld.](https://oreil.ly/qsoUq)

As of January 2020, they placed the field at 534,680 people.


13 In the survey, 12% of respondents replied Other and did not provide information that readily

fit these categories.


14 For example, Wallaert (2019)


15 [Willpower: Engber (2016); priming: Doyen et al. (2012); power pose: Dominus (2017). There](https://oreil.ly/oS06G)

are many resources online about the replication crisis; one list of problematic studies in
[psychology can be found at Jarrett (2016).](https://oreil.ly/lkYwy)


16 [See the discussion in Resnick (2018).](https://oreil.ly/sszd9)


# **Chapter 17. What You’ll Need** **for Your Team**

_Over the past ten years, a range of researchers across the Inter-American_
_Development Bank (IADB) have applied behavioral lessons in their_
_development projects or conducted field studies of their own. Starting in_
_2015, the IADB wanted to have a more coordinated approach, however._


_In working with the bank leadership, Carlos Scartascini created a unified_
_group to support and grow the diffuse efforts already in place. The core_
_team composed of fellows and visiting scholars provides training for_
_government officials in member countries and for IADB specialists (they’ve_
_trained more than two hundred staff members thus far), disseminates best_
_practices, and consults on individual projects as needed._


_Beyond the central team, they work with more than 20 dedicated_
_behavioralists in other departments and numerous others who apply_
_behavioral science across the bank, from education to sanitation. Nearly_
_every department has someone in-house who combines their area of_
_expertise with some knowledge of behavioral science for development._


_For the IADB, with $1 billion lent for development projects each year, this_
_structure helps them manage the massive scope and diversity of their work._
_It allows them to combine deep knowledge within each department, on the_
_specific needs of healthcare or infrastructure projects, for example, with_
_knowledge of the latest findings and techniques in behavioral science._


Behavioral science teams don’t have a single design or structure; they often
grow organically out of existing programs and departments, where people
in those departments find that behavioral science can aid their work. A few
large groups, like at the IADB, have evolved into a distributed model of
central support and diffuse practitioners. Here, we’ll look at what it takes to
build your own team, in your company.


## **From What They’ve Done to What You’ll Do**

Let’s dive into how you can get involved, especially what’s needed to start
applying behavioral science at your company. As we learned from the
Behavioral Teams survey, despite the rapid growth in the field, the best job
and career advice for people looking to enter the field is to build up from
within your existing organization.


Clearly, you’ll need a set of tools to think about and actually use behavioral
science in products and communications. That’s what the rest of this book
covers. What else is needed? Let’s look at two areas in particular: a strong
case for other stakeholders within the company, and the right people and
skills for the job.

## **Making the Case**


The best way to argue for the value of designing for behavior change isn’t
to argue at all—but rather to demonstrate it. As Matt Wallaert nicely puts it:
“Ideally, you wouldn’t talk about behavioral science at all in the beginning.
Instead, you’d do your job really well for a year, earn respect, and then tear
off the mask and say ‘Ta-da! It’s because of behavioral science!’”1


In other words, do as many individuals in the field are already doing: read
the books, take the online courses, do a formal program if you can. But first
and foremost, don’t look for “behavioral science jobs.” Instead, look for
how behavioral science can improve the career you already have: how it
can improve your design practice (like design companies like Mad*Pow
have done), how it can provide better consulting solutions to your clients
(as with Saudi Arabia’s first unit—see sidebar), or how it can improve your
product development.


Sometimes you don’t have the luxury to build behavioral science into your
work on your own, or you’ve started to, but need additional resources to
grow and expand that effort. At that point, it’s time to make the business
case for behavioral science.


### **Thinking Through the Business Model**

Helping users voluntarily change their behavior can directly support the
core business goals of a company, but these types of products do raise
special business considerations.


Recall from the Preface that there are two main (ethical) targets for
behavior change:


Behaviors that users want to change _within their daily lives_


Behaviors that occur _within the product itself_ and are required to
use the product


In the latter group, the business impact is clear and straightforward. Let’s
say the behavior change task is learning how to better organize email in an
email client. If you help users do this more effectively, they are more likely
to (a) buy later editions of the product in the future (or renew, if the product
is on a subscription model) and (b) recommend it to others. In both cases,
behavior change means more revenue.


For behaviors in the user’s daily life, the company’s business model will
depend on whether the behavior is frequent or one-time. Let’s say the target
behavior is exercising: it’s repeated. Standard business models work
perfectly well for this type of product and align user success with business
success:


_Revenue increases with the time users spend using the product_


_Subscriptions and reoccurring fees._ For example, a
product that helps people set, track, and compete with
friends over exercise goals. If the product is successful,
both exercising and revenues are sustained. A similar
model exists for products that automate user tasks
altogether—like target date funds in the investment space,
which charge an ongoing fee for automating the process of
asset allocation.


_Advertising._ For example, the same exercising
tracking/competition product could be free to the user but
advertise fitness products. If the product is successful, it
continues to deliver an interested, engaged audience for
advertising.


_Revenue increases with new sales_


_Market penetration._ For example, an exercise tracker from
Fitbit. People don’t really need two exercise trackers. But
if the product is successful at changing behavior, then
current customers refer others, and sales grow. If the
market becomes saturated, that’s a nice problem to have,
and the company can move on to new product lines (upsell).


_Cross-sell and up-sell._ For example, the company has
multiple exercise products (a tracker, shoes, clothing,
etc.). If one product is successful at changing behavior,


then the customer is more inclined to buy other products
from the company.


_Revenue increases with the success of users at changing their_
_behavior_


_Incentive-aligned third-party support._ For example, a
third-party benefit from the same thing that users benefit
from: behavior change. The third party would then pay for
the product on the user’s behalf. Employers benefit from
their employees being physically healthy and pay for
products like Keas to help employees exercise. Energy
companies benefit from their customers being energy
efficient, and pay for products like Oracle’s Opower.


Again, these are same business models as any other product—plus the
somewhat unusual option of third-party support.


Products that change a one-time or infrequent behavior have a more
difficult time aligning user success with business success. Consider, for
example, getting a mortgage, and products that help people shop for a better
one. Thankfully it’s not something that most users do very often. Standard
business models become problematic:


_Revenue increases with the time users spend using the product_


_Usually not relevant._ Customers just want to find a good
mortgage; they won’t pay more if it takes longer to find
one.


_Revenue increases with new sales_


_Cross-sell and up-sell._ This is feasible if the company
offers related services—like banks that offer mortgages
and checking accounts. However, customers have a hard
time assessing the quality of one-time services like
mortgage-buying assistance; that uncertainty leaves room


for chicanery. In the mortgage market, there’s a significant
temptation (financial incentive) to shift from providing
unbiased decision-making support to pushing mortgages
that generate high, lead-generation fees.


_Market penetration._ Generating new sales based on highquality decision support for mortgages is possible.
However, because customers have difficulty assessing
quality, the same temptations exist for the companies that
seek to “help” users make that decision. Hence, businesses
use gimmicks that made customers excited up front but
leave them loaded with significant fees and risk, like
balloon mortgages.


_Revenue increases with the success of users at changing their_
_behavior_


_Incentive-aligned third-party support._ A one-time change
in behavior would need to be very significant to attract
(incentive-aligned) third-party support. In the case of
decision-making support, Fannie Mae and Freddie Mac
have appropriate incentives for end users to receive
optimal mortgages, but few other entities have incentives
aligned with the end user for such a product.


And, of course, there are behavior change business models that clearly are
not aligned with the interests of the user. Gyms are the classic example of
businesses that profit because their users fail to change their behavior.
Many gyms rely on fees paid by users who plan to exercise but never do.

## **The Skills and People You Need**


From the Behavioral Teams survey, we learned that there’s no single path
into applied behavioral science. Recall that 52% of respondents in the
private sector and nonprofits had a formal degree in the field; 80% of the


others had learned some of their skills on the job. However, having the
_appropriate skills on hand_ isn’t optional. You can think about them as
falling into three categories.

### **Skillset 1: The Non-Behavioral Basics**


While some behavioral teams are centrally located centers of excellence,
according to our survey, the vast majority aren’t; they are embedded in
product, design, marketing, analytics, or other functions. And, for these
groups, the first skills that are needed are those used in the core work of the
team. If you’re applying behavioral science to product development, that
means design or product management, etc. If you’re working on
communications and marketing, it means knowing communications and
marketing.


Behavioral science isn’t a substitute to these core disciplines; it’s an added
skill and understanding of the mind. I’ve seen a number of behavioralists,
especially newly minted behavioral scientists coming out of school and
without a professional background, act as if they are designers or marketers
simply because their skills can _help_ design or marketing. It doesn’t end well
for them: without a foundation in that specific field, they make mistakes
that are obvious and avoidable to anyone trained in the field. Worse, they
can cause an allergic reaction in their departments by trying to take over
someone else’s job (who is trained), they end up being locked out and
distrusted.


The potential exception is consulting. When a consultant is hired into a
company or department, they have a certain license to give advice, but good
consultants know to listen first, and learn how to adapt their language and
approach to the context. And even then, behavioral science alone isn’t a
skillset that makes one a good consultant: instead, it can help consultants
understand and solve behavioral problems, after they already know how to
work with clients.

### **Skillset 2: Impact Assessment**


As I’ve argued throughout this book, and as casual observation has
probably told you too: people are really complex. Human behavior is really
complex. The interaction between people’s environment and their behavior
is really complex. And for all of these reasons, we can’t assume _anything_
_we do_ to change behavior—whether informed by behavioral science, design
thinking, or meditating on a mountaintop for great ideas—is going to have
its desired effect.


To be honest to ourselves, to be honest to our clients and to stakeholders
across our organizations, we need to rigorously assess causal impact. It’s an
important set of skills that generally _isn’t_ covered in Skillset 1 (domain
expertise in marketing, product development, design, etc.).


Where can one learn impact assessment? I’m afraid this is one of the few
things that isn’t easily learned on the job: there’s a foundation of statistical
knowledge that one needs that comes from careful study, usually at a
university (I do believe in autodidacts—they just aren’t as common here).


Note that I didn’t say that one needs to know how to do randomized control
trials. That’s for two reasons. First, while randomized control trials are
absolutely and without question the best tool for the job of causal impact
assessment, they just aren’t always feasible and they are, like everything,
[imperfect even when they are feasible. Sometimes we need to use a](https://oreil.ly/LO1ON)
statistical model to triangulate causality and a broader statistical skillset is
vital. Second, because I’ve found that if someone has a broad statistical
skillset, then they can learn how to analyze (first) and design (second)
randomized control trials. The reverse isn’t always true.


Even 10 years ago, it used to be very difficult to find solid statistical skills
in many organizations. With the rise of data science, that is changing. While
data science and behavioral science are really quite different (see next
section), data science team members can have the foundation of technical
rigor that one can build on and adapt to analyze RCTs.

### **Skillset 3: A Deep Understanding of the Mind and Its** **Quirks**


Lastly, we come to what most laypeople consider behavioral science: a
knowledge of the mind’s quirks and of nudges that can affect behavior. In
my work, I’ve found that given the right toolset and a fundamental
understanding of the mind, people can discover creative ways to work
around behavioral obstacles. Having a list of existing nudges on hand is
perhaps the _least_ important skill in applying behavioral science; again,
every intervention should be tested anyway.


It’s where these nudges come from that matters: knowing that people have
limitations, they use shortcuts to economize, and these shortcuts can go
awry depending on the context of a decision and action. That’s why I
covered this foundation in Chapters 1–3, instead of offering a list of biases
and fun stories about how people make mistakes. The fundamentals covered
there are a good start. Further reading in behavioral science that emphasizes
models and underlying mechanisms (not cute nudges) can help immensely
as well.


These are all skills that can be learned on the job and through individual
reading and coursework. However, beware of online courses that focus on
what I call a “bag of tricks” approach to behavior science: all biases, no
underlying theory that connects them. It’s flashy, but won’t provide the real
direction and understanding required to help your users overcome
behavioral obstacles.

### **What’s Not Listed: A PhD**


I’m a strong believer that formal study, in particular a PhD, is not required.
I do have a PhD myself, and I don’t think it’s required for this job. A PhD
provides many valuable skills, including statistical rigor to assess impact
(Skillset 2), and sometimes domain expertise, especially in marketing
(Skillset 1). Those are nonnegotiable and your team needs them with or
without PhDs. Also, at its best, the training for a PhD provides people with
a love of learning, an openness to exploration and being proven wrong, the
ability to take messy ideas and shape them into a coherent and predictive
theory, and an abiding skepticism about the correctness of any such theory
or model. These are also nonnegotiable, I believe they are essential for


doing thoughtful, effective applied work. These traits aren’t unique to
PhDs, however (or master’s degree holders, either, for that matter).
Thankfully, smart, curious, and thoughtfully skeptical people can be found
in many places—not just in PhD programs.

### **How You Combine These Skills on a Team**


Many behavioral teams consist of a single person, and that person has all of
these skills. Betterment’s Dan Egan is one such powerhouse. He consults
with groups across the company, but in the end, he’s playing each of these
roles. Other teams, especially those embedded in marketing, product, or
design, work side by side with their more traditional and domain-trained
colleagues and don’t need to have as much of the domain expertise
themselves. There doesn’t seem to be a single model, nor one that is
necessarily better than the others. The skills are necessarily—whether they
are direct reports of a central chief behavioral officer or partners across the
company doesn’t seem to matter as much.


In case you’re curious, on our team, we do a mix of both. I currently have
13 people who roll up to me, another 13 who are part of our behavioral
“group” (reporting to other managers but dedicated to our projects), and
many others that we have the pleasure of consulting with and partnering
with on projects on a more ad-hoc basis. Our product work started out very
much as pure consulting to help existing product teams; now we have
engineers and others working directly with us, for example. While I
certainly have lessons from each of the models we’ve experienced, I think
the particulars of a given situation are probably more relevant, to be frank.3
We now have a wonderful team of in-house researchers (PhD and nonPhD), but early on when it was just a few of us, we found it immensely
valuable to partner with outside academics to bolster our skills and run
projects we otherwise couldn’t muster. Let’s look at how to do that next.

### **Getting Help from Outside Researchers**


Experimental testing, especially for outcomes that are outside of the
product, can be an intimidating endeavor. Believe it or not, academic
researchers would probably love to help test your product’s impact. Many
of them can’t be “hired” in a traditional sense—because they have full-time
jobs in academic institutions and for professional reasons can’t accept
consulting contracts. But you can build partnerships of mutual benefit if
you have enough users of your product to support a scientifically valid
study and know how to navigate the process.


Sound impossible? This happened to me, and it’s how I first became deeply
involved in applied behavioral science. I worked full-time, and I was
studying on the side. I had no internal team to call upon, and no budget.
However, I found behavioral researchers who were doing interesting work
that related to our product, and I approached them at conferences or coldemailed them. I was fortunate to find great researchers who wanted to work
together to solve our users’ problems. Over the years, I learned immensely
from these partnerships—and in many ways they helped me become an
effective applied behavioral scientist myself.


Here’s what I learned through my own experience and subsequently by
helping other companies build these research partnerships:


1. _Find researchers in your field._ [Start with Google Scholar to search](https://oreil.ly/UZff9)

for the topics you work on, and see whose names are in the most
commonly cited articles (the results are sorted by the number of
citations). Academic conferences on your topic are another good
way to start, but they take more time and energy. The Behavioral
Science Policy Association also seeks to be a central hub,
connecting interested companies with interested researchers.


2. _Contact them_, asking for suggestions about academics who might

be interested in studying the topic with your user base. In
particular, ask who might be interested in testing the impact of
interventions. Follow up and contact the suggested researchers; the
researchers you initially contacted may be interested, of course.


3. _Discover what they need to benefit their work_ . Describe your

product and user base. Ask them what they need. Depending on the
person, their field, and where they are on the academic career path,
that will vary. Here are common options:


_Access to unique data._ In some disciplines, it is extremely
costly and difficult to obtain detailed information about
individual users, from demographic information to
observed preferences, and especially about changes in
behavior over time.


_Access to a large user base._ The power of scientific tests
increases with more users, but it is costly for most
researchers to gather a large enough test population on
their own. If your product already has them, excellent.


_Access to funding._ Financial support from companies to
academic social science researchers can be highly
problematic; it can taint researchers’ independence and
undermine their ability to publish the results of a study
with the company. However, if the company is looking for
expert advice, and not academic publication of the results,
some researchers certainly can be hired for paid
consulting arrangements. Other options include providing
grants for research on the topic, and supporting grant
proposals submitted by the researchers to third-party grant
agencies.


4. _Develop a shared research plan_ . With a small, trial project, try

working together. Set clear expectations on access to data, funding
(if any), staffing (on both sides), and timing of the study and
analyses.


5. _Don’t try to restrict the results or ideas_ . Academic research runs on

innovative ideas and the data to back them up. Companies can’t
lock down the ideas learned from the study—they must be shared


between the company and researchers. Similarly, if there is a whiff
of restriction on the publication of negative results, that will
undermine the reception of the study and turn away most
researchers. Paid consulting arrangements work differently, of
course.


6. _Respect the need for specific testing protocols_ . In order for a study

to be scientifically valid, researchers will have to execute the study
according to specific rules. For example, they may require very
specific wording for questions asked of users. That’s part of the
bargain; and, it will often help the company formulate much more
solid conclusions than if it had informally developed slapdash
surveys.


Thus, if the testing process seems overwhelming, don’t despair. Your first
option is to look to off-the-shelf testing tools, as discussed in Chapter 12. If
those aren’t enough, look for professional research partnerships with the
academic community. If your company is doing innovative things to help
users change their behavior (which of course you are!), researchers may be
interested in working with you.

### **Data Science and Behavioral Science**


Do you need data scientists on the team? Are they the same thing as
behavioral scientists? I’ve found that many people aren’t clear on the
differences between behavioral science and data science. Even within my
company, I can’t tell you how many times someone has asked me
something like, “So, can your team run a report on product usage for us?”
Product usage reports are certainly a useful thing to do; they just aren’t
really in the behavioral science wheelhouse (nor probably for many data
scientists either).


So what’s the difference between the two, and where is each needed? To
understand this, let’s take a step back from the discussion of team
composition, and look more deeply at the types of questions each
practitioner community seeks to answer.


Data science often seeks to understand how something works and _predict_
the future. Behavioral science seeks to _change_ the future, particularly
through changing human behavior. Or as Sarah van Caster puts it in her
[article “Data Science Meets Behavioral Science”:](https://oreil.ly/xGCed)


_Data science is the discipline that allows us to analyze the unseen—and_
_with machine learning, it allows us to look at large sets of data and_
_surface patterns, identifying when past performance is indicative of_
_future results. For instance, it lets us forecast what products are most_
_likely to be sold and which customers are most likely to buy. But what if_
_you not only want to understand potential outcomes, what if you want to_
_completely change outcomes, and more specifically, what if you want to_
_change the way in which people behave? Behavioral economics tells us_
_that to make a fundamental change in behavior that will affect the long-_
_term outcome of a process, we must insert an inflection point._


Because of these two different purposes, data scientists and behavioral
scientists often use different statistical methods. Data scientists can predict
the future very accurately and thoughtfully using variables that are
correlated with the outcome of interest. They use regressions, decision
trees, neural networks, and such to find hidden relationships between
context and outcome.


Behavioral scientists, when possible, use experiments since they are the
best tool to measure our ability to _cause_ a change in behavior or outcomes.
Analyzing experiments, when properly designed, doesn’t require advanced
statistics at all: a simple comparison of means (e.g., T-test) is often enough.
Behavioral scientists do also use regression and sometimes machine
learning techniques, but we do so in the service of understanding the causal
relationship between context, behavior, and outcomes.


Because of these two goals—predicting outcomes versus causing changing
behavior—data and behavioral scientists also differ in how they use _theory_ :
an explanation of why something works the way it does. Strictly speaking,
one needn’t understand _why_ there’s a relationship between A and B in order
to accurately predict B, given A. Many data scientists do have a theoretical


understanding of what they study, and that helps them with feature selection
and data analysis, but it’s not actually required.


In behavioral science, a positive result from an experiment tells us that, at
the particular moment of the experiment and for the particular people
involved, A caused B. It is our underlying explanation of why that
happened (which we seek to test in the experiment) that allows us to try
generalize to other situations and contexts. Behavioral theory makes it
easier to provide advice on how _other people, in other situations,_ could
change behavior and outcomes.


_Table 17-1. Comparing data science and behavioral science_


**Data science** **Behavioral science**


Theory: Helpful, but not required Not meaningful without it


Number of Jobs: Many Few

### **Leveraging Data Science When Designing for Behavior** **Change**


While data science is distinct and different from behavioral science, the rise
of data science and the tools that come with it have opened up new
possibilities for understanding, and designing for, behavior change.


The first and most obvious way in which data science can improve behavior
change work is that it can help identify behavioral obstacles by analyzing
the various paths in a behavioral map (or marketing funnel) to look for
blockages. And, similarly, to look for the naturally occurring segments of
the population for whom a particular approach might be needed and, after
an intervention has been deployed, to analyze its segment-specific impact.
Behavioral scientists have _started_ to look at these questions with techniques
called moderation and mediation analysis, but frankly most work is still
very much at the “try this, and see if it works for everyone level.” Data
scientists either within the team or helping out from other teams, have a
much more developed skillset in that area.


In addition, one of the big limitations of behavior change work—and the
experiments that come with it—is that most behavioral changes that we
create and measure are short term. There just aren’t that many experiments
that measure behavioral changes for longer than six months (and most are
far shorter). So we really don’t know what the long-term impacts of our
changes are. Data science and _computational behavioral science_ can help
solve this: by projecting the effect of behavioral interventions into the
future. This projection can be through closed-form equations or simulation
models, especially when the individuals are expected to interact with each
other and one person’s behavior change may affect another person over
time.


Do these projections tell us clearly and definitively what will happen in the
future, if people use our behavioral products or interventions? No. Actually,
they’ll often help us see how _we’re wrong_ . They’ll make predictions about
future behavior change that are simply unrealistic, and obviously so.
Computational behavioral science helps us more fully vet or test what we
know about behavior change: where those ideas are already vetted, and
we’ve found that they don’t make crazy and unreasonable predictions. They
help us model the long-term effects of our products and interventions for
our users, for our business, and for society.

## **Putting It into Practice**


If you’re not currently on a team that applies behavioral science in product
or communications development, understand that official job opportunities
in the field are small, at least compared to the people who could be
interested. The real opportunity lies in designing for behavior change as
part of one’s existing career, especially in design, product management,
marketing, and HR.


In these areas, behavioral science provides a powerful and unusual skillset
that peers in the field are unlikely to have.


Whether for you individually, or if you’re looking to start a team, three
skills are essential:


Domain expertise (in product, design, etc.)


Statistical skills to assess the impact of your efforts on behavior


A fundamental understanding of how the mind works and makes
decisions


The first two generally requite formal training, or at least previous
experience. The last can be learned on the job, with thoughtful study. This
book can help you and other members of your team, as can online courses
from Duke University, the University of Toronto, and others.


A PhD is not required—it’s one good way, but not the only way—to gain
these skills.


The skills and activities of data science are often confused with behavioral
science. In short, data science seeks to predict outcomes (whether or not we
_cause_ them); behavioral science seeks to causally change behavior and
outcomes. The two groups can and should work together—but respecting
the different background and goals of each.


1 Interview with Matt Wallaert (2019).


2 This sidebar was developed from an interview with Wiam Hasanain (2019) and subsequent

email exchange.


3 If you’d like to see another detailed breakdown of a behavioral team’s staffing, check out

[Clover Health’s.](https://oreil.ly/LhupD)


# **Chapter 18. Conclusion**

Throughout this book, we’ve looked at how to deliberately, and ethically,
develop products that help your users change their behavior, from
exercising more to drinking less.


To do so, we’ve tried to develop three major conceptual tools:


An understanding of how people make decisions and act in their
daily lives


A model of what’s required for someone to take action relating to
your product in a given moment


A process for applying that knowledge to the practical details of
product development


Let’s briefly review the big ideas that support each tool.

## **How We Make Decisions and Act**


In Chapter 1, we summarized the breadth of behavioral research with five
core lessons:


_We’re limited beings_ : we have limited attention, time, willpower,
etc. For example, there is a nearly an infinite number of things that
your users could be paying attention to at any moment. They could
be paying attention to the person who is trying to speak to them,
the interesting conversation someone else is having near them, the
report on their desktop that’s overdue, or the notification on your
app. Unfortunately, researchers have shown again and again that
people’s conscious minds can really only pay proper attention to
one thing at a time.


_Our minds use shortcuts_ to economize and make quick decisions
because of our limitations. Your users have a myriad of shortcuts
(aka heuristics) that help them sort through the range of options
they face on a day-to-day basis and make rapid, reasonable
decisions about what to do. For example, if they don’t know what
to do in a situation, they may look to what other people are doing
and try to do the same (aka _descriptive norms_ ). Similarly, _habits_
are a powerful way people’s minds economize and allow them to
act quickly by immediately triggering a behavior based on a cue.
Unfortunately, these shortcuts can go awry with ingrained and selfdestructive habits (over-drinking) or heuristics that are applied in
the wrong context (like herd behavior). Misapplied heuristics are
one cause of _biases_ : negative tendencies in behavior or decision
making (differing from an objective standard of “good”). Often
because of these biases, there’s a significant gap between people’s
intentions and their actions.


_We’re of two minds_ : what we decide, and what we do, depends on
both conscious thought and nonconscious reactions like habits.
This means that your users are often not “thinking” when they act;
or at least, they’re not choosing consciously. Most of their daily
behavior is governed by nonconscious reactions. Unfortunately,
their conscious minds _believe_ that they are in charge all the time,
even when they aren’t. We’re all “strangers to ourselves”; we don’t
know the causes of our own behavior and decisions. Thus, your
users’ self-reported comments about a problem in your product or
what they plan to do in the future aren’t necessarily accurate.


_Decision and behavior are deeply affected by context_, worsening or
ameliorating our biases and our intention–action gap. What your
users do is shaped by our contextual environment in obvious ways,
like when the architecture of a site directs them to a central home
page or to a dashboard. It’s also shaped by nonobvious influences,
like the people they talk and listen to (the _social environment_ ), by
what they see and interact with (their _physical environment_ ), and


by the habits and responses they’ve learned over time (their _mental_
_environment_ ).


We can _cleverly and thoughtfully design a context_ to improve people’s
decision making and lessen the intention–action gap. And that is the point
of _Designing for Behavior Change_ .

## **Shaping Behavior with Your Product: The** **CREATE Action Funnel**


In Chapters 2 and 3, we looked at the preconditions for action: what your
product team needs to either facilitate or support action (or to remove or
hinder negative actions). It started with a seemingly simple question: from
moment to moment, why would your users undertake one action and not
another? Six factors must align, at the same time, before someone will take
conscious action. Behavior change products help people close the
intention–action gap by influencing one or more of the following
preconditions: Cue, Reaction, Evaluation, Ability, Timing, and Experience.
For ease of remembering, they spell CREATE, because that is what’s
needed to create action.


To illustrate these six factors, let’s say your user is sitting on the couch
watching TV. Your app that helps them plan and prepare healthy meals for
their family is on the phone; they downloaded it last week. When and why
would they suddenly get up, find their mobile phone, and start using the
app?


We don’t often think about user behavior in this way—we usually assume
that somehow our users find us, love what we’re doing, and come back
whenever they want to. But researchers have learned that there’s more to it
than that because of the mind’s limitations and wiring. So, again imagine
your user is watching TV. What needs to happen for them to use the meal
planning app right now?


1. _Cue._ The possibility of using the app needs to somehow cross their

mind. Something needs to cue them to think about it; maybe
they’re hungry or see a commercial about healthy food on TV.


2. _Reaction._ They’ll intuitively react to the idea of using the app in a

fraction of a second. Is using the app interesting? Are other people
they know using it? What other options come to mind, and how do
they feel about them?


3. _Evaluation._ They might briefly think about it consciously,

evaluating the costs and benefits. What will they get out of it?
What value does the app provide? Is it worth the effort of getting
up and working through some meal plans?


4. _Ability._ They’ll check _whether_ it’s actually feasible to use the app

now. Do they know where their mobile phone is? Do they have
their username and password? If not, they’ll need to solve those
logistical problems before using the app.


5. _Timing._ They’d gauge _when_ they should take the action. Is it worth

doing now or after the TV show is over? Is it urgent? Is there a
better time? This may occur before or after checking for the ability
to act. Both have to happen, though.


6. _Experience._ Even if logically using the app is worth the effort and

makes sense to use it now, they’d be loath to try again if they’d
tried the app before (or something like it) and it made them feel
inadequate or frustrated. Idiosyncratic personal experiences can
overwhelm any “normal” reaction a person might have.


These six mental processes are gates that can block or facilitate action. You
can think of them as “tests” that any action must pass: your user must
complete them successfully in order for them to consciously, intentionally,
engage in the target action. And, they all have to come together at the same
time. For example, if they don’t have the urgency to stop watching TV and
act now, they could certainly do it later. But when “later” comes, they’ll still
face these six tests. They’ll reassess whether the action is urgent at that


point (or whether something else, like walking the dog, takes precedence).
Or maybe the cue to act will be gone and they’ll forget about the app
altogether for a while.


So, products that encourage people to take a particular action have to
somehow cue their users to think about the action, avoid negative intuitive
reactions to it, convince their conscious minds that there’s value in the
action, convince them to do it now and ensure that they can actually take
the action. We can think about these factors as a funnel: at each step, people
could drop off, get distracted, or do something else. The most common
outcome in behavior change work, and the one we should expect, is the
status quo. We seek to nudge that status quo into something new.


If someone already has a habit in place and the challenge is merely to
execute that habit, the process is mercifully shorter. The first two steps (cue
and reaction) are the most important ones, and, of course, the action still
needs to be feasible. Evaluation, timing, and experience can play a role, but
a lesser one, because the conscious mind is on autopilot.

## **DECIDE on the Behavioral Intervention and** **Build it**


Behavioral science helps us understand how our environments profoundly
shape our decisions and our behavior. It shouldn’t come as a surprise that a
technique that was tested in one setting (like a research laboratory) doesn’t
affect people in the same way in a real life. To be effective at designing for
behavior change, we need more than to understand the mind: we need a
process that helps us find the right intervention, the right technique, for a
specific audience and situation.


What does this process look like? I like to think about it as six steps, which
we can remember with the acronym DECIDE; that’s how we decide on the
right behavior-changing interventions in our products and communications.


First, Define the problem. Who’s the audience, and what is the outcome
we’re trying to drive? Second, Explore the context. Gather qualitative and


quantitative data about the audience and their environment. If possible,
reimagine the action to make it more feasible and more palatable for the
user before we build anything.


From there, Craft an intervention—a behavior-changing feature of the
product or communication. You craft on both the conceptual design
(figuring out what the product should do) and the interface design (figuring
out how the product should look). As we prepare to Implement the
intervention, we consider both the ethical implications and how to
instrument the product to track outcomes.


Finally, test the new design in the field to Determine its impact: did it move
the needle or did it flop? Based on that assessment, Evaluate what to do
next. Is it good enough? Since nothing is perfect the first time, we’ll often
need to iteratively refine it.


In shorthand:


1. _Define_ the problem


2. _Explore_ the context


3. _Craft_ the intervention


4. _Implement_ within the product


5. _Determine_ the impact


6. _Evaluate_ what to do next


It’s important to emphasize that the process is inherently iterative. That’s
because _human behavior is complicated, and thus stuff is hard!_ If one could
simply wave a magic wand and other people would act differently, we
wouldn’t need a detailed process for designing for behavior change (this
would be very disturbing). Instead, there’s a cyclical process of learning
about our users and their needs, and our efforts to address them if they miss
the mark. The most overlooked, yet the most essential part of the process,
isn’t great ideas and nifty behavioral science tricks: it’s careful


measurement of where our efforts go awry, and the wiliness and tools to
learn from those mistakes.

## **Other Themes**


Stepping back from these three conceptual models, there are some
underlying themes that I’d hoped to express here. These themes provide
additional color and guidance on how to design for behavior change:


_We’ve learned a great deal about how the mind makes decisions, but our_
_knowledge is still limited_


The behavioral social science literature provides the foundation for this
book, and there are numerous field experiments that illustrate how our
decision making works. The research on biases and heuristics is well
established, but research on how products can help change behavior is
still in its infancy. This book pulls together the best of what’s known
currently, but our knowledge is certainly not complete.


_First, understand your users_


Changing behavior is a highly personal affair. Our products should meet
users where they are in their daily lives and help them take action—that
starts with understanding their needs and interests, constraints, prior
experiences, and levels of expertise.


_There are no magic wands for behavior change_


There’s no sure-fire way to _make_ people take an action. Even if we fully
understood the decision-making process, we each have unique personal
histories and environments that shape our behavior. While we can’t
dictate behavior, we can facilitate it. If someone wants to act, welldesigned products can help them do it.


_Be intentional_


If the goal is to help people change behavior, then do it. Don’t hide
behind wishy-washy recommendations or “raising awareness” among
users; that leads us to design and build products that are internally
conflicted and ineffective. Be up front and proud of products that help
users change something important about their lives.


_A behaviorally effective product must first be a good product_


The product must be well designed, pleasant to use, and solve a user
need. Any considerations about changing behavior need to build on top
of that foundation—otherwise, people will simply choose not to use the
product.


_Avoid user work_


Look for technical solutions to avoid user work; it’s much easier to
engineer a solution than it is to change behavior. We can and should
celebrate user triumphs—but those triumphs should occur where hard
work was unavoidable, and not where the product was poorly designed.


_We don’t need to get fancy_


Look for the minimum viable action that a user can take to reach their
goal, and remember simple, obvious lessons about the psychology of
design: we like beauty, simplicity, familiarity, and following our peers.


_We should assume we’re (partially) wrong_


No matter what we design and build, we’ll get some things wrong. A
dose of humility in face of the vast complexity of human behavior is a
good thing. It spurs us to test the real, quantifiable impact of our
products, and test every major change we make to them.


There are certainly other lessons throughout the book, but why I think about
the underlying philosophy of how to approach designing for behavior
change, these points start to capture them.


## **Frequently Asked Questions**

Now, let’s turn to questions that I’ve often encountered in this field and that
you may have or face yourself. There’s no strict ordering or relationship
here; these are just some of the most common issues that people have
wanted to better understand.

### **How Do the Preconditions for Action Vary from Day to** **Day?**


For people to take action, the six CREATE preconditions must align for the
specific action, the specific environment, and the specific person (the actor).
Both the person and the environment vary over time, and thus so do the
preconditions for action:


_Environment_


As a person moves through the day, the environment generally changes.
The different environments shape whether the person will take a
particular action or not. For example, someone may have internet access
while waiting for a meeting and can use mobile apps, but not while
driving. The person may see reminders to exercise at home, but not
while at the bar.


_Actor_


Over the course of the day, _people_ also vary in themselves. Their
wakefulness varies, their tendency to be distracted varies, and of course,
so do their emotions. An action that seems interesting and worthwhile to
a rested, well-fed person can seem overly complex, too much work, and
not urgent to someone who is hungry and tired.


This variation is a mix of happenstance and structure. Day to day, a person’s
work schedule may be too irregular to identify stable moments of
opportunity for engagement with the product. But the commuting schedule
may be stable and clear. Where feasible, the product should align with the


moments and situations of opportunity, in which some of the preconditions
for action are already naturally in place, and then fill in the gaps.1


From the perspective of product design, look for structure within this dayto-day (and moment-to-moment) variation, and build on it to encourage
action. Are there particular times and places when the user of the product is
least distracted? Or most motivated to act? Where are the cues to act in the
person’s daily life?


You have two main options to harness the natural variation in people’s days.
You can do user research and try to find structured opportunities for
engagement that are common across the user base. Alternatively, you can
prompt users to self-identify the best times for them—when they want to
receive reminder messages, when they want to be motivated with uplifting
stories from other users, etc.

### **What Changes as a User Gains Experience with the** **Product?**


There are many ways people can change as they use a product. Rather than
a proscriptive pathway, there are different states that users can be in,
relative to the product. In each of these states, the dynamics of the CREATE
Action Funnel (Cue, Reaction, Evaluation, Ability, Timing, Experience) are
somewhat different:


_Not a user of the product_


_Dynamics._ For someone who has never used the product
before, its very newness is a benefit and a curse. Cues are
likely to be noticed. Newness can increase motivation to
explore. But newness can make the user unsure about the
logistics of actually using it and that person’s ability to
succeed. Also, our intuitive reaction to the idea is based
on our experiences with similar activities, which could be
good or bad.


_What the company should do._ Ensure the user knows
about the product at all (cue). Make sure the value is clear
(evaluation), and associate the product with familiar,
pleasant things (reaction).


_A one-time user of the product who had a positive experience_


_Dynamics._ Once we gain experience with a product, our
future intuitive reactions take that into account. If we liked
the product the first time we used it, excellent. We gain
knowledge of how to use it (decrease costs, increase
logistical ability).


_What the company should do._ Keep cueing the user; it’s
unlikely that the user has built a strong association
between the product and an existing cue in their
environment. Highlight the positive experience
(evaluation and reaction). Use knowledge gathered during
the first use to try to align the product with times and
situations when the user isn’t distracted and can take
action (ability and timing).


_A one-time user of the product who had a negative experience_


_Dynamics._ If the first experience was negative, we have
two obstacles to overcome: the allure of newness is gone,
and we have an intuitive negative reaction. It is much
harder to bring these users back.


_What the company should do._ Honestly, focus attention on
other users. This is a tough group to win back. And focus
attention on improving the experience of first-time users
in the future.


_A user who’s returned to the product one or more times_


_Dynamics._ When a user has successfully returned to the
product, that’s a sign that the conditions are ripe for future
use. Something in the user’s context has pulled them back.
However, it’s not clear yet how _stable_ that something is—
it might be a temporary assignment at work that makes the
user think about or need the product. It might be a core
desire. At this point, minor disruptions to the user’s
context (a different routine at work, etc.) can easily stop
them from returning.


_What the company should do._ Keep cueing the user until
there’s a strong association between the product and an
existing environmental cue. Highlight prior positive
experiences and successes. With user research, try to
understand the user’s context: are there temporary factors
pushing them to use it for which the product must find a
substitute?


_A user who regularly uses the product_


_Dynamics._ When the user returns to the product
repeatedly, there’s a stable context that pulls them back.
Only major changes in the user’s context are likely to
disrupt continued use—the user changes jobs, gets
divorced, takes on significant new activities that pressure
their time, or the product suddenly drops the particular
functionality they love.


_What the company should do._ Don’t screw it up. Be very
careful when changing functionality that’s driving usage.
Look for regular users who drop off—if the context
disruption is temporary, there’s a very good chance you
can win them back (but don’t take it for granted). If you
are working with a potentially habitual behavior, make
sure the cue and routine are constant over time.


_Habitual user_


_Dynamics._ If the user returns on a regular basis and
responds automatically to an environment cue, you’ve
successfully built a habit of use. (You can see whether it’s
a habit by looking at the usage pattern in the data and
through user research.) Since the behavior is largely on
autopilot, it’s highly resistant to change. Only major
changes in the cue or a lack of ability to act are likely to
break it.


_What the company should do._ Don’t mess with the cue or
change the fundamental learned routine that users enact.


Nir Eyal talks about how to leverage the initial usage of an application to
build future interest and make it easier or more valuable for users to return.
He refers to it as the “investment” step that occurs right after an individual
has had a positive experience with the product. He focuses on investment in
the formation of habits, but it’s an insight that can be applied for
nonhabitual behaviors as well.2


As users gain experience with a product, the type of support they need
changes. The most critical periods for adopting a new product to change
behavior is the first experience (when curiosity and newness is replaced by
an evaluation of the product) and in the transition from a returning user to a
regular user (when minor changes in circumstance can disrupt the new
behavior). Does the product provide an excellent first-time user experience?
Does it provide a compelling, ongoing reason to return to the product—
especially on a regular schedule with a stable cue to facilitate habit
formation?

### **How Can You Sustain Engagement with Your Product?**


Products that seek to change long-term behavior can’t do that if people stop
using the product. Sustained engagement requires an act of behavior change


just like the target behavior itself. At a high level, _driving continued usage_
_of a product follows the same rules outlined throughout this book_ .


Too often, companies just focus on providing value and wonder why users
don’t come back. Value is important—users have to want to use the product
or they won’t do so voluntarily. But there’s much more involved, and much
more that companies can do.


The six CREATE preconditions are need for _reengaging_ with a product, and
it’s the cue that I think has received the least attention and thought in
product development circles—at least outside of growth hacking. Perhaps
it’s because we think that if we build the greatest product in the world,
people will naturally come and use it.


To cue individuals to frequently reengage with a product:


_Continue to provide value_


Absolutely, this is essential. If users don’t think your product is
worthwhile, you aren’t going to be able to grab their attention
repeatedly (they’ll change their environment to avoid you). So, value is
the first step. But it’s only the first step.


_Uniquely become part of the person’s environment_


One way to remind people to use a product is to ensure its seen—by
placing the Fitbit by the side of the bed or by making your application
the home page on a browser. By _uniquely_, I mean that there aren’t other
shiny things the person is seeing at the same time; that’s a real problem
with tweets and emails, for example—they are extraordinarily crowded
channels.


_Uniquely become part of the person’s expected routine_


At a particular time of day (or situation), train the user to uniquely think
of the application as a way to do something or relieve boredom.
“Training” isn’t happenstance: ask the user to plan out a particular time
to use the product (i.e., as part of implementation intentions). If you’re
providing value, then help users form a habit around getting that value.


_Be so darn cool and memorable that people think of you, on their own_


We all aspire to this, and we think that a beautiful product will make
users dream about us. I don’t know about you, but I’ve seen a lot of
beautiful artwork in museums. I don’t dream about them, and neither do
I dream about more than a handful of products. So, invest in other ways
to get attention.


_Build strong associations with something that is part of the user’s_
_environment or daily routine_


If you can’t get in front of users’ eyeballs directly or reserve a slot on
their daily calendar, build on what’s already there. For example,
whenever there’s a crisp spring weekend day in DC (an existing aspect
of my environment), I think of the bike trailer my kid loves riding in
and head to the garage to get it.


_Be useful each and every time they see you_


Don’t train the user to ignore you. Does your carpet catch your
attention? No. It’s in your line of sight, and you step on it as part of your
daily schedule. But it does nothing for you most of the time. Same thing
with sending lots of emails to users. _Don’t be the carpet._


_Be new and different each time (or at least appear so!)_


One way to avoid being the carpet is to make sure that each attentiongrabbing piece of content contains something new (or potential for
newness)—social network notifications do this beautifully with their
teaser emails about friends doing stupid stuff. It’s more than a random
reward for logging into Facebook or Twitter—the attention grabber
itself is different each time.


To reiterate, you can think about behavior change as a two-stage problem.
First, there’s the behavior of engaging with your application. Second,
there’s the behavior that the application seeks to support. The same tools


taught throughout this book for the latter behavior are also applicable to the
former.

### **What Happens Before People Take Action the First** **Time?**


The CREATE Action Funnel provides the six preconditions for action, and
the DECIDE process ensures those preconditions are in place for a product.
But how do people normally progress from inaction to action _over time_ ?


There’s no consensus in the literature about how individuals move from
inaction to action on their own. There are many pathways by which people
become active, each of which brings together the preconditions for action in
their own way. The intentional design of products to support action,
described here, is just one of those pathways.


Consider the example of a person who wants to clean the house. They have
a positive intuitive reaction and decide that the benefits (parter won’t leave
them) outweigh the costs (an afternoon of TV watching lost) after a
conscious evaluation. But there are always more pressing things to do (no
time pressure), they forget to do it (no cue), or they don’t know how to do it
effectively and don’t have the right cleaning supplies (lacking ability).


Here’s a quick overview of different pathways by which this person could
move from failing to take the action to successfully doing it:


_Self-directed action_


They think about cleaning a few times and it doesn’t happen. When
they’re at the grocery store, they remember to pick up cleaning supplies
but don’t set aside time to use them. One day, they say enough is
enough and plan out a specific day and time to do it, set a reminder, and
remove other distractions.


_Intentional help from another person_


A friend hears them complaining about their dirty house and decides to
push a bit to get it done. The friend reminds them at the grocery store to


get supplies and makes them commit to cleaning on a particular day.


_Directed help from a product_


They download a task-management app based on David Allen’s book
_Getting Things Done_ (Penguin Books, 2001). They record all the things
they need to do (cleaning and otherwise) and, with the help of the app,
works out the logistics and timing to finally clean up the house.


_Sudden change in environment_


They want to clean the house but just don’t get it together for other
reasons (they change jobs and move). Their new house is much smaller
and they get rid of most of their stuff. It’s also much easier to clean, and
they find it’s easy to continue a habit of keeping the house clean once
they’ve started.


_Sudden change in life circumstances_


The user gets married. Their spouse won’t put up with the messiness
and lays down the law. The user shapes up.


_Social drift_


For various reasons, they get to know new people at work and some of
them become friends. The user visits their coworkers’ houses, which are
pleasantly clean. When they go home, they look at their house
differently. This happens a few times, and they’re ashamed of bringing
other people over. The user gets up the gumption and does it.


These are common pathways, but of course there are many more. The point
is that there simply isn’t a single route by which people change their
behavior over time. Sometimes there’s a single, culminating event that
forces change (marriage); at other times, things move more slowly (social
drift).


While these examples point to multiple _possible_ routes, anecdotes aren’t
science. Thus far, researchers haven’t established clear, generally accepted


rules for how individuals move from inaction to action over the course of
time. There’s a great deal of activity in the addiction and health space, with
models such as the Transtheoretical Model3 and Health Belief Model,4 but
their general applicability is unclear. We know a lot more about what
happens at the moment of action (a cue, a conscious choice to act, etc.) than
we do about what happens before that action.

## **Looking Ahead**


Designing for behavioral change has gone mainstream. Even a few years
ago, it was rare to find organizations with dedicated in-house behavioral
science teams; now we can count over 450. Major companies as diverse as
Walmart and Weight Watchers are designing for behavior change, as are
numerous small consultancies and scrappy NGOs. Since 2013, behavioral
teams have sprouted all around the world, and there appears to be no
slowdown on the horizon.


The benefits of this work are tremendous: from saving the lives of anemic
mothers to helping people save for the future. As the field grows, these
wonderful societal benefits will continue and expand. Significant
challenges, however, loom ahead: the most important of which is ethical.
Simply said, there are shady practices in our field that deceive and hurt
everyday people: from pushing gig economy drivers to drive past safe limits
to tricking people into giving up their detailed location data.


That is the nature of designing for behavior change today: exciting growth
and good being done side by side with troubling abuses. I believe that to
foster the former, we must confront the latter. The path isn’t clear, but by
applying behavioral science on ourselves and our job sites, we may be able
to more deeply design ethical behavior into our work, just as we seek to
(beneficially) shape others’ behavior and outcomes.


We’re at turning point in our field. We have a nuanced understanding of
how the mind works and how people take action, one that will continue to
grow and be adjusted over time, but one that provides us with guidance and
insights today. We have, effectively, a blueprint for behavior change—one


that many teams working in parallel around the globe have developed on
their own, which I’ve summarized here with the DECIDE framework.
Designing for behavior change is here to stay. What shape our field will
take exactly, and what mistakes and successes we’ll have, depends on what
we do with the foundation we’ve built over the last few years and how
seriously we face the challenges ahead.


1 The concept of fluctuating environmental and social factors that create opportunities for

action is a core concept of the Political Opportunity Structure tradition in political sociology
(e.g., McAdam et al. 2001). BJ Fogg also models fluctuations in motivation with his concept of
[a Motivation Wave over time. Fogg (2012).](https://oreil.ly/b71AS)


2 Eyal (2013, 2014)


3 Prochaska and Velicer (1997). Unlike my preceding assertion, this model proposes that there’s

a _single_ pathway to action. But it’s just not one that I see as generally applicable or true.


4 Janz and Becker (1984)


# **Glossary of Terms**

This book introduces many new concepts and terms, such as the _behavioral_
_map_ and the CREATE Action Funnel. This glossary provides definitions of
those terms, for your convenience. For the sake of brevity, though, many of
the common behavioral economics terms referenced in the book (e.g.,
_implementation intentions_ ) are not included here.


_A/A test_


an “experiment” in which there is no difference between the arms of the
test. An A/A test allows you to verify that the randomization process
and analysis code is working correctly. If you see a difference in
outcomes across the two groups, there’s something wrong!


_A/B test_


a method of comparing two versions of something against each other to
determine which one performs better. Two variants are shown to users at
random, and a statistical analysis is used to determine which variation
performs better for a given outcome metric. An A/B/C… test is an
extended version, with 3+ versions.


_A/Null test_


a method of testing that takes the baseline intervention (aka, version of
the product, feature, etc.) and tests it against no intervention at all. It
provides the clearest and simplest measure of that intervention’s impact.
It is also valuable to ensure that the intervention doesn’t actually make
the user _worse_ off (which is something that is missed with many A/B
tests).


_ability (per the CREATE Action Funnel)_


a stage in the CREATE Action Funnel when the user evaluates whether
or not she can take the target action now. The ability to take the target
action has four criteria: knowing logistically how to take the action,
having the resources necessary to act, having the skills necessary to act,
and having a sense of self-efficacy or belief in success. See _CREATE_
_Action Funnel._


_actor (aka target actor)_


the person who takes action because of the product. When the _actor_
takes the _action_, it causes the product’s _outcome_ . See _(target) action,_
_(target) outcome._


_action (aka target action)_


the behavior that the design process seeks to engender. When the _actor_
takes the _action_, it causes the product’s _outcome_ . Note: “action” and
“behavior” are used as synonyms throughout the book. See _(target)_
_actor, (target) outcome._


_behavioral bridge_


a description that links a behavior that the user already knows and is
comfortable with to a new, unfamiliar behavior. For example, an appeal
to users that describes the (unfamiliar) act of running a race as similar to
the (familiar) running around the office they normally do.


_behavioral map_


a detailed “story” of how the user progresses from being a neophyte to
accomplishing the action while using the product. The “story” can take
many forms, such as a journey map, written narrative, or a simple list of
actions. The behavioral map provides the conceptual design for the
product, providing its functional requirements. See _conceptual design_ .


_behavioral persona_


a stylized individual used to represent a group of users who are likely to
respond similarly to an appeal to change their behavior. For example,
the persona “active Jake” could represent users of the product who are
active in their daily lives and would be likely to join a competition to
see who exercises the most. See _persona_ .


_behavioral strategy_


a high-level strategy for changing behavior with a product. This book
discusses three strategies: supporting the conscious choice to take the
target action, building (or changing) habits, and “cheating.”


_behavioral tactic_


a low-level technique for changing behavior in a product. For example:
showing a peer comparison, highlighting loss aversion, or priming a
particular mindset. See also _behavioral strategy._


_cheating (per behavioral strategies)_


a strategy for changing behavior in which the burden of work is shifted
from the user to the product, and the user need only give consent for the
action to occur on his behalf. See _behavioral strategy._


_company objective_


what the company seeks to achieve, for itself, by building the product.


_conceptual design_


a set of documents or illustrations that indicate what the product should
do (i.e., what functionality the product should provide) at a conceptual
level. When designing for behavior change, the behavioral map fulfills
this role. See _behavioral map._


_context (of action)_


the three factors that shape a user’s decision whether or not to act.
Namely, the _user_ himself, the _environment_ the user is in, and the _action_


the user is deciding upon.


_CREATE Action Funnel_


a stylized model of how the mind makes the conscious decision to act.
Once the mind detects a cue, it has an intuitive reaction, which may
bubble up into conscious awareness for evaluation of the merits of
action, and an assessment of whether the user has the ability and right
timing to act, tempered by prior experience. If all of these mental
processes pass successfully without the user getting distracted or
deciding against the action, the user will execute the action. Together,
they spell the acronym CREATE. See cue, reaction, evaluation, ability,
timing, and experience.


_cue (per habits)_


something that causes a habit to occur. The cue can be something the
person sees, hears, smells, or touches in the environment (an external
cue) or an internal state like hunger (internal cue) that initiates the
habitual routine.


_cue (per the CREATE Action Funnel)_


the first stage in the CREATE Action Funnel when something first
makes the user think about taking the target action. The cue can be
something the person sees, hears, smells, or touches in the environment
(an external cue) or an internal state like hunger (internal cue) that starts
the process of taking action. For habitual actions, the cue alone can be
enough to cause the behavior to occur. See _CREATE Action Funnel._


_data bridge_


a mathematical relationship or statistical model that relates a target
outcome outside of the product to behavior within the product. For
example, “60% of the time that users indicate in the application that
they will create a vegetable garden, they actually create one.”


_designing for behavior change, DECIDE_


a six-stage process of designing a product with the specific purpose of
changing user behavior. The six stages are: _Define_ the problem, _Explore_
the context, _Craft_ the intervention, _Implement_ within the product,
_Determine_ the impact, _Evaluate_ what to do next.


_dual process theory(ies)_


a family of related theories in psychology that posit that the mind
effectively has two independent decision-making processes: one
deliberative and one intuitive. The deliberative, or “System 2,” process
is associated with intentional conscious thought. The intuitive, or
“System 1,” process is associated with automatic, emotional reactions or
implicit, “subconscious” behaviors.


_environment (of action)_


one of the three parts of the decision-making context (along with the
user and the action itself) that shapes a user’s decision to act. The
environment consists of the product that the person is interacting with
and the physical environment surrounding the person when he decides
whether or not to act. See _context._


_evaluation (per the CREATE Action Funnel)_


the third stage in the CREATE Action Funnel, when the user
consciously evaluates the value of taking the target action, often
considering its costs and benefits. See _CREATE Action Funnel._


_experience (per the CREATE Action Funnel)_


the sixth stage in the CREATE Action Funnel, which reminds
behavioral designers of the tremendous power of an individual’s past
experience. Even if “most” people have a particular reaction or bias, a
particular person’s past experience can override that response. See
_CREATE Action Funnel._


_external cue_


something in our environment that causes us to think about or take a
certain action. See _cue, internal cue._


_extrinsic motivation_


the desire to achieve a particular outcome, such as receiving a reward
for it (like money or winning a competition). See _intrinsic motivation._


_habit_


a repeated behavior that’s triggered by internal or external cues. A habit
is automatic: the action occurs outside of conscious control, and we may
not even be aware of it happening. Habits can be formed through simple
cue-routine repetition or can include a reward that becomes associated
with the cue and encourages the user to repeat the behavior. See _cue,_
_routine, reward._


_interface design_


a set of documents or illustrations that says how the product should look
and interact with the user.


_internal cue_


a prior thought or bodily state (like hunger) that leads us to think about
or take a certain action. See _cue, external cue._


_intrinsic motivation_


comes from the inherent enjoyment of the activity itself, without
considering any external pressure or reward. See _extrinsic motivation._


_mindset_


a mental mechanism for interpreting and responding to the world, which
shapes how we act. Mindsets as facets of the mind, which are built up in
different contexts. Here, the term is used to encompass a range of


psychological mechanisms that guide our behavior in ambiguous
contexts, including schemas and activated frames.


_Minimum Viable Action (MVA)_


the shortest, simplest version of the target action that users can be asked
to take, with which the company can still test whether the product has
the desired impact on behavior. See _target action._


_Multivariate Test_


a technique for testing a hypothesis in which multiple, independent
interventions are simultaneously tested. The goal being to determine
which combination or variations performs the best, out of all of the
possible combinations.


_outcome (aka target outcome)_


the real-world impact that the company seeks to have because of the
product. A measureable change in the world that happens when the
product succeeds in changing behavior. When the _actor_ takes the _action_,
it causes the product’s _outcome_ . See _(target) actor, (target) action._


_persona_


in the user experience field, a persona is a stylized individual used to
represent a group of similar users, usually based on a particular
demographic profile. See _behavioral persona_ .


_reaction (per the CREATE Action Funnel)_


the second stage in the CREATE Action Funnel when the user has an
automatic, System 1 reaction to the idea of taking action. That reaction
renders an intuitive verdict (whether the action is interesting or not)
based on prior associations with the action or similar experiences. It
also activates thoughts about other possible actions the person could
take. See _CREATE Action Funnel._


_reward (per habits)_


something that gives us a _reason_ to repeat a behavior. It might be
something inherently pleasant, like good food, or the completion of a
goal we’ve set for ourselves, like putting away all of the dishes.


_routine (per habits)_


the habitual action that a person takes when exposed to the habit’s cue.
For example, buying Starbucks coffee whenever a person sees the
Starbucks sign next to her office at 9 a.m. in the morning.


_self-narrative_


how we label ourselves, and how we describe our behavior in the past.


_small win_


a feeling of accomplishment after a (relatively small) action is taken.


_timing (per the CREATE Action Funnel)_


the fifth stage of the CREATE Action Funnel, in which the user
determine _when_ to act. See _CREATE Action Funnel._


_user story_


A term used in product development (especially agile development) for
a plain-English statement about what the user needs. It captures the
“who,” “what,” and “why” of a product requirement. For example, “As
a user, I want to [take an action], in order to [reason for action].” See
[Wikipedia for more information.](https://oreil.ly/XA9Qv)


_vision (aka product vision)_


_why the product is being developed_, at a high level.


# **Bibliography**

Alba, Joseph W. 2011. _Consumer Insights: Findings from_
_Behavioral Research_ . Edited by Joseph W. Alba. Cambridge, MA:
Marketing Science Institute.


Albergotti, Reed. 2014. “Furor Erupts Over Facebook’s
Experiment on Users.” _Wall Street Journal_, June 30, 2014.
_[https://oreil.ly/_j8xy](https://oreil.ly/_j8xy)_ .


Allcott, Hunt. 2011. “Social Norms and Energy Conservation.”
_Journal of Public Economics_ 95 (9–10): 1082–95.
_[https://doi.org/10.1016/j.jpubeco.2011.03.003](https://doi.org/10.1016/j.jpubeco.2011.03.003)_ .


Alter, Adam. 2018. _Irresistible: The Rise of Addictive Technology_
_and the Business of Keeping Us Hooked_ . New York: Penguin
Books.


American Thyroid Association. n.d. “Iodine Deficiency.” Accessed
April 1, 2020. _[https://oreil.ly/DdXEW](https://oreil.ly/DdXEW)_ .


Anderson, Stephen P. 2011. _Seductive Interaction Design: Creating_
_Playful, Fun, and Effective User Experiences_ . Berkeley, CA: New
Riders.


Anderson, Stephen P. 2013. “Mental Notes.”
_[http://getmentalnotes.com](http://getmentalnotes.com/)_ .


Appiah, Kwame Anthony. 2008. _Experiments in Ethics_ .
Cambridge, MA: Harvard University Press.


Ariely, Dan. 2009. _Predictably Irrational: The Hidden Forces That_
_Shape Our Decisions_ . New York: HarperCollins.


Ariely, Dan. 2010. _The Upside of Irrationality: The Unexpected_
_Benefits of Defying Logic at Work and at Home_ . New York: Harper


Perennial.


Ariely, Dan. 2013. _The Honest Truth About Dishonesty: How We_
_Lie to Everyone—Especially Ourselves_ . New York: Harper
Perennial.


Ariely, Dan, Jason Hreha, and Kristen Berman. 2014. _Hacking_
_Human Nature for Good: A Practical Guide to Changing Human_
_Behavior_ . Irrational Labs.


Balz, John, and Stephen Wendel. 2014. _Communicating for_
_Behavior Change: Nudging Employees Through Better Emails_ .
HelloWallet.


Bandura, Albert. 1977. “Self-Efficacy: Toward a Unifying Theory
of Behavioral Change.” _Psychological Review_ 84 (2): 191–215.
_[https://doi.org/10.1037/0033-295X.84.2.191](https://doi.org/10.1037/0033-295X.84.2.191)_ .


Banerjee, Abhijit, Esther Duflo, Rachel Glennerster, and Cynthia
Kinnan. 2015. “The Miracle of Microfinance? Evidence from a
Randomized Evaluation.” _American Economic Journal: Applied_
_Economics_, 7 (1) 22–53. _[http://doi.org/10.1257/app.20130533](http://doi.org/10.1257/app.20130533)_ .


Bargh, John A., Mark Chen, and Lara Burrows. 1996.
“Automaticity of Social Behavior: Direct Effects of Trait Construct
and Stereotype Activation on Action.” _Journal of Personality and_
_Social Psychology_ 71 (2): 230–244.


Baron, Jonathan. 2012. “The Point of Normative Models in
Judgment and Decision Making.” _Frontiers in Psychology 3_,
December 24, 2012. _[https://doi.org/10.3389/fpsyg.2012.00577](https://doi.org/10.3389/fpsyg.2012.00577)_ .


Baumeister, Roy F. 1984. “Choking Under Pressure: SelfConsciousness and Paradoxical Effects of Incentives on Skillful
Performance.” _Journal of Personality and Social Psychology_ 46
(3): 610–620. _[https://doi.org/10.1037/0022-3514.46.3.610](https://doi.org/10.1037/0022-3514.46.3.610)_ .


Bayer, Patrick J., B. Douglas Bernheim, and John Karl Scholz.
2009. “The Effects of Financial Education in the Workplace:
Evidence From A Survey Of Employers.” _Economic Inquiry_ 47
(4): 605–624. _[https://dx.doi.org/10.1111/j.1465-7295.2008.00156.x](https://dx.doi.org/10.1111/j.1465-7295.2008.00156.x)_ .


Benartzi, Shlomo, and Richard H. Thaler. 2004. “Save More
Tomorrow: Using Behavioral Economics to Increase Employee
Saving.” _Journal of Political Economy_ 112 (1) (February): S164–
S187. _[https://doi.org/10.1086/380085](https://doi.org/10.1086/380085)_ .


Berridge, Kent C., Terry E. Robinson, and J. Wayne Aldridge.
2009. “Dissecting Components of Reward: ‘Liking’, ‘Wanting’,
and Learning.” _Current Opinion in Pharmacology_ 9 (1)
(February): 65–73. _[https://doi.org/10.1016/j.coph.2008.12.014](https://doi.org/10.1016/j.coph.2008.12.014)_ .


Beshears, John, and Katherine Milkman. 2013. “Temptation
Bundling and Other Health Interventions.” Action Design DC
Meetup, April 21.


Blackson, Thomas. 2020. “The Tripartite Theory of the Soul.”
Ancient Greek Philosophy From the Presocratics to the Hellenistic
Philosophers. Last modified January 23, 2020.
_[https://oreil.ly/bXhqw](https://oreil.ly/bXhqw)_ .


Bogost, Ian. 2012. “The Cigarette of This Century.” _The Atlantic_,
June 6, 2012. _[https://oreil.ly/4u0jJ](https://oreil.ly/4u0jJ)_ ..


Bond, Samuel D., Kurt A. Carlson, and Ralph L. Keeney. 2008.
“Generating Objectives: Can Decision Makers Articulate What
They Want?” _Management Science_ 54 (1): 56–70.
_[https://oreil.ly/AWIaO](https://oreil.ly/AWIaO)_ .


Bond, Samuel D., Kurt A. Carlson, and Ralph L. Keeney. 2010.
“Improving the Generation of Decision Objectives.” _Decision_
_Analysis_ 7 (3): 235–326. _[https://doi.org/10.1287/deca.1100.0172](https://doi.org/10.1287/deca.1100.0172)_ .


Booth, Julie. 2019. “Assumption Slam: How Not to Make an A**
out of U and ME.” _Medium_, April 26, 2019. _[https://oreil.ly/OPNxs](https://oreil.ly/OPNxs)_ .


Brass, Marcel, and Patrick Haggard. 2008. “The What, When,
Whether Model of Intentional Action.” _The Neuroscientist_ 14 (4)
(August): 319–325. _[https://doi.org/10.1177/1073858408317417](https://doi.org/10.1177/1073858408317417)_ .


Brendryen, Håvar, and Pål Kraft. 2008. “Happy Ending: a
Randomized Controlled Trial of a Digital Multi-Media Smoking
Cessation Intervention.” _Addiction_ 103 (3): 478–484.
_[http://doi.org/10.1111/j.1360-0443.2007.02119.x](http://doi.org/10.1111/j.1360-0443.2007.02119.x)_ .


Cagan, Marty. 2008. _Inspired: How to Create Products Customers_
_Love_ . Sunnyvale, CA: SVPG Press.


Cash, Thomas F., Diane Walker Cash, and Jonathan W. Butters.
1983. “‘Mirror, Mirror, on the Wall...?’: Contrast Effects and SelfEvaluations of Physical Attractiveness.” _Personality and Social_
_Psychology Bulletin_ 9 (3): 351–58.
_[https://doi.org/10.1177/0146167283093004](https://doi.org/10.1177/0146167283093004)_ .


Chabris, Christopher, and Daniel Simons. 2010. _The Invisible_
_Gorilla: How Our Intuitions Deceive Us_ . New York: Broadway
Books (Crown Publishing).


Chatzisarantis, Nikos L. D., and Martin S. Hagger. 2007.
“Mindfulness and the Intention-Behavior Relationship Within the
Theory of Planned Behavior.” _Personality and Social Psychology_
_Bulletin_ 33 (5) (May): 663–676.
_[https://doi.org/10.1177/0146167206297401](https://doi.org/10.1177/0146167206297401)_ .


Chatzky, Jean. 2009. _Pay It Down! Debt-Free on $10 a Day_ . New
York: Penguin.


Choi, James J, David Laibson, Brigitte C Madrian, and Andrew
Metrick. 2002. “Defined Contribution Pensions: Plan Rules,
Participant Choices, and the Path of Least Resistance.” _Tax Policy_
_and the Economy_ 16: 67–114.


Cialdini, Robert B. 2008. _Influence: Science and Practice_ . 5th ed.
Boston: Pearson.


Cialdini, Robert B., Carl A. Kallgren, and Raymond R. Reno.
1991. “A Focus Theory of Normative Conduct: A Theoretical
Refinement and Reevaluation of the Role of Norms in Human
Behavior.” In _Advances in Experimental Social Psychology_, ed.
Mark P. Zanna, 24: 201–243. _https://doi.org/10.1016/S0065-_
_2601(08)60330-5_ .


Clear, James. 2012. “Identity-Based Habits: How to Actually Stick
to Your Goals This Year.” In _Atomic Habits_ . New York: Penguin.
_[https://oreil.ly/MGDMd](https://oreil.ly/MGDMd)_ .


Curtis, Dustin. 2009. “You Should Follow Me on Twitter.” _Dustin_
_Curtis_ (blog).


Dai, Hengchen, Katherine L. Milkman, and Jason Riis. 2014. “The
Fresh Start Effect: Temporal Landmarks Motivate Aspirational
Behavior.” _Management Science_ 60 (10): 2381–617.
_[http://dx.doi.org/10.1287/mnsc.2014.1901](http://dx.doi.org/10.1287/mnsc.2014.1901)_ .


Damasio, Antonio R, B.J. Everitt, and D Bishop. 1996. “The
Somatic Marker Hypothesis and the Possible Functions of the
Prefrontal Cortex [and Discussion].” _Philosophical Transactions:_
_Biological Sciences_ 351 (1346): 1413–1420.


Darley, John M, and C Daniel Batson. 1973. “‘From Jerusalem to
Jericho’: A Study of Situational and Dispositional Variables in
Helping Behavior.” _Journal of Personality and Social Psychology_
27 (1): 100–8. _[https://doi.org/10.1037/h0034449](https://doi.org/10.1037/h0034449)_ .


Darling, Matthew et al. 2017. “Practitioner’s Playbook.” ideas42.
_https://oreil.ly/bpyoA_ .


De Bono, Edward. 1973. _Lateral Thinking: Creativity Step by Step_ .
New York: Harper & Row.


De Bono, Edward. 2006. _Six Thinking Hats_ . London: Penguin
Books.


Dean, Jeremy. 2013. _Making Habits, Breaking Habits: Why We Do_
_Things, Why We Don’t, and How to Make Any Change Stick_ .
Boston, MA: Da Capo Press.


Deci, Edward L., Richard Koestner, and Richard M. Ryan. 1999.
“A Meta-Analytic Review of Experiments Examining the Effects
of Extrinsic Rewards on Intrinsic Motivation.” _Psychological_
_Bulletin_ 125 (6) (November): 627–668; 692–700.


Deci, Edward L., and Richard M. Ryan. 1985. _Intrinsic Motivation_
_and Self-Determination in Human Behavior_ . New York: Plenum
Press.


Demaree, David. 2011. “Google+ and Cognitive Overhead.” _David_
_Demaree_ (blog), July 20,2011. _https://oreil.ly/YDxBG_ .


Design Council. 2019. “What Is the Framework for Innovation?
Design Council’s Evolved Double Diamond.” _Design Council_ .
_[https://oreil.ly/W-4KG](https://oreil.ly/W-4KG)_ (January 20, 2020).


Deterding, Sebastian. 2010. “Just Add Points? What UX Can (and
Cannot) Learn from Games.” UXCamp Europe, Berlin, May 30,
2010. _[https://oreil.ly/c7e_2](https://oreil.ly/c7e_2)_ .


Dominus, Susan. 2017. “When the Revolution Came for Amy
Cuddy.” _The New York Times_, October 18, 2017.
_[https://oreil.ly/q4X2X](https://oreil.ly/q4X2X)_ .


Doyen, Stéphane, Olivier Klein, Cora-Lise Pichon, and Axel
Cleeremans. 2012. “Behavioral Priming: It’s All in the Mind, but
Whose Mind?” _PLoS ONE_ 7 (1) (January): e29081.
_[https://doi.org/10.1371/journal.pone.0029081](https://doi.org/10.1371/journal.pone.0029081)_ .


Duckworth, Angela L., Tamar Szabó Gendler, and James J. Gross.
2016. “Situational Strategies for Self-Control.” _Perspectives on_
_Psychological Science_ 11 (1): 35–55.
_[https://doi.org/10.1177/1745691615623247](https://doi.org/10.1177/1745691615623247)_ .


Duhigg, Charles. 2012. _The Power of Habit: Why We Do What We_
_Do in Life and Business_ . New York: Random House.


Dutch Authority for the Financial Markets. 2019. “AFM Invites
Businesses to Respond to Its ‘Principles for Choice Architecture’.”
_AFM_, November 25, 2019. _[https://oreil.ly/Z-E1b](https://oreil.ly/Z-E1b)_ .


Egan, Dan. 2017. “Our Evidence-Based Approach to Improving
Investor Behavior.” _Betterment_, October 12, 2017.
_[https://oreil.ly/ZWGCm](https://oreil.ly/ZWGCm)_ .


Eldridge, Laura L., Donna Masterman, and Barbara J. Knowlton.
2002. “Intact Implicit Habit Learning in Alzheimer’s Disease.”
_Behavioral Neuroscience_ 116 (4): 722–6.
_[https://doi.org/10.1037/0735-7044.116.4.722](https://doi.org/10.1037/0735-7044.116.4.722)_ .


Elliott, Justin, and Lucas Waldron. 2019. “Here’s How TurboTax
Just Tricked You Into Paying to File Your Taxes.” _ProPublica_,
April 22, 2019. _[https://oreil.ly/fZer2](https://oreil.ly/fZer2)_ .


Engber, Daniel. 2016. “Everything Is Crumbling.” _Slate_, March 6,
2016. _[https://oreil.ly/oS06G](https://oreil.ly/oS06G)_ .


Eyal, Nir. 2012. “How To Manufacture Desire” _TechCrunch_,
March 4, 2012. _https://oreil.ly/HepWM_ .


Eyal, Nir. 2013. “Hooked Workshop.” _Slideshare_, March 31, 2013.
_[https://oreil.ly/0xI76](https://oreil.ly/0xI76)_ .


Eyal, Nir. 2014. _Hooked: How to Build Habit-Forming Products_ .
ed. Ryan Hoover. New York: Portfolio.


Fellowes, Matt, and Katy Willemin. 2013. “The Retirement Breach
in Defined Contribution Plans.” HelloWallet Research Reports.


Fernandes, Daniel, John G. Lynch, and Richard G. Netemeyer.
2014. “Financial Literacy, Financial Education, and Downstream
Financial Behaviors.” _Management Science_ 60 (8): 1861–2109.
_[https://doi.org/10.1287/mnsc.2013.1849](https://doi.org/10.1287/mnsc.2013.1849)_ .


Festinger, Leon. 1957. _A Theory Of Cognitive Dissonance_ .
Redwood City, CA: Stanford University Press.


Filiz-Ozbay et al. 2013. “Do Lottery Payments Induce Savings
Behavior: Evidence from the Lab.” _Journal of Public Economics_
126 (June): 1–24. _[https://oreil.ly/YZibp](https://oreil.ly/YZibp)_ .


Fisher, Robert J. 1993. “Social Desirability Bias and the Validity of
Indirect Questioning.” _Journal of Consumer Research_ 20 (2): 303–
315.


Fogg, B.J. 2002. _Persuasive Technology: Using Computers to_
_Change What We Think and Do_ . San Francisco: Morgan
Kaufmann.


Fogg, B.J. 2009a. “A Behavior Model for Persuasive Design.” In
_Persuasive 2009: Proceedings of the 4th International Conference_
_on Persuasive Technology_, 40 (April): 1–7.
_[https://doi.org/10.1145/1541948.1541999](https://doi.org/10.1145/1541948.1541999)_ .


Fogg, B.J. 2009b. “The Behavior Grid: 35 Ways Behavior Can
Change.” In _Persuasive 2009: Proceedings of the 4th International_
_Conference on Persuasive Technology_, 42 (April): 1–5.
_[https://doi.org/10.1145/1541948.1542001](https://doi.org/10.1145/1541948.1542001)_ .


Fogg, B.J. 2012. “Motivation Wave.” _Keynote Address at Health_
_User Experience Design Conference_, April 15, 2012.
_https://oreil.ly/b71AS_ .


Fogg, B.J. 2020. _Tiny Habits: The Small Changes That Change_
_Everything_ . Boston: HMH Books.


Fogg, B.J., and Jason Hreha. 2010. “Behavior Wizard: A Method
for Matching Target Behaviors with Solutions.” In _Persuasive_
_Technology_, ed. Thomas Ploug, Per Hasle, and Harri OinasKukkonen. Lecture Notes in Computer Science 6137: 117–131.
Springer Berlin Heidelberg. _https://doi.org/10.1007/978-3-642-_
_13226-1_13_ .


Fogg, B.J., et al. 2001. “What Makes Web Sites Credible? A
Report on a Large Quantitative Study.” In _Persuasive Technology_
_Lab: Proceedings of the SIGCHI Conference on Human Factors in_
_Computing Systems_, 61–68. CHI ’01. New York: ACM.


Freedman, Jonathan L., and Scott C. Fraser. 1966. “Compliance
Without Pressure: The Foot-in-the-Door Technique.” _Journal of_
_Personality and Social Psychology_ 4 (2): 195–202.
_[https://doi.org/10.1037/h0023552](https://doi.org/10.1037/h0023552)_ .


Gabaix, Xavier, and David Laibson. 2005. “Shrouded Attributes,
Consumer Myopia, and Information Suppression in Competitive
Markets.” _The Quarterly Journal of Economics_ 121 (May): 505–
40. _[http://doi.org/10.3386/w11755](http://doi.org/10.3386/w11755)_ .


Gabriel, Felice Miller. 2016. “App Makers: It’s Time to Stop
Exploiting User Addiction and Get Ethical.” _VentureBeat_, April 2,
2016. _[https://oreil.ly/899Pr](https://oreil.ly/899Pr)_ .


Gallwey, W. Timothy. 1997. _The Inner Game of Tennis: The_
_Classic Guide to the Mental Side of Peak Performance_ . Revised
Edition. New York: Random House.


Garner, Randy. 2005. “Post-It Note Persuasion: A Sticky
Influence.” _Journal of Consumer Psychology_ 15 (3): 230–237.


Gazzaniga, Michael S., and Roger W. Sperry. 1967. “Language
After Section of the Cerebral Commissures.” _Brain_ 90 (1): 131–
148.


Gerber, Alan S., and Todd Rogers. 2009. “Descriptive Social
Norms and Motivation to Vote: Everybody’s Voting and so Should
You.” _The Journal of Politics_ 71 (01): 178–191.


Gigerenzer, Gerd. 2004. “Fast and Frugal Heuristics: The Tools of
Bounded Rationality.” _Blackwell Handbook of Judgment and_
_Decision Making_ (January): 62–88.
_[https://doi.org/10.1002/9780470752937.ch4](https://doi.org/10.1002/9780470752937.ch4)_ .


Gigerenzer, Gerd, and Peter M. Todd. 1999. “Fast and Frugal
Heuristics: The Adaptive Toolbox.” _Evolution and Cognition:_
_Simple Heuristics That Make Us Smart_ 3–34, Oxford University
Press.


Gilbert, Daniel, and Timothy D. Wilson. 2011. “The Social
Psychological Narrative, or, What Is Social Psychology, Anyway?”
_Edge.org_, June 7, 2011. _https://oreil.ly/LVulI_ .


Gladwell, Malcolm. 2005. _Blink: The Power of Thinking Without_
_Thinking_ . New York: Little, Brown and Company.


Gneezy, Uri, Stephan Meier, and Pedro Rey-Biel. 2011. “When
and Why Incentives (Don’t) Work to Modify Behavior.” _The_
_Journal of Economic Perspectives_ 25 (4): 191–209.


Goel, Vindu. 2014. “Facebook Tinkers With Users’ Emotions in
News Feed Experiment, Stirring Outcry.” _The New York Times_,
June 29, 2014. _[https://oreil.ly/EaxaF](https://oreil.ly/EaxaF)_ .


Goldstein, Daniel. 2011. “The Battle Between Your Present and
Future Self.” _TEDSalon NY2011_, November 2011.
_[https://oreil.ly/pfxPd](https://oreil.ly/pfxPd)_ .


Gollwitzer, Peter M. 1999. “Implementation Intentions: Strong
Effects of Simple Plans.” _American Psychologist_ 54 (7): 493–503.


Gonzalez, Robbie. 2018. “It’s Time For a Serious Talk About the
Science of Tech ‘Addiction.’” _Wired_, February 1, 2018.
_[https://oreil.ly/r1_iF](https://oreil.ly/r1_iF)_ .


GovTrack. 2019. “Deceptive Experiences To Online Users
Reduction Act (S. 1084).” _GovTrack.us_ . Last accessed June 29,
2019. _[https://oreil.ly/5pN2B](https://oreil.ly/5pN2B)_ .


Grier, Sonya, and Carol A. Bryant. 2005. “Social Marketing in
Public Health.” _Annual Review of Public Health_ 26 (1): 319–39.


Gupta, Shubhankar. 2020. “Multi-Armed Bandit (MAB) – A/B
Testing Sans Regret” _Split Testing Blog_ . _[https://oreil.ly/BMjIW](https://oreil.ly/BMjIW)_ .


Guynn, Melissa J., Mcdaniel, Mark A., and Einstein, Gilles O.
1998. “Prospective Memory: When Reminders Fail.” _Memory &_
_Cognition_ 26 (2): 287-98.


Haidt, Jonathan. 2006. _The Happiness Hypothesis: Finding_
_Modern Truth in Ancient Wisdom_ . Cambridge, MA: Basic Books.


Hallsworth, Michael, John A. List, Robert D. Metcalfe, and Ivo
Vlaev. 2017. “The Behavioralist as Tax Collector: Using Natural
Field Experiments to Enhance Tax Compliance.” _Journal of Public_
_Economics_, Elsevier 148 (April): 14– 31.


Halpern, David. 2015. _Inside the Nudge Unit: How Small Changes_
_Can Make a Big Difference_ . New York: Random House.


Hamilton, Jon. 2008. “Think You’re Multitasking? Think Again.”
_NPR.org_, October 2, 2008. _[https://oreil.ly/90J55](https://oreil.ly/90J55)_ .


Hammond, John S., Ralph L. Keeney, and Howard Raiffa. 2002.
_Smart Choices: A Practical Guide to Making Better Decisions_ .
New York: Crown Business.


Hanov, Steve. 2012. “20 Lines of Code That Will Beat A/B Testing
Every Time.” _Steve Hanov’s Blog_ (blog). _[https://oreil.ly/0VABH](https://oreil.ly/0VABH)_ .


Hayes, Lucy, Anish Thakrar, and William Lee. 2018. “Now You
See It: Drawing Attention to Charges in the Asset Management
Industry.” Rochester, NY: Social Science Research Network.
SSRN Scholarly Paper. _[https://oreil.ly/mKkRk](https://oreil.ly/mKkRk)_ .


Heath, Chip, and Dan Heath. 2010. _Switch: How to Change Things_
_When Change Is Hard_ . New York: Broadway Books (Crown
Publishing).


Hernandez, Marco, Jonathan Karver, Mario Negre, and Julie Perng.
2019. “Promoting Tax Compliance in Kosovo with Behavioral


Insights.” _World Bank_, March 5, 2019.


Hershfield, Hal E., et al. 2011. “Increasing Saving Behavior
Through Age-Progressed Renderings of the Future Self.” _Journal_
_of Marketing Research_ 48 (SPL, November): S23–S37.
_[https://doi.org/10.1509/jmkr.48.SPL.S23](https://doi.org/10.1509/jmkr.48.SPL.S23)_ .


Hilgert, Marianne A., Jeanne M. Hogarth, and Sondra G. Beverly.
2003. “Household Financial Management: The Connection
Between Knowledge and Behavior.” _Federal Reserve Bulletin_ 89:
309–22.


Hofmann, Wilhelm, Roy F. Baumeister, Georg Förster, and
Kathleen D. Vohs. 2012. “Everyday Temptations: An Experience
Sampling Study of Desire, Conflict, and Self-Control.” _Journal of_
_Personality and Social Psychology_ 102, no. 6 (June): 1318–35.


Hopkins, Anna, Jonathan Breckon, and James Lawrence. 2020.
“The Experimenter’s Inventory: A Catalogue of Experiments for
Decision-Makers and Professionals.” _Alliance for Useful Evidence_,
January, 2020. _[https://oreil.ly/RgOfq](https://oreil.ly/RgOfq)_ .


Ioannidis, John P. A. 2005. “Why Most Published Research
Findings Are False.” _PLoS Medicine_ 2 (8): e124.
_[https://oreil.ly/PvCZz](https://oreil.ly/PvCZz)_ .


Iyengar, Sheena S. 2010. _The Art of Choosing_ . New York: Hachette
Book Group.


Iyengar, Sheena S., and Mark R. Lepper. 2000. “When Choice Is
Demotivating: Can One Desire Too Much of a Good Thing?”
_Journal of Personality and Social Psychology_ 79 (6): 995–1006.


Jachimowicz, Jon and Johannes Haushofer. 2020. “COVID-19
Italy Survey March 12 2020 (N = 2500).” OSF.
_https://osf.io/4m2vh_ .


Jachimowicz, Jon, Sandra Matz, and Vyacheslav Polonski. 2017.
“The Behavioral Scientist’s Ethics Checklist.” _Behavioral_
_Scientist_, October 23, 2017. _[https://oreil.ly/qQkfx](https://oreil.ly/qQkfx)_ .


Jarrett, Christian. 2016. “Ten Famous Psychology Findings That
It’s Been Difficult To Replicate.” _Research Digest_, September 16,
2016. _[https://oreil.ly/lkYwy](https://oreil.ly/lkYwy)_ .


Janz, Nancy K., and Marshall H. Becker. 1984. “The Health Belief
Model: A Decade Later.” _Health Education & Behavior_ 11 (1)
(March): 1–47.


Jenkins Jr., G. Douglas, Atul Mitra, Nina Gupta, and Jason D.
Shaw. 1998. “Are Financial Incentives Related to Performance? A
Meta-Analytic Review of Empirical Research.” _Journal of Applied_
_Psychology_ 83 (5): 777–787.


Johnson, Eric, and Daniel Goldstein. 2003. “Do Defaults Save
Lives?” _Science_ 302 (5649): 1338–39.


Johnson, Jeff. 2010. _Designing with the Mind in Mind: Simple_
_Guide to Understanding User Interface Design Rules_ . Burlington,
MA: Morgan Kaufmann.


Johnson, Valen E. et al. 2017. “On the Reproducibility of
Psychological Science.” _Journal of the American Statistical_
_Association_ 112 (517): 1–10.


Kahneman, Daniel, Barbara L. Fredrickson, Charles A. Schreiber,
and Donald A. Redelmeier. 1993. “When More Pain Is Preferred to
Less: Adding a Better End.” _Psychological Science_ 4 (6): 401–5.


Kahneman, Daniel, and Amos Tversky. 1984. “Choices, Values,
and Frames.” _American Psychologist_ 39 (4): 341–50.


Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. 1991.
“Anomalies: The Endowment Effect, Loss Aversion, and Status
Quo Bias." _Journal of Economic Perspectives_ 5 (1): 193–206.


Kahneman, Daniel. 2011. _Thinking, Fast and Slow_ . New York:
Farrar, Straus and Giroux.


Kaldestad, Øyvind H. 2018. “Report: Deceived by Design.”
_Forbrukerrådet_, June 27, 2018. _[https://oreil.ly/Wj0ZP](https://oreil.ly/Wj0ZP)_ .


Kantrowitz, Mark. 2018. “Millions of Students Still Fail to File the
FAFSA Each Year.” _SavingForCollege.com_, September 17, 2018.
_[https://oreil.ly/MND3w](https://oreil.ly/MND3w)_ .


Karlan, Dean, and Jacob Appel. 2011. _More Than Good Intentions:_
_Improving the Ways the World’s Poor Borrow, Save, Farm, Learn,_
_and Stay Healthy_ . New York: Penguin.


Karlan, Dean, and Rebecca Mann, Jake Kendall, Rohini Pande,
Tavneet Suri, and Jonathan Sinman. 2016. “Making Microfinance
More Effective.” _Harvard Business Review_, October 5, 2016.
_[https://oreil.ly/BIkbY](https://oreil.ly/BIkbY)_ .


Karlan, Dean S., Margaret McConnell, Sendhil Mullainathan, and
Jonathan Zinman. 2011. “Getting to the Top of Mind: How
Reminders Increase Saving.” (working paper 16205, _National_
_Bureau of Economic Research_ ). _[https://oreil.ly/Ph04g](https://oreil.ly/Ph04g)_ .


Kearon, Ewing, and Wood. 2017. “System1: Unlocking Profitable
Growth.” United States System1 group.
_[https://www.system1group.com](https://www.system1group.com/)_ .


Kirby, Kris N. 1997. “Bidding on the Future: Evidence Against
Normative Discounting of Delayed Rewards.” _Journal of_
_Experimental Psychology: General_ 126 (1): 54–70.
_https://doi.org/10.1037/0096-3445.126.1.54_ .


Klein, Gary. 2007. “Performing a Project Premortem.” _Harvard_
_Business Review_, September 2007. _[https://oreil.ly/n3RrN](https://oreil.ly/n3RrN)_ .


Kolko, Jon. 2011. _Thoughts on Interaction Design a Collection of_
_Reflections_ . Second Edition. Burlington, MA: Morgan Kaufmann.


Kolotkin, Ronette L., Martin Binks, Ross D. Crosby, Truls Østbye,
Richard E. Gress, and Ted D. Adams. 2006. “Obesity and Sexual
Quality of Life.” _Obesity_ 14 (3): 472–479.


Kramer, Adam D. I., Jamie E. Guillory, and Jeffrey T. Hancock.
2014. “Experimental Evidence of Massive-Scale Emotional
Contagion Through Social Networks.” _Proceedings of the National_
_Academy of Sciences_ 111 (24): 8788–90.


Krug, Steve. 2006. _Don’t Make Me Think: A Common Sense_
_Approach to Web Usability_ . Berkeley, CA: New Riders.


Krulwich, Robert. 2009. “There’s a Fly in My Urinal.” _NPR.org_,
December 19, 2009. _[https://oreil.ly/D_iSB](https://oreil.ly/D_iSB)_ .


Kühberger, Anton, and Carmen Tanner. 2010. “Risky Choice
Framing: Task Versions and a Comparison of Prospect Theory and
Fuzzy-Trace Theory.” _Journal of Behavioral Decision Making_ 23
(3): 314–29.


Kwon, Diana. 2020. “Near Real-Time Studies Look for Behavioral
Measures Vital to Stopping Coronavirus.” _Scientific American_,
March 19, 2020. _[https://oreil.ly/GwXA4](https://oreil.ly/GwXA4)_ .


Laibson, David. 1997. “Golden Eggs and Hyperbolic
Discounting.” _Quarterly Journal of Economics_ 112 (2): 443–77.


Lally, Phillippa, Cornelia H. M. van Jaarsveld, Henry W. W. Potts,
and Jane Wardle. 2010. “How Are Habits Formed: Modelling
Habit Formation in the Real World.” _European Journal of Social_
_Psychology_ 40 (6): 998–1009.


Lanaria, Vincent. 2019. “Apple Wants to Prevent Apps from
Tricking Users into Signing up for Subscriptions.” _Tech Times_,
January 28, 2019. _[https://oreil.ly/_jTa4](https://oreil.ly/_jTa4)_ .


Langer, Ellen J., Arthur Blank, and Benzion Chanowitz. 1978.
“The Mindlessness of Ostensibly Thoughtful Action: The Role of


‘Placebic’ Information in Interpersonal Interaction.” _Journal of_
_Personality and Social Psychology_ 36 (6): 635–42.


Latané, Bibb, and John M. Darley. 1970. _The Unresponsive_
_Bystander: Why Doesn’t He Help?_ New York: Appleton-CenturyCrofts.


Leach, Will. 2018. _Marketing to Mindstates: The Practical Guide_
_to Applying Behavior Design to Research and Marketing_ .
Lioncrest Publishing.


Lewis, Chris. 2014. _Irresistible Apps: Motivational Design_
_Patterns for Apps, Games, and Web-Based Communities_ . New
York: Apress.


Lieb, David. 2013. “Cognitive Overhead, Or Why Your Product
Isn’t As Simple As You Think.” _TechCrunch_, April 20, 2013.
_https://oreil.ly/eXo8c_ .


List, John A., Sally Sadoff, and Mathis Wagner. 2010. “So You
Want to Run an Experiment, Now What? Some Simple Rules of
Thumb for Optimal Experimental Design.” (working paper 15701,
_National Bureau of Economic Research_ ).
_[http://doi.org/10.3386/w15701](http://doi.org/10.3386/w15701)_ .


Litvak, Paul M., Jennifer S. Lerner, Larissa Z. Tiedens, and
Katherine Shonk. 2010. “Fuel in the Fire: How Anger Impacts
Judgment and Decision-Making.” _International Handbook of_
_Anger: Constituent and Concomitant Biological, Psychological,_
_and Social Processes_, eds. Michael Potegal, Gerhard Stemmler,
and Charles Spielberger. New York, NY: Springer, 287–310.


Lockton, Dan with David Harrison and Neville A. Stanton. 2010.
“Design with Intent Toolkit.” _Requisite Variety_ .
_[https://oreil.ly/537E-](https://oreil.ly/537E-)_ .


Lockton, Dan. 2013. “Design with Intent: A Design Pattern Toolkit
for Environmental and Social Behaviour Change.” PhD Thesis,


Brunel University School of Engineering and Design.


Lusardi, Annamaria, and Olivia S. Mitchell. 2007. “Financial
Literacy and Retirement Preparedness: Evidence and Implications
for Financial Education.” _Business Economics_ 42 (1) (January):
35–44.


Lyons, Angela C., Lance Palmer, Koralalage S. U. Jayaratne, and
Erik Scherpf. 2006. “Are We Making the Grade? A National
Overview of Financial Education and Program Evaluation.”
_Journal of Consumer Affairs_ 40 (2): 208–235.


Maier, Steven F., and Martin E. Seligman. 1976. “Learned
Helplessness: Theory and Evidence.” _Journal of Experimental_
_Psychology: General_ 105 (1): 3–46.


Mandell, Lewis, and Linda Schmid Klein. 2009. “The Impact of
Financial Literacy Education on Subsequent Financial Behavior.”
_Journal of Financial Counseling and Planning Volume_ 20 (1): 16–
26.


Manis, Melvin, Jonathan Shedler, John Jonides, and Thomas E.
Nelson. 1993. “Availability Heuristic in Judgments of Set Size and
Frequency of Occurrence.” _Journal of Personality and Social_
_Psychology_ 65 (3): 448–57.


Martin, Neale. 2008. _Habit: The 95% of Behavior Marketers_
_Ignore_ . Upper Saddle River, NJ: FT Press.


Mathur, Arunesh, et al. 2019. “Dark Patterns at Scale: Findings
from a Crawl of 11K Shopping Websites.” Draft, June 25, 2019. 1–
32.


McAdam, Doug, Sidney Tarrow, and Charles Tilly. 2001.
_Dynamics of Contention_ . New York: Cambridge University Press.


McNeil, Barbara J., Stephen G. Pauker, Harold C. Sox, and Amos
Tversky. 1982. “On the Elicitation of Preferences for Alternative


Therapies.” _New England Journal of Medicine_ 306 (21) (May 27):
1259–62.


McNeil Jr., Donald G. 2006. “In Raising the World’s I.Q., the
Secret’s in the Salt.” _The New York Times_, December 16, 2006.
_[https://oreil.ly/EmZdB](https://oreil.ly/EmZdB)_ .


Meyer, David. 2018. “Google Is Accused of ‘Tricking’ Users into
Sharing Location Data Under the EU’s Strict New Privacy Laws.”
_Yahoo Finance_ . November 27, 2018. _[https://oreil.ly/4Nei3](https://oreil.ly/4Nei3)_ .


Michie, Susan, Maartje M. van Stralen, and Robert West. 2011.
“The Behaviour Change Wheel: A New Method for Characterising
and Designing Behaviour Change Interventions.” _Implementation_
_Science: IS_ 6 (April): 42.


Milkman, Katherine L., Julia A. Minson, and Kevin Volpp. 2013.
“Holding the Hunger Games Hostage at the Gym: An Evaluation
of Temptation Bundling.” SSRN Scholarly Paper ID 2183859.
Rochester, NY: Social Science Research Network.
_[https://oreil.ly/FR55W](https://oreil.ly/FR55W)_ .


Miller, George A. 1956. “The Magical Number Seven, Plus or
Minus Two: Some Limits on Our Capacity for Processing
Information.” _The Psychological Review_ 63 (2): 81–97.


Miltenberger, Raymond G. 2011. _Behavior Modification:_
_Principles and Procedures_ . 5 ed. Australia; Belmont, CA:
Wadsworth Publishing.


Monaghan, Angela. 2019. “Hotel Booking Sites Forced to End
Misleading Sales Tactics.” _The Guardian_, February 6, 2019.
_[https://oreil.ly/BoQwW](https://oreil.ly/BoQwW)_ .


Murgia, Madhumita. 2019. “When Manipulation Is the Digital
Business Model.” _Financial Times_ . _[https://oreil.ly/skPIF](https://oreil.ly/skPIF)_ .


Murphy, Anne L. 2005. “Lotteries in the 1690s: Investment or
Gamble?” _Financial History Review_ 12 (2): 227–46.


Nessmith, William E., Stephen P. Utkus, and Jean A. Young. 2007.
“Measuring the Effectiveness of Automatic Enrollment.” (working
paper, Vanguard Center for Retirement Research, Valley Forge,
PA).


Nisbett, Richard E., and Timothy D. Wilson. 1977. “The Halo
Effect: Evidence for Unconscious Alteration of Judgments.”
_Journal of Personality and Social Psychology_ 35 (4): 250–6.


Nisbett, Richard E., and Timothy D. Wilson. 1997b. “Telling More
than We Can Know: Verbal Reports on Mental Processes.”
_Psychological Review_ 84 (3): 231–59.


Noar, Seth M., Christina N. Benac, and Melissa S. Harris. 2007.
“Does Tailoring Matter? Meta-Analytic Review of Tailored Print
Health Behavior Change Interventions.” _Psychological Bulletin_
133 (4): 673–93.


Norman, Donald A. 1988. _The Design of Everyday Things_ . New
York: Basic Books.


Norton, Michael I., Daniel Mochon, and Dan Ariely. 2011. “The
‘IKEA Effect’: When Labor Leads to Love.” SSRN Scholarly
Paper ID 1777100. Rochester, NY: Social Science Research
Network. _[https://oreil.ly/nPot9](https://oreil.ly/nPot9)_ .


Nusca, Andrew. 2019. “Facebook Exec: ‘There Is No Such Thing
as Neutral Design.’” _Fortune_, March 5, 2019.
_[https://oreil.ly/WBYQo](https://oreil.ly/WBYQo)_ .


O’Donoghue, Ted, and Matthew Rabin. 2015. “Present Bias:
Lessons Learned and to Be Learned.” _American Economic Review_
105 (5): 273–79.


Oracle. 2020. “Oracle Utilities Measurement and Verification
Reports of the Opower.” January 19, 2020. _[https://oreil.ly/3YDYM](https://oreil.ly/3YDYM)_ .


Ouellette, Judith A., and Wendy Wood. 1998. “Habit and Intention
in Everyday Life: The Multiple Processes by Which Past Behavior
Predicts Future Behavior.” Psychological Bulletin 124 (1): 54.


Pease, Edward C., and Everette E. Dennis. 1995. _Radio: The_
_Forgotten Medium_ . New Brunswick, New Jersey: Transaction
Publishers.


Piacentini, John, et al. 2010. “Behavior Therapy for Children with
Tourette Disorder: A Randomized Controlled Trial.” _JAMA_ 303
(19) (May): 1929–37.


Pomeroy, Ross. 2013. “Don’t Be Afraid to Stereotype Strangers.”
_RealClearScience_, February 25, 2013. _[https://oreil.ly/OqOhl](https://oreil.ly/OqOhl)_ .


Pontefract, Dan. 2018. “The Foolishness Of Fail Fast, Fail Often.”
_Forbes_, September 15, 2018. _[https://oreil.ly/wXBcD](https://oreil.ly/wXBcD)_ .


Prochaska, James O., and Wayne F. Velicer. 1997. “The
Transtheoretical Model of Health Behavior Change.” _American_
_Journal of Health Promotion_ 12 (1) (September): 38–48


Resnick, Brian. 2018. “More Social Science Studies Just Failed to
Replicate. Here’s Why This Is Good.” _Vox_, August 27, 2018.
_[https://oreil.ly/sszd9](https://oreil.ly/sszd9)_ .


Reuters. 2019. “U.S. Senators Introduce Social Media Bill to Ban
‘Dark Patterns’ Tricks.” _Reuters_, April 9, 2019.
_[https://oreil.ly/6ARpC](https://oreil.ly/6ARpC)_ .


Riet, Jonathan van’t, Siet J. Sijtsema, Hans Dagevos, and Gert-Jan
De Bruijn. 2011. “The Importance of Habits in Eating Behaviour.
An Overview and Recommendations for Future Research.”
_Appetite_ 57 (3): 585–96.


Roberts, Jeff John. 2015. “LinkedIn Will Pay $13M for Sending
Those Awful Emails.” _Fortune_, October 5, 2015.
_[https://oreil.ly/MhDyd](https://oreil.ly/MhDyd)_ .


Rogers, Todd, Katherine L. Milkman, and Kevin G. Volpp. 2014.
“Commitment Devices: Using Initiatives to Change Behavior.”
_JAMA_ 311 (20): 2065–66.


Rolls, Barbara J. 2005. _The Volumetrics Eating Plan: Techniques_
_and Recipes for Feeling Full on Fewer Calories_ . New York:
Harper Collins.


Roozenbeek, Jon, and Sander van der Linden. 2019. “Fake News
Game Confers Psychological Resistance Against Online
Misinformation.” _Nature_, June 25, 2019. _[https://oreil.ly/24kS_](https://oreil.ly/24kS_)_ .


Russo, J. Edward, and Paul J. H. Schoemaker. 2002. _Winning_
_Decisions: Getting It Right the First Time_ . New York: Crown
Publishing Group.


Ryan, Richard M., and Edward L. Deci. 2000. “Intrinsic and
Extrinsic Motivations: Classic Definitions and New Directions.”
_Contemporary Educational Psychology_ 25 (1): 54–67.


Samuelson, William, and Richard Zeckhauser. 1988. “Status Quo
Bias in Decision Making.” _Journal of Risk and Uncertainty_ 1 (1):
7–59.


Schechner, Mark, and Sam Secada. 2019. “You Give Apps
Sensitive Personal Information. Then They Tell Facebook.” _Wall_
_Street Journal_, February 22, 2019. _[https://oreil.ly/Vt_Rg](https://oreil.ly/Vt_Rg)_ .


Schüll, Natasha Dow. 2012. _Addiction by Design: Machine_
_Gambling in Las Vegas_ . Princeton, NJ: Princeton University Press.


Schultz, P. Wesley, Jessica M. Nolan, Robert B. Cialdini, Noah J.
Goldstein, and Vladas Griskevicius. 2007. “The Constructive,


Destructive, and Reconstructive Power of Social Norms.”
_Psychological Science_ 18 (5) (May): 429–34.


Schwartz, Barry. 2004. _The Paradox of Choice: Why More Is Less_ .
New York: Harper Perennial.


Schwartz, Barry. 2014. “Is the Famous ‘Paradox of Choice’ a
Myth?” _PBS NewsHour_, January 29, 2014. _[https://oreil.ly/iVV7f](https://oreil.ly/iVV7f)_ .


Service, Owain et al. 2014. _EAST: Four Simple Ways to Apply_
_Behavioural Insights_ . London: The Behavioural Insights Team.
_[https://oreil.ly/3pe0O](https://oreil.ly/3pe0O)_ .


Shapiro, Shauna L., Linda E. Carlson, John A. Astin, and Benedict
Freedman. 2006. “Mechanisms of Mindfulness.” _Journal of_
_Clinical Psychology_ 62 (3): 373–86.


Shariat, Jonathan, and Cynthia Savard Saucier. 2017. _Tragic_
_Design: The Impact of Bad Product Design and How to Fix It_ .
Sebastopol, CA: O’Reilly Media.


Silver, Brian D., Barbara A. Anderson, and Paul R. Abramson.
1986. “Who Overreports Voting?” _The American Political Science_
_Review_ 80 (2) (June): 613–24.


Sin, Ray, Ryan Murphy, and Samantha Lamas. 2018. “Mining for
Goals.” _Morningstar_ .


Singler, Eric. 2018. “The First Nudge Building in Paris.” _Research_
_World_, October 23, 2018.


Soll, Jack B., Katherine L. Milkman, and John W. Payne. 2015. “A
User’s Guide to Debiasing.” _The Wiley Blackwell Handbook of_
_Judgment and Decision Making II_, John Wiley & Sons, Ltd, 924–
51.


Soman, Dilip. 2015. _The Last Mile: Creating Social and Economic_
_Value from Behavioral Insights_ . Toronto: Rotman-UTP Publishing.


Strack, Fritz, Leonard L. Martin, and Norbert Schwarz. 1988.
“Priming and Communication: Social Determinants of Information
Use in Judgments of Life Satisfaction.” _European Journal of_
_Social Psychology_ 18 (5): 429–42.


Strauss, Valerie. 2012. “Mega Millions: Do Lotteries Really
Benefit Public Schools?” _The Washington Post_ (blog), March 30,
2012. _[https://oreil.ly/_Das-](https://oreil.ly/_Das-)_ .


Sussman, Abigail B., and Christopher Y. Olivola. 2011. “Axe the
Tax: Taxes Are Disliked More than Equivalent Costs.” _Journal of_
_Marketing Research_ 48 (SPL): S91–101.


Syed, Matthew. 2015. _Black Box Thinking: Why Most People_
_Never Learn from Their Mistakes—But Some Do_ . New York:
Portfolio.


Thaler, Richard H., and Cass R. Sunstein. 2008. _Nudge: Improving_
_Decisions About Health, Wealth, and Happiness_ . New Haven,
Connecticut: Yale University Press.


Thaler, Richard H. 2018. “Nudge, Not Sludge.” _Science_ 361
(6401): 431–431.


Toft, Emma. 2017. “Trods Regler Om 48 Timers Tænkepause: Du
Kan Stadig Låne Penge Her Og Nu.” _DR_, September 15, 2017.
_[https://oreil.ly/d45vv](https://oreil.ly/d45vv)_ .


Tufano, Peter. 2008. “Saving Whilst Gambling: An Empirical
Analysis of UK Premium Bonds.” _The American Economic Review_
98 (2): 321–26.


Tversky, Amos, and Daniel Kahneman. 1973. “Availability: A
Heuristic for Judging Frequency and Probability.” _Cognitive_
_Psychology_ 5 (2) (September): 207–32.


Tversky, Amos, and Daniel Kahneman. 1981. “The Framing of
Decisions and the Psychology of Choice.” _Science_ 211 (4481)


(January): 453–58.


UK Behavioural Scientists. 2020. “Open Letter to the UK
Government Regarding COVID-19.” _[https://oreil.ly/XwQgN](https://oreil.ly/XwQgN)_ .


Valentino-DeVries, Jennifer. 2019. “How E-Commerce Sites
Manipulate You Into Buying Things You May Not Want.” _The New_
_York Times_, June 24, 2019. _[https://oreil.ly/M9dgE](https://oreil.ly/M9dgE)_ .


van Caster, Sarah. 2017. “Data Science Meets Behavioral
Science.” _Datanami_, February 20, 2017. _[https://oreil.ly/0I3Ls](https://oreil.ly/0I3Ls)_ .


Verba, Sidney, Kay Lehman Schlozman, and Henry E. Brady.
1995. _Voice and Equality: Civic Voluntarism in American Society_ .
Cambridge, MA: Harvard University Press.


Vinh, Khoi. 2018. “Design Is Never Neutral.” _Fast Company_,
August 15, 2018. _[https://oreil.ly/QzGpN](https://oreil.ly/QzGpN)_ .


Wallaert, Matt. 2019. _Start at the End: How to Build Products That_
_Create Change_ . New York: Portfolio (Penguin Random House).


Warren, Matthew. 2018. “First Analysis of ‘Pre-Registered’
Studies Shows Sharp Rise in Null Findings.” _Nature_, October 24,
2018. _[https://oreil.ly/h_BxX](https://oreil.ly/h_BxX)_ .


Watson, P.C. 1960. “On the Failure to Eliminate Hypotheses in a
Conceptual Task.” _Quarterly Journal of Experimental Psychology_
12 (3): 129–40.


Webb, Thomas L., and Paschal Sheeran. 2006. “Does Changing
Behavioral Intentions Engender Behavior Change? A Metaanalysis of the Experimental Evidence.” _Psychological Bulletin_
132 (2): 249–68.


Wendel, Stephen. 2019. _Spiritual Design_ . Oak Park, IL: Northeast
Press.


Wilson, Timothy D. 2002. _Strangers to Ourselves: Discovering the_
_Adaptive Unconscious_ . Cambridge, MA: Belknap Press.


Wilson, Timothy D. 2011. _Redirect: The Surprising New Science of_
_Psychological Change_ . New York: Little, Brown and Company.


Wilson, Timothy D, and Daniel T Gilbert. 2005. “Affective
Forecasting.” _Advances in Experimental Social Psychology_ 14 (3):
345–411.


Wilson, Timothy D., and Suzanne J. LaFleur. 1995. “Knowing
What You’ll Do: Effects of Analyzing Reasons on SelfPrediction.” _Journal of Personality and Social Psychology_ 68 (1):
21–35.


Wood, Wendy, and David T. Neal. 2007. “A New Look at Habits
and the Habit-Goal Interface.” _Psychological Review_ 114 (4): 843–
63.


Wood, Wendy, Jeffrey M. Quinn, and Deborah A. Kashy. 2002.
“Habits in Everyday Life: Thought, Emotion, and Action.” _Journal_
_of Personality and Social Psychology_ 83 (6): 1281–97.


Wood, Wendy, Leona Tam, and Melissa Guerrero Witt. 2005.
“Changing Circumstances, Disrupting Habits.” _Journal of_
_Personality and Social Psychology_ 88 (6): 918–33.


Wood, Wendy. 2019. _Good Habits, Bad Habits: The Science of_
_Making Positive Changes That Stick_ . New York: Farrar, Straus and
Giroux.


Yates, Tony. 2020. “Why Is the Government Relying on Nudge
Theory to Fight Coronavirus?” The Guardian. March 13, 2020.
_[https://oreil.ly/KdYx2](https://oreil.ly/KdYx2)_ .


Zajonc, Robert B. 1968. “Attitudinal Effects of Mere Exposure.”
_Journal of Personality and Social Psychology_ 9 (2, Pt.2): 1–27.


# **Index**

**Symbols**


401(k) plans


autoenrollment/autoescalation, Automate it


financial literacy seminars, The Value and Limitations of Educating
Your Users


**A**


A/A test, Glossary of Terms


A/B tests


defined, Other Types of Experiments, Glossary of Terms


(see also experiments)


for determining impact, Determining Impact with A/B Tests and
Experiments-Determining Impact with A/B Tests and Experiments


implementing, Implementing A/B Testing and Experiments


tools that support, Tools for Behavioral Tracking and Experiments


A/Null test, Other Types of Experiments, Glossary of Terms


Abdul Latif Jameel Poverty Action Lab (J-PAL), The Dedicated Teams


ability (CREATE Action Funnel stage), Ability, The User’s Ability to ActLook for “Real” Obstacles


defined, Glossary of Terms


eliciting implementation intentions, Elicit Implementation Intentions


increasing the power of other behaviors to stop negative behavior,
Ability: Increase the power of other behaviors


knowing user will succeed, The Other Side of the Wall: Knowing
You’ll Succeed


peer comparisons and, Peer Comparisons Can Help Here Too


real obstacles, Look for “Real” Obstacles


removing friction/channel factors, Remove Friction and Channel
Factors-Set appropriate defaults


accountability, Make Commitments to Friends


action (target action)


automating, Automate it


changing the context of, Reach Out of the Screen


clarifying, Clarify the Action


defined, Glossary of Terms


determining who should take action, Who Takes Action?


diagnosing why people don't start an action, Diagnosing Why People
Don’t Start-Diagnosing Why People Don’t Start


documenting initial idea of, Document Your Initial Idea of the ActionLook for the Minimum Viable Action


doing action for user, Do It for Them When You Can-Cheating at the
Action Funnel


(see also cheating)


examples from various domains, Examples from Various Domains


making incidental to other action, Make it incidental-Make it
incidental


metric for, A Metric for Action


minimum viable, Look for the Minimum Viable Action


obvious action as least likely to work, The Obvious Is Our Enemy


reevaluating assumptions about desired action, Is There a Better
Action for Them to Take?-Updating the Behavioral Personas


selecting the ideal action, Select the Ideal Target Action-Select the
Ideal Target Action


stopping negative actions (see negative actions, stopping)


techniques for generating alternate actions, Techniques for Generating
Ideas


Action Design Network (ADN), How This Book (and This New Edition)
Came About, What We Did: A Global Survey of Behavioral Teams, The
Nondedicated Teams


action metrics, A Metric for Action


action, creating, Creating Action-A Short Summary of the Ideas, From
Problems to Solutions


(see also CREATE Action Funnel)


action, taking, Deciding and Taking Action-A Short Summary of the Ideas,
Quirks of Action


actor (target actor), When Product Teams Don’t Have a Clear Problem
Definition, Who Takes Action?, Glossary of Terms


addictive products, Addictive Products-Addictive Products


ADN (Action Design Network), What We Did: A Global Survey of
Behavioral Teams, The Nondedicated Teams


advertising, We Use Shortcuts, Part II: Habits


Affordable Care Act (Obamacare), The Behavioral Map: What MicroBehaviors Lead to Action?


anchoring, We Use Shortcuts, Part I: Biases and Heuristics


Appel, Jacob, Evaluating Next Steps


Appiah, Kwame, The Behavioral Science of Ethics


Apple, Digital Tools, Especially, Seek to Manipulate Their Users


Applied Behavioral Science Team (Walmart/Sam's Club), A Summary of
the Process


Ariely, Dan, Pull Future Motivations into the Present


attention


avoiding cue to stop negative action, Attention: Avoid the Cue


increasing with mindfulness, Evaluation: Increase attention with
mindfulness


limitation, We’re Limited


attention economy, Addictive Products


attention treatment, Other Types of Experiments


authenticity, Be Authentic and Personal-Be Authentic and Personal


authority, speaking with, Display Strong Authority on the Subject


automation


defaulting and, Automate the act of repetition


of action on user's behalf, Automate it


of repetition of action, Automate the act of repetition


availability heuristic, We Use Shortcuts, Part I: Biases and Heuristics,
Quirks of Decision Making


**B**


B4Development, Stopping Negative Actions


Bains Douches Castagnary, The State of the Field


Banerjee, Abhijit, Evaluating Next Steps


baseline, How Many People Are “Enough”?


beauty, of site, Make the Site Professional and Beautiful


behavior change, Behavior Change…


alternatives to CREATE framework, A Simple Model of When, and
Why, We Act


behavioral science and, …And Behavioral Science


commonalities among various processes, The Process Is a Common
One


deliverables and outputs at each stage of process, The Details Do
Matter-The Details Do Matter


design and, …And Behavioral Science


practical guides/worksheets, Since We’re Human Too: Practical
Guidelines and Worksheets


putting into practice, Since We’re Human Too: Practical Guidelines
and Worksheets


six steps of DECIDE process, Understanding Isn’t Enough: We Need
Process-Understanding Isn’t Enough: We Need Process


summary of process, A Summary of the Process-Workbook Exercises


behavioral barriers, assessing, Assess Behavioral Barriers


behavioral bridge, Associate with the Positive and the Familiar, Glossary of
Terms


behavioral map, The Behavioral Map: What Micro-Behaviors Lead to
Action?-The Behavioral Map for Stopping Behaviors


building, Building the Behavioral Map-Building the Behavioral Map


defined, Glossary of Terms


drawing/adding behavioral detail, Write or Draw It Out, and Add
Behavioral Detail-Write or Draw It Out, and Add Behavioral Detail


for existing product, New Products or Features Versus Existing Ones


for new products/features, New Products or Features Versus Existing
Ones


for stopping behaviors, The Behavioral Map for Stopping Behaviors


reevaluating assumptions about desired action, Is There a Better
Action for Them to Take?-Updating the Behavioral Personas


behavioral metrics


as integral to product, Build in Behavioral Metrics from Day OneTools for Behavioral Tracking and Experiments


implementing A/B testing and experiments, Implementing A/B Testing
and Experiments


implementing behavioral tracking, Implementing Behavioral TrackingMeasuring behaviors and outcomes outside of the product


(see also behavioral tracking)


starting point for, What You Should Already Have


behavioral personas, Behavioral Personas-Behavioral Personas


defined, Glossary of Terms


updating in light of revised target action, Updating the Behavioral
Personas


behavioral research


Behavioral Teams Survey, What We Did: A Global Survey of
Behavioral Teams-What We Did: A Global Survey of Behavioral
Teams


current state of, The State of the Field-Putting It into Practice


behavioral science


basics, Behavioral Science 101: How Our Minds Are Wired-We Can
Design Context


behavior change and, …And Behavioral Science


context, We’re Deeply Affected by Context-We Can Design Context


deliberative versus reactive thinking, We’re of Two Minds


ethics of (see ethics of behavioral science)


human limitations and, We’re Limited-We’re Limited


quirks of action, Quirks of Action


quirks of decision making, Quirks of Decision Making-Quirks of
Decision Making


shortcuts: biases and heuristics, We Use Shortcuts, Part I: Biases and
Heuristics-We Use Shortcuts, Part I: Biases and Heuristics


shortcuts: habits, We Use Shortcuts, Part II: Habits-We Use Shortcuts,
Part II: Habits


Behavioral Science Policy Association (BSPA), What We Did: A Global
Survey of Behavioral Teams, Getting Help from Outside Researchers


behavioral scientists, as team members, Data Science and Behavioral
Science


behavioral strategy, Glossary of Terms


behavioral tactic, Glossary of Terms


behavioral teams (see teams)


Behavioral Teams Survey, What We Did: A Global Survey of Behavioral
Teams-What We Did: A Global Survey of Behavioral Teams


business model for teams, Business Model


challenges for teams, The Challenges-The Replication Crisis in
Science


creation of survey, What We Did: A Global Survey of Behavioral
Teams-What We Did: A Global Survey of Behavioral Teams


dedicated teams, The Dedicated Teams-The Dedicated Teams


focus areas, Focus Area


geographic distribution of teams, Who’s Out There?-Who’s Out
There?


nondedicated teams, The Nondedicated Teams


origins of teams, Origins


placement of teams, Placement


practical challenges of running a team, The Practical Challenges of
Running a Team


replication crisis in science, The Replication Crisis in Science-The
Replication Crisis in Science


size of teams, The Dedicated Teams


types of teams, Who’s Out There?


behavioral tracking


implementing, Implementing Behavioral Tracking-Measuring
behaviors and outcomes outside of the product


measuring behaviors/outcomes outside of the product, Measuring
behaviors and outcomes outside of the product


measuring behaviors/outcomes within the product, Measuring
behaviors and outcomes within the product


tools for, Tools for Behavioral Tracking and Experiments


Behavioural Insights Team (UK), The Process Is a Common One, Crafting
the Intervention: Cue, Reaction, Evaluation, The Dedicated Teams,
Business Model


Benartzi, Shlomo, Frame Text to Avoid Temporal Myopia


Berman, Kristen, Creating Action


Berra, Yogi, When Product Teams Don’t Have a Clear Problem Definition


Betterment, Rushed Choices and Regrettable Action, How You Combine
These Skills on a Team


bias, We Use Shortcuts, Part I: Biases and Heuristics-We Use Shortcuts,
Part I: Biases and Heuristics, Quirks of Decision Making


cognitive, Behavioral Science 101: How Our Minds Are Wired


confirmation, Cue


fundamental attribution, Remember the Fundamental Attribution Bias


present, We Use Shortcuts, Part I: Biases and Heuristics


recency, Quirks of Decision Making


status quo, We Use Shortcuts, Part I: Biases and Heuristics


blinking text, Bonus Tactic: Blinking Text


Bogost, Ian, Addictive Products


Bono, Evaluating Next Steps


Brignull, Harry, Ethics of Behavioral Science


BSPA (Behavioral Science Policy Association), What We Did: A Global
Survey of Behavioral Teams, Getting Help from Outside Researchers


Buddha/Buddhism, We’re of Two Minds, Evaluation: Use conscious
interference, Handling Prior Experience


Burroughs, Augusten, Quirks of Action


Busara Center, Implementing Within the Product, Who’s Out There?,
Business Model


BVA Nudge Unit, The State of the Field


**C**


Cagan, Marty, Integrate


Cambridge Analytica, Digital Tools, Especially, Seek to Manipulate Their
Users


Chabris, Christopher, Cue


Chatzky, Jean, Provide “Small Wins”


cheating (behavioral strategy), Do It for Them When You Can-Cheating at
the Action Funnel


automating a repetition of action, Automate the act of repetition


automating an action, Automate it


defined, Glossary of Terms


justification for, But Isn’t Cheating, Well, Cheating?


multi-step interventions and, Again, Cheat If You Can


one-time actions, Strategies to Cheat at One-Time Actions-Make it
incidental


repeated actions, Strategies to Cheat at Repeated Actions-Automate
the act of repetition


Choi, James, The CREATE Action Funnel


choice architecture, …And Behavioral Science


choice overload, Avoid Choice Overload


Cialdini, Robert, Digital Tools, Especially, Seek to Manipulate Their Users


Clover Health, Exploring the Context


cognitive bias, Behavioral Science 101: How Our Minds Are Wired


cognitive capacity, We’re Limited


cognitive overhead, Avoid Cognitive Overhead


COM-B Behaviour Change Wheel, A Simple Model of When, and Why,
We Act


commitment contracts, Use Commitment Contracts and Commitment
Devices


commitment devices, Use Commitment Contracts and Commitment
Devices


commitment, effort and, Hard work builds commitment


company objectives, Working with Company-Centric Goals, State the
company’s objectives, Glossary of Terms


company-centric goals


examples of desired outcomes/target actions, Examples from Various
Domains


objectives of company, State the company’s objectives


target outcomes and, Working with Company-Centric Goals-Define
the user outcomes


user outcomes defined for, Define the user outcomes


vision for product, State the vision


competition (among behaviors)


removing distractions, Remove Distractions: Knock Out the
Competition


strategies for counteracting, Remove Distractions: Knock Out the
Competition


competition (social motivator), Use Competition


computational behavioral science, Leveraging Data Science When
Designing for Behavior Change


conceptual design, Understanding Isn’t Enough: We Need Process,
Glossary of Terms


confidence level, How Many People Are “Enough”?


confirmation bias, Cue


conscious (System 2) thinking, We’re of Two Minds


conscious evaluation, The Conscious Evaluation-Pull Future Motivations
into the Present


(see also decision making)


avoiding choice overload, Avoid Choice Overload


avoiding cognitive overhead, Avoid Cognitive Overhead


avoiding direct payments, Avoid Direct Payments


commitment contracts/commitment devices, Use Commitment
Contracts and Commitment Devices


competition and, Use Competition


incentives and, Make Sure the Incentives Are Right


leveraging existing motivations before adding new ones, Leverage
Existing Motivations Before Adding New Ones


leveraging loss aversion, Leverage Loss Aversion


making sure instructions are understandable, Make Sure Instructions
Are Understandable


pulling future motivations into the present, Pull Future Motivations
into the Present-Pull Future Motivations into the Present


slowing down the process, Slow Them Down


techniques for, A Few Notes on Decision Making


testing out different types of motivators, Test Different Types of
Motivators


context (of action), Behavioral Science 101: How Our Minds Are Wired,
We’re Deeply Affected by Context-We Can Design Context


defined, Glossary of Terms


elements of, Reach Out of the Screen


exploring (see exploring the context)


redesigning, We Can Design Context


coronavirus (COVID-19), What Types of Behaviors This Can Help With


Covenant Eyes, Attention: Avoid the Cue


crafting the intervention (DECIDE stage)


advanced topics, Crafting the Intervention: Advanced Topics-Exercises


conscious evaluation, The Conscious Evaluation-Pull Future
Motivations into the Present


and CREATE Action funnel, Crafting the Intervention: Cue, Reaction,
Evaluation


creating habits, Creating Habits-Creating Habits


cueing the user to act, Cueing the User to Act-Bonus Tactic: Blinking
Text


Fitbit example, Crafting the Intervention: Ability, Timing, Experience


getting timing right, Getting the Timing Right-Make a Reward Scarce


handling prior experience, Handling Prior Experience-Check In Again:
You’re Not Interacting with the Same Person


hindering action, Hindering Action-Ideas for Hindering Other Actions


intuitive reaction, Narrate the Past to Support Future Action-Make the
Site Professional and Beautiful


making it clear where to act, Make It Clear Where to Act


multi-step interventions, Multi-Step Interventions-Hard work builds
commitment


New Moms example, Crafting the Intervention: Advanced Topics


UK Behavioural Insights Team example, Crafting the Intervention:
Cue, Reaction, Evaluation


user's ability to act, The User’s Ability to Act-Look for “Real”
Obstacles


CREATE Action Funnel, From Problems to Solutions, The CREATE
Action Funnel-A Short Summary of the Ideas, Shaping Behavior with Your
Product: The CREATE Action Funnel


ability stage (see ability)


alternative frameworks to, A Simple Model of When, and Why, We
Act


as means of understanding negative behavior, Stopping Negative
Actions


basics, A Simple Model of When, and Why, We Act


changes as user gains experience with product, What Changes as a
User Gains Experience with the Product?-What Changes as a User
Gains Experience with the Product?


changing nature of repeated actions, The Funnel Repeats Each Time
the Person Acts and Each Time Is Different


changing the context of action, Reach Out of the Screen


cheating at, Cheating at the Action Funnel


cheating strategy, Cheating at the Action Funnel


cognitive/practical barriers in, The Funnel Repeats Each Time the
Person Acts and Each Time Is Different


conscious evaluation, The Conscious Evaluation-Pull Future
Motivations into the Present


cue stage (see cue)


cueing the user to act, Cueing the User to Act-Bonus Tactic: Blinking
Text


defined, Glossary of Terms


diagnosing context problems with, Diagnosing the Problem with
CREATE-Diagnosing Why People Don’t Stop


diagnosing why people don't start a positive action, Diagnosing Why
People Don’t Start-Diagnosing Why People Don’t Start


diagnosing why people don't stop a negative action, Diagnosing Why
People Don’t Stop


evaluating multiple decisions with, Worksheet: Evaluating Multiple
Interventions with CREATE


evaluation stage (see evaluation)


experience stage (see experience)


interaction of stages with one another, The Stages Can Interact with
One Another


interventions to overcome obstacles, Crafting the Intervention: Cue,
Reaction, Evaluation


intuitive reaction, Narrate the Past to Support Future Action-Make the
Site Professional and Beautiful


looking beyond motivation, Look Beyond Motivation


progression of users from inaction to action over time, What Happens
Before People Take Action the First Time?-What Happens Before
People Take Action the First Time?


reaction stage (see reaction)


relative nature of each stage, Each Stage Is Relative


sustaining engagement with product, How Can You Sustain
Engagement with Your Product?


techniques for hindering actions, Ideas for Hindering Other Actions


timing stage (see timing)


using to add obstacles to negative actions, Using CREATE to Add
Obstacles to Action


value and limitations of educating users, The Value and Limitations of
Educating Your Users-The Value and Limitations of Educating Your
Users


variations in preconditions, How Do the Preconditions for Action Vary
from Day to Day?


credit card companies, Where Things Have Gone Wrong: Four Types of
Behavior Change


cross-sectional analysis, A Cross-Sectional or Panel Data Analysis of
Impact


cue (CREATE Action Funnel stage), Cue-Cue


aligning with user's spare time, Align with When People Have Spare
Time


asking the user to act, Ask Them


avoiding to prevent negative actions, Attention: Avoid the Cue


blinking text, Bonus Tactic: Blinking Text


crafting the intervention, Cueing the User to Act-Bonus Tactic:
Blinking Text


defined, Glossary of Terms


going to where user's attention already is, Go Where the Attention Is


making it clear where to act, Make It Clear Where to Act


product strategies for external cueing, Cue


relabel existing feature as cue, Relabel Something as a Cue


reminders and, Use Reminders


removing distractions, Remove Distractions: Knock Out the
Competition


cue (habits), We Use Shortcuts, Part II: Habits, We Use Shortcuts, Part II:
Habits


defined, Glossary of Terms


external, Cue, Glossary of Terms


internal, Cue, Glossary of Terms


Curtis, Dustin, Ask Them


**D**


Dai, Hengchen, Use Fresh Starts


dark patterns, Ethics of Behavioral Science


data bridge


building, Figure Out How to Measure the Outcome and Action by
Hook or by Crook (Not by Survey), Build the Data Bridge


defined, What Happens If the Outcome Isn’t Measurable Within the
Product?, Glossary of Terms


data science, Leveraging Data Science When Designing for Behavior
Change


"Data Science Meets Behavioral Science" (van Caster), Data Science and
Behavioral Science


data scientists, Data Science and Behavioral Science


de Bono, Edward, Techniques for Generating Ideas


debiasing, Rushed Choices and Regrettable Action


Deceptive Experiences To Online Users Reduction (DETOUR) Act, Ethics
of Behavioral Science, Use Legal and Economic Incentives as Well


DECIDE process, The Details Do Matter, DECIDE on the Behavioral
Intervention and Build it


(see also specific stages: Defining the problem; Exploring the context;
Crafting the intervention; Implementing within the product;
Determining impact; Evaluating next steps)


basics, Understanding Isn’t Enough: We Need Process-Understanding
Isn’t Enough: We Need Process


defined, Glossary of Terms


putting into practice, Since We’re Human Too: Practical Guidelines
and Worksheets


six steps of, Understanding Isn’t Enough: We Need ProcessUnderstanding Isn’t Enough: We Need Process


decision making, Deciding and Taking Action-A Short Summary of the
Ideas, How We Make Decisions and Act


avoiding choice overload, Avoid Choice Overload


avoiding cognitive overhead, Avoid Cognitive Overhead


handling prior experience, Use Techniques to Support Better Decisions


making sure instructions are understandable, Make Sure Instructions
Are Understandable


quirks of, Quirks of Decision Making-Quirks of Decision Making


removing unnecessary decision points, Remove unnecessary decision
points


slowing down the process, Slow Them Down


techniques for, A Few Notes on Decision Making


decision points


defined, Ability


removing unnecessary, Remove unnecessary decision points


decision-making process map, A Map of the Decision-Making Process-A
Map of the Decision-Making Process


defaulting, automation and, Automate the act of repetition


defaults, setting appropriate, Set appropriate defaults


defining the problem (DECIDE stage), Defining the Problem-Worksheet:
The Behavioral Project Brief


action's relation to outcome, Reminder: Action != Outcome


determining who should take action, Who Takes Action?


documenting initial idea of the action, Document Your Initial Idea of
the Action-Look for the Minimum Viable Action


examples from various domains, Examples from Various Domains


hypothesis for behavior change, A Hypothesis for Behavior Change-A
Hypothesis for Behavior Change


nailing down the target outcome, Nail Down the Target Outcome-A
Quick Checklist


(see also outcome)


putting lessons into practice, Putting It into Practice-Worksheet: The
Behavioral Project Brief


starting with product's vision, Start with the Product’s Vision


when product teams lack a clear problem definition, When Product
Teams Don’t Have a Clear Problem Definition-When Product Teams
Don’t Have a Clear Problem Definition


deliberative (System 2) thinking, We’re of Two Minds


descriptive norms, We Use Shortcuts, Part I: Biases and Heuristics


Design Council, The Process Is a Common One


Design of Everyday Things, The (Norman), Make It Clear Where to Act


designing for behavior change, DECIDE (see DECIDE process)


Designing with the Mind in Mind (Johnson), Make It Clear Where to Act


determining impact of product or communication (DECIDE stage),
Determining Impact with A/B Tests and Experiments-Determining Impact
with A/B Tests and Experiments


A/B tests and experiments for, Determining Impact with A/B Tests and
Experiments-Determining Impact with A/B Tests and Experiments


(see also experiments)


cross-sectional analysis, A Cross-Sectional or Panel Data Analysis of
Impact


data bridge construction, Build the Data Bridge


nonexperimental approaches, Other Ways to Determine Impact-Unique
Actions and Outcomes


panel data analysis, A Cross-Sectional or Panel Data Analysis of
Impact


pre-post analysis, A Pre-Post Look at Impact-A Pre-Post Look at
Impact


unique actions/outcomes, Unique Actions and Outcomes


when outcome isn't measurable within the product, What Happens If
the Outcome Isn’t Measurable Within the Product?-Build the Data
Bridge


when you can't run an A/B test, Determining Impact When You Can’t
Run an A/B Test-Putting It into Practice


DETOUR (Deceptive Experiences To Online Users Reduction) Act, Ethics
of Behavioral Science, Use Legal and Economic Incentives as Well


disclosure rules, Rushed Choices and Regrettable Action, The Value and
Limitations of Educating Your Users


distractions, removing, Remove Distractions: Knock Out the Competition


Don't Make Me Think (Krug), Make It Clear Where to Act


Double Diamond, The Process Is a Common One


double-blind experiments, Other Considerations


dual process theory(ies), We’re of Two Minds, Glossary of Terms


Duhigg, Charles, We Use Shortcuts, Part II: Habits, Reaction: Replace the
routine by hijacking the reaction, Creating Habits


**E**


EAST Framework, A Simple Model of When, and Why, We Act


economic incentives, Use Legal and Economic Incentives as Well


education insurance, Implementing Within the Product


education of users, The Value and Limitations of Educating Your Users-The
Value and Limitations of Educating Your Users


Egan, Dan, Rushed Choices and Regrettable Action, How You Combine
These Skills on a Team


Emanuel, Dana, Crafting the Intervention: Advanced Topics


eMBeD (Mind, Behavior, and Development Unit), World Bank, Crafting
the Intervention: Cue, Reaction, Evaluation


engagement, sustaining, How Can You Sustain Engagement with Your
Product?


environment (of action)


defined, Glossary of Terms


effect on ethical behavior, The Behavioral Science of Ethics


ethical review, Run the Ethical Review


ethics checklist, Remind Ourselves with an Ethics Checklist


ethics of behavioral science, Ethics of Behavioral Science-A Short
Summary of the Ideas


addictive products, Addictive Products-Addictive Products


changing the environment to support ethical uses of behavioral
science, A Path Forward: Using Behavioral Science on Ourselves-Use
Legal and Economic Incentives as Well


environment's effect on ethical behavior, The Behavioral Science of
Ethics


four types of behavior change, Where Things Have Gone Wrong: Four
Types of Behavior Change-Addictive Products


poisoning the water, Poisoning the Water


profit motive and, We’ll Follow the Money Too


user manipulation by digital companies, Digital Tools, Especially,
Seek to Manipulate Their Users-Digital Tools, Especially, Seek to
Manipulate Their Users


why designing for behavior change is especially sensitive, Why
Designing for Behavior Change Is Especially Sensitive-Why
Designing for Behavior Change Is Especially Sensitive


evaluating next steps (DECIDE stage), Evaluating Next Steps-Putting It
into Practice


determining what changes to implement, Determine What Changes to
Implement-Integrate


determining when product is good enough, When Is It “Good
Enough”?


gathering information about current impact of product and potential
improvements, Gather


integrating potential improvements to product, Integrate


measuring impact of each major change, Measure the Impact of Each
Major Change-Qualitative Tests of Incremental Changes


prioritizing of potential improvements to product, Prioritize


qualitative tests of incremental changes, Qualitative Tests of
Incremental Changes


evaluation (CREATE Action Funnel stage), Evaluation-Evaluation


conscious evaluation, The Conscious Evaluation-Pull Future
Motivations into the Present


defined, Glossary of Terms


increasing attention with mindfulness, Evaluation: Increase attention
with mindfulness


using conscious interference to stop negative actions, Evaluation: Use
conscious interference


exercise trackers, Automate the act of repetition, Go Where the Attention
Is, A Cautionary Tale: My Exercise Band-A Cautionary Tale: My Exercise
Band, A Pre-Post Look at Impact


(see also Fitbit)


exercise, action metrics for, A Metric for Action


experience (CREATE Action Funnel stage), Experience, Handling Prior
Experience-Check In Again: You’re Not Interacting with the Same Person,
Glossary of Terms


experiments


analyzing results of, Analyzing the Results of Experiments-Other
Considerations


consistent metrics for outcomes, Other Considerations


determining how long to run, How Long of a Wait Is “Enough”?


determining Minimum Meaningful Effect, Using Business Importance
to Determine “Enough”-Using Business Importance to Determine
“Enough”


determining statistical significance, Is the Effect Large “Enough”?
Determining Statistical Significance


double-blind, Other Considerations


experimental design in detail, Experimental Design in Detail-Points to
Remember in Designing an Experiment


for determining impact, Determining Impact with A/B Tests and
Experiments-Determining Impact with A/B Tests and Experiments


getting help from outside researchers, Getting Help from Outside
Researchers-Getting Help from Outside Researchers


implementing, Implementing A/B Testing and Experiments


minimum sample size for, How Many People Are “Enough”?-How
Many People Are “Enough”?


optimization, Experimental Optimization-How Experimental
Optimization Works


randomized control trials, The How and Why of Randomized Control
Trials-Why Experiments Are (Almost) Better Than Sliced Bread


reasons for doing, When and Why to Test


rules for designing, Points to Remember in Designing an Experiment


tools to support, Tools for Behavioral Tracking and Experiments


various types of, Types of Experiments-Other Types of Experiments


exploring the context (DECIDE stage), Exploring the Context-Exploring
the Context


beached fish example, Understanding Our Efforts: A Brief Story
About a Fish-Understanding Our Efforts: A Brief Story About a Fish


behavioral map, The Behavioral Map: What Micro-Behaviors Lead to
Action?-The Behavioral Map for Stopping Behaviors


diagnosing problem with CREATE, Diagnosing the Problem with
CREATE-Diagnosing Why People Don’t Stop


learning about your users, What Do You Know About Your Users?Behavioral Personas


putting lessons into practice, Putting It into Practice-Exploring the
Context


understanding our efforts, Understanding Our Efforts: A Brief Story
About a Fish-Exercise: Review the Map


value and limitations of educating users, The Value and Limitations of
Educating Your Users-The Value and Limitations of Educating Your
Users


external cue


defined, Cue, Glossary of Terms


product strategies using, Cue


external cues, Cue


extrinsic motivation, Leverage Existing Motivations Before Adding New
Ones, Glossary of Terms


Eyal, Nir, The Nondedicated Teams, What Changes as a User Gains
Experience with the Product?


**F**


Facebook, Digital Tools, Especially, Seek to Manipulate Their Users,
Where Things Have Gone Wrong: Four Types of Behavior Change


fake news, Stopping Negative Actions


false negatives, How Many People Are “Enough”?


false positives, How Many People Are “Enough”?


feedback loops


for stopping behaviors, Ideas for Hindering Other Actions


multi-step interventions and, Generate a Feedback Loop


financial aid for students, Creating Action


Financial Conduct Authority (UK), Rushed Choices and Regrettable Action


financial incentives, Avoid Direct Payments


financial literacy seminars, The Value and Limitations of Educating Your
Users


financial services, Rushed Choices and Regrettable Action


Fischer, Deb, Ethics of Behavioral Science


fish, beached, Understanding Our Efforts: A Brief Story About a Fish


Fitbit, Narrate the Past to Support Future Action, Leverage Existing
Motivations Before Adding New Ones, Crafting the Intervention: Ability,
Timing, Experience, Generate a Feedback Loop


Flash (app example), When Product Teams Don’t Have a Clear Problem
Definition


behavioral project brief, Putting It into Practice


defining the problem, Putting It into Practice-Worksheet: The
Behavioral Project Brief


ethical checklist for, Worksheet: Ethical Checklist


examples of desired outcomes/target actions, Examples from Various
Domains


refining the actor and action, Worksheet: Refining the Actor and
Action


user-centric versus company-centric products, Define the user
outcomes


Flo Health, Digital Tools, Especially, Seek to Manipulate Their Users


Fogg, BJ


Behavior Model, The Stages Can Interact with One Another


on habits, Changing Existing Habits


on triggers, Creating Habits


Fraser, Scott C., But Isn’t Cheating, Well, Cheating?


Freedman, Jonathan L., But Isn’t Cheating, Well, Cheating?


fresh starts, Use Fresh Starts


friction


decision points and, Ability


removing, Remove Friction and Channel Factors-Set appropriate
defaults


removing unnecessary decision points, Remove unnecessary decision
points


setting appropriate defaults, Set appropriate defaults


fudge factor, removing, Remove the Fudge Factor


fundamental attribution bias, Remember the Fundamental Attribution Bias


**G**


G*Power, How Many People Are “Enough”?


gambling, Creating Habits


GDPR (General Data Protection Regulation), Why Designing for Behavior
Change Is Especially Sensitive


German Corporation for International Cooperation (GIZ), Crafting the
Intervention: Cue, Reaction, Evaluation


Get Bad News (psychological vaccine), Stopping Negative Actions


Gilbert, Daniel, Use Story Editing


goals


company-centric (see company-centric goals)


savings, Defining the Problem


Gong, Min, A Summary of the Process


Google, Digital Tools, Especially, Seek to Manipulate Their Users


Google Analytics, Tools for Behavioral Tracking and Experiments


Google Scholar, Getting Help from Outside Researchers


Grameen Bank, Evaluating Next Steps


gut feelings, Reaction


**H**


habits, We Use Shortcuts, Part II: Habits-We Use Shortcuts, Part II: Habits


changing existing, Changing Existing Habits-Ability: Increase the
power of other behaviors


creating, Creating Habits-Creating Habits


crowding out with new behaviors, Ability: Increase the power of other
behaviors


defined, Glossary of Terms


unintentional actions and, Quirks of Action


Haidt, Jonathan, We’re of Two Minds


halo effect, We Use Shortcuts, Part I: Biases and Heuristics


Hamms, Gil, The Behavioral Science of Ethics


Happiness Hypothesis, The (Haidt), We’re of Two Minds


Hasanain, Wiam, Making the Case


healthcare, Oregon lottery for, Be Authentic and Personal


HelloWallet, How This Book (and This New Edition) Came About,
Document Your Initial Idea of the Action, Provide “Small Wins”,
Measuring behaviors and outcomes outside of the product


heuristics, Behavioral Science 101: How Our Minds Are Wired, We Use
Shortcuts, Part I: Biases and Heuristics-We Use Shortcuts, Part I: Biases
and Heuristics


Hidalgo, Anne, The State of the Field


hindering negative actions, Hindering Action-Ideas for Hindering Other
Actions


habitual actions, Habitual Actions


techniques for, Ideas for Hindering Other Actions


Homer, Pull Future Motivations into the Present


Hooked (Eyal), The Nondedicated Teams


Hopkins, Claude C., We Use Shortcuts, Part II: Habits


Hreha, Jason, Creating Habits


hypothesis for behavior change, A Hypothesis for Behavior Change-A
Hypothesis for Behavior Change


**I**


IADB (Inter-American Development Bank), What You’ll Need for Your
Team


ideas42, The Process Is a Common One, The Process Is a Common One,
Crafting the Intervention: Advanced Topics, The Dedicated Teams,
Business Model


IKEA effect, We Use Shortcuts, Part I: Biases and Heuristics


impact assessment, Skillset 2: Impact Assessment


(see also determining impact of product or communication)


implementation intentions, Relabel Something as a Cue, Elicit
Implementation Intentions


implementing within the product (DECIDE stage), Implementing Within
the Product-Final Review


behavioral metrics as integral to product, Build in Behavioral Metrics
from Day One-Tools for Behavioral Tracking and Experiments


determining what changes to implement, Determine What Changes to
Implement-Integrate


ethical review for, Run the Ethical Review


exercise band example, A Cautionary Tale: My Exercise Band-A
Cautionary Tale: My Exercise Band


leaving space for creative process, Leave Space for the Creative
Process-A Cautionary Tale: My Exercise Band


Safaricom example, Implementing Within the Product


inattentional blindness, Cue


incentives


conscious evaluation and, Make Sure the Incentives Are Right


using social power to change, Raise the Stakes: Use Social Power to
Change Incentives


incremental changes, Qualitative Tests of Incremental Changes


Innovations for Poverty Action (IPA), The Dedicated Teams


Inspired (Cagan), Integrate


Instituto Mexicano de Economia del Compartamiento, Who’s Out There?


instructions, making understandable, Make Sure Instructions Are
Understandable


intention, Assess Intention


intention–action gap, Behavioral Science 101: How Our Minds Are Wired,
Quirks of Action, The CREATE Action Funnel


Inter-American Development Bank (IADB), What You’ll Need for Your
Team


interface design, Understanding Isn’t Enough: We Need Process, Glossary
of Terms


internal cue, Cue, Glossary of Terms


International Review Board (IRB), Create a Review Body


interventions, crafting (see crafting the intervention)


intrinsic motivation, Leverage Existing Motivations Before Adding New
Ones, Glossary of Terms


Intuit, Digital Tools, Especially, Seek to Manipulate Their Users


intuitive (System 1) thinking, We’re of Two Minds, Reaction


intuitive reaction, Narrate the Past to Support Future Action-Make the Site
Professional and Beautiful


(see also reaction)


associating with positive/familiar experiences, Associate with the
Positive and the Familiar


authenticity of appeal, Be Authentic and Personal-Be Authentic and
Personal


bringing success to top of mind, Bring Success Top of Mind


display strong authority on subject, Display Strong Authority on the
Subject


gut feelings, Reaction


narrating past to support future action, Narrate the Past to Support
Future Action


peer comparisons, Use Peer Comparisons


personal appeals, Be Authentic and Personal-Be Authentic and
Personal


professionalism/beauty of site, Make the Site Professional and
Beautiful


social proof and, Deploy Social Proof


Ioannidis, John, The Replication Crisis in Science


iodine deficiency, Make it incidental


IPA (Innovations for Poverty Action), The Dedicated Teams


Irrational Labs, Creating Action


Iyengar, Sheena S., Avoid Choice Overload


**J**


J-PAL (Abdul Latif Jameel Poverty Action Lab), The Dedicated Teams


Jive Voice, Associate with the Positive and the Familiar


Johnson, Jeff, Make It Clear Where to Act


**K**


Kahneman, Daniel, We’re Deeply Affected by Context-We’re Deeply
Affected by Context


Karlan, Dean, Evaluating Next Steps


Kosovo, Crafting the Intervention: Cue, Reaction, Evaluation


Krug, Steve, Make It Clear Where to Act


**L**


language instruction, action metrics for, A Metric for Action


Last Mile, The (Soman), The Process Is a Common One


learned helplessness, Narrate the Past to Support Future Action


legal incentives, Use Legal and Economic Incentives as Well


Lepper, Mark R., Avoid Choice Overload


Lieb, David, Avoid Cognitive Overhead


limitations of human cognition/memory, We’re Limited-We’re Limited


LinkedIn, Digital Tools, Especially, Seek to Manipulate Their Users


loss aversion, Leverage Loss Aversion, Handling Prior Experience


**M**


marketing swag, Go Where the Attention Is


Matamo, Tools for Behavioral Tracking and Experiments


memory, limitations of, We’re Limited


mental environment, We’re Deeply Affected by Context


metrics


action, A Metric for Action


behavioral metrics as integral to product, Build in Behavioral Metrics
from Day One-Tools for Behavioral Tracking and Experiments


for target outcome, Define the Metric to Measure Outcomes


ideal characteristics, Define the Metric to Measure Outcomes


micro-behaviors, The Behavioral Map: What Micro-Behaviors Lead to
Action?-The Behavioral Map for Stopping Behaviors


microcredit, Evaluating Next Steps


Milkman, Katherine L., Rushed Choices and Regrettable Action, Use Fresh
Starts


Mind, Behavior, and Development Unit (eMBeD), World Bank, Crafting
the Intervention: Cue, Reaction, Evaluation


mindfulness, Evaluation: Increase attention with mindfulness


mindset, Glossary of Terms


minimum meaningful effect (MME), Using Business Importance to
Determine “Enough”-Using Business Importance to Determine “Enough”


minimum sample size, How Many People Are “Enough”?-How Many
People Are “Enough”?


Minimum Viable Action (MVA), Look for the Minimum Viable Action,
Glossary of Terms


mission statements, Start with the Product’s Vision


money, as motivator, Avoid Direct Payments


More Than Good Intentions (Karlan and Appel), Evaluating Next Steps


Morningstar, How This Book (and This New Edition) Came About,
Defining the Problem


mortgage disclosures, The Value and Limitations of Educating Your Users


motivation


leveraging existing motivations before adding new ones, Leverage
Existing Motivations Before Adding New Ones


looking beyond, Look Beyond Motivation


pull future motivations into the present, Pull Future Motivations into
the Present-Pull Future Motivations into the Present


testing out different types of motivators, Test Different Types of
Motivators


multi-step interventions, Multi-Step Interventions-Hard work builds
commitment


cheating strategies, Again, Cheat If You Can


combining multiple steps into one, Combine Where Possible


common mistakes, Common Mistakes


effort and commitment, Hard work builds commitment


feedback loops, Generate a Feedback Loop


providing small wins with each step, Provide “Small Wins”


multiarm comparisons, Other Types of Experiments


multiarmed bandit, Other Types of Experiments


multivariate testing, Other Types of Experiments, Glossary of Terms


Musk, Elon, Determining Impact with A/B Tests and Experiments


**N**


Naru, Faisal, What We Did: A Global Survey of Behavioral Teams


negative actions, stopping, Stopping Negative Actions-A Short Summary of
the Ideas


avoiding the cue, Attention: Avoid the Cue


behavioral map for, The Behavioral Map for Stopping Behaviors


changing existing habits, Changing Existing Habits-Ability: Increase
the power of other behaviors


creating obstacles, Hindering Action-Ideas for Hindering Other
Actions


diagnosing why people don't stop, Diagnosing Why People Don’t Stop


replace the routine by hijacking the reaction, Reaction: Replace the
routine by hijacking the reaction


rushed choices and regrettable action, Rushed Choices and Regrettable
Action-Rushed Choices and Regrettable Action


using CREATE to add obstacles to, Using CREATE to Add Obstacles
to Action


New Moms (nonprofit), Crafting the Intervention: Advanced Topics


noise, How Many People Are “Enough”?


nonconscious habits, Behavioral Science 101: How Our Minds Are Wired


nonconscious judgments, Behavioral Science 101: How Our Minds Are
Wired


nonconscious reactions, Reaction-Reaction


Norman, Donald A., Make It Clear Where to Act


Norwegian Consumer Council, Digital Tools, Especially, Seek to
Manipulate Their Users


Nudge (Thaler and Sundstein), What Types of Behaviors This Can Help
With, Ideas for Hindering Other Actions


Nudge Lebanon, Stopping Negative Actions


Nudge Rio, Who’s Out There?


**O**


Obama, Barack, The Behavioral Map: What Micro-Behaviors Lead to
Action?


objectives, of company, State the company’s objectives


obstacles, Look for “Real” Obstacles


obvious actions, as likely failures, The Obvious Is Our Enemy


Odyssey (Homer), Pull Future Motivations into the Present


OECD (Organisation for Economic Co-operation and Development), What
We Did: A Global Survey of Behavioral Teams


one-sided test, How Many People Are “Enough”?


one-time actions, Strategies to Cheat at One-Time Actions-Make it
incidental


Opower, Measuring behaviors and outcomes outside of the product,
Determining Impact with A/B Tests and Experiments


optimization, of experiments, Experimental Optimization-How
Experimental Optimization Works


Oracle Utilities, Measuring behaviors and outcomes outside of the product,
Determining Impact with A/B Tests and Experiments


Oregon healthcare lottery, Be Authentic and Personal


organ donations, Remove Friction and Channel Factors


Organisation for Economic Co-operation and Development (OECD), What
We Did: A Global Survey of Behavioral Teams


outcome (target outcome)


checklist for, A Quick Checklist


clarifying, Clarify the Outcome-What if no one can agree on the
product’s intended outcome?


defined, Glossary of Terms


defining the metric to measure, Define the Metric to Measure
Outcomes


determining, Nail Down the Target Outcome-A Quick Checklist


disagreements on product's intended outcome, What if no one can
agree on the product’s intended outcome?


examples from various domains, Examples from Various Domains


focusing on outcomes instead of actions, Avoid stating how the
product (might) do it


importance of clear definition, Why go through the trouble?


narrowing scope of, That and nothing else


prioritizing/combining multiple outcomes, Prioritize and combine


states of mind versus observable outcomes, Avoid states of mind


working with company-centric goals, Working with Company-Centric
Goals-Define the user outcomes


**P**


panel data analysis, A Cross-Sectional or Panel Data Analysis of Impact


paradox of choice, We’re Limited


Paris Nudge Building, The State of the Field


Paulin, Ingrid Melvær, What We Did: A Global Survey of Behavioral
Teams


Payne, John W., Rushed Choices and Regrettable Action


peer comparisons, Use Peer Comparisons, Peer Comparisons Can Help
Here Too


personal appeals, Be Authentic and Personal-Be Authentic and Personal


personal finance applications, Automate the act of repetition


personas, Glossary of Terms


(see also behavioral personas)


physical environment, We’re Deeply Affected by Context


power calculation, How Many People Are “Enough”?


Power of Habit, The (Duhigg), We Use Shortcuts, Part II: Habits, Reaction:
Replace the routine by hijacking the reaction, Creating Habits


pre-post analysis, A Pre-Post Look at Impact-A Pre-Post Look at Impact


present bias, We Use Shortcuts, Part I: Biases and Heuristics


prior experience, Experience, Handling Prior Experience-Check In Again:
You’re Not Interacting with the Same Person


(see also experience)


checking in with same person at later time, Check In Again: You’re
Not Interacting with the Same Person


handling, Handling Prior Experience-Check In Again: You’re Not
Interacting with the Same Person


making intentionally unfamiliar, Make It Intentionally Unfamiliar


story editing, Use Story Editing-Use Story Editing


use fresh starts, Use Fresh Starts


using techniques to support better decisions, Use Techniques to
Support Better Decisions


prioritizing


improvements, Prioritize


multiple outcomes, Prioritize and combine


Prius effect, Evaluation: Use conscious interference


privacy rights, Digital Tools, Especially, Seek to Manipulate Their Users


professionalism, of site, Make the Site Professional and Beautiful


profits, increased, We’ll Follow the Money Too


ProPublica, Digital Tools, Especially, Seek to Manipulate Their Users


Python, How Many People Are “Enough”?, Is the Effect Large “Enough”?
Determining Statistical Significance


**Q**


qualitative tests, Qualitative Tests of Incremental Changes


quirks of action, Quirks of Action


quirks of decision-making, Quirks of Decision Making-Quirks of Decision
Making


**R**


R (package)


power calculation function, How Many People Are “Enough”?


statistical significance testing, Is the Effect Large “Enough”?
Determining Statistical Significance


Radicalise game, Stopping Negative Actions


random assignment, Points to Remember in Designing an Experiment


random rewards, We Use Shortcuts, Part II: Habits, Creating Habits


random selection, Points to Remember in Designing an Experiment


randomization, in experiment design, Why Experiments Are (Almost)
Better Than Sliced Bread


randomized control trials (RCTs), The How and Why of Randomized
Control Trials-Why Experiments Are (Almost) Better Than Sliced Bread


reaction (CREATE Action Funnel stage), Reaction-Reaction


defined, Glossary of Terms


hijacking to stop negative actions, Reaction: Replace the routine by
hijacking the reaction


intuitive, Narrate the Past to Support Future Action-Make the Site
Professional and Beautiful


(see also intuitive reaction)


reactive (System 1) thinking, We’re of Two Minds, Reaction


recency bias, Quirks of Decision Making


Reinsurance Group of America, Who’s Out There?


reminders, as cues, Use Reminders


repeated actions, Strategies to Cheat at Repeated Actions-Automate the act
of repetition


replication crisis, The Replication Crisis in Science-The Replication Crisis
in Science


retirement savings


401(k) autoenrollment/autoescalation, Automate it


automating employee contributions, Look Beyond Motivation


financial literacy seminars, The Value and Limitations of Educating
Your Users


revenue, Thinking Through the Business Model-Thinking Through the
Business Model


review body/review board, Create a Review Body


reward schedule, We Use Shortcuts, Part II: Habits


reward substitution, Pull Future Motivations into the Present


rewards, We Use Shortcuts, Part II: Habits, Creating Habits


defined, We Use Shortcuts, Part II: Habits, Glossary of Terms


scarce/time-sensitive, Make a Reward Scarce


Riis, Jason, Use Fresh Starts


Roozenbeek, Jon, Stopping Negative Actions


routines, We Use Shortcuts, Part II: Habits, Creating Habits-Creating Habits


defined, We Use Shortcuts, Part II: Habits, Creating Habits, Glossary
of Terms


replacing to stop negative actions, Reaction: Replace the routine by
hijacking the reaction


Runkeeper, Automate the act of repetition


**S**


Safaricom, Implementing Within the Product


Sam's Club Applied Behavioral Science Team, A Summary of the Process


sample size, minimum, How Many People Are “Enough”?-How Many
People Are “Enough”?


Saudi Arabia, Making the Case


Save More Tomorrow, Frame Text to Avoid Temporal Myopia


savings goals and, Defining the Problem


savings lotteries, Make it incidental


Scartascini, Carlos, What You’ll Need for Your Team


self-narrative


defined, Glossary of Terms


narrating past to support future action, Narrate the Past to Support
Future Action


story editing and, Use Story Editing-Use Story Editing


Simons, Daniel, Cue


simultaneous comparison experiments, Other Types of Experiments


(see also A/B tests)


simultaneous impact experiments, Other Types of Experiments


situational self-control, Stopping Negative Actions


small wins


defined, Glossary of Terms


multi-step interventions and, Provide “Small Wins”


smoking cessation, The Behavioral Map for Stopping Behaviors


social accountability, Make Commitments to Friends


social environment, We’re Deeply Affected by Context


social motivation, competition as, Use Competition


social power, Raise the Stakes: Use Social Power to Change Incentives


social proof, Deploy Social Proof


Soll, Jack B., Rushed Choices and Regrettable Action


Soman, Dilip, The Process Is a Common One


Spanish-language resources for applied behavioral science, Who’s Out
There?


spare time, user's, Align with When People Have Spare Time


staggered rollout, Other Types of Experiments


Start at the End (Wallaert), The Process Is a Common One


states of mind, observable outcomes versus, Avoid states of mind


statistical power, How Many People Are “Enough”?


statistical significance, Is the Effect Large “Enough”? Determining
Statistical Significance


StatsModel package, How Many People Are “Enough”?


status quo bias, We Use Shortcuts, Part I: Biases and Heuristics


story editing, Use Story Editing-Use Story Editing


structure of attention, Align with When People Have Spare Time


student loans, Creating Action


sunk cost effect, Hard work builds commitment


Sunlight Foundation, Start with the Product’s Vision


Sunstein, Cass, What Types of Behaviors This Can Help With


swag, Go Where the Attention Is


System 1 Group, Digital Tools, Especially, Seek to Manipulate Their Users


System 1 thinking, We’re of Two Minds, Reaction


System 2 thinking, We’re of Two Minds


**T**


target action (see action)


target actor (see actor)


target outcome (see outcome)


tax reporting, Crafting the Intervention: Cue, Reaction, Evaluation


teams, What You’ll Need for Your Team-Putting It into Practice


(see also Behavioral Teams Study)


advanced degrees and, What’s Not Listed: A PhD


combining skillsets on a team, How You Combine These Skills on a
Team


data scientists and behavioral scientists on, Data Science and
Behavioral Science


impact assessment, Skillset 2: Impact Assessment


leveraging data science when designing for behavior change,
Leveraging Data Science When Designing for Behavior Change


making business case for, Making the Case-Thinking Through the
Business Model


non-behavioral basics, Skillset 1: The Non-Behavioral Basics


partnerships with outside researchers, Getting Help from Outside
Researchers-Getting Help from Outside Researchers


requirements for, What You’ll Need for Your Team-Putting It into
Practice


skills and people for, The Skills and People You Need-Leveraging
Data Science When Designing for Behavior Change


thinking through the business model, Thinking Through the Business
Model-Thinking Through the Business Model


understanding of mind and its quirks, Skillset 3: A Deep
Understanding of the Mind and Its Quirks


teaser rates, Where Things Have Gone Wrong: Four Types of Behavior
Change


temporal myopia, Frame Text to Avoid Temporal Myopia


testimonials, Deploy Social Proof


text


blinking, Bonus Tactic: Blinking Text


framing to avoid temporal myopia, Frame Text to Avoid Temporal
Myopia


Thaler, Richard H., What Types of Behaviors This Can Help With, Frame
Text to Avoid Temporal Myopia, Ideas for Hindering Other Actions


Thorp, Justin, Make Commitments to Friends


time-sensitive rewards, Make a Reward Scarce


timing (CREATE Action Funnel stage), Timing-Timing, Getting the Timing
Right-Make a Reward Scarce


defined, Glossary of Terms


framing text to avoid temporal myopia, Frame Text to Avoid Temporal
Myopia


making a reward scarce, Make a Reward Scarce


making commitments to friends, Make Commitments to Friends


reminding user of prior commitment to act, Remind of a Prior
Commitment to Act


Tulchinskaya, Anna, Relabel Something as a Cue


Tversky, Amos, We’re Deeply Affected by Context-We’re Deeply Affected
by Context


two-sided test, How Many People Are “Enough”?


**U**


Ulysses contract, Pull Future Motivations into the Present


United Kingdom (see Behavioural Insights Team)


urgency, decision making and, Timing-Timing


user data, Why Designing for Behavior Change Is Especially Sensitive


user outcomes, defining, Define the user outcomes


user personas, Behavioral Personas-Behavioral Personas


(see also behavioral personas)


user story, Glossary of Terms


user-centric approach


defining behavioral problems for, Working with Company-Centric
Goals


examples of desired outcomes/target actions, Examples from Various
Domains


users


behavior in daily life, How Do They Behave in Daily Life?-How Do
They Behave in Daily Life?


behavior in existing application, How Do They Behave in the
Application?


behavioral personas, Behavioral Personas-Behavioral Personas,
Updating the Behavioral Personas, Glossary of Terms


learning about, What Do You Know About Your Users?-Behavioral
Personas


progression from inaction to action over time, What Happens Before
People Take Action the First Time?-What Happens Before People
Take Action the First Time?


value and limitations of educating, The Value and Limitations of
Educating Your Users-The Value and Limitations of Educating Your
Users


**V**


van Caster, Sarah, Data Science and Behavioral Science


van der Linden, Sander, Stopping Negative Actions


vanity metrics, That and nothing else


vision (product vision)


and company-centric goals, State the vision


clarifying, Start with the Product’s Vision


defined, Glossary of Terms


**W**


Wallaert, Matt, Addictive Products, The Process Is a Common One, Making
the Case


Walmart Applied Behavioral Science Team, A Summary of the Process


Warner, Mark, Ethics of Behavioral Science


wearables, Go Where the Attention Is, Generate a Feedback Loop


(see also exercise trackers; Fitbit)


"Why Most Published Research Findings are False" (Ioannidis), The
Replication Crisis in Science


Wilson, Tim, Use Story Editing


World Bank Mind, Behavior, and Development Unit (eMBeD), Crafting the
Intervention: Cue, Reaction, Evaluation


**Y**


Young, Scott, The State of the Field


YouVersion, Creating Habits


Yunus, Mohammad, Evaluating Next Steps


**Z**


Zinman, Jonathan, Evaluating Next Steps


Zumdahl, Laura, Crafting the Intervention: Advanced Topics


**About the Author**


**Dr. Stephen Wendel** is a behavioral social scientist who studies how digital
products can help individuals manage their money more effectively. He
currently serves as the Head of Behavioral Science at Morningstar, a
leading provider of independent investment research. At Morningstar, he
leads a team of behavioral scientists and practitioners to conduct original
research on savings and investing behavior, applies behavioral insights to
Morningstar’s products and services, and frequently speaks with the media
and industry groups on these topics.


Stephen has authored three books on applied behavioral science: _Designing_
_for Behavior Change_ (November 2013), _Improving Employee Benefits_
(September 2014), and _Spiritual Design_ (October 2019). Outside of work,
he is also the Founder and Chair of the nonprofit Action Design Network,
which helps more than 15,000 practitioners apply behavioral research to
product development with monthly events in 15 cities across North
America.


Stephen holds a BA from U.C. Berkeley, a master’s from Johns HopkinsSAIS, and a PhD from the University of Maryland, where he analyzed the
dynamics of behavioral change over time. He has a wife and two wonderful
kids, who don’t care about behavioral science at all.


He can be reached on LinkedIn or Twitter @sawendel, and via his website
at _https://www.behavioraltechnology.co_ .


**Colophon**


The cover of _Designing for Behavior Change_ hosts a coral reef of mixed
species. Corals are marine invertebrates of the class _Anthozoa_, though
researchers in the past thought they were minerals or plants. In fact, a coral
reef is made up of thousands of tiny sessile creatures called polyps. They
thrive in tropical and subtropical waters. The most famous is the Great
Barrier Reef off the coast of Australia.


These ecosystems are at least as large, lasting, and biodiverse as Earth’s
oldest forests. Their characteristic, stunning colors come from algae that
inhabit polyp tissues. Corals suffer from rising water temperatures and
acidity, endangering their own lives and those they support, including most
ocean life and all who rely on oceans. Many of the animals on O’Reilly’s
covers are endangered; all of them are important to the world.


The cover illustration is by Karen Montgomery, based on a black and white
engraving from _Meyers Kleines Lexicon_ . The cover fonts are Gilroy
Semibold and Guardian Sans. The text font is Adobe Minion Pro; the
heading font is Adobe Myriad Condensed; and the code font is Dalton
Maag’s Ubuntu Mono.


