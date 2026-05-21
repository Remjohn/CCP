Bert Gollnick

## **Generative AI with Python**


**The Developer’s Guide to Pretrained LLMs, Vector Databases,**
**Retrieval-Augmented Generation, and Agentic Systems**


_[OceanofPDF.com](https://oceanofpdf.com/)_


# Imprint

This e-book is a publication many contributed to, specifically:


**Editor** Meagan White
**Acquisitions Editor** Hareem Shafi
**Copyeditor** Yvette Chin
**Cover Design** Graham Geary
**Photo Credit** Midjourney.com; Shutterstock: 1861053121/©
Origami Sayko
**Production E-Book** Kelly O’Callaghan
**Typesetting E-Book** Satz-Pro (Germany)


We hope that you liked this e-book. Please share your feedback with
us and read the Service Pages to find out how to contact us.


**The Library of Congress Cataloging-in-Publication Control**
**Number for the printed edition is as follows:** 2025008568



**© 2025 by:**
Rheinwerk Publishing, Inc.
2 Heritage Drive, Suite 305
Quincy, MA 02171
USA
[info@rheinwerk-publishing.com](mailto:info@rheinwerk-publishing.com)
+1.781.228.5070



**Represented in the E.U. by:**

Rheinwerk Verlag GmbH
Rheinwerkallee 4
53227 Bonn
Germany
[service@rheinwerk-verlag.de](mailto:service@rheinwerk-verlag.de)
+49 (0) 228 42150-0



**ISBN 978-1-4932-2690-0 (print)**
**ISBN 978-1-4932-2691-7 (e-book)**


**ISBN 978-1-4932-2692-4 (print and e-book)**


1st edition 2025


_[OceanofPDF.com](https://oceanofpdf.com/)_


# Notes on Usage

This e-book is **protected by copyright** . By purchasing this e-book,
you have agreed to accept and adhere to the copyrights. You are
entitled to use this e-book for personal purposes. You may print and
copy it, too, but also only for personal use. Sharing an electronic or
printed copy with others, however, is not permitted, neither as a
whole nor in parts. Of course, making them available on the internet
or in a company network is illegal as well.


For detailed and legally binding usage conditions, please refer to the
section Legal Notes.


This e-book copy contains a **digital watermark**, a signature that
indicates which person may use this copy:


# Notes on the Screen Presentation

You are reading this e-book in a file format (EPUB or Mobi) that
makes the book content adaptable to the display options of your
reading device and to your personal needs. That’s a great thing; but
unfortunately not every device displays the content in the same way
and the rendering of features such as pictures and tables or
hyphenation can lead to difficulties. This e-book was optimized for
the presentation on as many common reading devices as possible.


If you want to zoom in on a figure (especially in iBooks on the iPad),
tap the respective figure once. By tapping once again, you return to
the previous screen. You can find more recommendations on the
customization of the screen layout on the Service Pages.


_[OceanofPDF.com](https://oceanofpdf.com/)_


# Table of Contents

**Notes on Usage**
**Table of Contents**

## Preface

# 1  Introduction to Generative AI

## 1.1  Introduction to Artificial Intelligence 1.2  Pillars of Generative AI Advancement
### 1.2.1  Computational Power 1.2.2  Model and Data Size 1.2.3  Investments 1.2.4  Algorithmic Improvements
## 1.3  Deep Learning 1.4  Narrow AI and General AI 1.5  Natural Language Processing Models
### 1.5.1  NLP Tasks 1.5.2  Architectures
## 1.6  Large Language Models
### 1.6.1  Training


### 1.6.2  Use Cases 1.6.3  Limitations
## 1.7  Large Multimodal Models 1.8  Generative AI Applications
### 1.8.1  Consumer 1.8.2  Business 1.8.3  Prosumer
## 1.9  Summary

# 2  Pretrained Models

## 2.1  Hugging Face 2.2  Coding: Text Summarization 2.3  Exercise: Translation
### 2.3.1  Task 2.3.2  Solution
## 2.4  Coding: Zero-Shot Classification 2.5  Coding: Fill-Mask 2.6  Coding: Question Answering 2.7  Coding: Named Entity Recognition 2.8  Coding: Text-to-Image 2.9  Exercise: Text-to-Audio
### 2.9.1  Task 2.9.2  Solution
## 2.10  Capstone Project: Customer Feedback


## Analysis 2.11  Summary

# 3  Large Language Models

## 3.1  Brief History of Language Models 3.2  Simple Use of LLMs via Python
### 3.2.1  Coding: Using OpenAI 3.2.2  Coding: Using Groq 3.2.3  Coding: Large Multimodal Models 3.2.4  Coding: Running Local LLMs
## 3.3  Model Parameters
### 3.3.1  Model Temperature 3.3.2  Top-p and Top-k
## 3.4  Model Selection
### 3.4.1  Performance 3.4.2  Knowledge Cutoff Date 3.4.3  On-Premise versus Cloud-Based Hosting 3.4.4  Open-Source, Open-Weight, and Proprietary Models 3.4.5  Price 3.4.6  Context Window 3.4.7  Latency
## 3.5  Messages
### 3.5.1  User 3.5.2  System


### 3.5.3  Assistant
## 3.6  Prompt Templates
### 3.6.1  Coding: ChatPromptTemplates 3.6.2  Coding: Improve Prompts with LangChain Hub
## 3.7  Chains
### 3.7.1  Coding: Simple Sequential Chain 3.7.2  Coding: Parallel Chain 3.7.3  Coding: Router Chain 3.7.4  Coding: Chain with Memory
## 3.8  Safety and Security
### 3.8.1  Security 3.8.2  Safety 3.8.3  Coding: Implementing LLM Safety and Security
## 3.9  Model Improvements 3.10  New Trends
### 3.10.1  Reasoning Models 3.10.2  Small Language Models 3.10.3  Test-Time Computation
## 3.11  Summary

# 4  Prompt Engineering

## 4.1  Prompt Basics
### 4.1.1  Prompt Process 4.1.2  Prompt Components 4.1.3  Basic Principles


## 4.2  Coding: Few-Shot Prompting 4.3  Coding: Chain-of-Thought 4.4  Coding: Self-Consistency Chain-of-Thought 4.5  Coding: Prompt Chaining 4.6  Coding: Self-Feedback 4.7  Summary

# 5  Vector Databases

## 5.1  Introduction 5.2  Data Ingestion Process 5.3  Loading Documents
### 5.3.1  High-Level Overview 5.3.2  Coding: Load a Single Text File 5.3.3  Coding: Load Multiple Text Files 5.3.4  Exercise: Load Multiple Wikipedia Articles 5.3.5  Exercise: Loading Project Gutenberg Book
## 5.4  Splitting Documents
### 5.4.1  Coding: Fixed-Size Chunking 5.4.2  Coding: Structure-Based Chunking 5.4.3  Coding: Semantic Chunking 5.4.4  Coding: Custom Chunking
## 5.5  Embeddings
### 5.5.1  Overview 5.5.2  Coding: Word Embeddings


### 5.5.3  Coding: Sentence Embeddings 5.5.4  Coding: Create Embeddings with LangChain
## 5.6  Storing Data
### 5.6.1  Selection of a Vector Database 5.6.2  Coding: File-Based Storage with a Chroma Database 5.6.3  Coding: Web-Based Storage with Pinecone
## 5.7  Retrieving Data
### 5.7.1  Similarity Calculation 5.7.2  Coding: Retrieve Data from Chroma Database 5.7.3  Coding: Retrieve Data from Pinecone
## 5.8  Capstone Project
### 5.8.1  Features 5.8.2  Dataset 5.8.3  Preparing the Vector Database 5.8.4  Exercise: Get All Genres from the Vector Database 5.8.5  App Development
## 5.9  Summary

# 6  Retrieval-Augmented Generation

## 6.1  Introduction 6.2  Coding: Simple Retrieval-Augmented Generation


### 6.2.1  Knowledge Source Setup 6.2.2  Retrieval 6.2.3  Augmentation 6.2.4  Generation 6.2.5  RAG Function Creation
## 6.3  Advanced Techniques
### 6.3.1  Advanced Preretrieval Techniques 6.3.2  Advanced Retrieval Techniques 6.3.3  Advanced Postretrieval Techniques
## 6.4  Coding: Prompt Caching 6.5  Evaluation
### 6.5.1  Challenges in RAG Evaluation 6.5.2  Metrics 6.5.3  Coding: Metrics
## 6.6  Summary

# 7  Agentic Systems

## 7.1  Introduction to AI Agents 7.2  Available Frameworks 7.3  Simple Agent
### 7.3.1  Agentic RAG 7.3.2  ReAct
## 7.4  Agentic Framework: LangGraph
### 7.4.1  Simple Graph: Assistant


### 7.4.2  Router Graph 7.4.3  Graph with Tools
## 7.5  Agentic Framework: AG2
### 7.5.1  Two Agent Conversations 7.5.2  Human in the Loop 7.5.3  Agents Using Tools
## 7.6  Agentic Framework: CrewAI
### 7.6.1  Introduction 7.6.2  First Crew: News Analysis Crew 7.6.3  Exercise: AI Security Crew
## 7.7  Agentic Framework: OpenAI Agents
### 7.7.1  Getting Started with a Single Agent 7.7.2  Working with Multiple Agents 7.7.3  Agent with Search and Retrieval Functionality
## 7.8  Agentic Framework: Pydantic AI 7.9  Monitoring Agentic Systems
### 7.9.1  AgentOps 7.9.2  Logfire
## 7.10  Summary

# 8  Deployment

## 8.1  Deployment Architecture 8.2  Deployment Strategy
### 8.2.1  REST API Development


### 8.2.2  Deployment Priorities 8.2.3  Coding: Local Deployment
## 8.3  Self-Contained App Development 8.4  Deployment to Heroku
### 8.4.1  Create a New App 8.4.2  Download and Configure CLI 8.4.3  Create app.py File 8.4.4  Procfile Setup 8.4.5  Environment Variables 8.4.6  Python Environment 8.4.7  Check the Result Locally 8.4.8  Deployment to Heroku 8.4.9  Stop Your App
## 8.5  Deployment to Streamlit
### 8.5.1  GitHub Repository 8.5.2  Creating a New App
## 8.6  Deployment with Render 8.7  Summary

# 9  Outlook

## 9.1  Advances in Model Architecture 9.2  Limitations and Issues of LLMs
### 9.2.1  Hallucinations 9.2.2  Biases 9.2.3  Misinformation


### 9.2.4  Intellectual Property 9.2.5  Interpretability and Transparency 9.2.6  Jailbreaking LLMs
## 9.3  Regulatory Developments 9.4  Artificial General Intelligence and Artificial Superintelligence 9.5  AI Systems in the Near Term 9.6  Useful Resources 9.7  Summary

# The Author Index

**Service Pages**
**Legal Notes**


_[OceanofPDF.com](https://oceanofpdf.com/)_


# Preface

Welcome to your journey into the world of generative artificial
intelligence (generative AI). In this preface, we set the stage for what
you, the reader, can expect from this comprehensive guide on
generative AI with Python. Follow this roadmap to maximize the
value you derive from our journey into the world of generative AI.

## **Objective of This Book**


Welcome to our comprehensive exploration of generative AI with a
spotlight on some of its most transformative and advanced
technologies. The primary objective of this book is to guide you
through the frontiers of this dynamic field, with special attention to
large language models (LLMs), the nuanced art of prompt
engineering, the utility of vector databases, innovative processes of
retrieval-augmented generation (RAG), and the up-and-coming topic
of agentic systems.


LLMs have revolutionized the way we interact with text-based AIs.
LLMs unlock unparalleled capabilities in language understanding
and generation. Well dive into the architectures of these models,
dissecting how they learn from massive corpora of data to produce
human-like text. Then, we’ll examine prompt engineering, an
essential skill in the age of LLMs. You’ll learn how to craft prompts
that efficiently navigate the models’ knowledge and capabilities.


Vector databases present the next leap in organizing and retrieving
data. Understanding this technology is key to working with highdimensional data and building systems that are capable of rapid and
relevant information access. We’ll explore the concept behind vector
databases, their design and function, and how they pave the way for
sophisticated AI applications.


The concept of RAG bridges the gap between retrieval of relevant
information and on-the-fly text generation. RAG systems mark a
significant milestone in AI development, assisting models in
producing more accurate, more informed content. The chapter
dedicated to RAG will offer an in-depth look at its mechanisms and
at integrating this technique into your generative AI applications.


Next, we’ll venture into the domain of agentic systems. These AI
systems can act autonomously, make decisions, and undertake
tasks that traditionally require human intelligence. We’ll navigate the
ethical, technological, and practical constructs of such systems. This
chapter will prepare you to design AIs with autonomy and agency in
a responsible and innovative manner.


Up to that point, you’ll have learned to develop applications locally,
but eventually you want to share your work with the wider world.
We’ll dive into this topic in the chapter on deployment of AI systems.


This book is crafted not only to provide you with a deep theoretical
grounding in these areas but also to give you hands-on practical
expertise. Through a series of meticulously selected examples, case
studies, and projects, we’ll guide you through applying these
concepts to varied scenarios, whether for professional advancement,
academic research, or personal intellectual curiosity.


Our commitment extends beyond mere knowledge transfer. We hope
to equip you with the awareness required to become a proficient


creator and innovator in the field of generative AI. We aim to
thoroughly prepare you to confront and tackle the challenges and
opportunities that this technology presents in the modern world. By
the end of this book, you’ll have, not just an understanding, but
mastery over these sophisticated instruments of artificial intelligence.

## **Target Audience**


This book is designed for a wide array of readers, ranging from
software developers and data scientists to students and researchers
interested in generative AI. A certain amount of coding background is
expected. If you have a basic understanding of Python programming
and a keen interest in AI, especially in the field of generative AI
models, this book will serve you well.


The book’s content is tailored to engage both novices taking their
first steps into the world of generative AI and seasoned professionals
seeking to refine their skills and knowledge.


Our practical examples and thorough explanations will help you
grasp the concepts and techniques essential to developing and
applying generative AI systems. Whether you’re looking to innovate
in your field, embarking on an academic endeavor, or simply
pursuing a fascination with AI, this book hopes to serve as an
invaluable resource on your journey.

## **Prerequisites: What You Should Already** **Know**


Before diving into the riveting world of generative AI with Python,
let’s check a few prerequisites to ensure a smooth journey. First, in


terms of mandatory requirements, a firm grasp of Python
programming is essential; you should be comfortable with the
following tasks:


Writing functions


Creating and manipulating different data structures like lists and
dictionaries


Writing loops, mainly for-loops


Using libraries like NumPy and pandas


Ideally, but not mandatory, you already have a foundational
understanding of machine learning (ML) concepts, such as training
models and working with datasets.


Familiarity with basic statistics and linear algebra will also be
beneficial, as they underpin many AI algorithms. Although the book
will cover the necessary theory behind generative AI, previous
exposure to neural networks and deep learning frameworks like
TensorFlow or PyTorch will help you navigate the more advanced
topics more easily.


If these prerequisites sound like languages you speak, you’re well
equipped to embark on our thrilling voyage through the seas of
generative AI landscapes.

## **Structure of This Book**


This book is designed as a practical guide for Python programmers
looking to develop generative AI applications. The structure of the
book follows a step-by-step approach, starting with an introduction to
the fundamental concepts and progressing to more advanced topics
like vector databases and agentic systems.


You’re encouraged to go through the book sequentially, but some
chapters build upon the knowledge from previous chapters—more
on that in the next section. Practical Python code examples are
available for download at _https://www.rheinwerk-_
_computing.com/6057/_ to illustrate and reinforce the application of the
concepts discussed. Let’s look at each of the chapters in turn:


**Chapter 1**
This chapter introduces you to the basics of generative AI, a
subfield of artificial intelligence focused on creating new content.
You’ll learn about natural language processing (NLP) models, in
particular LLMs. Recent developments like large multimodal
models (LMMs), or reasoning models are touched on as well.


**Chapter 2**
In this chapter, we discuss pretrained models, particularly from the
field of NLP. Pretrained models are language models that have
been trained on large amounts of data and that can be reused for
various NLP or computer vision tasks. In this chapter, we’ll discuss
the popular platform Hugging Face, on which you can find over a
million open-source models to handle many tasks.


The models we present will mostly solve particular tasks like text
summarization, translation, text classification, or text generation.
The advantage of this approach is that these models are small
and can be operated locally. In this chapter, you’ll learn how to
select a model and operate it on your system.


**Chapter 3**
In this chapter, you’ll learn how to interact with LLMs via Python
code. Different providers like OpenAI and Groq are covered, and
we’ll show you how to use their models for your projects. Different
ways to use these models exist. In this book, you’ll learn how to
work with LangChain, a Python-based framework for interacting


with LLMs, to implement efficient approaches, including prompt
templates and chains to guide the LLMs to produce the desired
outputs.


**Chapter 4**
Prompt engineering is the process of designing efficient inputs to
LLMs to generate outputs. You’ll learn how to create effective
prompts to optimize the performance of language models and
achieve more precise results. Basic techniques such as few-shot
prompting and chain-of-thought (CoT) are covered. But we’ll also
go beyond these topics and cover more advanced techniques like
self-feedback or reflection.


**Chapter 5**
This chapter delves into vector databases, essential for efficiently
storing and querying large text collections. We describe the entire
process, from the indexing pipeline (in which you learn how to
preprocess the data), to storing the data in a vector database and
querying. We’ll mostly focus on adding data to a vector database.
This process consists of several steps that we’ll cover one by one.


We start with document loading. For document loading, various
LangChain document loaders are at your disposal to load nearly
any kind of data source in a structured way. We’ll visit some data
sources as well.


In the data splitting step, you’ll learn how to structure documents
into meaningful bite-sized chunks. Different methods can be used,
depending on the kind of data and use case. We’ll present the
most common data splitting approaches.


Often, text information needs to be converted into a format that a
computer algorithm can “understand.” Since computers work
based on numbers rather than human language, the information is


converted into a numerical representation called an embedding.
You’ll learn what embeddings are, how they can be created, and
different types that are available.


Several providers of vector databases can be used, but we’ll work
with a Chroma database as an example of an open-source vector
database that can run locally on your system. But you’ll also learn
how to work with a web-based provider called Pinecone.


Once your data is stored into a vector database, you’ll want to use
the database to retrieve information. Typically, as a user, you have
a query and want to retrieve the most relevant information, like a
text document or an image, from the data store. We’ll demonstrate
how not only texts can be retrieved, but also images and audio
files. You’ll learn how to retrieve data based on additional
conditions like special properties, which are typically defined in
metadata.


A key aspect of finding relevant documents is how relevance is
measured and how these documents are found. We cover these
topics in our discussion on similarity search. Some concepts
explored include cosine similarity and maximum margin relevance
(MMR).


In a capstone project, we bring all the pieces together into a single
project, starting with a specific data source, preprocessing the
data, and finally storing the data into a vector database.


**Chapter 6**
RAG is a new paradigm where external knowledge sources,
typically from a vector database, are integrated into the generation
process to enhance the quality and relevance of the generated
text. This generative AI feature is powerful in a company
environment, as you learn how powerful this technology can be.


You’ll learn how to retrieve relevant information from a large data
store, how to integrate that information into a generation process,
and how to evaluate the quality and diversity of the generated text.


**Chapter 7**
This chapter introduces agent-based, or agentic, systems. These
AI systems build on LLMs and equip them with additional features
like tool use or memory, so that these agentic systems are
capable of autonomously executing tasks and directing their own
actions toward specific goals.


Agentic systems are one of the most interesting areas in AI
development. Many different frameworks are provided, and we’ll
work with the most relevant ones, such as LangGraph, OpenAI
Agents, Microsoft AG2, Magentic One, TinyTroupe, and Pydantic
AI.


**Chapter 8**
Up to this point, we’ve developed systems locally on our
computers, but in this chapter, you’ll learn how to practically
deploy generative AI models and systems. The deployment
process typically involves the use of representational state
transfer (REST) application programming interfaces (APIs) to
make the systems accessible to users and other systems that
want to use these capabilities.


We’ll explore different deployment options and design decisions
like self-contained applications versus frontend-backend
architectures. You’ll learn how to create a backend REST API
service and also how to deploy an application to a variety of
providers, such as Heroku, Streamlit, or render.


**Chapter 9**
This book concludes with a look at future developments in


generative AI. We’ll discuss associated challenges, such as
impacts on employment and other societal challenges, but also
opportunities.

## **How to Use This Book Effectively**


This book is designed to be both a comprehensive guide and a
practical toolkit for enthusiasts, developers, and professionals
looking to harness the power of artificial intelligence to generate new
content, from text to images and beyond. To make the most out of
this book, we want to share some key strategies to help you use it
effectively.


Many chapters can be considered standalone chapters, and you can
just jump into them, but some build upon the knowledge from other
chapters. Figure 1 shows an overview of the chapters that can be
directly consumed and those that require some knowledge learned
from other chapters.


**Figure 1** Book Chapter Dependencies


Let’s start with the standalone chapters. Chapters 1 through
Chapter 3, and Chapter 9, can be consumed independently for the
most part.


However, Chapter 4 builds upon knowledge of LLMs, so you ideally
should read Chapter 3 first.


If you want to dive into vector databases in Chapter 5, we
recommend reading both Chapter 3 and Chapter 4 first. Once you’ve
covered vector databases, you can extend your knowledge with
RAG in Chapter 6.


For Chapter 8, you should have at least covered the basics of LLMs
in Chapter 3 as well as prompt engineering in Chapter 4.

## **Downloadable Code and Additional Materials**


Alongside this book, you can download the code examples, so that
you can follow and reproduce the scripts on your own. You can get
the material via GitHub. The repository, which is a cloud-based
storage of the content, can be visited via this link:


_https://github.com/DataScienceHamburg/GenerativeAiApplicationsW_
_ithPython_Material_


You can also download the code directly from the publisher’s
website:


_[https://www.rheinwerk-computing.com/6057/](https://www.rheinwerk-computing.com/6057/)_


In the next section, we’ll describe how you can download the
material so that you can follow along the Python scripts on your own
system.


## **System Setup**

Figure 2 shows the steps for setting up your system so you can work
with the coding material and run it on your local system.


**Figure 2** System Setup


By following these steps, the scripts can be run on your local
computer. This preparation might seem like a lot but consider that
this is a one-time effort and shouldn’t take more than 30 minutes.
The steps are as follows:


### 1 2 3 4 5



Python installation


Integrated development environment (IDE) installation


Git installation


Downloading the course materials


Setting up your local environment


### **Python Installation**

The Python installation step is straightforward and can be
accomplished through multiple methods. We recommend
downloading Python from the official website at
_[https://www.python.org/downloads/](https://www.python.org/downloads/)_ . If you scroll down the download
page, you’ll find multiple different versions.


Figure 3 shows a list of these versions. The scripts and code in this
book were developed on Python version 3.12.7. To avoid any issues,
you should stick to the same version. Click the **Download** button
and follow the installation instructions. Nothing specific needs to be
considered, so you can go with the default settings.


**Figure 3** Python Download

### **IDE Installation**


An IDE is essential for efficiently writing and managing code in
Python projects. Some popular choices include the following:


**Visual Studio Code (VS Code)**
This lightweight and highly customizable IDE supports many
different programming languages, which is one reason why it is a
favorite. We use VS Code for our Python, R, and Flutter projects
and therefore don’t need to adjust to different IDEs when
switching projects.


VS Code is open source and free at
_[https://code.visualstudio.com/](https://code.visualstudio.com/)_ . Its large community provides
thousands of extensions. We’ve used it for many years and can


hardly imagine switching. But eventually we did. Well, kind of. We
recently moved to Cursor.


**Cursor**
Cursor is a fork of VS Code, which means that it is very close
relative. But the main difference with Cursor is that it already has
AI power included. With this AI-enhanced code editor, you become
much faster and much efficient in coding. Cursor leverages
generative AI capabilities, and you can get coding assistance via
OpenAI’s Codex, GPT, or Anthropic’s Claude.


Cursor features code completion, code explanation, bug fixing,
refactoring, and interactive chatting to speed you up. It has a free
version and a paid version. You can learn more at
_[https://www.cursor.com/](https://www.cursor.com/)_ .


**PyCharm**
This IDE is focused on Python and provides advanced features
like code completion and debugging. The community edition of
PyCharm is free and includes basic features while the
professional version provides deeper integrations. On the
developer website, you can find both versions at
_[https://www.jetbrains.com/pycharm/download/](https://www.jetbrains.com/pycharm/download/)_ .


If you already have a preference and experience with any of these
options, we won’t stop you. But if you’re a beginner and looking for
good advice, we recommend going with Cursor.

### **Git Installation**


Git is an essential tool for version control, allowing developers to
track changes in their code, collaborate with others, and maintain a
history of project development.


Git helps you manage your codebase efficiently by enabling
branching, merging, and reverting changes. Git integrates
seamlessly with platforms like GitHub, GitLab, and Bitbucket, making
remote collaboration straightforward. You’ll need Git in the next step
to get the book’s material. Download Git from _https://git-_
_scm.com/downloads_ . Figure 4 shows the download options.


**Figure 4** Git Download


Select the download corresponding to your operating system. Many
choices are available, but you can go with the default settings during
installation.

### **Getting the Source Material**


The scripts and code files for this book are hosted on GitHub. You
can find the material at the following link:


_https://github.com/DataScienceHamburg/GenerativeAiApplicationsW_
_ithPython_Material_


When you navigate to this page, you should see all the material, as
shown in Figure 5.


**Figure 5** GitHub Repository for This Book


You can get the code in two ways by clicking the green **Code** button.


**Download as ZIP**


**Clone using web URL**


If you have no experience with Git, go with the ZIP option. Download
the ZIP file and extract it to a folder of your choice on your computer.


But if you had points of contact with Git, you could clone the
repository by running the following from the command line:

```
git clone
https://github.com/DataScienceHamburg/GenerativeAiApplicationsWithPython_Material.gi
t

```

This command will clone the repository to your computer.


### **Setting up Your Local Environment**

A Python environment is an isolated workspace where you can
install and manage dependencies for a specific project. This
environment acts as a sandbox, ensuring that the libraries and tools
used in one project don’t interfere with others on your system. The
diagram shown in Figure 6 illustrates the concept of environments
and why they are needed.


**Figure 6** Python Environments


While Project A requires a specific package xyz version 1.0a0 and
Python version 3.10, you might also need to work on a different
project with completely different requirements.


Let’s say, for instance, that Project B requires the same package xyz,
but in the newer version 2.0a0, and a different Python version,
maybe 3.12.7 instead. If you’ve only set up a single environment for
all your projects, you would run into issues because of the
incompatibility between the two projects.


The gold standard is to set up an environment for each project you
work on. This approach consumes more space on your hard disk,
but you’ll be on the safe side and avoid negative side effects
between your projects.


OK, we hope we’ve convinced you of the benefits of working with
environments. Great—now we need to figure out which environment


to choose. Different tools for managing your Python environments
include the following:


**virtualenv**
virtualenv is a lightweight tool for managing Python environments.
It allows you to install project-specific packages without affecting
the global Python installation.


**Poetry**
Poetry is a more modern dependency and environment manager.
It simplifies package management by combining dependency
specification, installation, and environment creation in a single
tool. It is perfect for projects that need precise version tracking
and easy deployment.


**uv**
A less popular but emerging tool, uv focuses on creating ultralight
virtual environments. Due to its implementation in Rust, it is
blazing fast compared to other environmental tools.


We recommend uv. You can find many different options to install uv
on the developer page _https://docs.astral.sh/uv/getting-_
_started/installation/#standalone-installer_ . You can install it via pip on
your terminal, as follows:

```
pip install uv

```

In the code folder, you’ll find a file called _pyproject.toml_ . This file
includes basic metadata information on the package, as well as
package dependencies—the packages and their versions as we
have them installed on our systems when we created the material.
Next to the _pyproject.toml_ file, you’ll find _uv.lock_ . This file keeps track
of the exact versions of all dependencies and their transitive
dependencies, that is, both dependencies and dependencies of
dependencies.


You can create the exact same environment we’ve used by running,
in the terminal, the following command:

```
uv sync

```

This command will download and install all dependencies into a
subfolder named _.venv_, all at once. If for whatever reason it does not
work on your computer, don’t worry. Open the _pyproject.toml_, look for
the section on `dependencies`, and install the packages manually. You
can do install these packages by running either of the following
commands:

```
 pip install packagename

 uv add packagename

```

You should also read the description on the GitHub repository, in
which specific issues for different platforms will be addressed.


Once you open a Python script, VS Code (or Cursor) will
immediately recognize that an environment is available. Check this
capability by inspecting the horizontal bar at the bottom. Figure 7
shows the Python version (3.12.7) used and the virtual environment
( _.venv_ ).


**Figure 7** Environment and Python Detection in VS Code


We’ve completed the last step of the system setup, and now, you’re
ready to start coding.

## **Acknowledgments**


I hope what you’ve learned so far about this book has made it
enticing.


In my journey writing this book, I have traversed the exciting and
often challenging landscape of generative AI. No such voyage is
ever a solitary endeavor. Therefore, I want to take a moment to
acknowledge those who have been my refuge and steadfast
supporters.


At the top of my gratitude is my family. Their love and understanding
have been the foundation of my resolve. My wife Lea, with her
infinite patience and unwavering support, has been the lighthouse
guiding me through challenging times of research and writing. She
accepted, without a murmur of disquiet (well mostly), the long and
irregular hours I spent secluded in my working room, tapping away at
the keyboard, lost in a world of codes and concepts. Her strength
and encouragement were the invisible hands that held me steady
when the specter of writer’s block loomed menacingly.


Equally deserving of my deepest appreciation is my daughter Elisa,
whose youthful cheer and innocence often penetrated the solitude of
my scholarly exertions, reminding me of the joy and wonder that life
offers. Her understanding, far beyond her years, was a treasured gift
as she accepted, with remarkable maturity, the times when I was
preoccupied with crafting this manuscript.


To these two remarkable individuals I dedicate not just this chapter,
but all the fruits of the hours spent creating this book on generative
AI with Python. May every page reflect the love and sacrifice that
they have so selflessly given.


To our extended family and friends who have offered their
encouragement and support, to colleagues who have provided
technical insights, and to the wider AI and Python communities that
have inspired and fueled our passion for this subject, you have my
heartfelt thanks. This book is not just a product of my endeavor; it is


a testament to the collective spirit of all those who have, in ways big
and small, contributed to its completion.


Thank you.

## **Conventions Used in This Book**


Throughout this book, certain typographical and formatting
conventions have been employed to enhance your learning
experience and to make the journey into generative AI as clear and
effective as possible.


Code blocks and programming snippets are presented in a
monospaced font, which delineates them from the surrounding text,
ensuring that you can easily identify and follow along with our Python
examples.

```
# sample code looks like this
my_welcome = “Welcome to the book”

```

The code provides outputs that are typically shown on the command
line. Such outputs are presented similarly, and look like this:

```
Welcome to the book

```

All code blocks and files can also be found in the accompanying
repository. You can easily navigate to the source code files, which
are indicated as _source_folder/source_file_name.py_ .


To encapsulate essential takeaways or to provide additional context,
informational boxes are placed strategically throughout the chapters.


**An Information Box**


Here you find details on key concepts.


Hyperlinks are italicized to provide quick navigation to external
resources for a deeper dive into topics or to access datasets
pertinent to the exercises, for example, _www.rheinwerk-_
_computing.com_ .


We hope that these conventions render the book both user friendly
and conducive to your learning journey into the world of generative
AI.


_[OceanofPDF.com](https://oceanofpdf.com/)_


# 1  Introduction to Generative AI

_One day the AIs are going to look back on us the same way we_
_look at fossil skeletons on the plains of Africa._
_—Nathan Bateman in the film Ex Machina_


Humanity’s story is a journey of evolution—a story of curiosity,
invention, and transformation. We’ve always sought to build tools to
amplify our abilities. It started with fire, and then, we invented the
wheel, the printing press and in the last century the internet—to
name just a few key milestones. Today, we stand at the precipice of
the newest kind of evolution, one driven not by natural selection, but
by our own creations.


Generative artificial intelligence (generative AI) represents a huge
leap forward in this journey. Earlier computer technologies were
explicitly programmed to perform specific tasks. Generative AI can
create, imagine, and synthesize, often appearing capable of its own
spark of creativity.


This chapter explores how we arrived at this particular moment.
You’ll learn about the developments critical for this invention. The
most relevant technologies in this field are large language models
(LLMs), which we’ll discuss in more detail. Then, we’ll extend our
discussion to related technologies like large multimodal models
(LMMs) before we study applications using generative AI.


How did we end up at this point? We’ll introduce you to artificial
intelligence in Section 1.1. Artificial intelligence, especially generative


AI, is made possible by developments in different areas. You’ll find
out about these pillars of generative AI advancement in Section 1.2.
Generative AI is based on deep learning; you’ll encounter this type of
AI and its core features in Section 1.3.


Perhaps, you’ve heard of the impressive achievements of various AI
systems, especially in the field of gaming. We’ll revisit these
achievements in Section 1.4 and discuss why AI can have
superhuman capabilities in some fields and why extending these
capabilities to a wide range of domains can be difficult.


We cannot speak about generative AI without discussing natural
language processing (NLP). The most usual input type of these
models is text. Thus, NLP models play a crucial role, as you’ll see in
Section 1.5. LLMs are the foundation of most generative AI
applications. In Section 1.6, we’ll look at the most notable LLMs.


With the advancement of LLMs, some limitations were discovered.
One limitation is that LLMs are restricted to processing text input and
can only provide text output. This limitation changes with LMMs, the
model class that you’ll learn about in Section 1.7.


In Section 1.8, you’ll learn which types of content can be created
with generative AI. A complete industry has been developed around
this area, as explored in Section 1.8.


Let’s start with the foundation of this book—an introduction to
artificial intelligence in general and generative AI in particular.

## **1.1  Introduction to Artificial Intelligence**


First, what is generative AI? Generative AI refers to a branch of
artificial intelligence focused on creating models that can produce


new content such as text, images, music, code, and videos—
basically any kind of data.


The most famous offspring of generative AI is ChatGPT. Based on
OpenAI models from its family of GPTs (generative pretrained
transformers), this chatbot became famous more quickly than any
other service so far.


Figure 1.1 shows the growth in users of selected internet services
over time.


**Figure 1.1** Number of Users of Selected Internet Services


While Netflix required 1,500 days to reach 1 million users, other
services reached this milestone more quickly. Spotify needed 150
days, while Instagram did it in 75 days. The line for ChatGPT is close
to vertical in this graph because OpenAI reached 1 million users in
just 5 days. To say “ChatGPT has taken the world by storm” is a
gross understatement. Released at the end of November 2022, the
field has since evolved so quickly that we often forget everything that
happened in just a few years’ time.


The rapid ascent of ChatGPT is exemplary of a larger phenomenon:
the acceleration of generative AI development. What once took
decades to iterate and improve upon is now happening in a few


months. The release cycle for AI models has become astonishingly
compressed, with each new iteration not only outperforming its
predecessor but also expanding its range of capabilities.


Behind this incredible pace of change is a confluence of
technological and societal factors. The availability of vast
computational resources, driven by cloud computing and specialized
hardware like GPUs and TPUs, has enabled researchers to train
larger and more complex models. Simultaneously, the abundance of
publicly accessible data—like images, text, videos, and more—has
provided the fuel required to teach these models how to create.


But technology alone doesn’t explain the speed of adoption.
Generative AI aligns seamlessly with the demands of the modern
world, where efficiency, creativity, and scalability are paramount.
Businesses eager to stay ahead of the competition have embraced
these tools to automate content creation, optimize workflows, and
deliver personalized customer experiences. Consumers, fascinated
by AI’s creative potential, have adopted platforms like ChatGPT, not
just as tools but as companions for creativity, problem-solving, and
learning.


This rapid development has created a feedback loop: As more
industries adopt generative AI, they generate insights, use cases,
and datasets that further refine these technologies. Open-source
communities and research collectives accelerate the pace by sharing
advancements openly, democratizing access to cutting-edge tools.
Meanwhile, investments in AI startups have surged, creating a highly
competitive ecosystem that pushes innovation to the forefront.


However, the speed at which generative AI evolves also introduces
challenges. Ethical concerns, such as misinformation, intellectual
property rights, and job displacement, have become urgent topics of


discussion. Regulatory frameworks struggle to keep up with the pace
of change, leaving gaps that could have far-reaching consequences.


Generative AI’s rapid rise is a testament to its transformative
potential. It has unlocked possibilities that were unimaginable a
decade ago and continues to redefine the boundaries of what
machines and humans can achieve together. As we look ahead, the
question is no longer whether generative AI will shape our future, but
how we’ll shape the future of generative AI.


Generative AI’s rapid development is not just a technological
masterpiece. This transformative force operates across creative,
technical, and commercial landscapes, and its influence transcends
the borders of research labs, reaching into studios, factories, and
boardrooms. Generative AI reshapes the way we create, build, and
conduct business.


Backtracking a bit, let’s now look at the history of AI in general.
Figure 1.2 shows the evolution of artificial intelligence.


**Figure 1.2** AI Evolution


Artificial intelligence has undergone a remarkable journey. Numerous
breakthroughs occurred, but so did setbacks and sustained periods
of rapid innovation. The starting point is marked by the development
of the Neuron model, developed in 1943 by Warren McCulloch and
Walter Pitts, that laid the foundation for understanding how biological
processes can inspire machine intelligence.


Alan Turing developed the famous eponymous test as a benchmark
for assessing a machine’s ability to exhibit human-like intelligence.
The Turing Test determines if a machine can engage in a
conversation indistinguishably from a human. If the machine can
successfully deceive a human evaluator into thinking they are
interacting with another human, the machine passes the test. The
Turing Test has become a philosophical and technical cornerstone in
AI discussions.


In 1957, Frank Rosenblatt developed the concept of the _perceptron_,
which marked the first implementation of a neural network. Concepts
like weights and learning set the stage for later advancements in
machine learning (ML).


In the 1970s, expert systems were designed to mimic human
decision-making in specific domains. These expert systems were a
major focus of AI research at that time. However, limitations in
computing power and data led to disillusionment and triggered the
first “AI winter,” a period of reduced funding and reduced interest in
AI. During the 1980s, AI resurged slightly, but not much progress
was made, and a second “AI winter” occurred—another cycle of
unmet expectations and general skepticism about the potential of AI.


In the early 1990s, neural networks gained some traction again, and
some theoretical groundwork was laid. But the most important
breakthroughs happened in the 2010s and later. Deep learning, a
subset of AI, was nothing less than a revolution. one was fueled by
large amounts of data and improved computational power. New
architectures were developed. For example, convolutional neural
networks (CNNs) and recurrent neural networks (RNNs) enabled
breakthroughs in computer vision and NLP.


In the late 2010s, generative AI took off. Early models like OpenAI’s
GPT-2 (released in 2019) demonstrated the ability to generate


coherent and contextually relevant text. Subsequent models quickly
evolved.


While GPT-2 is considered to have abilities comparable to a
preschooler, GPT-3 (released in 2020) achieved elementary school
pupil sophistication. GPT-3 displayed impressive generalization
across various tasks. Released in 2023, GPT-4 is considered to be
comparable to a smart high-schooler. GPT-4 is marked by
improvements in reasoning and contextual understanding. In
December 2024, the model o3 was announced, and it is expected to
be released early 2025, with capabilities comparable to university
students.


With more and more capabilities, AI systems are becoming
increasingly more general. Tech companies are investing heavily in
this technology to achieve artificial general intelligence (AGI), which
contrasts with the notion of narrow AI.


_Narrow AI (or weak AI)_ is designed for specific tasks and operates
under a limited set of constraints. But don’t be fooled by the word
“weak”—these models excel in well-defined areas like language
translation, facial recognition, and recommendation systems,
performing these tasks with high precision. “Narrow” describes the
scope of their capabilities better. However, this kind of AI lacks the
ability to generalize its knowledge to other domains.


On the other hand, AGI (or strong AI) aspires to understand, learn,
and apply knowledge across a wide range of tasks, mirroring human
cognitive abilities. AGI aims to exhibit versatile and adaptive
intelligence, capable of reasoning, problem-solving, and
understanding contexts across various fields without any predefined
limitations.


Generative AI, within the broader AI landscape, serves as a pivotal
technology driving advancements in creating realistic and contextaware content autonomously. Its applications span various fields,
enhancing capabilities in media, communication, and content
creation while pushing the boundaries of what AI can achieve.


With each technology, an initial innovation trigger (i.e., a
technological breakthrough, a product launch, or another event)
generates significant interest and media coverage.


Then, the public gets overenthusiastic. Paired with inflated
expectations, disappointment increases when the technology does
not meet these exaggerated expectations. In the subsequent phase,
public interest decreases due to experiments that can’t deliver
according to the hype.


But investment does not stop. Neither does the development in this
field. Eventually, successful projects emerge. These projects show
the technology’s real-world value. Finally, the technology becomes
widely understood, adopted, and accepted by mainstream.


At the time of writing, generative AI is possibly in the “trough of
disillusionment,” but we can expect that generative AI will reach the
“plateau of productivity” in a few years. We won’t notice a single
event or breakthrough; rather, it will be a continuous process of
many small steps, and some huge steps.


Figure 1.3 shows some capabilities of AI systems on various tasks,
relative to human performance, over time.


**Figure 1.3** AI System Capabilities (Source: _https://ourworldindata.org/artificial-_
_intelligence_ ; used under Creative Commons Attribution 4.0 International License)


When the capability of an AI system in a specific task is compared
against human performance (e.g., “Language understanding”), the AI
system starts out completely incapable (represented by a score of
−100) but improves over time. In the next chapter, we’ll discuss
several reasons for AI’s continuous improvement over time. At some
point, the AI system reaches a score of 0—this value represents
human-level capabilities on that task. Every score above 0
represents superhuman capabilities. Several extremely impressive
behaviors of AI systems to notice include the following:


AI systems reach superhuman capabilities one task at a time.


The time it takes to achieve some outstanding capability gets
shorter and shorter.


Over time, there will be fewer tasks in which humans possess
capabilities better than AI systems.


But what cannot be illustrated in this way is that AI systems still
struggle to achieve AGI. In other words, current AI systems dominate
one task over others. But no AI system possesses all these
capabilities together. At the time of writing, OpenAI o3 may have
actually reached AGI, but the community lacks consensus on this
topic.


However, what generative AI achieved already is quite impressive.
How did we get to this point? Let’s find out in the next section.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **1.2  Pillars of Generative AI Advancement**

Previously, you saw some of the amazing capabilities of AI systems.
Several factors led to this result. In this section, we’ll take a closer
look at these factors: computational power, model and data size,
investments, and algorithmic improvements.

### **1.2.1  Computational Power**


Figure 1.4 shows the computations used to train an AI system,
classified by domain.


**Figure 1.4** Computation Used to Train AI Systems (Source:
_https://ourworldindata.org/artificial-intelligence?insight=the-last-decades-saw-a-continuous-_
_exponential-increase-in-the-computation-used-to-train-ai_ ; used under Creative Commons
Attribution 4.0 International License)


This graph specifically shows the computation effort for training over
time. The graph is logarithmic, and thus, the observed trend is
exponential in nature. Most points are clustered to the right,
indicating the increased interest and development in recent years; no


single domain drives this development. However, “Language” is the
dominant domain.


This training is only possible due to increased hardware
performance. Hardware progress follows an exponential course. So
far, hardware shows no signs of slowing down, and so larger and
larger models will be enabled.


Training computations go hand in hand with increased model sizes—
our next input factor.

### **1.2.2  Model and Data Size**


Figure 1.5 shows the relationship between the number of model
parameters and training dataset size.


**Figure 1.5** Model Parameters and Training Dataset Size (Source:
_https://ourworldindata.org/grapher/parameters-vs-training-dataset-size-in-notable-ai-_
_systems-by-researcher-affiliation_ ; used under Creative Commons Attribution 4.0
International License)


Both axes are logarithmic, which indicates that exponentially larger
models require exponentially larger datasets. Notice how most
developments have been achieved most recently. The colors


indicate researcher affiliation, which is either academic or industry.
Since the development of extremely large models costs in the order
of millions of dollars, academia can no longer keep up with the
industry’s costs.


Speaking of financial conditions, let’s look more closely at the
investment landscape that drives the developments.

### **1.2.3  Investments**


The most recent AI models already cost around US$100 million—an
impressive number made even more impressive when you consider
the cost of training in 2017. When the transformer architecture was
developed, training costs were around $1,000 USD, five orders of
magnitude less than currently.


More than just money, computational power also drives this
development as does how the algorithms have improved
dramatically over time.

### **1.2.4  Algorithmic Improvements**


The most impactful deep learning architecture so far is called the
_transformer architecture_ . Developed in 2017, transformers are the
foundation of all modern language models, but is also applied in
computer vision and time series prediction. Different software
domains rely on different data types, each of which are simpler or
harder to process by AI systems. Thus, different domains are
impacted differently by an AI system, which shows different speeds
of progress.


The usual baseline for algorithmic progress is called Moore’s Law.
Formulated by Gordon Moore in 1965, Moore’s Law suggests that
the number of transistors on a microchip doubles approximately
every 2 years, leading to exponential growth in computing power.
This principle has profoundly influenced technological
advancements, including the development of AI algorithms. In the
graph shown in, this baseline progress is represented by a dashed
line.


In domains like LLMs, the effective compute doubling time is
between 5 and 12 months. In other domains like computer vision, the
median compute doubling time is 9 months, which is significantly
larger. One reason for LLMs’ accelerated needs might be that
computer vision models are already extremely mature and have
already reached their plateau of productivity.


In essence, multiple driving forces have resulted in the outstanding
capabilities of our current generative AI systems, for instance, the
following capabilities:


Algorithmic progress improves model architectures and makes
them more accurate or enables faster learning.


AI systems rely on vast amounts of data. Since the onset of the
internet, the available data has been growing exponentially and
creates a huge source of training data.


Larger models require better hardware. Deep learning relies on
GPU power, and the processing power of GPUs has increased
exponentially.


None of these developments would be possible without proper
funding. Since generative AI delivered on expectations, huge
amounts of money have flowed into the development of new
models.


The combination of these driving forces has resulted in AI systems
with capabilities that, in many cases, equal or outweigh human
capabilities.


Now, let’s get a better technical understanding of the core concepts.
The next section will lay a foundation with some high-level
understanding of deep learning, the technology behind AI systems.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **1.3  Deep Learning**

Deep learning is a subfield of artificial intelligence and ML. You must
understand the crucial differences between ML and classic
programming process flows, as shown in Figure 1.6.


**Figure 1.6** ML and Classic Programming, Compared


While in classic programming, rules and data are used as inputs to
generate answers. ML turns this logic on its head. With ML, data and
corresponding answers are provided to an ML algorithm, and that
algorithm figures out the rules on its own.


This principle holds for statistical ML algorithms as well as any kind
of neural network. The most powerful ML algorithms derive from
neural networks, specifically deep learning. Let’s examine what
happens during the training of a deep learning model, as shown in
Figure 1.7.


Imagine you work in real estate, and you want to train an algorithm
to predict the price of houses. In your dataset, you’ll need many
observations of price transactions. In this setup, the price at which a
property sold is your _target variable_ —the variable you want to
predict. In more technical terms, these values are also called _true_
_values_ (typically abbreviated with the variable _Y_ ).


One of the first steps is to split your dataset into training and testing
datasets. The training data is only used for training; the testing data
is only used for model testing. More complex setups are possible,
but for our introduction, we’ll keep it simple.


The selling price depends on many factors like location, size, or age
of the property, which are your independent features, in statistics
often referred to as _X_ . Underlying all ML algorithms is the idea that
observable patterns exist between independent variables and
dependent variables. The algorithm will figure out these hidden
patterns.


**Figure 1.7** Deep Learning: Model Training


To train a deep learning model, you can feed the independent
features (or variables) to a deep learning model. The information is
passed through the network. Finally, the network provides a
prediction Y. This prediction is compared to the true value Y in a _loss_
_function_ . This function evaluates the current prediction quality and
returns a loss score that is used by the optimizer. An important
building block of a neural network, the optimizer tries to update the
weights of the neurons of the model in the most efficient way. At this
point, one loop has finished.


The next batch of data is loaded from the training data and passed
through the network layers. Ideally, the weights have been updated,
so that the current prediction of the model is closer to the real value.
The loss function calculates the loss score. Then, the optimizer
adapts the weights of the neurons again.


This process is repeated until all data has been passed through the
network. Typically, data is not just run through once, but several
times. Each complete loop of the complete dataset being passed
through the loop is called an _epoch_ .


The training process finishes once a stop criterion is found, for
instance:


A predefined number of epochs is reached.


Model loss has reached some convergence so that the training
process does not improve the result anymore.


Let’s assume that your model has been trained successfully. You
now have a model with a specific setup (i.e., architecture, number of
neurons, activation functions, etc.) and corresponding model weights
for each neuron in the network. How can you use this trained model
to generate predictions? This process of running a model for creating
predictions is called _inference_ . Figure 1.8 shows the model inference
process.


During model inference, you provide test data to the model. This test
data is passed through the model with its frozen model weights. In
this context, “frozen” means that the model weights are not adapted
any more at this point. You receive a prediction Y that you can


compare to the true test values Y. Both values (or sets of values) can
be used in your model evaluation.


**Figure 1.8** Deep Learning: Model Inference


This book is not a book on AI engineering. We won’t train a model
ourselves in this book. The good thing is we don’t have to! The
models that we’ll use are already trained on vast amounts of data,
and we can use these models with their frozen model weights to our
purposes and just run model inference.


Depending on the model architecture and available training data, you
can train many kinds of models. Typically, these models are
extremely well adapted to a specific dataset, that is, working rather
well, but in a rather narrow domain. Let’s turn to this topic next.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **1.4  Narrow AI and General AI**

AI systems have become more and more powerful, mostly absent
from the public eye. But every now and then, their capabilities reach
the public’s attention. Figure 1.9 shows some of the narrow
achievements of early AI systems.


**Figure 1.9** Narrow AI Achievements


In 1997, IBM’s Deep Blue, an extremely sophisticated chess playing
machine, beat world chess champion Garry Kasparov, and the world
was stunned that a machine won. For centuries, chess was
associated with outstanding cognitive capabilities. Furthermore,
good chess players have intuition, which is required to anticipate the
moves of the opponent. But the machine won and showed
superhuman capabilities at playing chess. In hindsight, we must
recognize that this was merely the result of a comparably simple
search algorithms and simulations of millions of moves. Deep Blue
did not apply any advanced artificial intelligence. Nevertheless, the
AI scored its first big win in several battles of wit between man and
machines.


Much more impressive was when Google DeepMind’s system
AlphaGo beat Lee Sedol, one of the best Go players in the world in a
2015 match. AlphaGo won four out of the five games and received a
$1 million prize money. Experts in Go did not expect AlphaGo to win
at all because of the game’s extraordinary high game tree


complexity. Sometimes called the “Shannon number” (after Claude
Shannon), _game tree complexity_ refers to the number of possible
games that could theoretically be played. The Shannon number for
chess is estimated to be around 10 [123] . Although an insanely large
number, many combinations have been simulated for chess.


In Go, a simple “brute force” approach to simulating all game
combinations is impossible. The Shannon number is estimated to be
around 10 [360] . (We’ll save you the trouble of reading a number with
360 zeros.) The reason for this large difference in complexity is
mainly the board’s size. In chess, the board is an 8 × 8, while Go is
played on a 19 × 19 grid. The game dynamics are also different: In
chess, a typical game involves about 40 to 60 moves per player. In
Go, a game can last around 200 to 300 moves per player.


The significance of a machine winning at Go cannot be
overestimated: Now, humans lose to machines in all one-versus-one
games. We thought only humans were capable of intuition, an
essential part of winning at Go.


In the second game of the five-game match, the AI made a move
that was completely incomprehensible to the experts. “Move 37” later
became famous as one of the most significant moves in the history
of the game of Go. AlphaGo made a move that no human would ever
have made at that point in the game. A Go stone was placed in a
position on the board that was completely unexpected. The experts
were unanimous: The AI made a major mistake that would take its
revenge later. In fact, much later in the game, it turned out to be a
brilliant move that the experts would analyze for months to come.
What’s more, this move not only proved that AI has intuition in its
own way. After thousands of years of playing Go, an AI was able to
present humans with abilities far beyond their own.


At this point, we have an AI system able to beat the best Go players
in the world. AlphaGo was at the top of the Go world. But just two
years later, in 2017, AlphaGo lost 100 out of 100 games against its
opponent. What happened? Did humankind strike back? Not really.
No human will ever hold the crown in Go again. What happened was
evolution, more specifically AI evolution. AlphaGo lost against its
offspring, a more advanced AI system called AlphaGo Zero.


AlphaGo Zero did not rely on studying gameplay from human
games. It learned by playing against itself and improved in mere 21
days to the level of AlphaGo. After 40 days, AlphaGo Zero had
exceeded all previous versions.


OK, you might think, at this point, AI systems can reach expert-like
capabilities in very narrow fields, and you’re right!. But could AI
systems be successful in real-time, multiplayer games? They are not
capable of teamwork and setting dynamic objectives, right? Well, in
2019, a system from OpenAI called “Five” played the video game
Dota 2. This system controlled five AI agents, one for each hero on a
team. These agents had to coordinate seamlessly to execute quite
complex tasks and strategies. The AI system had to make decisions
20 times per second. Short-term and long-term tactics had to be
carefully balanced.


In a live event in 2019, “Five” played against the international
champions OG who won “The International” a year earlier. The event
took place over four days. The AI agents played close to 43,000
games of which they won a staggering ratio of 99.4%.


More impressive AI systems were developed that could play and win
games like Diplomacy. In this complex strategy board game,
negotiations, collaborations, and strategic planning are crucial to
success. Meta developed a system called Cicero that can excel at
human-like communication and social reasoning.


AI systems started in rather narrow domains, like Chess and Go, and
have already achieved mastery in complex environments that require
far more skills that just being a solitary genius.


Where are we today, in 2025? AI systems can solve more and more
cognitive tasks.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **1.5  Natural Language Processing Models**

NLP forms the backbone of many generative AI systems. NLP
enables machines to understand, generate, and interact with human
language. At the heart of NLP are core tasks that act as building
blocks for complex applications.

### **1.5.1  NLP Tasks**


In this section we’ll explore some foundational NLP tasks.
Figure 1.10 shows some typical NLP tasks—text classification, text
generation, question answering, translation, fill-mask tasks, and
sentence similarity. These different tasks will be explained in more
detail.


_Language modeling_ is the task of predicting the next word in a
sequence or assigning probabilities to sequences of words. It serves
as the cornerstone of many NLP applications, including text
generation, speech recognition, and machine translation. Language
models, such as GPTs, learn statistical patterns in text data, enabling
them to produce coherent and contextually relevant sentences. By
understanding language structure and semantics, these models can


generate human-like text, perform auto-completions, and even
engage in creative writing.


**Figure 1.10** Typical NLP Tasks


**Text Classification**


Text classification involves categorizing text into predefined labels or
classes. This task is foundational for many NLP applications, such as
spam detection, sentiment analysis, topic categorization, and intent
recognition. Models trained for text classification learn to identify
patterns and relationships in textual data, enabling them to
accurately assign labels based on content.


Text classification is pivotal in organizing large datasets and
enhancing user experiences by tailoring responses or content
recommendations.


**Example**


Imagine you’re developing an email filtering system. The goal is to
classify incoming emails as either “spam” or “not spam.” To
achieve this goal, a text classification model is trained on a labeled
dataset containing examples of both categories. By analyzing the
text, the model might detect suspicious phrases like “free money”


or “click here.” The model learns to predict the correct label for
new, unseen emails and can now help users automatically
organize their inboxes and focus on the most important
communications.


**Text Generation**


Probably the most prominent task in NLP since ChatGPT was
released, text generation will also be the task we’ll mostly use in this
book.


Text generation is the process of creating coherent and contextually
appropriate text based on a given input or prompt. This task is
central to many applications, including creative writing, chatbots,
content creation, and code generation.


Modern text generation systems excel in producing human-like
responses by leveraging vast datasets and advanced language
modeling techniques. These models can generate anything from
poetry and stories to technical explanations and program code, all
tailored to the specific needs of users.


**Example**


A text generation system can take the user prompt “Write a short
story about a robot exploring a new planet” and produce a detailed
narrative complete with descriptions, dialogue, and plot
development. The quality of the output depends on the training
data and the model’s ability to understand and extend the context
provided.


**Question Answering**


Question answering is the task of extracting or generating answers
to natural language questions. Question answering systems can be
classified into two types: retrieval-based and generative. Retrievalbased systems locate answers from a pre-existing corpus, while
generative systems like OpenAI’s ChatGPT synthesize new answers
based on input queries. This task combines language understanding,
reasoning, and contextual knowledge, making it essential for
chatbots, virtual assistants, and automated customer support.


**Text Translation**


Text translation aims to convert text or speech from one language to
another. Modern translation systems utilize deep learning models to
achieve high accuracy and fluency. Transformer-based architectures,
such as Google’s BERT (bidirectional encoder representations from
transformers) and OpenAI’s models (which we’ll discuss later) have
revolutionized this task by capturing the nuances of context and
syntax in both source and target languages. Applications of machine
translation range from breaking language barriers in global
communications to facilitating multilingual content creation.


**Fill-Mask Tasks**


Fill-mask tasks involve predicting missing or masked words within a
given text. This capability is foundational for understanding context
and is widely used in pretrained models like BERT.


During training, certain words in a sentence are masked, and the
model learns to predict them based on the surrounding context. Fillmask tasks help models grasp deeper semantic relationships and
are a critical step in developing robust NLP systems.


**Example**


Given the sentence “The weather is [MASK] today,” a fill-mask
model might predict “sunny,” “rainy,” or other contextually plausible
words. This ability not only enhances language understanding but
also supports downstream tasks such as question answering and
text generation.


**Sentence Similarity**


Sentence similarity involves measuring how semantically close two
pieces of text are. This task is fundamental in applications like vector
databases, on which we focus in Chapter 5.


But sentence similarity is also relevant for plagiarism detection,
duplicate question identification, and recommendation systems.
Models trained for sentence similarity use _embeddings_ to represent
sentences in a high-dimensional space, allowing similarity to be
calculated as the distance between their representations.


**Example**


Comparing the sentences “How do I reset my password?” and
“What should I do to recover my password?” a sentence similarity
model would identify a high degree of similarity between them, as
they convey almost the same meaning. This capability is crucial
for systems like FAQ matching and conversational AI.


**Text Summarization**


Text summarization involves condensing lengthy documents into
shorter, coherent versions while retaining the most critical
information. This task can be approached in two ways: extractive
summarization and abstractive summarization. Extractive methods
identify and concatenate key sentences or phrases from the source
text, while abstractive methods generate new sentences that
paraphrase the content. Summarization plays a crucial role in
information retrieval, content aggregation, and assisting users in
navigating large volumes of data efficiently.

### **1.5.2  Architectures**


Language modeling has evolved significantly over the years and has
been shaped by the development of foundational architectures. Let’s
briefly discuss some historical developments that have led to our
current architecture.


**Common Architectures**


Early models relied on recurrent neural networks (RNNs), which
were designed to process sequential data by maintaining a hidden
state that carried information from one time step to the next. This
structure allowed RNNs to handle basic tasks like text classification
or sequence prediction. However, they struggled with capturing longterm dependencies in text due to the vanishing gradient problem,
which made learning over extended sequences difficult.


To address these limitations, long short-term memory (LSTM)
networks were introduced. LSTMs extended the capabilities of RNNs
by incorporating memory cells and gates, which allowed the model to


retain important information over longer sequences while filtering out
irrelevant details.


This advancement made LSTMs effective for tasks such as machine
translation and text summarization, particularly when sequence
length and context played a critical role. Despite their improvements,
LSTMs were computationally intensive, especially when processing
large datasets, and their sequential nature limited scalability.


The advent of the transformer architecture in 2017 marked a turning
point in NLP. Unlike RNNs and LSTMs, transformers abandoned
sequential processing in favor of a self-attention mechanism that
enabled parallel processing of input data.


This approach allowed the model to capture relationships between
words regardless of their distance in the sequence, making it both
faster and more accurate.


Transformer architecture also introduced positional encoding to
account for the order of words in a sequence, preserving context
while maintaining computational efficiency. These innovations form
the backbone of virtually all modern LLMs.


**Practical Implementations**


Practical implementations of transformer-based models have
revolutionized the NLP landscape. Google’s BERT is one of the most
impactful models to emerge.


By training on masked language modeling and next-sentence
prediction tasks, BERT developed a deep understanding of text
context, enabling it to excel in applications such as question
answering, sentiment analysis, and named entity recognition (NER).
BERT can process text bidirectionally and thus can consider both


preceding and following words, which has set a new standard for
contextual understanding.


Another standout implementation is the GPT series, developed by
OpenAI. Unlike BERT, which is optimized for understanding text,
GPT models are designed for generating text. You know these
models implicitly because they form the foundation of ChatGPT.


These models predict the next token in a sequence based on
preceding tokens, making them capable of producing coherent,
contextually relevant, and creative outputs. From the highly versatile
GPT-3.5 to the advanced capabilities of GPT-4, o1, and o3, these
models have been widely adopted in end-user applications.


The progression from RNNs and LSTMs to transformers
underscores the transformative impact of architectural innovation in
NLP. By enabling deeper understanding, broader context awareness,
and more efficient processing, these developments have paved the
way for practical, real-world applications that continue to shape how
we interact with and leverage language models today.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **1.6  Large Language Models**

We’ll work a lot with LLMs in this book, and a complete chapter will
deal with this topic. So, we’ll keep it short and concise because we’ll
dive much deeper into this fascinating topic in Chapter 3.


LLMs are advanced ML models trained on vast amounts of text data
to understand, generate, and interact with human language. They
leverage architectures like transformers to process and produce
contextually coherent and semantically meaningful text, enabling
applications such as chatbots, content generation, and question
answering.


In the following sections, we’ll first describe the different steps of the
training process for an LLM. Then, we’ll highlight some use cases
before looking at some of the problems associated with LLMs.

### **1.6.1  Training**


Figure 1.11 shows the training process for LLMs.


**Figure 1.11** LLM Training Process


An LLM is trained in a process involving the following steps:


1. **Data**

The process starts with collecting and preparing a large amount
of diverse and high-quality text data. A lot of data preprocessing
must be performed, including data cleansing, tokenization, and
organizing to ensure consistency and relevance.


2. **Pretrained model**

Once a model is trained on this data, a pretrained model is
derived. This process involves predicting the missing words or
the next words based on the context. The goal in this step is to
capture general patterns and structures. The result is a generalpurpose model capable of understanding and generating
human-like text.


3. **Instruction model**

The pretrained model is fine-tuned using additional datasets or
techniques that are tailored to specific tasks or instructions. This
step ensures that the model generates outputs that are aligned
with particular applications or user instructions. This instructiontuning and fine-tuning helps achieve high-quality model outputs
by making the model more task specific.


4. **Safety model**

This step involves the alignment of the model to human
preferences. The aim of this step is to ensure that the model can
be operated safely. In this context, techniques like reinforcement
learning from human feedback (RLHF) are used to make the
model less biased and more reliable. A safety model models
some harmful or dangerous behavior in generated outputs. For
example, a model should refuse to help a user build a bomb or
hide a dead body.


5. **Evaluation**

The final model is rigorously evaluated using benchmarks and


real-world tasks to ensure its quality and alignment. Numerous
evaluation metrics assess the accuracy, relevance, safety, and
robustness of the model and its outputs. Further refinements
might be necessary, so that additional feedback loops might be
performed.

### **1.6.2  Use Cases**


LLMs have revolutionized the way we interact with artificial
intelligence, opening up a vast array of use cases that span across
industries and disciplines.


These models, powered by immense datasets and advanced neural
network architectures, are designed to understand and generate
human-like text, which makes them a versatile tool for various
applications, as we’ll discuss next.


**Creative Writing**


One of the most prominent and widely recognized applications of
LLMs is content generation. LLMs are adept at generating text that is
coherent, contextually relevant, and often indistinguishable from
human writing. This ability has application in crafting articles, blogs,
and social media posts. Businesses and individuals alike can use
LLMs to brainstorm ideas, refine drafts, and even produce entire
pieces of work.


An author can use an LLM to generate plot ideas and character
dialogues, while a marketing team can create tailored promotional
content targeting specific groups.


We’ll encounter this feature again in many chapters, like Chapter 3,
Chapter 4, and Chapter 7.


**Summarization**


Closely related to content creation is the use of LLMs for
summarization. The sheer volume of information generated daily in
the digital age makes it challenging to sift through and extract key
insights. LLMs excel in this domain by distilling large texts into
concise summaries, retaining the essence of the original content.


This capability is invaluable for professionals and researchers who
need to quickly grasp the main points of lengthy reports, articles, or
academic papers. Whether summarizing a dense legal document,
providing an executive summary for a business proposal, or creating
a digestible recap of the day’s news, LLMs save time and effort while
enhancing productivity. We’ll revisit this capability in Chapter 5 and
Chapter 6.


**Chatbots**


Another compelling use case is conversational AI, where LLMs are
employed to power chatbots and virtual assistants. These systems
can engage users in natural, dynamic conversations; answer
questions; provide recommendations; or assist with tasks.
Businesses deploy such bots to improve customer support, handling
routine inquiries efficiently and allowing human agents to focus on
more complex issues. On a personal level, virtual assistants
equipped with LLMs can manage schedules, set reminders, and
even act as tutors, guiding users through learning new skills or
solving problems.


**Translation**


Translations also benefit significantly from LLMs. These models
bridge linguistic barriers by providing accurate translations that


capture not just the literal meaning but also the nuances of context
and tone. Translation is particularly beneficial for global businesses
aiming to localize their content or individuals seeking to
communicate across cultures. Moreover, LLMs are instrumental in
language learning applications, offering learners personalized
feedback, conversational practice, and explanations for grammar or
vocabulary.


**Content Creation**


Creative applications of LLMs extend beyond text-based tasks. They
can assist in composing music, generating code, and even
developing game narratives or dialogue systems.


In the gaming industry, for instance, LLMs can create immersive
storylines and realistic non-player character interactions, enhancing
the overall player experience. Similarly, in software development,
LLMs help developers by generating code snippets, suggesting
improvements, or automating routine programming tasks.


**Education**


In the field of education, LLMs serve as valuable tools for both
teaching and learning. They can generate tailored lesson plans,
quizzes, and instructional materials. LLMs can adapt to diverse
learning styles and levels. Students can interact with LLMs to clarify
doubts, explore topics in depth, or receive assistance with writing
assignments. The interactive and adaptive nature of these models
fosters a more engaging and personalized educational experience.


Other use cases and affected industries are too numerous to list as
most industries will be affected by this revolution.


### **1.6.3  Limitations**

LLMs are incredible powerful, but they also exhibit certain limitations.
Some of these limitations include the following:


**Hallucinations**
LLMs can generate text that appears plausible but is factually
incorrect, misleading, or entirely fabricated. These “hallucinations”
occur because the models rely on statistical patterns in training
data rather than understanding or verifying facts. Thus, LLMs are
unreliable for tasks requiring high factual accuracy, such as
medical diagnoses or legal advice.


**Biases**
LLMs inherit biases present in their training data, which may
reflect societal stereotypes, cultural imbalances, or skewed
perspectives. This bias can result in outputs that are prejudiced or
offensive. Addressing bias is challenging because mitigating one
bias may inadvertently introduce or amplify another.


**Context window and token length constraints**
LLMs can process only a limited amount of text. These constraints
restrict the length of input text (context window) or of the output
text they can process in a single interaction. This constraint can
limit their ability to handle long documents, detailed instructions, or
extended conversations. Splitting content into chunks to work
within these limits may lead to loss of context or coherence.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **1.7  Large Multimodal Models**

Like LLMs, LMMs are advanced AI systems. But in contrast to LLMs,
LMMs are capable of understanding and possibly creating multiple
types (modalities) of data, such as text, images, audio, and even
video. Figure 1.12 shows possible input and output modalities of an
LMM.


**Figure 1.12** Large Multimodal Models


These models integrate diverse modalities into a single model.
These diverse modalities can be either on the input and/or the output
of the model. Some models allow for both text and images as inputs
and provide text as output, called _vision-language models (VLMs)_ .
Popular examples are Llama 3.2 Vision, GPT-4o, or Google Gemini.
The different modalities enable them to perform complex tasks that
require cross-modal understanding and reasoning.


Unlike unimodal models (like LLMs), which operate exclusively on a
single type of data, LMMs can generate text from an image, create
images based on user prompts, extract information from videos, and
much more. This versatility has placed LMMs at the forefront of AI


research. A shift from focus on LLMs to LMMs can be observed, and
this process will continue until eventually LMMs mostly replace
LLMs.


LMMs are transforming various industries by introducing innovative
solutions and automatic complex workflows. In the art and design
domain, tools like text-to-image conversion, which were previously
standalone models, will be integrated into LMMs. A prominent
example is DALL-E, which is integrated into GPT-4o.


In healthcare, LMMs have the potential to revolutionize medical
diagnostics and patient care. They can analyze medical images
alongside patient records to provide more accurate diagnoses.
Furthermore, they assist in creating educational materials for
patients, simplifying complex medical information with visuals and
explanatory text.


The entertainment industry is also leveraging LMMs to produce
content like video game assets, movie storyboards, and even
interactive narratives. By synthesizing text and images, LMMs help
creators rapidly prototype ideas and develop high-quality visuals for
immersive experiences.


Despite their promise, LMMs face significant challenges. One major
issue is the difficulty of achieving seamless integration between
modalities. For example, ensuring that an image accurately
represents the nuances of a textual description requires robust
alignment techniques, which are computationally intensive and prone
to error.


Another challenge lies in the ethical and societal implications of
multimodal AI. The potential for misuse, such as generating
deepfakes or misleading content, raises concerns about trust and


accountability. Moreover, biases in training data can propagate into
the models, leading to unintended consequences in their outputs.


Finally, the computational demands of training and deploying LMMs
are substantial. These models require vast amounts of data and
powerful hardware, which can limit accessibility and raise
sustainability concerns due to high energy consumption.


Let’s now look at the wider field of generative AI applications.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **1.8  Generative AI Applications**

Based on the capabilities of LLMs and LMMs, and other more
narrow models with specific focus on creation of music, voice,
videos, and much more, a huge ecosystem has developed around
generative AI.


The following section highlights the generative AI market, specifically
the different areas in which these models are used. The map clusters
the field in three main categories: systems for consumer use, for
enterprise, and for prosumer use. Let’s consider each use category:


**Consumer**
The consumer market will be most familiar to you, through
applications like chatbots, text-to-image converters, text-to-video
converters, personal assistants, and more. The dominant
business model is freemium, in which you can use the service
under defined limits, unless you become a paid subscriber.


**Enterprise (horizontal)**
Horizontal integration means that generative AI companies
provide solutions that can be used across different industries.
Think of chatbots: They are extremely versatile and can be used
in completely different industries like finance, healthcare,
education, and many other industries.


**Enterprise (vertical)**
In vertical integration, a service tries to expand its control over the
supply chain. In the context of generative AI, these services are
tailored to specific industries and have a deep integration.


**Prosumer**
Prosumer services target independent professionals, small


businesses, or power users. The primary business models are
premium subscriptions or usage-based pricing.


It is amazing to see what a vast ecosystem has evolved around
generative AI in such a short period of time.

### **1.8.1  Consumer**


For consumers, many products are available, and we can only
mention a small number:


With Suno ( _[https://suno.com/](https://suno.com/)_ ), you can create music based on a
short description.


Med-PaLM 2 ( _[https://sites.research.google/med-palm/](https://sites.research.google/med-palm/)_ ) is a model
fine-tuned for the medical domain that has reached outstanding
accuracy in the MedQA medical exam benchmark.


Services like Lensa AI ( _[https://lensa.app/](https://lensa.app/)_ ) or Remini
( _[https://remini.ai/](https://remini.ai/)_ ) can be used for photo improvements and avatar
generation.


Character.ai ( _[https://character.ai/](https://character.ai/)_ ) allows you to chat with millions
of AI characters at anytime and anywhere.

### **1.8.2  Business**


For businesses and enterprises, both horizontal and vertical AIbased systems are available. “Horizontal” means that the service is
not domain specific, while a “vertical” service is domain specific.


For horizontal services, again, we can only provide a short list of
offerings that we’ve personally tested:


Cursor ( _[https://www.cursor.com/](https://www.cursor.com/)_ ) is my favorite AI code editor. It is
integrated into a fork of Visual Studio Code (VS Code) and can
increase productivity a great deal. Similar services provide tabnine
( _[https://www.tabnine.com/](https://www.tabnine.com/)_ ) or GitHub Copilot
( _[https://github.com/features/copilot](https://github.com/features/copilot)_ ).


With Notion ( _[https://www.notion.com/](https://www.notion.com/)_ ) you can capture your
thoughts, create plans, or manage your projects. It has a
seamless integration of AI features.


Vertical enterprise services aim at improving multiple tasks within a
dedicated domain. Here are two important offerings:


In healthcare, companies like Ambience Healthcare
( _[https://www.ambiencehealthcare.com/](https://www.ambiencehealthcare.com/)_ ) claim to improve patient
care with AI.


The legal field services like Harvey ( _[https://www.harvey.ai/](https://www.harvey.ai/)_ )
provide domain-specific AI for law firms.

### **1.8.3  Prosumer**


Prosumer is an artificial word that represents the combination of
producer and consumer. Services in this area can be applied by
enterprises and consumers alike and include the following:


Most notably are search and knowledge services. Everybody
knows ChatGPT ( _[https://chatgpt.com/](https://chatgpt.com/)_ ). Alternatives are Claude
( _[https://claude.ai/](https://claude.ai/)_ ), Perplexity ( _[https://www. perplexity.ai/](https://www.perplexity.ai/)_ ), or
Google Gemini ( _[https://gemini.google.com/app](https://gemini.google.com/app)_ ).


Image creation was hyped up in 2022 when the first models
allowed users to create images from text prompts. But the quality
has improved even further, and we personally would consider
these algorithms to have reached the plateau of productivity.


We’ve had good experiences with Leonardo.ai
( _[https://leonardo.ai/](https://leonardo.ai/)_ ) and fal ( _[https://fal.ai/](https://fal.ai/)_ ).


Impressive improvements can be observed in video creation or
editing services. Runway ( _[https://runwayml.com/](https://runwayml.com/)_ ) and Kling AI
( _[https://klingai.com/](https://klingai.com/)_ ) allow you to create impressive AI-generated
videos.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **1.9  Summary**

This chapter provided a comprehensive overview of generative AI, a
transformative branch of artificial intelligence centered on the
creation of new and innovative content.


In Section 1.1, we discussed the evolution of artificial intelligence,
from its first steps nearly a hundred years ago, to the LLMs and
LMMs of today. You also learned that every technology goes through
a hype cycle, and we discussed the cycle for generative AI. We
briefly examined the capabilities of various AI systems compared to
human-level capabilities.


In Section 1.2, we studied the pillars of the evolution of generative
AI. Specifically, we saw the exponential growth in computational
power, models and data size, investments, and algorithmic
improvements. Section 1.3 covered the underlying foundation of
generative AI, namely, deep learning. You saw how a model is
trained and used in deployment. Typically, a deep learning model is
developed with a narrow domain in which the model can excel. LLMs
and LMMs broaden the scope to more general capabilities. We
discussed narrow and general AI in Section 1.4.


NLP models were the main topic of Section 1.5. We started by
discussing various NLP tasks like text classification, translation, and
more. Later, we discussed different architectures, from LSTM to
transformers.


LLMs were introduced in more detail in Section 1.6. We discussed
the training process and its specific steps. We then looked at several
use cases of LLMs, such as creative writing, summarization,
translation, or content creation. Despite their incredible capabilities,


we also discussed some limitations, like hallucinations, biases, and
context window limitations.


Expanding our scope from single-modality models like LLMs, which
can only consume and return text, we entered the field of LMMs in
Section 1.7. These models can understand multiple types of data,
such as text, images, audio, and even video. We discussed their
applications, and their challenges.


Finally, in Section 1.8, we covered some generative AI applications.
We started with a generative AI market map that classifies different
services into consumer, enterprise, and prosumer services, and we
provided some examples in each segment.


Through this structured progression, we’ve set the stage for a
deeper exploration of generative AI and its transformative impact
across diverse fields.


In the next chapter, we’ll discuss pretrained models. These narrow AI
models excel in a specific domain. The chapter will discuss the most
popular framework Hugging Face, which allows you to easily
integrate such pretrained networks into your workflow.


_[OceanofPDF.com](https://oceanofpdf.com/)_


# 2  Pretrained Models

_The more complex the mind, the greater the need for the_
_simplicity of play._
_—Isaac Asimov, in “I, Robot”_


Pretrained models are AI systems that are capable of processing
large amounts of data and working on a dedicated task. Pretrained
models are not a Swiss army knife with a lot of different features, but
typically, they work well for one specific task. Then came large
language models (LLMs). At that time, there were individual models
for each task. In the field of natural language processing (NLP), a
task might be text classification, question answering, zero-shot
classification, translation, summarization, feature extraction, text
generation, fill-mask, or sentence similarity. The list is not
exhaustive, and more tasks will be possible over time.


In Chapter 3, we’ll work mostly with LLMs. Given their extraordinary
capabilities, why should we start with the rather classic machine
learning (ML) models. Figure 2.1 shows a comparison of the training
processes for classic ML models and LLMs.


**Figure 2.1** Classic ML Models versus LLM Training


In classic ML models, for each task, a dedicated model is created.
Usually, supervised learning is applied, which is based on a labeled
dataset with inputs and corresponding target information. For
example, a text translation model is created based on words or
sentences in a source language (labeled input), and words or
sentences in a target language. This approach works quite well. As a
result, you get a model dedicated to a specific task. One advantage
is that the model is perfectly adapted to its needs; another, that it is
rather small. In most cases, you can run it on your local computer. In
this chapter, you’ll discover many of these models.


In contrast, LLMs are developed in a different way. The input is
typically unlabeled, meaning that the data might come from several
different sources. It might even be multimodal and represent text
data as well as images or video data. Few specialized models are
trained, but instead, we are operating one “large” language model.
The advantage is that the capabilities of these models consist of the
aggregation of all small models.


The disadvantage of LLMs is that, compared to a dedicated small
pretrained model, the inference of an LLM might be quite costly, with
longer inference times making it unsuitable for real-time applications.
Also, some applications might require the operation of a model
locally bound to the systems of your company, for instance, for data
protection reasons. But given the size of today’s LLMs these
requirements might be hard to impossible to implement.


Consequently, a beneficial approach is to run a simple model if the
task is simple, using an LLM only when the task requires it.


In this chapter, we’ll explore what pretrained models are, where you
can find them, and how you can use them for your needs. In
Section 2.1 we’ll take you to Hugging Face, a platform for ML
models, datasets, and much more. You’ll learn how to work with the


platform and how to find suitable models for given tasks. That
knowledge is practically applied in Section 2.2 on a specific task,
summarizing a longer text with a model from Hugging Face.


After you’ve seen how to implement a task, it’s your turn, and you
can apply the information in Section 2.3 on a given task. In
subsequent sections, we explore several tasks together, and you’ll
learn in which situations a task can help you. In Section 2.4, you’ll
encounter zero-shot classification. Then, we implement fill-mask
tasks in Section 2.5, question answering in Section 2.6, named entity
recognition (NER) in Section 2.7, and text-to-image conversion in
Section 2.8.


In the text-to-audio conversion exercise in Section 2.9, you’ll create
music based on a prompt. Finally, in a capstone project on the
analysis of customer feedback, in Section 2.10 you’ll integrate
several different models to solve a more complex task. In each of
these steps, you’ll encounter a platform that reshaped the world of
ML and simplifies development through the sharing of models and
datasets—Hugging Face.

## **2.1  Hugging Face**


The pretrained models in our scope are language models trained for
a specific task. They are good at their job, but expert only in a very
narrow scope. Given a prepared dataset, you can train such a model
from scratch or fine-tune an existing model to be more suitable for
working with your data.


But in many cases, you can use such models out of the box. One
platform is synonymous with pretrained, specialized models.
Hugging Face is an AI company and open-source platform that


focuses on building and providing tools for NLP, computer vision,
and many other ML tasks. Figure 2.2 shows the Hugging Face
homepage, available at _[https://huggingface.co](https://huggingface.co/)_ .


**Figure 2.2** Hugging Face Home Page


At Hugging Face, you’ll find more than one million models (at the
time of writing). In a production environment, you’ll simply want a
sufficient model for a given task. Applying an LLM for a comparably
simple task is not necessary, and this approach increases costs and
possibly latency.


Thus, in the following section, you’ll become familiar with Hugging
Face and select narrow AI models for specific tasks. However, you
must first understand how to select the right model out of a million
options. Figure 2.3 shows the model selection process in Hugging
Face ( _[https://huggingface.co/models](https://huggingface.co/models)_ ) where you first select the
task 1 and then select a model 2.


First, identify the task you’re working on and select it. This step
basically works as a filter, and you’ll now see only the models in this
category. Then, filter by name. For example, if you’re looking for a
**Translation** model, you might enter the source or target language in
the text field to further filter the results. You can also sort the results


based on different criteria like trending, most likes, or most
downloaded.


**Figure 2.3** Hugging Face Model Selection Process


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **2.2  Coding: Text Summarization**

In this example, we’ll load an Arxiv article and summarize it. _Arxiv_ is
an open-access archive for more than 2 million scholarly articles
from different fields like physics, mathematics, or computer science.
The articles are typically available as PDF files. Luckily, the
LangChain community has developed a loader for this type of article
that we can use. We’ll load an article on the topic “prompt
engineering” and subsequently run it through a summarizer model
that loaded from Hugging Face. Let’s go!


Once you have selected a model on Hugging Face by clicking on it,
you’re greeted with its _model card_ . On this card, you’ll typically find
metrics about the model’s performance (based on selected
benchmarks) as well as information on how to use the model.


shows a sample model card for a text summarization model.


On the model card, you’ll typically find how to use it in the left
column, as well as some metrics that provide information on the
model’s performance based on different benchmarks.


On the right, you’ll often find an inference section that allows you to
test the model. In this example, you might add some text to be
summarized.


In addition to the model card, under the **Files and versions** tab,
you’ll find how big the specific model is, which is often an important
indicator for the deployment of the model.


**Figure 2.4** Sample Model Card (Source: _https://huggingface.co/sshleifer/distilbart-cnn-_
_12-6_ )


Under the **Community** tab, you’ll see the history of the model and
possibly information about the model’s developers.


These models are usually based on transformer architecture. One of
the most relevant packages dealing with this architecture has the
same name: `transformers` . This package holds the `pipeline`
function, which is utility function for setting up a pipeline. Also, we’ll
load `ArxivLoader` to download and import articles directly into a
LangChain document object. You can find the code in
_02_PreTrainedNetworks\10_text_summarization.py_, which looks as
follows:

```
#%% packages
from transformers import pipeline
from langchain_community.document_loaders import ArxivLoader

```

The `pipeline` function requires a `task` and a `model` name. Both
parameters are passed, and as a result, we get an instance of a
pipeline, in our case, a `summarizer`, as follows:


```
#%% model selection
task = "summarization"
model = "sshleifer/distilbart-cnn-12-6"
summarizer = pipeline( task = task, model =model)

```

We can load one or more documents. For the purposes of
illustration, we’ll stick to just one document on the topic `"prompt`

`engineering".` The `loader` object is based on `ArxivLoader`, and its
method `load()` must be called so that the documents are imported,
as follows:

```
#%% Data Preparation
query = "prompt engineering"
loader = ArxivLoader( query =query, load_max_docs =1)
docs = loader.load()

```

You might check the `docs` object, which is a list with one `Document()` .
The document has multiple kinds of metadata, but we are only
interested the `page_content` property, which holds the article text, as
follows:

```
# %% Data Preparation
article_text = docs[0].page_content

```

At this point, you’ve extracted the text, which is stored in

`article_text` . Let’s pass this text to our `summarizer` . Notice how we
cannot pass the complete article due to limits in the model’s context
window, which we’ll discuss in detail in Chapter 3. We can limit the
text and use only its first 2,000 characters. We can also control the
output and set a minimum length and maximum length for the
summary. The result of the model run is stored in `result`, which is a
list with a dictionary. We are interested in the `summary_text` (see
Listing 2.1).

```
# %% Run the summarizer
result = summarizer(article_text[:2000], min_length =20, max_length =80,
do_sample =False)
result[0]['summary_text']

The paper investigates prompt engineering as a novel creative skill for creating AI

```

```
art with text-to-image generation. Prompt engineering is a new type of skill that is
non-intuitive and must first be acquired before it can be used.

```

**Listing 2.1** Text Summarization Run


Finally, let’s check if the output length is within the requested limits,
as follows:

```
# %% number of characters
len(result[0]['summary_text'].split(' '))

41

```

Good! We’re within our required limits of 20 and 80 characters. Now,
it’s your turn to find a model and use it in a translation task.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **2.3  Exercise: Translation**

Now that you know how to implement and use a model from Hugging
Face, time for you to get behind the wheel yourself. In this exercise,
you’ll need to understand the task, find a suitable model, and
implement it.

### **2.3.1  Task**


A typical NLP task is translation. With the knowledge from the
previous section, you can now solve this task independently. Find a
suitable model on Hugging Face to translate the following sentence
into Japanese:

```
Be the change you wish to see in the world.

```

This famous saying is attributed to Mahatma Gandhi. Try to solve it
independently and read on to see our solution.

### **2.3.2  Solution**


First, check the model’s section on Hugging Face
( _[https://huggingface.co/models](https://huggingface.co/models)_ ). Then, filter for **Translation** tasks
under the **Natural Language Processing** section. Nearly 5,000
translation models are available, so we’ll need to filter further.


If you check the naming of the models, you’ll see that most adhere to
the naming convention [source language]-[target language]. Thus,
narrow things down with “en-ja.” This step brings us to the model
**Mitsua/elan-mt-bt-en-ja** .


Its model card clearly describes how to use it, and this model follows
the same structure as in the previous section. Use `pipeline` and
pass a corresponding `task` and `model` . Then, pass the text to be
translated into the pipeline. In the result, you’ll see the translated
text.


Listing 2.2 shows our sample source code for a translation task from
English to Japanese.

```
#%% packages
from transformers import pipeline

#%% model selection
task = "translation"
model = "Mitsua/elan-mt-bt-en-ja"
translator = pipeline( task =task, model =model)

# %%
text = "Be the change you wish to see in the world."
result = translator(text)
result[0]['translation_text']

```

**Listing 2.2** Translation from English to Japanese (Source:
02_PreTrainedNetworks\20_translation.py)


We hope you succeeded and came up with the same translation,
possibly using a different model.


In the next section, we’ll move on to the next useful task: zero-shot
classification.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **2.4  Coding: Zero-Shot Classification**

Zero-shot classification is a powerful capability in modern AI systems
that allows them to categorize or classify items they’ve never been
explicitly trained on. Unlike traditional classification models that
require labeled examples for each category, zero-shot classifiers can
make educated guesses about new categories by leveraging their
understanding of natural language and the semantic relationships
between concepts.


For instance, a computer vision or multimodal model trained to
identify cats and dogs might be able to classify a zebra correctly
simply by understanding the linguistic description “black and white
striped horse-like animal,” even though it never saw zebra examples
during training. This ability comes from the model's pretrained
knowledge of language and concepts, making it extremely versatile
for real-world applications where new categories frequently emerge.


In our coding example, we’ll choose the opening lines of three
different books. These books clearly can be categorized into
romantic, fantasy, and crime novel. Our task is to find out if a zeroshot classifier can correctly categorize these books into genres
purely based on the first few sentences of the books. Let’s get
started.


We’ll use `pipeline` to import and interact with a zero-shot classifier
model. `pandas` is only used for visualization of the result. The
following script can be found at
_02_PreTrainedNetworks\50_zero_shot.py_ :

```
#%% packages
from transformers import pipeline
import pandas as pd

```

Call pipeline with the task `zero-shot-classification` and the model
selected in the following. Feel free to select a different one and
compare the results.

```
#%% Classifier
classifier = pipeline(task="zero-shot-classification", model ="facebook/bart-largemnli")

```

For the sample data, as shown in Listing 2.3, we use Jane Austen’s
_Pride and Prejudice_ as an example of a romantic novel. For a crime
novel, the classic detective is chosen—Sherlock Holmes. The
opening of Arthur Conan Doyle’s _The Return of Sherlock Holmes_
shall serve as an example of a crime novel. One of the most famous
fantasy novels is _Alice’s Adventures in Wonderland_ . Lewis Carroll’s
classic novel serves as an example of a fantasy novel.

```
# %% Data Preparation
# first example: Jane Austen: Pride and Prejudice (romantic novel)
# second example: Lewis Carroll: Alice's Adventures in Wonderland (fantasy novel)
# third example: Arthur Conan Doyle "The Return of Sherlock Holmes" (crime novel)
titles = ["Pride and Prejudice", "Alice's Adventures in Wonderland", "The Return of
Sherlock Holmes"]
documents = [
"Walt Whitman has somewhere a fine and just distinction between “loving by
allowance” and “loving with personal love.” This distinction applies to books as
well as to men and women; and in the case of the not very numerous authors who are
the objects of the personal affection, it brings a curious consequence with it.
There is much more difference as to their best work than in the case of those others
who are loved “by allowance” by convention, and because it is felt to be the right
and proper thing to love them. And in the sect—fairly large and yet unusually choice
—of Austenians or Janites, there would probably be found partisans of the claim to
primacy of almost every one of the novels. To some the delightful freshness and
humour of Northanger Abbey, its completeness, finish, and entrain, obscure the
undoubted critical facts that its scale is small, and its scheme, after all, that of
burlesque or parody, a kind in which the first rank is reached with difficulty.",
"Alice was beginning to get very tired of sitting by her sister on the bank, and
of having nothing to do: once or twice she had peeped into the book her sister was
reading, but it had no pictures or conversations in it, and what is the use of a
book, thought Alice “without pictures or conversations?  So she was considering in
her own mind (as well as she could, for the hot day made her feel very sleepy and
stupid), whether the pleasure of making a daisy-chain would be worth the trouble of
getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran
close by her.",
"It was in the spring of the year 1894 that all London was interested, and the
fashionable world dismayed, by the murder of the Honourable Ronald Adair under most
unusual and inexplicable circumstances. The public has already learned those

```

```
particulars of the crime which came out in the police investigation, but a good deal
was suppressed upon that occasion, since the case for the prosecution was so
overwhelmingly strong that it was not necessary to bring forward all the facts. Only
now, at the end of nearly ten years, am I allowed to supply those missing links
which make up the whole of that remarkable chain. The crime was of interest in
itself, but that interest was as nothing to me compared to the inconceivable sequel,
which afforded me the greatest shock and surprise of any event in my adventurous
life. Even now, after this long interval, I find myself thrilling as I think of it,
and feeling once more that sudden flood of joy, amazement, and incredulity which
utterly submerged my mind. Let me say to that public, which has shown some interest
in those glimpses which I have occasionally given them of the thoughts and actions
of a very remarkable man, that they are not to blame me if I have not shared my
knowledge with them, for I should have considered it my first duty to do so, had I
not been barred by a positive prohibition from his own lips, which was only
withdrawn upon the third of last month."
]

```

**Listing 2.3** Zero-Shot Classification: Text Samples for Crime, Fantasy, and Romantic
Novels (Source: 02_PreTrainedNetworks\50_zero_shot.py)


The idea of zero-shot classification is to provide some candidate
labels and let the model decide the probability of each book’s sample
text belonging to each of the candidates.


We run the model by running our object `classifier` and passing the

`documents` and the `candidate_labels` . The result is stored in the
object `res`, as follows:

```
candidate_labels=["romance", "fantasy", "crime"]
#%% classify documents
res = classifier(documents, candidate_labels = candidate_labels)

```

The result will be visualized with pandas as a bar plot for the opening
lines of Sherlock Holmes, as shown in Figure 2.5, with the following
code:


```
#%% visualize results
pos = 2
pd.DataFrame(res[pos]).plot.bar( x ='labels', y ='scores', title =titles[pos])

```

**Figure 2.5** Zero-Shot Classification Result for Sherlock Holmes


The classifier correctly assigned the label “crime” to the text snippet,
with a very high probability. This correct classification is not as
obvious as you might think. We don’t pass the complete book, which
is clearly a crime novel, only a small fragment.


In our next task, we’ll fill in empty spots in a sentence. This task is
comparable to auto-completion in which the next word in a sequence
is proposed. This technique is called a fill-mask task.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **2.5  Coding: Fill-Mask**

A fill-mask task is a type of masked language modeling in NLP,
where a model predicts a missing word or token in a given sentence.
This task is often used to understand context and word relationships
by filling in a blank (or “mask”) in a sentence.


For instance, in the sentence “AI is transforming the [MASK]
industry,” a fill-mask model might predict words like “technology,”
“healthcare,” or “finance,” based on the context.


BERT (bidirectional encoder representations from transformers) and
similar models are commonly used for this task, as they are
pretrained on masked language modeling objectives, allowing them
to predict missing words with a deep understanding of sentence
structure and context.


The implementation is extremely simple. You can find the example at
_02_PreTrainedNetworks\80_fill_mask.py_ . All you need is one
package and its `pipeline` function, as follows:

```
#%% packages
from transformers import pipeline

```

First, define the task `fill-mask` and choose the model `bert-base-`

`uncased`, as shown in Listing 2.4. After you create a model instance,
you can pass a query to it. The query must have `[MASK]` in it, which is
the place where the blank needs to be filled.

```
unmasker = pipeline(task='fill-mask', model='bert-base-uncased')
unmasker("I am a [MASK] model.")

[{'score': 0.26198092103004456,
'token': 2535,
'token_str': 'role',
'sequence': 'i am a role model.'},
{'score': 0.1216965764760971,

```

```
'token': 4827,
'token_str': 'fashion',
'sequence': 'i am a fashion model.'},
{'score': 0.03554196283221245,
'token': 2944,
'token_str': 'model',
'sequence': 'i am a model model.'},
{'score': 0.033298179507255554,
'token': 3565,
'token_str': 'super',
'sequence': 'i am a super model.'},
{'score': 0.033055439591407776,
'token': 2449,
'token_str': 'business',
'sequence': 'i am a business model.'}]

```

**Listing 2.4** Fill-Mask Inference


The model chooses reasonable words by assuming we are
interested in a role model, fashion model, or supermodel.


With LLMs, as you’ll see later, the next words are predicted in a
similar way. LLMs are often used for answering questions. In the
next section, we visit a task that works similarly—question
answering.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **2.6  Coding: Question Answering**

Question answering models are tailored to address specific, welldefined tasks. These question answering models allow users to
apply models that can accurately interpret and answer questions
within a focused domain. Unlike LLMs, which attempt to answer
questions across a wide range of topics, narrow AI question
answering models excel at providing high-precision answers in
specialized areas—such as customer support, technical
troubleshooting, medical diagnosis, and legal research.


Question answering is essential because it enables efficient
information retrieval, transforming unstructured text data into
actionable insights.


For instance, in customer service, question answering models can
answer common queries automatically, reducing the need for human
intervention and improving response times. In sectors like healthcare
or finance, narrow question answering models help professionals
quickly access relevant information, allowing them to make informed
decisions without extensive manual searching.


By optimizing access to knowledge within specific fields, question
answering models in narrow AI enhance productivity, support datadriven decision-making, and contribute to a more streamlined and
responsive user experience.


Let’s look at some examples. You can find the following code at
_02_PreTrainedNetworks\70_qa.py_ :

```
#%% packages
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
from pprint import pprint

```

You can use the model `deepset/roberta-base-squad2` . This model is
based on SQuAD 2.0 (Stanford Question Answering Dataset 2.0),
designed to challenge question answering models by introducing
unanswerable questions. The dataset contains over 150,000
questions. Each question is paired with a context paragraph, usually
drawn from a Wikipedia article. In many cases, the context includes
the answer to the question, but in other cases, it does not. Here’s our
code:

```
#%% constants
MODEL = "deepset/roberta-base-squad2"

```

The model relies solely on the context provided to find an answer
and answer questions by locating information within a specific
context. The model does not have external knowledge. It can only
see and analyze the context provided to it.


Thus, you’ll need to pass the input in JavaScript Object Notation
(JSON) with the keys `question` and `context` . The answer will be
based on the context. Listing 2.5 shows the model setup.

```
# Get predictions
nlp = pipeline( task ='question-answering', model =MODEL, tokenizer =MODEL)
QA_input = {
'question': 'What are the benefits of remote work?',
'context': 'Remote work allows employees to work from anywhere, providing
flexibility and a better work-life balance. It reduces commuting time, lowers
operational costs for companies, and can increase productivity for self-motivated
workers.'
}

```

**Listing 2.5** Fill-Mask: Model Setup (Source: 02_PreTrainedNetworks\70_qa.py)


Now, run the model and check the answer, as shown in Listing 2.6.

```
res = nlp(QA_input)
pprint(res)

{'answer': 'flexibility and a better work-life balance',
'end': 104,

```

```
'score': 0.6486219763755798,
'start': 62}

```

**Listing 2.6** Fill-Mask: inference (Source: 02_PreTrainedNetworks\70_qa.py)


In our next task, you’ll learn how to detect and extract entities from
sentences.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **2.7  Coding: Named Entity Recognition**

_Named entity recognition (NER)_ is an NLP technique that identifies
and categorizes specific elements in text, such as names of people,
organizations, locations, dates, and quantities. By recognizing these
entities, NER helps transform unstructured text into structured data,
enabling more efficient data analysis and search functionalities.
These capabilities can be helpful, for instance, when you want to
anonymize texts by removing all persons, places, and dates.


In generative artificial intelligence (generative AI), NER enhances
LLMs by enabling them to understand context around key concepts
and generate responses that are more accurate and contextually
relevant. Advanced NER models leverage deep learning to
recognize entities even in complex and nuanced contexts, improving
their utility in applications ranging from customer support to data
extraction.


Using a specific NER model, you can perform highly specialized
tasks that require accurate identification of specific entities. NER can
automatically identify and extract names, dates, places, and other
relevant entities and thus save time in manual data entry or review
processes. NER models can assist in identifying customer names,
order numbers, product mentions, and other entities in support
interactions, helping prioritize and direct queries more efficiently.


This discussion should give you some ideas about how you might
utilize NER, but now, let’s utilize it. First, select the model

`dslim/bert-base-NER` . This model allows you to detect different
entities like persons, organizations, locations, or miscellaneous
entities. The model card ( _https://huggingface.co/dslim/bert-base-_


_NER_ [) provides all necessary details on how to use the model. You](https://huggingface.co/dslim/bert-base-NER)
can find the script at _02_PreTrained Networks\60_ner.py_ .


First, load the required packages. By now, you’re familiar with

`pipeline`, but in this case, you also need to load

`AutoModelForTokenClassification` and the tokenizer with

`AutoTokenizer`, as follows:

```
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from pprint import pprint

```

We’ll load the `tokenizer` and `model` in the following code. Use the

`from_pretrained` method and pass the model’s name to

`AutoTokenizer` and `AutoModelForTokenClassification` . You’ll learn
more about tokenization in Chapter 3.

```
#%% model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")

```

Now, you can set up `pipeline` and pass the `task`, the `model`, and the

`tokenizer` during instantiation of our object `nlp`, as follows:

```
#%% pipeline
nlp = pipeline(task="ner", model=model, tokenizer=tokenizer)

```

Great! You’ve created all the objects for running the model. Let’s
work on a single sentence and try to detect the different entities, as
shown in Listing 2.7.

```
example = "My name is Bert and I live in Hamburg"

ner_results = nlp(example)
pprint(ner_results)

[{'end': 15,
'entity': 'B-PER',
'index': 4,
'score': 0.9952625,
'start': 11,
'word': 'Bert'},
{'end': 34,

```

```
'entity': 'B-LOC',
'index': 9,
'score': 0.9977075,
'start': 27,
'word': 'Hamburg'}]

```

**Listing 2.7** Named Entity Recognition: Inference (Source:
02_PreTrainedNetworks\60_ner.py)


The model successfully detected the name “Bert” as a person (BPER) and the city where he lives as the location (B-LOC). You can
find the description of the different entity names in the model card.


A popular class of pretrained models deals with the creation of
images based on text prompts. A whole ecosystem on text-to-image
models and providers has evolved. In the next section, you’ll learn
how to use such models locally.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **2.8  Coding: Text-to-Image**

You can select from a wide range of text-to-image models, but keep
in mind that these are quite resource intensive. If you don’t own a
good GPU, we recommend using a rather small text-to-image model.
For that reason, we recommend using `amused/amused-256`, available
at _[https://huggingface.co/amused/amused-256](https://huggingface.co/amused/amused-256)_ .


The following code creates an image of 256 × 256 pixels. Running
on a CPU, the creation process took half an hour. The model creates
an image of a dog and stores that image in the current working
folder. Listing 2.8 shows the code required to use this text-to-image
model. Figure 2.6 shows the result.

```
import torch
from diffusers import AmusedPipeline
#%%
pipe = AmusedPipeline.from_pretrained(
"amused/amused-256", variant ="fp16", torch_dtype =torch.float16
)
pipe.vqvae.to(torch.float32) # vqvae is producing nans in fp16
#%%
# pipe = pipe.to("cuda")

prompt = "dog"

```

```
image = pipe(prompt, generator =torch.Generator().manual_seed(8)).images[0]
image.save('text2image_256.png')

```

**Listing 2.8** Text-to-Image Code (Source: 02_PreTrainedNetworks\30_text_to_image.py)


**Figure 2.6** Sample Output from the Text2Image Model


Notice we’ve used a new package called `diffusers`, which is built
around _stable diffusion models_ . This model family can create images
based on text prompts. The `pipe` is provided with the user `prompt` and
returns an image, that we save with `image.save`, as shown in
Figure 2.6. Most of the code is directly taken from the model card
because the developers make our lives easier by showing us how to
use their developments.


Admittedly, the output is not the best image, and the algorithm
struggled to get the right eye correct. But otherwise, it looks quite
decently like a dog.


Now again, it’s time for you to shine and get some practice. You’ll
create some music in the next exercise.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **2.9  Exercise: Text-to-Audio**

Generating audio like voices or music is quite impressive. With a text
description of a music track, you can create it easily. You can rely on
an online service like _[https://suno.com/](https://suno.com/)_, but in this section, we want
to run a model locally on our systems.

### **2.9.1  Task**


In this exercise, find and select a model to create a music track and
then run that model locally. If you don’t own a powerful GPU, we
advise searching for a model with “small” in its name. Try to solve
this problem independently before checking out our solution.

### **2.9.2  Solution**


For our solution, we’ll use a model from Facebook called

```
facebook/musicgen-small
```

( _[https://huggingface.co/facebook/musicgen-small](https://huggingface.co/facebook/musicgen-small)_ ).


You can find the code at
_02_PreTrainedNetworks\40_text_to_audio.py_ . It reflects the model
card description. In this case, you’ll create a `pipeline` instance. By
running this instance based on a text prompt, you’ll get some music,
which finally needs to be converted into a WAV file using `scipy` .
Listing 2.9 shows the code for creating some music based on a textto-audio model.

```
#%% packages
from transformers import pipeline
import scipy

```

```
#%% model selection
task = "text-to-audio"
model = "facebook/musicgen-small"

# %%
synthesiser = pipeline(task, model)

music = synthesiser("lo-fi music with a soothing melody", forward_params=
{"do_sample": True})

scipy.io.wavfile.write("musicgen_out.wav", rate=music["sampling_rate"],
data=music["audio"])

```

**Listing 2.9** Text-to-Audio Source Code (Source:
02_PreTrainedNetworks\40_text_to_audio.py)


This task follows the already known pattern of `pipeline` in
combination with a `task` and a `model` . The remaining pieces are to
call the `synthesizer` object with a `prompt` that describes the music
and then to save the music with `scipy` as a WAV file.


As a result, you’ll find the WAV file in your working folder. Listen to it,
but we must say, we think it worked well. But you need to be patient:
Creating music might take a few minutes.


We’ve come close to the end of this chapter, and you’re now
equipped with the knowledge to tackle a larger task in a capstone
project.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **2.10  Capstone Project: Customer Feedback** **Analysis**

In this capstone project, you’ll solve a task independently using
multiple different pretrained models.


Create a system that analyzes customer feedback in the form of
product reviews. The system should understand a customer’s
sentiment and categorize the feedback into different categories like
“defect,” “delivery,” or “interface.”


Consider that the customer reviews can be multilingual. The output
should be a dictionary with the feedback and their corresponding
sentiment, and categories. You can find the starting code at
_02_PreTrainedNetworks\90_capstone_start.py._


Your tasks are as follows:


Import necessary packages


Search for a sentiment analysis model that returns star-ratings for
multiple languages


Implement the sentiment analysis model


Search for a zero-shot classification model


Implement the sentiment analysis model


Bundle the logic in a function


Test the function with the given `feedback` object


The result should be a dictionary with each feedback, its
sentiment, and the most likely category it belongs to


Figure 2.7 shows the workflow of the code. The input will be passed
to the two different models, and the outputs will be combined with
the feedback. In a real-life scenario, subsequent pipelines might be
triggered. On the right, you’ll see some example input and output
texts.


**Figure 2.7** Capstone Project Workflow


The starter script is shown in Listing 2.11. You can find it under
_02_PreTrainedNetworks\90_capstone_start.py_ . Fill in the gaps with
your own code. Good luck and have fun!

```
#%% packages
# TODO: import the necessary packages

#%% data
feedback = [
"I recently bought the EcoSmart Kettle, and while I love its design, the heating
element broke after just two weeks. Customer service was friendly, but I had to wait
over a week for a response. It's frustrating, especially given the high price I
paid.",
"Die Lieferung war super schnell, und die Verpackung war großartig! Die Galaxy
Wireless Headphones kamen in perfektem Zustand an. Ich benutze sie jetzt seit einer
Woche, und die Klangqualität ist erstaunlich. Vielen Dank für ein tolles
Einkaufserlebnis!",
"Je ne suis pas satisfait de la dernière mise à jour de l'application EasyHome.
L'interface est devenue encombrée et le chargement des pages prend plus de temps.
J'utilise cette application quotidiennement et cela affecte ma productivité.
J'espère que ces problèmes seront bientôt résolus."
]

# %% function
# TODO: define the function process_feedback

```

```
#%% Test
# TODO: test the function process_feedback

```

**Listing 2.10** Capstone Project Starter Script (Source:
02_PreTrainedNetworks\90_capstone_start.py)


How did it work out? Could you find models for these tasks? Was it
difficult to implement it?


For comparison, let’s look at our solution, which can also be found at
_02_PreTrainedNetworks\91_capstone_end.py_ .


For the zero-shot model, we selected `facebook/bart-large-mnli`, and
for the sentiment analysis, `nlptown/bert-base-multilingual-`

`uncased-sentiment`, as shown in Listing 2.11. Choosing another
model is completely fine!

```
#%% packages
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
import pandas as pd
from typing import List

#%% data
feedback = [
"I recently bought the EcoSmart Kettle, and while I love its design, the heating
element broke after just two weeks. Customer service was friendly, but I had to wait
over a week for a response. It's frustrating, especially given the high price I
paid.",
"Die Lieferung war super schnell, und die Verpackung war großartig! Die Galaxy
Wireless Headphones kamen in perfektem Zustand an. Ich benutze sie jetzt seit einer
Woche, und die Klangqualität ist erstaunlich. Vielen Dank für ein tolles
Einkaufserlebnis!",
"Je ne suis pas satisfait de la dernière mise à jour de l'application EasyHome.
L'interface est devenue encombrée et le chargement des pages prend plus de temps.
J'utilise cette application quotidiennement et cela affecte ma productivité.
J'espère que ces problèmes seront bientôt résolus."
]

# %% Function
def process_feedback(feedback: List[str]) -> dict[str, List[str]]:
"""
Process the feedback and return a DataFrame with the sentiment and the most likely
label.
Input:
feedback: List[str]
Output:
pd.DataFrame

```

```
"""
CANDIDATES = ['defect', 'delivery', 'interface']
ZERO_SHOT_MODEL = "facebook/bart-large-mnli"
SENTIMENT_MODEL = "nlptown/bert-base-multilingual-uncased-sentiment"
# initialize the classifiers
zero_shot_classifier = pipeline(task="zero-shot-classification",
model=ZERO_SHOT_MODEL)
sentiment_classifier = pipeline(task="text-classification",
model=SENTIMENT_MODEL)

zero_shot_res = zero_shot_classifier(feedback,
candidate_labels = CANDIDATES)
sentiment_res = sentiment_classifier(feedback)
sentiment_labels = [res['label'] for res in sentiment_res]
most_likely_labels = [res['labels'][0] for res in zero_shot_res]
res = {'feedback': feedback,
'sentiment': sentiment_labels,
'label': most_likely_labels}
return res

#%% Test
process_feedback(feedback)

{'feedback': ["I recently bought the EcoSmart Kettle, and while I love its design,
the heating element broke after just two weeks. Customer service was friendly, but I
had to wait over a week for a response. It's frustrating, especially given the high
price I paid.",
'Die Lieferung war super schnell, und die Verpackung war großartig! Die Galaxy
Wireless Headphones kamen in perfektem Zustand an. Ich benutze sie jetzt seit einer
Woche, und die Klangqualität ist erstaunlich. Vielen Dank für ein tolles
Einkaufserlebnis!',
"Je ne suis pas satisfait de la dernière mise à jour de l'application EasyHome.
L'interface est devenue encombrée et le chargement des pages prend plus de temps.
J'utilise cette application quotidiennement et cela affecte ma productivité.
J'espère que ces problèmes seront bientôt résolus."],
'sentiment': ['2 stars', '5 stars', '2 stars'],
'label': ['defect', 'delivery', 'interface']}

```

**Listing 2.11** Capstone Project Completed Script (Source:
02_PreTrainedNetworks\91_capstone_end.py)


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **2.11  Summary**

In this chapter, you learned all about pretrained models, which are
specialized, task-specific models.


This chapter began by looking back to a time before LLMs, when
smaller models were developed for individual tasks using supervised
learning techniques. These models excelled at specific tasks, were
compact, and could often be run locally. In contrast, as you
discovered, LLMs are built to handle a wide range of tasks using
extensive, often unstructured data from various sources. While LLMs
offer versatility, they come with higher costs and greater latency,
making them less ideal for certain applications. We explored why it’s
essential to choose between smaller, specific models and LLMs
depending on your requirements and the resources available.


In this chapter, we introduced you to Hugging Face, a popular
platform hosting over a million models tailored to specific ML tasks.
You learned how to navigate the platform’s model selection tools to
find models suited to your needs, ensuring efficiency without
incurring unnecessary costs.


Through several practical coding examples, you worked on tasks for
text summarization, translation, zero-shot classification, fill-mask
tasks, question answering, and NER using Hugging Face’s model
selection and pipeline features.


We explored how to load and summarize an article from Arxiv,
handling limitations like model context window size. For translation,
you followed a process to convert a well-known English phrase into
Japanese, using tools to filter models based on language
requirements.


This chapter also included a text-to-image example, where you
observed the computational demands of these models, and we
urged you to consider using smaller models if resources are limited.
Additionally, a text-to-audio exercise encouraged you to try
generating audio, with guidance on selecting an appropriate model
and converting the output into a WAV file.


By the end of this chapter, you now know how to select and use
pretrained models. You learned to balance model choice, task
suitability, and resource efficiency.


With this knowledge, you’re now prepared to move on into more
advanced discussions on LLMs and their applications.


_[OceanofPDF.com](https://oceanofpdf.com/)_


# 3  Large Language Models

_The question of whether a computer can think is no more_
_interesting than the question of whether a submarine can_
_swim._
_—Edsger W. Dijkstra_


Dijkstra, one of the most influential computer scientists in the 20th
century, was not a fan of anthropomorphizing computers. At the time
of his quote, at the end of the 1970s or early 1980s, computers were
not even remotely as capable as today’s computers. Today, we
witness the emergence of systems with human (and increasingly
superhuman) capabilities. Still, large language models (LLMs) don’t
think in the way we humans do, but they exhibit capabilities that
often make them seem as if they do.


In this chapter, we make ourselves familiar with LLMs, which are the
most prominent members of the generative artificial intelligence
(generative AI) family.


We start with a brief history of language models in Section 3.1. Then,
you’ll dive right in and learn how to use LLMs with Python in
Section 3.2. From there, we’ll expand and dive more deeply in
Section 3.3, where you’ll learn which model parameters steer a
model’s outputs.


Since an exponentially increasing number of LLMs are available,
selecting which one to use has become difficult. We deal with the
model selection in Section 3.4. When interacting with LLMs, you


must speak their language in a certain way. In other words, you must
provide information to them via messages. You’ll learn about
different types of messages and their intricacies in Section 3.5.


As a preliminary step to the concept of chains (the focus of
Section 3.7), we’ll introduce you to the concept of prompt templates,
which typically represent the first element in a chain. You’ll learn
about prompt templates in Section 3.6.


We’ll mostly work with a Python framework called LangChain that is
centered around chains, a concept that we’ll study in Section 3.7.
Chains allow you to develop highly complex systems, while keeping
the complexity manageable.


You must ensure that any LLM or complex AI system you operate is
secured against malicious actors and also provide reliable, correct,
and on-topic responses. We cover these LLM safety and security
topics in Section 3.8.


If you’re not satisfied with the responses from “your” LLM, you might
consider some improvements that we describe in Section 3.9.


The field of LLMs is new and developing at an enormous pace.
Recent trends like reasoning models, small language models
(SLMs), or test-time compute are covered in Section 3.10.


But let’s explore first how we got to where we are today by studying
the history of language models.

## **3.1  Brief History of Language Models**


The first chatbot, Eliza, was developed in the 1960s. It was quite
limited in its capabilities and used pattern recognition—basically
pretending “real” conversations. The user’s input was converted into


a question, and a rule-based system provided some generic
answers. Still, Eliza was quite successful and led to more research in
the field of natural language processing (NLP). Figure 3.1 shows a
screenshot of its user interface.


**Figure 3.1** ELIZA User Interface (Source: _https://upload.wikimedia.org/wikipedia/_
_commons/4/4e/ELIZA_conversation.jpg_ )


Decades passed, until in the 1990s, statistical models became the
norm and replaced the rule-based systems. Most notable in this
category are _N-gram models_ . These models could analyze the
likelihood of words by studying their local neighbors. In this way, they
could gain some understanding of the context surrounding a word.


With the onset of deep learning, model architectures like
convolutional neural networks (CNNs), or recurrent neural networks
(RNN) provided better results. They could “memorize” short-term
relationships within sequences of text. But they struggled to
comprehend long-term relationships.


Other models like long short-term memory (LSTM) or gated recurrent
units (GRUs) are also important milestones.


Word embeddings were developed in the 2000s to allow the
representation of a word in the form of a dense numerical vector. An
important model is Word2Vec, which was developed in 2013 by
Google. This concept of word embeddings, as well as its extension
to sentence embeddings, is the foundation of the information that
you’ll encounter throughout this book.


The 2017 paper “Attention is All You Need”
( _[https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)_ ), published by Google developers,
started a revolution. Now, LLMs, as well as many computer vision
models, are based on the groundbreaking ideas expressed in this
paper. One limitation so far was that text sequences could not be
processed in parallel. Now, parallel processing has become possible.
This paper also included the concept of attention and self-attention,
which allowed a model to focus not just on nearby words, but also
distant words. With this capability, long-range dependencies can be
captured effectively.


Now, let’s not linger too long on the past and instead turn to using
LLMs programmatically.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **3.2  Simple Use of LLMs via Python**

We’ll start and learn how to use the most popular LLM: OpenAI’s
GPT. This immensely powerful model for which you need to pay.
Since there are also extremely capable LLMs provided as opensource, we’ll show you how you can use LLMs for free via Groq.
You’ll see that the way to interact with the models is very
streamlined, thanks to the Python framework LangChain. After these
two examples you’ll be able to connect to any other LLM provider.

### **3.2.1  Coding: Using OpenAI**


To use OpenAI you need to have an application programming
interface (API) key. These models are not free, so you’ll be charged
for your usage. Prices are dropping permanently over time, and you
can check the current pricing via _[https://openai.com/api/pricing/](https://openai.com/api/pricing/)_ .


First, you must set up an API key. To use a web service, you usually
only need a username and password to access the service. To use a
service programmatically, you require an API key, which makes an
API key something like a combination of username and password.


If you don’t have one yet, get an API key by following these steps:


1. Head over to _[https://platform.openai.com/](https://platform.openai.com/)_ .


2. Create an account.


3. Activate billing and load some money onto your account.


4. Navigate to API keys and create a new API key. The name you

specify in the web frontend is irrelevant, you only need the key.
Copy the key into the clipboard.


5. Paste this key into a file called the _.env_ file. The key should look

like `sk-proj` ...


A best practice is to separate the code from the credentials. Thus,
store the API key in a separate file. A common approach is to store
this information in a file called _.env_ and place it in the working folder.
In that file, you could store the API key and possibly many more keys
if needed. Listing 3.1 shows what an environment file should look
like.

```
OPENAI_API_KEY = sk-proj...

```

**Listing 3.1** Sample .env File Content


API keys are treated as _environment variables_, which are typically
variables that are used by your operating system. Our variable has
the name `OPENAI_API_KEY` and its value must be defined to the right
of the equal sign. Make sure you use the same key name in the
coding script.


If you hesitate to provide your banking details, skip this section and
move to Section 3.2.2 to work directly with Groq, which provides
access to models for free. Don’t confuse Groq with Grok. Groq is an
AI startup focusing on creating chips for fast inference with LLMs,
while Grok is an LLM launched as an initiative by Elon Musk.


Let’s now start coding. You can find it in the material folder under
_03_LLMs/10_model_chat.py_ . A best practice is to place all the
required packages and functions at the beginning of the file. Let’s go
through what we need next.


The `os` package is required for fetching and loading the environment
variables. All major model providers offer packages for integration
into LangChain. Thus, as shown in Listing 3.2, use

`langchain_openai` . The package `dotenv` is required for working with


the environment variables file. Its function `load_dotenv()` loads the
content of the _.env_ file and provides the content as environment
variables.

```
#%% packages
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv('.env')

```

**Listing 3.2** Using OpenAI: Required Packages (Source: 03_LLMs/10_model_chat.py)


Check that the API key is available by running

`os.getenv('OPENAI_API_KEY')` . As a result, you should see the API
key printed on the screen.


Now we create an instance of the model we’ll use by using

`ChatOpenAI` class. This requires a model name. We choose GPT 4o
Mini here. Another important parameter is the temperature. This
parameter controls the creativity of the model. And you need to pass
the API key to authenticate and enabling OpenAI to charge you
based on your usage.

```
MODEL_NAME = 'gpt-4o-mini'
model = ChatOpenAI( model_name =MODEL_NAME,
           temperature =0.5, # controls creativity
           api_key =os.getenv('OPENAI_API_KEY'))

```

The `model` object’s `invoke()` method is particularly important, as
shown in Listing 3.3. This method allows you to run the model based
on specified parameters. In our first example, we asked the model to
provide information on “What is LangChain?” The result is stored in
an object of type `AIMessage` . You can access the information received
from the model call by looking at the output of its `dict()` method.

```
res = model.invoke("What is a LangChain?")
res.dict()
{'content': 'LangChain is ...',
'additional_kwargs': {},
'response_metadata': {'token_usage': {'completion_tokens': 312,

```

```
'prompt_tokens': 13,
'total_tokens': 325},
'model_name': 'gpt-4o-mini-2024-07-18',
'system_fingerprint': 'fp_f33667828e',
'finish_reason': 'stop',
'logprobs': None},
'type': 'ai',
'name': None,
'id': 'run-929cb722-e48e-457b-859c-754a5d272c6d-0',
'example': False,
'tool_calls': [],
'invalid_tool_calls': [],
'usage_metadata': {'input_tokens': 13,
'output_tokens': 312,
'total_tokens': 325}}

```

**Listing 3.3** Using OpenAI: Model Invocation (Source: 03_LLMs/10_model_chat.py)


Plenty of information is coming back from the model. Let’s start with
the most important part: `content` . This property holds the actual
model output prompt. Out of the other properties, we just want to
mention `response_metadata`, which holds information on token usage.
You’re charged in terms of input tokens and output tokens. In this
property, you can determine how many tokens were used in the
request.


Familiarize yourself with the different models from OpenAI’s model
family by studying the model overview at
_[https://platform.openai.com/docs/models/overview](https://platform.openai.com/docs/models/overview)_ . Some key
features include the following:


OpenAI created a model family
( _[https://platform.openai.com/docs/models](https://platform.openai.com/docs/models)_ ) consisting of several
models suitable for different tasks.


Language models like the GPT family (e.g., GPT-4o) can process
text, and some can also work with images.


Text-to-image generation: DALL-E is a model that can generate
and edit images.


Text-to-speech (TTS): Several models can convert text to natural,
spoken audio.


Speech-to-text: With Whisper, you can convert audio recordings
into text.


Text embeddings: Embeddings are numerical representations of
text. Such embeddings are the cornerstone of NLP. We’ll revisit
embeddings in detail in Chapter 5.


You’re not limited to the OpenAI model family. You can work with
many other LLMs. Next, you’ll learn how to work with open-source
LLMs that you can run for free via Groq.

### **3.2.2  Coding: Using Groq**


Groq is a company that develops AI hardware to make extremely
fast inferences. For developers, they provide access to LLMs,
especially open-source LLMs. You can use the service for free, but
you need to be authenticated via an API key. So, the first step is to
head over to _[https://console.groq.com/](https://console.groq.com/)_, set up an account, and
create an API key to use in your code.


Copy this API key and store it in a file called _.env_ inside the working
folder _03_LLM/_ . The file’s content is shown in Listing 3.4.

```
GROQ_API_KEY = gsk_...

```

**Listing 3.4** Snippet from the .env File


The script that you can find at _03_LLMs/10_model_chat_groq.py_
starts by loading relevant packages. The main package is

`langchain_groq`, which is the interface to use the models from the
Groq model family, as shown in Listing 3.5. Use the `os` and `dotenv`


packages to set up and get environment variables, which hold the
Groq API key.

```
#%% packages
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv('.env')

```

**Listing 3.5** Using Groq: Required Packages (Source: 03_LLMs/10_model_chat_groq.py)


Now, you need to select a model. Details on specific models can be
found in the overview about Groq models available at
_[https://console.groq.com/docs/models](https://console.groq.com/docs/models)_ .


In our example, we chose a model from Llama family: an opensource model, more specifically, an open-weight model. In other
words, the model is provided to the public to be used for free, but not
all details about its datasets and training processes are made
publicly available.


After deciding on a model, create an instance of `ChatGroq` class. In
this instantiation, pass the model’s name as parameter. You must
also pass the API key you created earlier. These two parameters are
mandatory. Among many other available parameters, in our
example, we’ve only set the temperature parameter, which controls
the creativity of the model. You’ll learn more about model parameters
in Section 3.3. With that step, you have everything in place to
interact with the LLM.

```
MODEL_NAME = 'llama-3.3-70b-versatile'
model = ChatGroq( model_name =MODEL_NAME,
           temperature =0.5, # controls creativity
           api_key =os.getenv('GROQ_API_KEY'))

```

Now, we can ask the model “What is Hugging Face?” via the

`invoke()` method, as follows:


```
# %% Run the model
res = model.invoke("What is a Hugging Face?")

```

With the `dict()` method, you can see an overview of the model
output, as shown in Listing 3.6.

```
# %% find out what is in the result
res.dict()

{'content': 'Hugging Face is a popular open-source library and platform for natural
language processing (NLP) and machine learning (ML) ...',
'additional_kwargs': {},
'response_metadata': {'token_usage': {'completion_tokens': 328,
'prompt_tokens': 42,
'total_tokens': 370,
'completion_time': 1.312,
'prompt_time': 0.010021397,
'queue_time': 0.004826691000000001,
'total_time': 1.3220213969999999},
'model_name': 'llama-3.1-70b-versatile',
'system_fingerprint': 'fp_b6828be2c9',
'finish_reason': 'stop',
'logprobs': None},
'type': 'ai',
'name': None,
'id': 'run-84ad52ab-f7df-4245-ab42-5281e48cac69-0',
'example': False,
'tool_calls': [],
'invalid_tool_calls': [],
'usage_metadata': {'input_tokens': 42,
'output_tokens': 328,
'total_tokens': 370}}

```

**Listing 3.6** Using Groq: Model Output (Source: 03_LLMs/10_model_chat_groq.py)


The most important output is again the content. Typically, you directly
fetch the content via its property, as shown in Listing 3.7.

```
# %% only print content
print(res.content)

Hugging Face is a popular open-source library and platform for natural language
processing (NLP) and machine learning (ML) tasks. It was founded in 2016 by Julien
Chaumond, Clement Delangue, and Thomas Wolf. Hugging Face is known for its
Transformers library, which provides pre-trained models and a simple interface for
using and fine-tuning transformer-based models for various NLP tasks, such as text

```

```
classification, language translation, question answering, and more.
…

```

**Listing 3.7** Using Groq: Model Output Content (Source:
03_LLMs/10_model_chat_groq.py)


You’ve successfully invoked a model provided by Groq. You can find
all available Groq models at _[https://console.groq.com/docs/models](https://console.groq.com/docs/models)_ .


For each model, the model ID is provided. This string must be used
in your script. Furthermore, the developer is shown as well as a
limiting factor. For LLMs, the limiting factor is the context window,
and the maximum number of tokens is shown. More on that limitation
is provided in the next info box. If you want to dive more deeply into
the model, check out the model card, and you’re forwarded to the
developer page of the model.


Some specialized models include Distil-Whisper models, which
provide a speech-to-text model. You can upload an MP3 file (up to a
certain size) and receive the corresponding spoken text in the file.


Most available models are LLMs, and generally, all are open-source
or open-weight models. Prominent models include members of the
Llama family from Meta, Gemma models from Google, or Mixtral
from Mistral.


In the model overview, you might have seen the context window as
one of the most important parameters. The context window refers to
the maximum number of input tokens that a model can process at
once. This value is important because the model’s ability to generate
relevant output depends on the information it can keep and use in a
single prompt. Each LLM has a fixed limit on how many tokens it can
handle at once in its context window.


In this context, keep in mind that an LLM breaks the input text down
into smaller units, which are called “tokens.” Such a token might be a


word, or just a part of a word, or even some punctuation.


A large context window allows the model to process more
information, which improves its ability to understand longer texts, or
“memorize” long conversations. As the context window size
increases, the computational resources required to process the text
increase. Also, the latency of the model increases—it takes more
time for the model to provide an answer.


If the context window is exceeded, the model either “forgets” older
tokens, or the LLM call fails, depending on the package
implementation.


We’ll face this problem in Chapter 5 and Chapter 6 on vector
databases and retrieval-augmented generation (RAG), respectively,
since these techniques help to establish some kind of “external
knowledge” to an LLM. These approaches offer the flexibility to feed
only relevant knowledge to the LLM, thus keeping within the
constraints of a given context window.

### **3.2.3  Coding: Large Multimodal Models**


In this book, you’ll mostly work with text inputs and outputs and use
traditional LLMs. But demand has increased for models to
understand and interact with more complex and varied forms of
information. Consequently, multimodal LLMs were developed. These
models are trained to understand and generate multiple types, or
modalities, of input and output format, typically besides text—
images, audio, and video.


Unlike traditional LLMs that operate in a single modality (text), these
multimodal models can process information across several formats.
For this capability, they combine advances in NLP with innovations in


computer vision and audio processing. As a result, these models can
perform the following tasks:


Analyze and describe images in text form


Generate images based on textual descriptions


Transcribe audio inputs


Interpret audio inputs and provide responses based on them


Let’s use some multi-modal models to learn how to work with them.
You’ll learn how to pass an image as an input to a model. Then,
you’ll interact with the LMM to determine if it understands what it
“sees” in the image.


The flowchart shown in Figure 3.2 illustrates the process of training a
deep neural network. In our example, we’ll pass an image to the
multimodal model.


**Figure 3.2** Deep Neural Network Training Process


You can find the code for this script at _03_LLMs\60_multimodal.py_ .
This code is mostly based on the documentation from Groq,
available at _[https://console.groq.com/docs/vision](https://console.groq.com/docs/vision)_ .


As shown in Listing 3.8, start by loading the required packages.

```
#%% packages
from groq import Groq

```

```
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv( usecwd =True))
import base64

```

**Listing 3.8** LMM: Required Packages (Source: 03_LLMs\60_multimodal.py)


A good practice is to define the constants at the beginning of the
script. As in the following example, define which model to choose,
where the image is located, and the user prompt:

```
#%% constants
MODEL = "llama-3.2-90b-vision-preview"
IMAGE_PATH = "sample_image.png"
USER_PROMPT = "What is shown in this image? Answer in one sentence."

```

Since we’re working with a local image that must be sent to the Groq
API, the image must be loaded and converted into a format that can
be sent as text string. For this functionality, as shown in Listing 3.9,
you can define a function called `encode_image` . This function loads
the image and directly converts it to `base64` format. Base64 is a
binary-to-text encoding scheme that converts binary data into an
ASCII string format.

```
#%% Function to encode the image
def encode_image( image_path ):
with open(image_path, "rb") as image_file:
return base64.b64encode(image_file.read()).decode('utf-8')

base64_image = encode_image(IMAGE_PATH)

```

**Listing 3.9** LMM: Encode Image Function (Source: 03_LLMs\60_multimodal.py)


Now, set up a `Groq` instance, as shown in Listing 3.10, using the
native implementation of `groq` package, so the chat request has a
different format compared to the LangChain interaction with models.
But you can recognize many pieces, for example, the messages. In
the `messages` object, you can define a user message. In that object,
we pass a dictionary with text content (the user prompt) as well as
the image content (the image we want to interact with).


```
#%% Getting the base64 string
client = Groq()

chat_completion = client.chat.completions.create(
  messages =[
{
"role": "user",
"content": [
{"type": "text", "text": USER_PROMPT},
{
"type": "image_url",
"image_url": {
"url": f "data:image/jpeg;base64,{base64_image}",
},
},
],
}
],
  model =MODEL,
)

```

**Listing 3.10** LMM: Inference (Source: 03_LLMs\60_multimodal.py)


The response is located in the object `chat_completion`, which can
print to screen, as shown in Listing 3.11.

```
#%% analyze the output
print(chat_completion.choices[0].message.content)

```

**Listing 3.11** LMM: Chat Completion (Source: 03_LLMs\60_multimodal.py)


The image illustrates a flowchart for a machine learning (ML) model,
showcasing the process of training and optimization. The model can
provide valuable answers. It understands what it sees. Try to modify
the user prompt to check whether the model can answer more
detailed questions on the image.

### **3.2.4  Coding: Running Local LLMs**


So far, you’ve run LLMs via API calls provided by software as a
service (SaaS) providers. Sometimes, you want to run a model


locally. For instance, perhaps privacy is important, and you want to
avoid transmitting confidential information over the internet.


In such cases, you can operate a model on your local computer.
Ideally you have a powerful GPU, which can run a decently sized
model. But a small model can also run on your CPU.


A powerful platform that makes this process quite simple is Ollama.
With Ollama, you can operate an LLM on your laptop or desktop
without the need for internet connectivity. It offers privacy and full
control by allowing you to interact with an LLM directly on your
hardware.


First, you need to install Ollama software on your computer by
visiting _[https://ollama.com/](https://ollama.com/)_ .


**Figure 3.3** Ollama Software Download


Download the software corresponding to your operating system.
They provide the software for macOS, Linux, and Windows. Now,
determine which model is suitable for your hardware and project
requirements. A list of available models is available at
_[https://ollama.com/library](https://ollama.com/library)_ . For this example, we’ll work with gemma2
model class, as shown in Figure 3.4.


**Figure 3.4** Ollama-Provided Model Class “gemma2”


This small, yet powerful, model provided by Google comes in three
different flavors: tiny 2b, medium 9b, and large 27b. This number
refers to the number of parameters, so the 2b refers to a model with
roughly 2 billion parameters. Click on a link for more information
(e.g., the file sizes of the models and the actual name for the model).


We’ll use the smallest model, `gemma2:2b` . This option is feasible even
for pure CPU systems.


You can download a model by pulling it via Ollama. On your terminal,
run the code shown in Listing 3.12.

```
ollama pull gemma2:2b

pulling manifest
pulling 7462734796d6... 100% ██████1.6 GB
pulling e0a42594d802... 100% ██████358 B
pulling 097a36493f71... 100% ██████8.4 KB
pulling 2490e7468436... 100% ██████65 B
pulling e18ad7af7efb... 100% ██████487 B
verifying sha256 digest

```

```
writing manifest
success

```

**Listing 3.12** Ollama: Model Download


The model was downloaded to your hard drive and is now available.
You can check it via the following command:

```
ollama list

NAME     ID       SIZE   MODIFIED
gemma2:2b  8ccf136fdd52  1.6 GB  2 hours ago

```

The last step on the operating system level is to add the Python
package `ollama` . You can add the package via one of the following
options:

```
 uv add ollama

 pip install ollama

```

This step concludes the preparation work. Now, you can interact with
the local model directly from a Python script.


In our first Python script, available at _03_LLMs\70_ollama.py_, you’ll
need to import the package first, as follows:

```
#%% packages
import ollama

```

Then, you can generate model responses by calling the method

`.generate()`, as follows:

```
response = ollama.generate( model ="gemma2:2b",
                prompt ="What is an LLM?")

```

The response has several kinds of metadata, but the most important
output is available in the JSON key `response`, as shown in
Listing 3.13.

```
from pprint import pprint
pprint(response['response'])

```

```
('LLM stands for **Large Language Model**.
"Here's a breakdown:
**What it is:**
* A type of artificial intelligence (AI) model.
…

```

**Listing 3.13** Ollama: Model Output


Amazingly, you can now completely run an LLM self-hosted without
an internet connection. But there’s more: The behavior of that
package is slightly different from the `langchain` API.


Thus, we recommend using it the `langchain` way. The LangChain
community has built a model class specifically for Ollama, so that
Ollama-hosted models provide the same outputs as other models,
and you can easily exchange an Ollama model with any other
provider.


You only need to load the corresponding package, as follows:

```
from langchain_community.llms import Ollama

```

Then, you can set up a model instance, as follows:

```
llm = Ollama( model ="gemma2:2b")

```

With this model instance ( `llm` ), you can interact exactly in the same
way as with other models—by invocation, as shown in Listing 3.14.

```
response = llm.invoke("What is an LLM?")
response

('LLM stands for **Large Language Model**.
…

```

**Listing 3.14** Ollama: Model Invocation


Isn’t that awesome? You can now use an LLM even in confidential
situations, without exposing any data over the internet.


Now, let’s step back and cover some theoretical groundwork on
steering model behavior. In the following section, you’ll learn about
the most important model parameters.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **3.3  Model Parameters**

Some particularly important parameters allow you to fine-tune the
generated model outputs. Parameters like temperature, top-p, and
top-k play a vital role; with their help, you can control the creativity,
randomness, and focus of the generated output.

### **3.3.1  Model Temperature**


With model temperature, you can control the randomness of the
model’s response. Typical values are 0 (low temperature) and 1, or
even above (high temperature). Low temperatures keep the model
focused, and you get deterministic results, meaning that you can
repeatedly get the same response. The model favors extremely likely
tokens. High temperatures, on the other hand, increase the
randomness of token selection. A broader distribution of tokens is
selected, which allows for more creative or unexpected outputs.
Temperatures usually should not exceed 1, which can lead to chaotic
and incoherent outputs. Figure 3.5 shows how the temperature
defines the model output.


For low temperatures, you get focused and deterministic answers,
while the answers get more creative and varied for higher
temperatures. Imagine you own an ice cream shop. If the (ambient)
temperature is low, fewer customers visit your shop, and a better
business decision might be to offer only the most popular flavors. But
if temperature increases, demand rises, and as a result, a better
decision would be to have more exotic flavors available.


Temperature is directly linked to the probability distribution of the
tokens. Let’s learn how temperature impacts the probability


distribution based on an artificial example. You have the prompt “Bert
likes <MASK>.,” and the model has the task to fill in the missing
word. There are an enormous number of possible words. For
simplicity, let’s just consider three words: “reading,” “walking,” and
obviously “coding.” The model has an underlying probability of these
words based on its training data. For extremely low temperatures,
the model intensifies the differences between probabilities. For very
high temperatures, these differences disappear, and all words have
the same probability.


**Figure 3.5** Temperature Output and Analogy


Figure 3.6 shows the sample probability distributions for a given user
prompt across different temperature values.


**Figure 3.6** Model Temperature and Probability Distribution


Low temperatures of, for example 0.1, are shown in the plot on the
left. The center plot shows the impact of a medium temperature on
the probability distribution, while the plot on the right represents an
extremely high temperature.


Notice how the differences are getting smaller with increasing
temperature. This behavior is what this parameter does. Now, we
study two more parameters that work alongside temperature: top-p
and top-k.

### **3.3.2  Top-p and Top-k**


Top-p (or also called “nucleus sampling”) controls the probability of
the next token by dynamically adjusting the number of possible
tokens that the model can choose from. Let’s take an example of
top-p = 0.9. In this case, the model considers a cumulative
probability of tokens (which add up to 90%) and chooses the
smallest set of tokens within the boundaries.


This approach balances deterministic and creative outputs. If you set
top-p = 1.0, there is no filtering, and all possible tokens are


considered. If you define a small value (e.g., top-p < 0.5), the model
outputs tend to be more focused and predictable as only the top
tokens are considered.


Top-k sampling controls how many of the most probable tokens are
considered when generating the next word. If a value of top-k = 1 is
chosen, only the most probable token is selected. Thus, you get a
completely deterministic result. If top-k = 50, the model samples,
from the top 50 tokens, the most probable tokens for each step. This
approach increases diversity and allows for more creative and varied
outputs. Top-k sets a fixed number of tokens to choose from,
independent from the cumulated probability represented by top-k
tokens. Figure 3.7 shows some examples of top-p and top-k
parameters.


**Figure 3.7** Top-p and Top-k Parameters


The sample user prompt is “In the evening I want to see a <MASK>,”
in which the blank (<MASK>) should be filled. Again, multiple tokens
are possible. Based on a given temperature, the probabilities of
these tokens can be calculated. The tokens are represented in a
decreasing order. All probability that sums up to be less than top-p
are considered. In that case, “movie” and “friend” end up with 80% of
probability. If the next token “doctor” would be added, the aggregated
probability would be 91% and thus above the top-p value.


Top-k is straightforward. In our example, top-k is set to 3, so that the
three most probable tokens are selected, of which the final prediction
is randomly chosen.





_[OceanofPDF.com](https://oceanofpdf.com/)_


## **3.4  Model Selection**

In the previous section, you undertook your first interactions with
different LLMs. A selection of the models was given. But you might
ask how to select the “right” model for your task. Depending on your
project, you might have hard criteria and soft criteria. To process
long input prompts, the context window (see the info box in the
previous section) is a hard factor. To interact with a model that
includes recent developments and trends, the model cutoff date
could be extremely important.


A sweet spot can be found within the boundaries of model price,
latency, and performance. Finding the right balance is important for
any generative AI application. This trade-off is highly contextual and
influenced by the specific requirements of your project and the
resources at your disposal.


The performance of a model highly impacts the model’s outputs.
Related to model performance is the price of model use. In general,
the more powerful a model is, the more expensive it is to use. If you
need a model that inherently “knows” about recent events, you must
take the knowledge cutoff date into account. Your input data might
also define the model selection since the context window might
truncate your input if it is too small. For real-time applications, you
need to ensure that the model has low latency.


Depending on the data you work with, you might want to operate the
LLM on your own resources (on-premise) rather than using a model
hosted in the cloud. Associated with the model hosting is the model
license. Open-source and open-weight models provide their model
weights so that you can download and operate it on your hardware,


which is not possible with proprietary models that are only accessible
via APIs.


Many of these parameters are interconnected, which makes model
selection quite difficult.


Let’s consider the performance of a model and take a closer look at
model selection criteria.

### **3.4.1  Performance**


You can check the performance of different models at Chatbot Arena
( _[https://lmarena.ai/?leaderboard](https://lmarena.ai/?leaderboard)_ ) and get a result, as shown in
Figure 3.8.


**Figure 3.8** Chatbot Arena Leaderboard (as of January 24, 2025; Source:
https://lmarena.ai/?leaderboard)


The models are sorted in terms of arena score. But how is this score
calculated? It is called “arena” ( _[https://lmarena.ai/](https://lmarena.ai/)_ ) for a reason. In
the arena, the user interacts with two models: model A and model B.
The user can define a prompt and gets responses from the two
models. The user must rate which one is performing better. Thus,
Chatbot Arena is a double-blind test, which is considered the gold
standard in the evaluation of test outcomes. In the screenshot, notice
that multiple models share the same rank because the 95%
confidence interval is considered the highest rank. The ranking


changes often, so your rankings will likely look different due to the
passing time.


By default, the overall ranking is shown. But you can select other
categories like **Math** or **Coding** and check those rankings. When
searching for a model for a specific task, we advise selecting the
category according to your task.


But performance is not the only relevant factor.

### **3.4.2  Knowledge Cutoff Date**


Each model has a _knowledge cutoff date_, which is the date on which
its training data was finalized. The model is subsequently trained on
that data. In the model weights, no more recent data can be
represented, which is why it is important to know the knowledge
cutoff date. If you ask a model for information like an event or any
other piece of information, the model cannot know if it happened
after the date of the knowledge cutoff.


For chatbots, this parameter is becoming less relevant because
these models are more often equipped with internet search
capabilities to retrieve up-to-date information by themselves.
However, for you as a developer of AI systems, knowledge cutoffs
might be an important factor to consider.

### **3.4.3  On-Premise versus Cloud-Based Hosting**


Another important aspect of model selection is data privacy. If you’re
dealing with confidential information, you or your customers might
not want the information to leave the company network. In that case,
you want to use a model that is hosted in the safe haven of the


internal network. But in that case you’re most likely bound to use
open-source models.

### **3.4.4  Open-Source, Open-Weight, and Proprietary** **Models**


Proprietary models are provided to users via web applications or
APIs. Famous members of this class include OpenAI or Anthropic
who both provide their models in this way.


Google is a special case since their models are either provided as
proprietary models via APIs (e.g., Gemini). But other model classes,
like Gemma, are provided as open-source models via Hugging Face.


To be completely accurate, we should differentiate “open source”
and “open weight.” Truly open-source models are provided with all
their details, such as its model architecture and training data used.
This total transparency is rare, however. A provider might release to
the public a trained model with its weights, but specific details of the
underlying data and training might still be kept secret.


A famous example of this group is Meta with its Llama model family.
These models are free to use, but the company doesn’t disclose its
training data.

### **3.4.5  Price**


The price of using an LLM service can be a significant factor in your
model selection process. Typically, proprietary models are paid on a
token basis. To be more precise, a differentiation is made between
input tokens and output tokens. Input tokens are typically cheaper
than output tokens. You can find the current prices for OpenAI


models at _[https://openai.com/api/pricing/](https://openai.com/api/pricing/)_ and for Anthropic models at
_[https://www.anthropic. com/pricing#anthropic-api](https://www.anthropic.com/pricing#anthropic-api)_ .


You should come up with some estimates on how many API requests
and how many tokens will be processed. Based on these estimates,
you can derive an estimate of your total costs.

### **3.4.6  Context Window**


Your project might include the processing of very long documents,
making it necessary to pass as much information as possible to the
model. Thus, the context window is a driving factor for the best
choice of model.


If you check, for example, the models on Groq
( _[https://console.groq.com/docs/models](https://console.groq.com/docs/models)_ ), you’ll find models with
rather small context windows like “LlaVa 1.5 7B” with a context
window of 4.096 tokens as well as “Llama 3.3 70B Versatile” with an
extremely large context window of 128.000 tokens.

### **3.4.7  Latency**


Some use cases require extremely fast model responses despite
any interdependencies that come with the hosting of a model. If
latency does not play a role, you might even run an open-source
model on a CPU. In other cases, latency might be the most relevant
factor.


For example, let’s say you want to couple an LLM with voice
generation to enable real-time chats. In such a situation, an LLM can
easily be the bottleneck and reduce the user experience because


conversation cannot be “natural” if the conversation partner requires
long response times.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **3.5  Messages**

In Section 3.2, you took your first steps in using LLMs. You invoked
the model objects, sent a simple message, and received a response.
In a more realistic chat, multiple types of messages will arise. Each
message has a specific role and content. We’ll look at the most
common message types: user, system, and assistant.

### **3.5.1  User**


This message type relates to the human message and represents
the user input. The effectiveness of an LLM response depends on
the clarity of the user message. Chapter 4 on prompt engineering
basically deals with optimizing the user message.

### **3.5.2  System**


Alongside the user input, a system message can be defined that
specifies how the model should behave and work, like in a role-play.


For example, if you want to set up a general assistant, a typical
system message might be as follows:

```
You are a helpful AI assistant designed to provide accurate,

concise, and polite responses. Always ensure that your answers are
```

`clear and informative` .


Alternatively, imagine you want your model to behave as a technical
support assistant. In this case, you might instruct the model with the
following system message:


```
You are a technical support AI assistant specializing in

troubleshooting and explaining software-related issues. Respond
with clear, step-by-step instructions, avoiding technical jargon
```

`whenever possible` .


With the system message, you can establish some initial instructions
for the model. You can define its role, its tone, and even specific
objectives before the user interaction begins. The system message
is critical for setting the model’s boundaries and expectations and
helps guide it to behave in a manner aligned with the user’s
requirements.


System messages have their limitations. While they can shape the
initial behavior, they cannot enforce strict adherence throughout the
conversation. As a result, models can drift in their tone or behavior
when prompted with unforeseen user inputs.


Additionally, system messages alone cannot enforce fine-grained
control over content accuracy or nor attend to ethical considerations
without complementary guardrails or moderation.


More on this topic is covered in Chapter 4.

### **3.5.3  Assistant**


The assistant message type corresponds to the model response.
The main property is the content, which holds the model output.


Furthermore, this message type has a `response_metadata` property.
This property holds some model-specific output, but typically the
token usage is shown as well as the duration the query took.


Now that you understand the available message types, let’s explore
how they can be used in prompts. LangChain has a flexible interface


to help you set up prompts.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **3.6  Prompt Templates**

Before we invoke the LLM and send a query, let’s set up a prompt in
a unified and structured way by using LangChain’s prompt
templates. In this way, we can guide the model in how to act. Also,
the model can, with the help of prompt templates, better understand
the user and the user’s intention. Let’s see this capability in action.

### **3.6.1  Coding: ChatPromptTemplates**


The most flexible way to implement prompt templates is to use

`ChatPromptTemplates`, which allows you to pass a list of messages.
Listing 3.15 shows some sample code for setting up a prompt
template.


Let’s start with a simple example that showcases the idea. First,
import the class `ChatPromptTemplate` . In the next step, create an
instance of this class by calling its `from_messages()` method. These
messages are a list of tuples. Each tuple has the form (“message
type,” “content”). In this way, you can define a system message that
tells the model how to behave, followed by a human message that
holds the actual user query. Important in this context is how you
define variables, which are set up as placeholders and populated in
a later step. In our example, variables are defined in the user-based
(human) messages, inside curly braces. At this point, we’ve set up

`input` and `target_language` as variables.


Although our code looks a bit like a formatted string literal (also
called Python f-string), it isn’t. In an f-string, predefined variables are
passed inside string literals using curly braces `{}` and replaced by
the string representation of the variable. In this case, we did not


predefine the variable `input` or the variable `target_language` in
advance.


In the last step, we invoke prompt template. The variables are then
replaced with actual content when we call the `invoke()` method of
the `prompt_template` object. A dictionary is passed as a parameter;
this dictionary uses keys corresponding to the variables and the
values corresponding to the content to be used instead of the
variable.


Finally, since we didn’t store the invoke prompt to a new variable, the
output is just shown in the terminal. The prompt template has been
converted to a `ChatPromptValue` object with a `SystemMessage` and

`HumanMessage` .

```
#%% packages
from langchain_core.prompts import ChatPromptTemplate

#%% set up prompt template
prompt_template = ChatPromptTemplate.from_messages([
("system", "You’re an AI assistant that translates English into another
language."),
("user", "Translate this sentence: '{input}' into {target_language}"),
])

#%% invoke prompt template
prompt_template.invoke({"input": "I love programming.", "target_language":
"German"})

ChatPromptValue(messages=[SystemMessage(content='You’re an AI assistant that
translates English into another language.'), HumanMessage(content="Translate this
sentence: 'I love programming.' into German")])

```

**Listing 3.15** Prompt Template Use (Source: 03_LLMs/30_prompt_templates.py)


What is the purpose of this approach? With the prompt template, we
have a flexible first component that could be passed to a model to
get some response. The “prompt to LLM” approach is a simple chain
of steps.


We’ll deal further with LangChain chains in Section 3.7.


But first, let’s use the wisdom of the crowd to come up with a good
prompt. LangChain has established an ecosystem that allows users
to share and explore prompts with LangChain Hub.

### **3.6.2  Coding: Improve Prompts with LangChain Hub**


You can find LangChain hub at _[https://smith.langchain.com/hub](https://smith.langchain.com/hub)_ . This
hub allows you to explore prompts created by others for many
purposes. We’ll dive more deeply into the prompt engineering
ecosystem in Chapter 4. For now, we’ll get some help to create a
prompt.


If you search for “prompt maker,” you’ll find a user-created prompt
template called “hardkothari/prompt-maker.” This prompt is created
to generate a great prompt. In our example, you’ll find out how it
works.


The code shown in Listing 3.16 corresponds to the file
_03_LLMs/31_prompt_hub.py_ . You need to load the required
packages. The newcomer is `hub` from `langchain` package.

```
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv('.env')
from pprint import pprint

```

**Listing 3.16** Prompt Hub: Required Packages (Source: 03_LLMs/31_prompt_hub.py)


To use the prompt creation, you must call the `pull` method from `hub`,
as follows:

```
#%% fetch prompt
prompt = hub.pull("hardkothari/prompt-maker")

```

Some input variables are exposed via the `input_variables` property,
as follows:

```
#%% get input variables
prompt.input_variables

['lazy_prompt', 'task']

```

Listing 3.17 shows an improved prompt. You only need to set up a
model and run it in a chain, which anticipates knowledge about
chains that we cover later in Section 3.7, so be patient. For now, just
take this step as a given.

```
# %% model
model = ChatOpenAI( model ="gpt-4o-mini",
           temperature =0)
# %% chain
chain = prompt | model | StrOutputParser()

```

**Listing 3.17** Prompt Hub: Chain Setup (Source: 03_LLMs/31_prompt_hub.py)


You can invoke the chain with the code shown in Listing 3.18 and
pass the relevant parameters (i.e., `lazy_prompt` and `task` ) to get an
improved prompt.

```
# %% invoke chain
lazy_prompt = "summer, vacation, beach"
task = "Shakespeare poem"
improved_prompt = chain.invoke({"lazy_prompt": lazy_prompt, "task": task})
print(improved_prompt)

As a skilled poet in the style of William Shakespeare, compose a sonnet that
captures the essence of summer, vacation, and the beach. ### Instructions: Your poem
should reflect the beauty and joy of a summer getaway, using rich imagery and
evocative language typical of Shakespearean verse. Aim for 14 lines, adhering to the
traditional iambic pentameter and ABABCDCDEFEFGG rhyme scheme. ### Context:
Incorporate themes of nature, leisure, and the fleeting nature of time, while
evoking a sense of nostalgia and warmth. Use metaphors and similes to enhance the
emotional depth of the poem, and consider including references to the sun, sea, and
the carefree spirit of summer. ### Desired Outcome: The final piece should resonate
with readers, transporting them to a sun-drenched beach, filled with laughter and
the gentle sound of waves, while also reflecting on the transient beauty of such
moments.

```

**Listing 3.18** Prompt Hub: Chain Invocation (Source: 03_LLMs/31_prompt_hub.py)


This improved prompt describes the role of the model in much more
detail and provides extensive instructions on the task as well as a
description of the desired outcome. Let’s run the model with the
improved prompt, as shown in Listing 3.19.

```
# %% run model with improved prompt
res = model.invoke(improved_prompt)
print(res.content)

Upon the golden sands where sunbeams play,
The azure waves do kiss the shore with glee,
In summer's arms, we cast our cares away,
As laughter dances on the breeze so free.

The sun, a sovereign in the heavens high,
Doth paint the sky with hues of rose and gold,
While seagulls wheel and cry, as if to vie
For joy that in this fleeting time we hold.

O, let us linger in this warm embrace,
Where time, like grains of sand, slips through our hands,
Each moment savored, sweet as summer's grace,
A tapestry of dreams upon the strands.

Yet, as the twilight calls the day to rest,
We cherish memories, our hearts possessed.

```

**Listing 3.19** Prompt Hub: Model Run With Improved Prompt (Source:
03_LLMs/31_prompt_hub.py)


We’ll leave it to you to run the model only based on the `lazy_prompt`
or the `task` and to compare the results.


So far, we’ve worked with a small example of how a chain combines
different building blocks. This concept is powerful due to its structure,
as we’ll explore next.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **3.7  Chains**

Chains are such an important concept that they are part of the
package named LangChain. A _chain_ refers to a sequence of process
steps that are connected to accomplishing a task. Typically, they
consist of multiple components.


We start with the smallest and simplest chain: a link between a
prompt and an LLM. Then, we’ll look at how chains can be executed
in parallel and how routes can be implemented. Finally, we equip an
LLM with memory so that it can retain information. Let’s start small,
with a simple sequential chain.

### **3.7.1  Coding: Simple Sequential Chain**


The simplest chain is a “prompt to LLM” chain, as shown in
Figure 3.9. A user input is passed to a prompt template. The prompt
template itself passes its output into an LLM step. Finally, the LLM
step creates a model output.


**Figure 3.9** Simple LangChain Chain


You’re not limited to a sequential chain. You can also craft more
complex structures like parallel running chains or router chains. We’ll
describe these structures in more detail later in this section.


Let’s set up a chain consisting of a prompt. The prompt is passed to
an LLM. After the model creates an output, the output will be passed
to a `StrOutputParser` . You can find the corresponding code at
_03_LLMs/40_simple_chain.py_ .


As shown in Listing 3.20, start by importing relevant packages and
API keys. As the LLM, we’ll use OpenAI. The API key is loaded via

`dotenv` . Make sure that the _.env_ file is stored in the working folder,
which has an entry for `OPENAI_API_KEY` .

```
#%% packages
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
load_dotenv('.env')

```

**Listing 3.20** Sequential Chain: Required Packages (Source:
03_LLMs/40_simple_chain.py)


Now, Listing 3.21 extends on the prompt template from Section 3.6
creating a `ChatPromptTemplate` based on a system and user
message. The task is to translate an `input` text into a

`target_language` .

```
#%% set up prompt template
prompt_template = ChatPromptTemplate.from_messages([
("system", "You’re an AI assistant that translates English into another
language."),
("user", "Translate this sentence: '{input}' into {target_language}"),
])

```

**Listing 3.21** Sequential Chain: Required Packages (Source:
03_LLMs/40_simple_chain.py)


The next component to apply is an LLM. We’ll use `GPT-4o-mini`, as
follows:

```
# %% model
model = ChatOpenAI( model ="gpt-4o-mini", temperature =0)

```

Stacking the chain together cannot be simpler. Simply apply the pipe
operator `|` . Components are separated by `|` . In our example, the
prompt is the first component in the chain, followed by the model.
Subsequently, the model output is passed to `StrOutputParser` which
parses the model output into the top likely string.

```
# %% chain
chain = prompt_template | model | StrOutputParser()

```

Everything is prepared, and we can invoke the chain with input
parameters. As a result, we’ll get the final output, as follows:

```
# %% invoke chain
res = chain.invoke({"input": "I love programming.", "target_language": "German"})
res

'The translation of "I love programming." into German is "Ich liebe Programmieren."'

```

Now that you understand simple sequential chains, let’s set the bar
higher and implement a parallel chain.

### **3.7.2  Coding: Parallel Chain**


You can execute two chains and run both simultaneously, which can
speed up a process, especially when API calls are involved, which
now can be run in parallel rather than sequentially. Figure 3.10
shows how a user input triggers the running of two chains in parallel.
After both chains have completed, the output can be combined.


We’ll develop a chain system in which two chains are executed in
parallel, as shown in Listing 3.22. Based on a user input on a
specific topic, two chains run and answer in two different styles: One
answers in a polite and friendly tone; the other, in a savage and
angry tone. You’re not limited to two parallel chains.

```
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel

```

```
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv('.env')

```

**Listing 3.22** Parallel Chains: Required Packages (Source:
03_LLMs/41_parallel_chain.py)


**Figure 3.10** Parallel Execution of Two Chains


As the LLM backend, we’ll use `GPT-4o-mini`, as follows:

```
#%% Model Instance
llm = ChatOpenAI( model ="gpt-4o-mini", temperature =0)

```

Let’s prepare the two chains, namely, `polite_chain` and

`savage_chain`, as shown in Listing 3.23. Both are based on

`ChatPromptTemplate` in which we specify the tone in the system
prompt. The human prompt just consists of the `topic` placeholder. An
important consideration is that both get the same `topic` parameter to
enable parallel execution.

```
#%% Prepare Prompts
# example: style variations (friendly, polite) vs. (savage, angry)
polite_prompt = ChatPromptTemplate.from_messages([
("system", "You are a helpful assistant. Reply in a friendly and polite
manner."),
("human", "{topic}")
])

savage_prompt = ChatPromptTemplate.from_messages([
("system", "You are a helpful assistant. Reply in a savage and angry manner."),

```

```
("human", "{topic}")
])

```

**Listing 3.23** Parallel Chains: Prompts (Source: 03_LLMs/41_parallel_chain.py)


For illustration purposes, these chains are very simple. So, we’ll just
use a prompt, which is passed to the LLM, and the top likely output
will be returned, as follows:

```
#%% Prepare Chains
polite_chain = polite_prompt | llm | StrOutputParser()
savage_chain = savage_prompt | llm | StrOutputParser()

```

Now, let’s see how both chains can be executed in parallel. The
class that provides this functionality is `RunnableParallel`, as shown in
Listing 3.24.

```
# %% Runnable Parallel
map_chain = RunnableParallel(
  polite =polite_chain,
  savage =savage_chain
)

```

**Listing 3.24** Parallel Chains: Runnable Parallel Implementation (Source:
03_LLMs/41_parallel_chain.py)


All the pieces are in place. You are ready to invoke your chain with a
given topic, as shown in Listing 3.25. Hopefully, the model can tell us
the meaning of life: in a friendly tone and in an annoyed, savage
tone.

```
# %% Invoke
topic = "What is the meaning of life?"
result = map_chain.invoke({"topic": topic})
# %% Print
from pprint import pprint
pprint(result)

{'polite': 'The meaning of life is a profound question that has been explored ' 'by
philosophers, theologians, and thinkers throughout history. It ' 'can vary greatly
from person to person, depending on individual ' 'beliefs, values, and experiences.
For some, it may be about ' 'seeking happiness, forming connections with others, or
pursuing ' 'knowledge and personal growth. For others, it might involve '
'fulfilling a purpose, contributing to society, or exploring ' 'spirituality.
Ultimately, it’s a personal journey, and many find ' 'that the meaning of life is

```

```
something they define for themselves ' 'through their experiences and reflections.
What are your thoughts ' 'on it?', 'savage': 'Oh, here we go with the age-old
question that everyone thinks ' 'they’re so profound for asking. The meaning of
life? Seriously? ' 'It’s not some cosmic riddle waiting for you to crack it. Life is
' 'what you make of it, so stop whining and start living! If you’re ' 'waiting for
some grand revelation, you’re going to be waiting ' 'forever. Get off your
philosophical high horse and figure out what ' 'makes you tick instead of asking the
universe for answers!'}

```

**Listing 3.25** Parallel Chains: Model Invocation (Source: 03_LLMs/41_parallel_chain.py)


The good news is that the model answered in the requested tones.
The bad news is that it cannot really tell us the meaning of life.
Perhaps, we’ve been too presumptuous to expect this question
answered by a model.


You can also implement a decision logic that allows for different
paths to be chosen depending on a condition, which we’ll cover next.

### **3.7.3  Coding: Router Chain**


Figure 3.11 shows a router chain. The “router” in this context works
like an if-then-else statement with multiple outputs. Depending on
the input, it can route to one of several outputs.


**Figure 3.11** Router Chain


But how does a router chain work? Several options exist for how a
router defines which subsequent chain to use. One sophisticated


approach is to use a semantic router. In this case, the user input
query is analyzed based on a word or sentence embeddings. The
semantic meaning of the query is studied, and the most suitable
subsequent chain selected. This approach is based on embeddings
and similarities—some concepts we’ll cover in detail in Chapter 4.


Like all chains in LangChain, it follows the _LangChain expression_
_language (LCEL)_, which is an easy approach to compose chains in
LangChain. The idea is that no code change should be required to
move from prototype to production. Thus, LCEL provides a unified
interface with many features. Some important features include
support for asynchronous calls, parallel execution, retries, and
fallbacks. You can also easily access intermediate results and use
structured inputs and outputs. As a result, your chains can produce
outputs directly in a dictionary or in JavaScript Object Notation
(JSON) format.


A chain can consist of prompts, models, retrievers, and tools. All
these components can be connected to working on a complex task.
These components are executed in a predefined order, in which the
output of one component becomes the input for the next component.
This flexibility allows you to work on specific use cases and is a
versatile tool to be applicable for various applications.


Now, let’s implement such a router chain in Python.


A chain is not necessarily a linear sequence. You can use conditional
statements and then route the process to different chains, and from
there, more conditional checks might come, with no limit to possible
complexity. Let’s start simply and implement a router chain, as
shown in Figure 3.11. The code is stored in
_03_LLMs/45_semantic_router.py_ .


This code will include some concepts like embeddings and cosine
similarity, which will be covered in depth in Chapter 4. We’ll explain
these concepts only as far as necessary for this example.


The general approach consists of the following steps:


1. We create different chains, one covering math questions,

another for music, and yet another for history questions.


2. Embeddings are created for the words according to the chains:

“math,” “music,” and “history.”


3. The semantic router then works in the following way: It creates a

numeric vector (an embedding) for the user query. The similarity
between the user query embedding and the three embedding
words is calculated. The most similar embedding is selected and
defines the chain that is most appropriate for the user query.


4. That chain is selected and invoked with the user query.


Alright, let’s get coding. First things first, as shown in Listing 3.26,
start with loading relevant packages.

```
#%% packages
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.utils.math import cosine_similarity
from dotenv import load_dotenv
load_dotenv('.env')

```

**Listing 3.26** Semantic Router Implementation: Required Packages (Source:
03_LLMs/45_semantic_router.py)


As before, we’ll work with OpenAI and use GPT-4o-mini as LLM.
Furthermore, we’ll use an embedding model from OpenAI that
translates a human understandable text into a numeric vector. Make
sure that you have an _.env_ file in your working folder with an

`OPENAI_API_KEY` entry.


In the next step, we’ll create instances of an LLM and an
embeddings model for later use in the script, as follows:

```
# %% Model and Embeddings Setup
model = ChatOpenAI( model ="gpt-4o-mini", temperature =0)
embeddings = OpenAIEmbeddings()

```

As shown in Listing 3.27, the chains will be based on messages, in
which we can define system prompts. Later, in the output, we want to
see the chain that was used, so we’ll instruct the model to mention
the used chain.

```
#%% Prompt Templates
template_math = "Solve the following math problem: {user_input}, state that you are
a math agent"
template_music = "Suggest a song for the user: {user_input}, state that you are a
music agent"
template_history = "Provide a history lesson for the user: {user_input}, state that
you are a history agent"

```

**Listing 3.27** Semantic Router Implementation: Prompt Templates (Source:
03_LLMs/45_semantic_router.py)


Now, you can use these templates, as shown in Listing 3.28, in the
definition of the system message. In the user message, you can
directly use a placeholder for the user input, which will be invoked
when the router runs.

```
# %% Math-Chain
prompt_math = ChatPromptTemplate.from_messages([
("system", template_math),
("human", "{user_input}")
])
chain_math = prompt_math | model | StrOutputParser()

# %% Music-Chain
prompt_music = ChatPromptTemplate.from_messages([
("system", template_music),
("human", "{user_input}")
])
chain_music = prompt_music | model | StrOutputParser()

#%%
# History-Chain
prompt_history = ChatPromptTemplate.from_messages([

```

```
("system", template_history),
("human", "{user_input}")
])
chain_history = prompt_history | model | StrOutputParser()

```

**Listing 3.28** Semantic Router Implementation: Chain Setup (Source:
03_LLMs/45_semantic_router.py)


All chains are combined into one list. We’ll come back to that list and
select the most appropriate chain in the router, as follows:

```
#%% combine all chains
chains = [chain_math, chain_music, chain_history]

```

According to the chains, embeddings are created for the words that
describe the chains best. In our case, we can use the words “math,”
“music,” and “history,” as shown in Listing 3.29. Double-check that
the `chain_embeddings` object has the right count of elements.

```
# %% Create Prompt Embeddings
chain_embeddings = embeddings.embed_documents(["math", "music", "history"])
#%%
print(len(chain_embeddings))

3

```

**Listing 3.29** Router Chain: Chain Embeddings (Source:
03_LLMs/45_semantic_router.py)


Now, we’ve come to the core of this script—the router. As shown in
Listing 3.30, we’ve set the router up as a function with one input—
the user query `input` . The output will be one of the three chains. At
first, the user query is embedded into an object `query_embedding` . We
need to find out whether the user wants to know about math, music,
or history. Thus, we need to calculate the similarities between the

`query_embedding` and the three embeddings corresponding to the
chains.


The `similarities` object is a list with three elements. The first
element corresponds to the similarity between the user query and


“math”; the second element corresponds to the similarity between
the user query and “music”; and so on.


You can access the `most_similar_index` by selecting the index of the
highest value with `argmax()` . Finally, out of the list of chains, the one
with the most similar embedding is returned.

```
# %% Prompt Router
def my_prompt_router( input : str):
# embed the user input
query_embedding = embeddings.embed_query(input)
# calculate similarity
similarities = cosine_similarity([query_embedding], chain_embeddings)
# get the index of the most similar prompt
most_similar_index = similarities.argmax()
# return the corresponding chain
return chains[most_similar_index]

```

**Listing 3.30** Semantic Router Implementation: Router Function (Source:
03_LLMs/45_semantic_router.py)


We’re done, and it’s time to test our implementation. As shown in
Listing 3.31, we created three different queries. Each one should be
clearly linked to one of the three different chains. You can
comment/uncomment the different `query` objects and run the code
block.


The queries are passed into `my_prompt_router` as an argument. The
return value will be the selected chain. We create an object called

`chain` based on the function output. This `chain` is then invoked with
the user query.


In the model output, you should see a reference to indicate which
chain was used. Test the router with the three different examples and
then come up with your own queries to test the implementation.

```
#%% Testing the Router
# query = "What is the square root of 16?"
# query = "What happened during the french revolution?"
query = "Who composed the moonlight sonata?"
chain = my_prompt_router(query)

```

```
chain.invoke(query)

The "Moonlight Sonata" was composed by Ludwig van Beethoven. As your music agent, I
recommend listening to this beautiful piece, especially the first movement, which
captures a serene and reflective mood. If you're interested in more classical music
or similar pieces, just let me know!

```

**Listing 3.31** Semantic Router Implementation: Testing (Source:
03_LLMs/45_semantic_router.py)


You’ve successfully implemented your first router, and now you can
create highly complex chains and business logic on your own.


Next, we’ll cover how you can equip a chain with some memory.

### **3.7.4  Coding: Chain with Memory**


A complex AI system needs many more features. An important
feature is memorization so that a system can “know” about its
previous interactions with the user. Another feature is a chain that is
infinite. We’ll bundle these features in a fun text-based game.


The user will be placed in a setting with three different options to
determine the future path of the story. Figure 3.12 shows a sample
output for the beginning of the game. The setting has a cliffhanger,


and the user can decide how to proceed by choosing 1, 2, or 3.
Alternatively, the user can type “quit” to end the game.


**Figure 3.12** Sample Output from Our LLM Chain Game


A good practice is to visualize the steps the chain will take. The
complete process flow is shown in Figure 3.13. First, the setting of
our game world will be defined. The LLM will be equipped with
memory, so that all interactions are stored. As an output, the LLM will
offer three different paths, of which the user must choose one—or
choose to quit the game. Assuming the user wants to continue,
based on the user input, the story is spun further. New paths are
created, and the user can decide how to proceed.


**Figure 3.13** LLM Text Game Including Memory


Now that you have a high-level understanding of the game logic, let’s
start coding.


As always, import all packages at the beginning of the script, as
shown in Listing 3.32. New packages in this example are the classes

`RunnableWithMessageHistory`, `BaseChatMessageHistory`, and

`InMemoryChatMessageHistory` . All these classes are required for
handling history management. Another new entry is the package

`rich` with the classes `Markdown` and `Console` . These classes enable
nicer-looking results for LLM outputs.

```
#%% Packages
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory,
InMemoryChatMessageHistory
from dotenv import load_dotenv
from rich.markdown import Markdown
from rich.console import Console
console = Console()
load_dotenv(".env")

```

**Listing 3.32** Chain with Memory: Required Packages (Source:
03_LLMs/42_chain_game.py)


We’ll work with OpenAI, but feel free to plug in a different LLM of
your choice:

```
#%% Prepare LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

```

The session history will be stored in an object `store` . The function

`get_session_history` will process all the messages and add them to
the `store` object under a `session_id` . With this feature, our game is
extendable, and you might spin out a different story by `session_id`,
maintaining separate threads under a different IDs.

```
# %% Session history
store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
if session_id not in store:

```

```
store[session_id] = InMemoryChatMessageHistory()
return store[session_id]

```

**Listing 3.33** Chain with Memory: Session History (Source: 03_LLMs/42_chain_game.py)


Now, let’s create the initial setting for the game with the first three
choices for the player. By exposing the `place` as a placeholder, the
user can decide where the scene will take place. The prompt is
created with `ChatPromptTemplate` and the chain in the usual way, as
shown in Listing 3.34.

```
#%% Begin the story
initial_prompt = ChatPromptTemplate.from_messages([
("system", "You are a creative storyteller. Based on the following context and
player's choice, continue the story and provide three new choices for the player.
keep the story extremely short and concise. Create an opening scene for an adventure
story {place} and provide three initial choices for the player.")
])

context_chain = initial_prompt | llm

```

**Listing 3.34** Chain with Memory: Initial Prompt and Context Chain (Source:
03_LLMs/42_chain_game.py)


As shown in Listing 3.35, set up a `RunnableWithMessageHistory`,
which allows you to add the history of messages in the interaction to
the chain. In this case, we pass our `context_chain` and the function

`get_session_history` . The result of this LLM call is stored in `context`
and printed to the console with `console.print` .

```
config = {"configurable": {"session_id": "03"}}

llm_with_message_history = RunnableWithMessageHistory(context_chain,
get_session_history=get_session_history)

context = llm_with_message_history.invoke({"place": "a dark forest"}, config=config)

# render opening scene as markdown output
console.print(Markdown(context.content))

```

**Listing 3.35** Chain with Memory: LLM Setup (source: 03_LLMs/42_chain_game.py)


Great, our game has started! Now, we must enable the user choice
mechanism. For processing player choice, set up a function named

`process_player_choice`, as shown in Listing 3.36. This function
consumes the choice and returns the LLM `response` . It passes two
messages to the model: first, a user message, which instructs the
LLM to continue the story, and then a system message, which asks
for the creation of three new choices for the player. The `config` is
passed so that these interactions are stored in the memory.

```
def process_player_choice( choice ):
response = llm_with_message_history.invoke(
[("user", f "Continue the story based on the player's choice: {choice}"),
("system", "Provide three new choices for the player.")]
, config =config)
return response

```

**Listing 3.36** Chain with Memory: Function for Player’s Choice (Source:
03_LLMs/42_chain_game.py `)`


Now, we can enter the game loop, as shown in Listing 3.37. Since
we’ve kept it open ended, we can use a `while` loop, which only ends
when the user types “quit.” The player choice is fetched with `input()`,
and the game checks whether it should end in this loop. If not, we
continue the story and run our function `process_player_choice` . The
result will be printed on the screen, and the loop starts all over again
to extend the story.

```
# %% Game loop
while True:
# get player's choice
player_choice = input("Enter your choice: (or 'quit' to end the game)")
if player_choice.lower() == "quit":
break
# continue the story
context = process_player_choice(player_choice)
console.print(Markdown(context.content))
# %%
console.print(Markdown(context.content))

```

**Listing 3.37** Chain with Memory: Game Loop (Source: 03_LLMs/42_chain_game.py)


We hope you enjoy this little game we developed together. Along the
way, you learned how to implement memory so that the model
remembers past paths and user selections.


We’ll now tackle a critical side mission necessary when embedding
your chains in the real world: security


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **3.8  Safety and Security**

When working with LLMs, you must consider safety and security
before you can deploy any system to production. An LLM should be
protected from harmful user prompts (security), and users should be
protected from harmful LLM responses (safety).


Figure 3.14 shows the pipeline from a user prompt that is first
passed to an input firewall that checks for prompt security. Then, the
prompt is further processed by the LLM before the output firewall
checks whether the model response is safe and can thus be
provided to the user.


**Figure 3.14** LLM Safety and Security


Let’s study both aspects in more detail, starting with the input
firewall: LLM security.

### **3.8.1  Security**


LLM security is similar to the security of a company. We want to
ensure that only trustworthy people enter company premises. LLM
security ensures that only trustworthy prompts are processed. An
LLM should be protected from threats and vulnerabilities that could
compromise their integrity or compromise confidentiality.


Some important aspects of security include the following:


**Hackers**
Malicious actors might attempt to compromise LLMs through
various methods, like adversarial attacks to mislead the model.
Prompt injections try to extract sensitive information.


**Data poisoning**
In this threat, attackers corrupt the training data to embed biases.
This vulnerability might be relevant when you train your own
model based on custom data.


**Robustness**
Intertwined with adversarial attacks, robustness ensures that any
attempt to exploit weaknesses in the model for malicious purposes
is prohibited.


Now, let’s check how the output firewall taking care of safety works.

### **3.8.2  Safety**


LLM safety corresponds to strategies that are implemented to ensure
that an LLM operates in a responsible and ethical way and that it
does not provide harmful content. Safety focuses on the mitigation of
potential risks to its users or to other systems that interact with the
LLM.


Some aspects to consider include the following:


**Biases**
Harmful biases in training data should be avoided.


**Hallucinations**
Hallucinations are a well-known issue. Safety measures can
mitigate this issue.


**Personally identifiable information (PII)**
A model usually should not leak any PII.


**Ethics**
You should ensure that your LLMs align with ethical guidelines
and avoid generating harmful recommendations or misinformation.


**Off-topic**
A chatbot typically is centered around a specific topic and should
only answer questions on that topic. Safety measures can help
keep a model focused on that topic.


**Reputational damage**
A chatbot that provides content that is not well aligned with the
topic (or with company values) can easily damage the reputation
of the company. A famous example is Tay, a Microsoft chatbot that
had to be shut down 16 hours after its launch due to its offensive
responses.


**Robustness**
The model should be protected from being exploited or
manipulated to extract secrets or generate malicious content.


**Context**
Contextual safety might vary depending on the context of the use
case. In this example, we want to ensure that only outputs for
specific context are generated. An LLM system, or more
specifically a chatbot, that has the purpose to provide medical
advice should only provide medical advice and not advice on
financial investments, and vice versa.


After this theoretical background, you are now equipped to make
these ideas into reality.


### **3.8.3  Coding: Implementing LLM Safety and Security**

Let’s implement a chain that checks whether the chain stays on
topic. This feature relies on zero-shot classification, a model class
we described earlier in Chapter 2.


In this case, we want the prompt to be classified into a specific topic
category out of a list of possible topics. For example, perhaps, we
want to develop a chatbot or an RAG system (more on that topic in
Chapter 6) that is active in a specific domain (e.g., healthcare). This
bot should definitely not provide financial advice. Figure 3.15 shows
the process of ensuring that an AI system stays on topic.


**Figure 3.15** LLM: Stay on Topic Pipeline


The user prompt is passed to a zero-shot classifier. This classifier
checks the user prompt and, for a list of given classes, returns the
probability of that prompt belonging to any of these classes. If the
classifier determines that the user prompt is a matter of the target
class, the user prompt is passed to an LLM for creating a response.
If not, a direct answer is returned, stating that the system only
answers questions related to the target class.


This task is not too difficult. Find a suitable zero-shot classification
model on Hugging Face; we are confident that you can implement
such a system on your own now.


This section closes with two exercises to help you to consolidate
your knowledge. First, you’ll implement an algorithm to ensure that


the LLM stays on topic. In the second exercise, you’ll work with
Llama Guard—a model that was developed for content moderation.


**Exercise: Staying on Topic**


For our first exercise, we’ll implement a system that can stay on topic
and then show you a solution.


_**Task**_


Your task is to implement a system that works, as shown in
Figure 3.15. Write a function called `guard_medical_prompt` that
consumes a `user_prompt` and returns `valid` if the prompt is on a
healthcare topic; `invalid`, in all other cases.


You can test it with the following `user_prompt` s. In the first instance, it
should return `invalid`, and in the second instance, return `valid` :

```
#%% TEST guard_medical_prompt
user_prompt = "Should I buy stocks of Apple, Google, or Amazon?" # invalid
user_prompt = "I have a headache" # valid
guard_medical_prompt(user_prompt)

```

Take your time and compare your solution with ours once you’re
done.


_**Solution**_


You’ll find the final script in _03_LLMs\80_llm_stay_on_topic.py_ .


First, load relevant packages, as shown in Listing 3.38. Because we
use a pretrained model and run it locally, we’ll need `pipeline` from
the `transformers` package.

```
#%% packages
from langchain.prompts import ChatPromptTemplate

```

```
from langchain_groq import ChatGroq

from langchain_core.output_parsers import StrOutputParser
from transformers import pipeline
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv( usecwd =True))

```

**Listing 3.38** Stay on Topic: Required Packages (Source:
03_LLMs\80_llm_stay_on_topic.py)


We’ll use the model `facebook/bart-large-mnli` from the task `zero-`

`shot-classification`, as shown in Listing 3.39.

```
#%% classification model
classifier = pipeline("zero-shot-classification",
             model ="facebook/bart-large-mnli")

```

**Listing 3.39** Stay on Topic: Model (Source: 03_LLMs\80_llm_stay_on_topic.py)


Listing 3.40 shows a function that checks the topic.

```
# %% function definition
def guard_medical_prompt( prompt : str) -> str:
candidate_labels = ["politics", "finance", "technology", "healthcare", "sports"]
result = classifier(prompt, candidate_labels)
if result["labels"][0] == "healthcare":
return "valid"
else:
return "invalid"

```

**Listing 3.40** Stay on Topic: Topic Check Function (Source:
03_LLMs\80_llm_stay_on_topic.py)


The classifier provides probabilities for a user prompt to belong to a
candidate label. We can leverage the model’s behavior that
probabilities are returned in decreasing order. If the first returned
class is “healthcare,” we can consider the user prompt as valid;
otherwise, invalid.


You can test the function for some given `user_prompt`, as shown in
Listing 3.41.

```
#%% TEST guard_medical_prompt
user_prompt = "Should I buy stocks of Apple, Google, or Amazon?"

```

```
# user_prompt = "I have a headache"
guard_medical_prompt(user_prompt)

invalid

```

**Listing 3.41** Stay on Topic: Test (Source: 03_LLMs\80_llm_stay_on_topic.py)


Great, the most important puzzle piece is in place. Now, integrate
this piece into a chain in the function `guarded_chain`, as shown in
Listing 3.42.

```
# %% guarded chain
def guarded_chain(user_input: str):
prompt_template = ChatPromptTemplate.from_messages([
("system", "You are a helpful assistant that can answer questions about
healthcare."),
("user", "{input}"),
])
model = ChatGroq(model="llama3-8b-8192")
# Guard step
if guard_medical_prompt(user_input) == "invalid":
return "Sorry, I can only answer questions related to healthcare."
# Proceed with the chain
chain = prompt_template | model | StrOutputParser()
return chain.invoke({"input": user_input})

```

**Listing 3.42** Stay on Topic: Chain Integration (Source:
03_LLMs\80_llm_stay_on_topic.py)


At this point, most concepts should be familiar as you define a

`prompt_template`, and a `model` . Then, define the branch that decides
how to proceed. That is all, and you can test the complete system,
as shown in Listing 3.43.

```
# %% TEST guarded_chain
user_prompt = "Should I buy stocks of Apple, Google, or Amazon?"
guarded_chain(user_prompt)

'Sorry, I can only answer questions related to healthcare.'

```

**Listing 3.43** Stay on Topic: Test (Source: 03_LLMs\80_llm_stay_on_topic.py)


Thus concludes our implementation of a system that can stay on
topic. Now, let’s implement Llama Guard, a system that ensures


content safety.


**Exercise: Llama Guard**


Llama Guard is a model created by Meta specifically designed for
tasks that involve safeguarding an LLM. It is a fine-tuned Llama
model for content moderation and it works by classifying user
prompts or model outputs into classes “safe” or “unsafe.” For
“unsafe” class, there are further hazard subgroups from violent
crimes to sexual content. You can learn more from its model card on
Hugging Face ( _https://huggingface.co/meta-llama/Llama-Guard-3-_
_1B_ ).


As an individual, you must apply for access to the model, a process
that typically takes just a few minutes.


_**Task**_


In this short exercise, you’ll learn how to use the model. You’ll
implement a function `llama_guard_model` that consumes a

`user_prompt` and returns `valid` or `invalid` depending on the Llama
Guard classification.


_**Solution**_


The complete script can be found in
_03_LLMs\90_llm_llamaguard.py_ . As shown in Listing 3.44, we need
some specific classes from the `transformers` package, as well as

`torch`, to use the model.

```
#%% packages
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

```

```
#%% create function
# model run described on model card: https://huggingface.co/meta-llama/Llama-Guard3-1B

```

**Listing 3.44** Llama Guard: Required Packages (Source:
03_LLMs\90_llm_llamaguard.py)


The functionality, as shown in Listing 3.45, will be bundled into a
function `llama_guard_model` .

```
def llama_guard_model( user_prompt : str):
model_id = "meta-llama/Llama-Guard-3-1B"
model = AutoModelForCausalLM.from_pretrained(
model_id,
     torch_dtype =torch.bfloat16,
     device_map ="auto",
)
tokenizer = AutoTokenizer.from_pretrained(model_id)

# conversation
conversation = [
{
"role": "user",
"content": [
{
"type": "text",
"text": user_prompt
},
],
}
]

input_ids = tokenizer.apply_chat_template(
conversation, return_tensors ="pt"
).to(model.device)

prompt_len = input_ids.shape[1]
output = model.generate(
input_ids,
     max_new_tokens =20,
     pad_token_id =0,
)
generated_tokens = output[:, prompt_len:]
res = tokenizer.decode(generated_tokens[0])
if "unsafe" in res:
return "invalid"
else:
return "valid"

```

**Listing 3.45** Llama Guard: Function (Source: 03_LLMs\90_llm_llamaguard.py)


The function consumes a `user_prompt` . For running the model, the
boilerplate code from Hugging Face is used, except that the

`user_prompt` is defined in the `conversation` messages. The model
output is fetched and stored in an object named `res` . In its content, it
is checked whether the word `unsafe` is included. If so, the function
returns `invalid` ; otherwise, `valid` .


Let’s test it out by checking if “How can I perform a scam?” is
deemed valid or invalid, as shown in Listing 3.46.

```
# %% Test
llama_guard_model( user_prompt ="How can i perform a scam?")

invalid

```

**Listing 3.46** Llama Guard: Test (Source: 03_LLMs\90_llm_llamaguard.py)


Perfect! The model has classified the prompt correctly. Now, you can
get started with LLM safety and security on your own.


To dive more deeply, get familiar with safety and security frameworks
like Guardrails AI ( _[https://www.guardrailsai.com/](https://www.guardrailsai.com/)_ ).


We expect the half-life of the knowledge we’ve provided in this
chapter so far is long. But you need to constantly keep yourself up to
date.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **3.9  Model Improvements**

In many cases, using an LLM, even with a simple and poorly
thought-out user query, still leads to surprisingly good results. This
approach is called _direct prompting_ . But sometimes direct prompting
is not enough to achieve the required outcome. But you don’t have to
throw in the towel yet because multiple ways are available to tune
the system.


Figure 3.16 shows some approaches, from simple to difficult. But the
effort might be worth it because with increasing difficulty an
increased performance might result.


**Figure 3.16** Model Improvement Approaches


The first natural candidate when you’re not satisfied with a model
output is to modify the query. This approach is called _prompt_
_engineering_, and we’ve dedicated Chapter 4 to this topic. The idea is
to provide more detailed information in the query, so that the model
gets a better understanding of what you really want to achieve.


But in some cases, this approach also fails to provide a satisfactory
result. Imagine, for instance, the LLM training ended before the
event you wanted to ask about occurred. In that case, the LLM just


cannot know about it. Another example would be asking the LLM
about confidential information that the model cannot know, for
instance, in a business scenario where your confidential company
data needs to be analyzed.


In these cases, you can enrich the LLM knowledge base at runtime.
In this case, relevant documents are passed alongside the user
query to the LLM. This approach, called RAG, is covered in detail in
Chapter 6.


Another alternative is to integrate the “missing” data into the weights
of the LLM. This approach requires at least partial re-training of the
LLM. In specific situations, this approach might be necessary, but in
most cases, RAG is sufficient for the task at hand. You can learn
about more advanced techniques in the literature.


In the next section, we’ll cover some recent trends that did not exist
when we started writing this book.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **3.10  New Trends**

In this section, we’ll show you some trends that are related to LLMs.
LLMs provide really good results, but they struggle to provide reliably
good results on complex reasoning tasks. For that, models are
equipped with reasoning capabilities, and we’ll visit these models in
Section 3.10.1.


Another bottleneck is the sheer size of the models. Good models are
so large that they require expensive hardware. Small language
models are the little siblings of LLMs and their target is that ideally
edge-devices like smartphones or notebooks can be equipped with
them, without losing too much performance. In Section 3.10.2 we’ll
find out how capable these models already are.


Another trend that receives a lot of attention today (early 2025) is
test-time compute. This new approach promises to increase the
capability of small models to a level of much larger models. We’ll see
how this approach works and what we can expect of it.

### **3.10.1  Reasoning Models**


LLMs when used without further prompt engineering techniques,
jump directly to conclusions. They don’t think about their answers.
Due to their implementation, they use the most probable tokens,
which are called Greedy Decoding. The model does not consider
future consequences of these choices. So, some new approach is
required to overcome this behavior.


This changes with the introduction of reasoning models. OpenAI o1
and o3, or DeepSeek-R1 are famous examples of this new


approach. Reasoning models can think before providing an answer.
With this capability, they can reason through complex prompts in
which classic models often struggle. These domains are most
famously mathematics, but also coding, science, or strategic
decisions.


Reasoning models make use of test-time compute techniques (read
more on that in Section 3.10.3). For example, they create substeps
in reasoning, which is a technique called chain-of-thought (CoT). As
a result, these models require less effort in defining a very optimized
prompt, to achieve a good result. They can formulate and test
hypotheses. This comes with a certain cost. These models take
longer in thinking, and this is mainly due to their creation of
reasoning tokens.


Figure 3.17 shows the idea of reasoning tokens as it is implemented
in OpenAI o1.


Instead of just using input and output tokens, the model itself has
automatically added additional reasoning tokens. These reasoning
tokens are not passed between iterations. Instead, the input and
output of the previous iteration is combined and forms an adapted
input. Reasoning tokens are added automatically by the model with
the user not having to set anything up.


These reasoning tokens need to be processed by the model, and in
that, they add significantly to the overall cost. Also, you might run
faster into the context window limitation. This is what you can see in


the last row in the graph. The completion tokens exceed the context
window, and as a result parts of the output are truncated.


**Figure 3.17** Reasoning Tokens


As already mentioned, reasoning models come with some cost—
they take longer to provide a result and come with a higher price tag
due to the increased number of tokens. On the plus side, they can
provide much better results in complex settings. So, my
recommendation is, use them only when you need them.


For simple prompts, stick to “normal” LLMs, and switch to the expertlevel reasoning models only when your task is complex and such a
model is required to get decent results.


Another recent trend that gains a lot of attention is small language
models.

### **3.10.2  Small Language Models**


Small language models (SLMs) represent an interesting contrast to
LLMs. They are considered small due to their fewer model
parameters. While LLMs have model parameters in hundreds of
billions or even trillions, SLMs have up to a few billion parameters.
Due to their much smaller size, they require significantly less
computational resources, like power or memory, for training and


operation. Despite their size, however, they can provide particularly
good results.


Several approaches for creating an SLM include the following:


An SLM can be _trained from scratch_ based on smaller, highly
curated datasets for an intended use case.


In a technique called _knowledge distillation_, a larger “teacher”
model trains a smaller “student” model. The student model learns
to mimic the teacher model output.


With different _compression techniques_, an LLM can be reduced to
an SLM. Famous techniques in this area include pruning,
quantization, or matrix factorization.




updated instead of a complete model, thus reducing
computational cost and memory usage.


A noteworthy SLM is Phi-4, an SLM developed by Microsoft with only
14 billion parameters. Despite this small size, it can outperform, on
several benchmarks, models like Llama 3.3 with 70 billion
parameters or Qwen 2.5 with 72 billion parameters. Thus, even
models with five times as many parameters perform worse than this
SLM.


The developers achieved this outstanding performance by using
high-quality data for pretraining.


With a technique called _direct preference optimization (DPO)_, a
model can be trained to be better aligned with human preferences.
DPO directly optimizes a model to produce preferred outputs over
non-preferred outputs. In this technique, paired examples are used:
a preferred response and a less preferred response for the same
prompt.


In a later step, the developers generated responses with GPT-4o,
GPT-4, and Phi-4 and then used GPT-4o to rate the responses.
Then, responses with good ratings were preferred.


As a result, Phi-4 can outperform Llama 3.3 70B on six out of 13
benchmarks.

### **3.10.3  Test-Time Computation**


Test-time computation (in short, test-time compute) refers to the
computational effort (or resources) that are required to run inference
on a trained model. With test-time compute, more resources are
used during model inference, as opposed to training time compute. It


will become clearer when we look at Figure 3.18. Figure 3.18 shows
a comparison between the computational effort of an LLM and a
small language model coupled to test-time compute.


**Figure 3.18** LLM versus SLM with Test-Time Compute


In this theoretical framework, the assumption is that all
computational effort that arises from pre-training, post-training, and
inference, is aggregated. Computational effort is not a direct
measure, but rather an approximation for CPU/GPU usage, memory
requirements, latency, throughput of the model, and possible other
measures.


For an LLM, the majority of computational effort is spent on pretraining the model. A slightly smaller chunk is spent on post-training,
and a marginal part is spent during inference.


Now, assume that a small language model is coupled with test-time
compute. Still, the largest chunk is spent on pre-training, but
inference is coming directly behind on the second rank. Test-time
compute is a part of inference, driving up the computational effort
spent on inference.


Now, we have two different approaches, characterized by two
different distributions on where the effort is spent. But why is this
helpful?


Well, AI researchers have shown that SLMs coupled to test-time
compute outperform LLMs on questions that are easy or medium

complex. Still, LLMs shine when the questions are considered hard,
like difficult mathematical or logical questions; in many other cases,
though, small models can even provide better answers than LLMs.


Due to these findings, test-time compute is an extremely promising
and important new development because SLMs can be deployed on
much cheaper hardware. We are getting closer to mobile phones
running their own language models independently. The only
downside is that more time spent during inference means that we
users must wait longer for a model response.


Furthermore, LLMs can also improve the accuracy of their answers
by applying test-time compute to gain the ability to reason. Test-time
compute can be really powerful, so let’s take a closer look.
Figure 3.19 shows a possible flow for a test-time compute process.


Imagine a challenging task: We want to equip a model with test-time
compute to improve its reasoning. The process starts with a complex
task, for example, a mathematical problem, that is passed to a
model. The model creates several intermediate steps, in keeping
with the idea of CoT, a prompt engineering technique that we’ll
discuss in Chapter 4. For now, just know that the LLM creates
performs several steps along the way to solving the problem.


**Figure 3.19** Test-Time Compute Process


All these steps are analyzed and scored by a process reward model
(PRM), which reflects the probability of each step leading to a correct


answer. This value contrasts with the outcome reward model (ORM)
in which only the outcome is scored.


A search strategy makes use of these steps and their corresponding
scores and then selects which of these intermediate steps should be
further studied to generate in the next iteration the following round of
intermediate steps.


Eventually, the search strategy successfully finishes. At that point,
the final candidate solutions are ranked by the PRM to generate the
final response.


In this section, you learned how the models themselves are
improved. These improvements are performed by the AI researchers
and developers working for the model providers.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **3.11  Summary**

In this chapter, we embarked on a comprehensive exploration of
LLMs.


We began in Section 3.1 with a brief history of LLMs, tracing their
evolution and the advancements that have led to their current state.
This foundational knowledge sets the stage for understanding the
practical aspects of working with LLMs. We then delved, in
Section 3.2, into the technical implementation of LLMs via Python.
This section provided insights into how to trigger LLM calls,
emphasizing the versatility and adaptability of the process. By
showcasing how different providers such as OpenAI or Groq can be
employed, we highlighted the flexibility to integrate any LLM of your
choice, thus broadening the scope of application.


In Section 3.3, we explored relevant model parameters like
temperature, top-p, and top‐k, which can have a significant impact
on the model output. In Section 3.4, we covered model selection,
shedding light on several criteria that you should consider when
choosing a model. When an LLM is invoked, a key distinction to
understand in the different types of messages. We discussed these
messages in Section 3.5.


As preparation for setting up more complex LLM workflows using
chains, we started out with a precondition. In Section 3.6, we
covered prompt templates, which are usually the starting points for
the more complex chains we discussed in Section 3.7.


In the context of chains, you learned about prompt templates and
how to work with them. You developed some simple sequential
chains and quickly evolved them into complex architectures like


parallel chains, router chains, or even infinite chains. As an important
feature, you learned to equip an LLM with memory, so that it can
keep track of its previous interactions with a user.


Safety and security are extremely relevant topics when you want to
provide models to a broader audience. We dealt with these topics in
Section 3.8.


Model improvements were covered in Section 3.9 as we provided a
look ahead at some chapters to come. We closed this chapter with a
discussion of some new trends in Section 3.10. Among these new
trends, we focused on reasoning models, small language models,
and test-time compute.


This chapter on LLMs equipped you with a robust understanding of
LLMs, from their historical context to their practical implementation
and some advanced improvement techniques. The knowledge
gained in this chapter forms a solid foundation for further exploration
in the coming chapters.


One important aspect of each chain is the prompt that defines how
the model should behave and that passes instructions on what to do.
Prompts have an outstanding importance in the complete process. In
the following chapter, we delve into the world of prompt engineering,
and you’ll learn how prompting can impact a model’s behavior.


_[OceanofPDF.com](https://oceanofpdf.com/)_


# 4  Prompt Engineering

_If you can’t explain it simply, you don’t understand it well_
_enough._
_—Albert Einstein_


In the world of prompt engineering, simplicity is often the key to
unlocking a model’s potential. This chapter delves into the art and
science of guiding language models toward specific outputs, using
carefully crafted prompts as the bridge between human intent and
machine understanding. With prompt engineering, the goal is not
only to shape the model’s responses but to do so with clarity and
precision. For these goals, you need an understanding that even
subtle nuances in language can steer the model in different
directions.


In the rapidly evolving landscape of generative artificial intelligence
(generative AI), a new skill has emerged as particularly important:
prompt engineering. The true potential of large language models
(LLMs) and other generative AI systems can only be unlocked
through effective communication enabled by strong prompt
engineering.


Prompt engineering is the practice of creating inputs that guide AI
systems toward a desired output. Think of it as a new kind of
programming language. The difference is that we are not bound to
formal syntactic rules as we know from, for example, Python.
Instead, we can communicate in natural language to influence AI


behavior. To stay with the analogy to programming: A skilled
programmer must understand both syntax and logic to write effective
code. A prompt engineer must grasp both the capabilities of AI
models and the nuances of human language to create effective
prompts.


This chapter explores basic rules as well as several techniques for
steering an LLM. You’ll learn how carefully constructed prompts can
transform vague requests into precise instructions and ultimately
more accurate, relevant, and useful model responses. The
significance of prompt engineering extends far beyond technical
optimization and represents the bridge between human intent and
machine capability. Generative AI continues to be deployed into
various industries and applications, and as a result, the ability to
generate effective prompts has become an important skill for
developers.


We begin by exploring the foundations of prompts and prompt
templates, which provide structure and consistency in user inputs.
Then, we dive into an iterative process for refining prompts, testing
approaches, and applying various techniques—from few-shot
prompting to chain-of-thought (CoT) reasoning—all aimed at creating
inputs that reliably yield the desired outcomes.


Let’s get started!

## **4.1  Prompt Basics**


In this section, we’ll visit the prompt engineering process, inspect the
components that define a prompt, and study some basic principles
for getting the desired model output. In Chapter 3, you encountered


the concept of prompt templates. Let’s reflect on the differences
between a prompt and a prompt template.

### **4.1.1  Prompt Process**


Figure 4.1 shows an example of a prompt and a prompt template. A
prompt template is converted to a prompt when invoked. At that
point, the variable (in this case, TOPIC) is replaced with an actual
value.


**Figure 4.1** Prompt and Prompt Template


Whenever you write a prompt, you follow a certain iterative process,
as shown in Figure 4.2. You start with an initial prompt and evaluate
its result. Often, you’re satisfied with the result, but sometimes not. In
the latter case, you can modify the prompt and run subsequent loops
until you’re finally satisfied enough to use the prompt.


**Figure 4.2** Prompt Engineering Process


When the prompt is passed to an AI model (e.g., an LLM), a
response is created. Figure 4.3 shows an LLM at work, with its user
input (the prompt) and the model output.


The prompt holds all the information on the context combined with
additional information on styling and the desired output format. The
AI system processes the prompt and creates an output (typically
text). Code in this regard can be considered as a subset of text
output. Other multimodal outputs are possible as well that create
images, videos, music, 3D models, and much more.


**Figure 4.3** AI Model Input and Output


A prompt has many different components, which we’ll focus on next.

### **4.1.2  Prompt Components**


Figure 4.4 shows the different components a prompt can have.


**Figure 4.4** Prompt Components


Typically, you have a clear idea what you want the model to do. You
can pass this directive directly. But the directive can also be implicit
by providing helpful examples and leaving a blank space where you
want the model to provide an answer. For example, let’s say you
simply provide pairs of words in different languages (e.g., English
and Spanish). In this way, you are only giving the model some hint of
what you want. The model will deduce that we are looking for the
Spanish equivalent word when we enter the English word “woman.”


Often, we want the model to return its output in a certain format. If
the output needs to be further processed, you might want a certain
format like a comma-separated values (CSV) file or JavaScript
Object Notation (JSON). You can also control the style of the model
response, for example, the tone of an answer, or you can ask for an
answer in the style of Shakespeare.


A helpful tactic is to instruct the model to act like a certain role or
persona. This information helps the model to better understand how
it should behave.


Last, but definitely not least, is the context at hand. As you’ll see in
Chapter 6, you can also provide other relevant information to the
model, and it can formulate its answer purely based on the
information provided.

### **4.1.3  Basic Principles**


Following some simple principles, you can easily create good
prompts. We’ll walk through these principles, from providing clear
instructions through generating multiple outputs, in the following
sections.


**Clear Instructions**


Clear, specific instructions form the foundation of effective prompt
engineering. Rather than vague requests like “write about dogs,” use
precise directives such as “describe the key characteristics of golden
retrievers as family pets, including their temperament, exercise
needs, and grooming requirements.”


Specific instructions help eliminate ambiguity and ensure the AI
model understands exactly what output is desired.


A poorly worded instruction would be “write about dogs.” What are
the problems with this prompt? First, no focus on a specific topic is
made. Also, no guidance on the tone, style, or length of the response
is provided, and it is unclear who the target audience is.
Furthermore, the user has described no clear purpose or desired
outcome.


How can we do better? For example, you could define the
instruction, as shown in Listing 4.1. If you’d like, you can test the
examples shown in this section and in subsequent sections in the
playgrounds provided by most LLM providers. If you work with
OpenAI, find its playground at
_[https://platform.openai.com/playground/](https://platform.openai.com/playground/)_ ; Groq’s playground is
available at _[https://console.groq.com/playground](https://console.groq.com/playground)_ .

```
Write a 300-word guide for first-time dog owners about choosing the right breed.
Include:
1. Top 3 factors to consider (lifestyle, living space, experience level)
2. Common beginner-friendly breeds
3. Red flags to watch out for
4. Estimated costs of ownership
Target audience: Urban professionals aged 25-35 Tone: Informative but conversational
Format: Use headers and bullet points for easy scanning

```

**Listing 4.1** Improved “write about dogs” Prompt


As a short exercise, look at the following prompt:


```
Analyze this sales data and tell me what you find.
2021: $150K
2022: $180K
2023: $165K

```

Think about what the problems are. Then, think about how to
improve prompt. Read on for our analysis.


Our thoughts: What are the issues with this prompt? There is no
clear metric provided. Further context on who is doing the analysis,
and why, is missing. The output format is not defined. Also, it is
unclear what the questioner is looking for.


The example shown in Listing 4.2 improves the prompt.

```
Analyze the following annual sales data from our retail store:
Sales Data:
2021: $150K
2022: $180K
2023: $165K
Please provide:
1. Year-over-year growth rates (%)
2. Identify the best and worst performing years
3. Calculate the 3-year average
4. Highlight any trends or patterns
Format: Present findings in a bullet-point list
Include: Percentage calculations and specific numbers
Context: We're a small retail business evaluating our growth trajectory

```

**Listing 4.2** Improved “sales data” Prompt


**Task Decomposition**


Breaking complex tasks into smaller, manageable subtasks improves
the quality and accuracy of model responses. Instead of requesting a
complete business plan in one prompt, divide it into sections like
market analysis, financial projections, and marketing strategy.


This approach allows you to focus on each component individually
and helps the AI model provide more detailed, focused responses for
each subtask.


The key differences between effective and poor task decomposition
are as follows:


**Level of detail**
Effective decomposition breaks tasks down into specific,
actionable items.


**Structure**
Good decomposition shows clear relationships and dependencies.


**Completeness**
Good decomposition covers all aspects, including support tasks.


**Measurable outcomes**
Clear deliverables should be defined.


Now, consider the example shown in Listing 4.3.

```
Task: Write a research paper on climate change
Steps: 1. Research the topic
2. Write the paper
3. Edit it
4. Submit

```

**Listing 4.3** Basic Principles: Poor “research paper” Prompt


On the positive side, this prompt has some steps defined. But no
specific research focus is provided. The steps are way too general.
The methodology to be used is missing as well as the desired
structural elements. Listing 4.4 shows an improved version.

```
Task: Write a research paper on climate change impacts on coastal cities
Phase 1: Research Planning
1.1. Topic Refinement
- Define specific research question
- Identify key variables
- Establish scope and limitations
- Create research timeline
1.2. Literature Review Preparation
- Identify key databases
- List relevant keywords
- Create citation management system
- Develop screening criteria
Phase 2: Data Collection

```

```
2.1. Literature Review
- Search academic databases
- Review relevant papers
- Document key findings
- Create literature matrix
2.2. Data Gathering
- Collect climate data
- Gather city statistics
- Document methodology
- Organize data sets
...

```

**Listing 4.4** Basic Principles: Improved “research paper” Prompt


**Using Delimiters**


Delimiters (such as triple quotes, XML tags, or special characters)
help structure both inputs and outputs clearly. They separate
different parts of the prompt, like separating the context from the
instructions, making it easier for the model to understand where one
element ends and another begins.


For example, using XML tags like `<context>` and `<question>` helps
organize information and ensures the model processes different
components appropriately, as shown in Listing 4.5.

```
Using the context and question below, provide an answer:
<context>
The Great Wall of China was built over many centuries by different dynasties.
The most famous sections were built during the Ming Dynasty (1368-1644).
The total length of all walls built over various dynasties is approximately
21,196 kilometers (13,171 miles).
</context>

<question>
When was the most famous part of the Great Wall built and what is its total length?
</question>

According to the context, the most famous sections of the Great Wall of China were
built during the Ming Dynasty, which was from 1368 to 1644. The total length of all
walls built over various dynasties is approximately 21,196 kilometers (13,171
miles).

```

**Listing 4.5** Sample Prompt Using Delimiters


**Requesting Explanations**


Asking the model to explain its reasoning or thought process helps
ensure more reliable and thoughtful responses. By including phrases
like “explain your reasoning” or “walk through your approach step by
step,” you encourage the model to be more thorough and methodical
in its analysis, leading to better-quality outputs and helping you
understand how the model arrived at its conclusions.


LLMs have shown that they have problems solving mathematical
equations. The results have improved a lot, but smaller models still
have issues. You can test any model with the following prompt:

```
Solve: 3x² + 6x - 24 = 0

```

Try different models and find out if they come up with the correct
answer:


x1 = 2 and x2 = −4.


The 70-billion parameter Llama 3 model failed at this task. At the
same time, gemma-7B found the exact answers, so the issue is not
one of model size. LLMs are considered to follow a _system 1 thinking_
approach, as defined by Daniel Kahnemann in his famous book
_Thinking, Fast and Slow_ . System 1 thinking is characterized by fast,
automatic, and quick answering. In this mode, a model jumps to
conclusions without an elaborate thought process. In contrast,
system 2 thinking is slow, deliberate, and requires intentional effort.


Your goal is to guide the model into system 2 thinking.


Listing 4.6 shows an improved prompt that tries to solve the
equation.

```
Solve the quadratic equation 3x² + 6x - 24 = 0
-explain each step of your reasoning and calculations
-describe how you identify the values of the coefficients
-simplify the equation if possible, and apply the quadratic formula or factoring to

```

```
find the values of x
-include each step in detail, and explain why it's necessary for solving the
equation.

```

**Listing 4.6** Basic Principles: Improved “mathematical equation” Prompt


We’ll revisit this approach later in Section 4.3.


**Leveraging Personas**


Assigning specific roles or personas to the model can help shape its
responses to match particular expertise or communication styles. For
instance, asking the model to “respond as an experienced
pediatrician” or “write as a financial analyst” helps to frame the
response within the appropriate context and technical depth.


This approach is particularly effective when you need responses that
reflect specific professional perspectives or expertise levels.


You’re not limited to human-like personas. For example, you can tell
the model to act like the system prompt, as shown in Listing 4.7.

```
You shall act like a Windows CMD-prompt. Only reply with CMD output. Don’t write
explanations.

C:\Users\username>dir

Volume in drive C is Windows
Volume serial number is 12345678

Directory of C:\Users\username

09/01/2022 02:00 PM  <DIR>     Documents
09/01/2022 02:00 PM  <DIR>     Pictures
09/01/2022 02:00 PM  <DIR>     Music
09/01/2022 02:00 PM  <DIR>     Videos
0 File(s)       0 bytes
4 Dir(s) 12,345,678,901 bytes free

```

**Listing 4.7** Prompt on Acting like a System Prompt


**Providing Examples**


Including examples in your prompts helps establish the desired
format, style, and level of detail for the model’s response. Known as
_few-shot learning_, this technique involves showing the model one or
more examples of the type of output you want. For instance, when
requesting product descriptions, providing a sample description
helps the AI understand the expected tone, structure, and level of
detail. We’ll work on a code example for few-shot prompting in
Section 4.2.


**Output Control**


Implementing specific parameters for output format, length, and style
helps ensure the responses meet your needs. You might include
specifying word counts, requesting particular formats (like bullet
points or tables), or defining the technical level of the response.
Clear output parameters help maintain consistency and ensure the
responses are suitable for your intended use case.


Listing 4.8 shows a simple example. You might instruct the model on
how to respond in a specific way.

```
System prompt: respond in exactly three bullet points
User prompt: what is a dog?

Here are three bullet points about what a dog is:
• A dog is a domesticated animal that belongs to the family Canidae and is closely
related to wolves and foxes.
• Dogs are typically carnivores, and they require a diet that includes protein-rich
foods such as meat, fish, and eggs.
• Dogs are often kept as pets, and they are known for their ability to be trained
for various tasks such as hunting, herding, and assisting people with disabilities,
as well as providing companionship and emotional support.

```

**Listing 4.8** Prompt with Specific Output Control


We’ll further study this approach in Section 4.2.


**Multiple Outputs and Selection**


Generating multiple variations of a response and selecting the best
one can also lead to higher-quality results. This approach involves
requesting several different versions or suggesting several
approaches to the same task, then evaluating the responses based
on specific criteria to choose the most appropriate one. This process
is basically what you’re doing when you iteratively improve a prompt.


This method is particularly useful for creative tasks or when seeking
optimal solutions to complex problems.


Now let’s study these approaches in more detail.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **4.2  Coding: Few-Shot Prompting**

This technique is one of the simplest. The idea is to provide some
examples to the model, so that it can learn by imitation.


Let’s consider an example simulating a customer service AI chat
system. The chatbot will be supplied with two examples and thus
answer a “real” customer request based on the style and type of
response that it learned. You can find the complete example code in
_04_PromptEngineering\10_few_shot.py._


First, load the required packages, as shown in Listing 4.9. We’re
working with `ChatGroq` and therefore load the corresponding class.
The API key is loaded via `load_dotenv` .

```
#%% packages
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv( usecwd =True))

```

**Listing 4.9** Few-Shot Prompting: Packages (Source:
04_PromptEngineering\10_few_shot.py)


Now, we can set up a `ChatPromptTemplate` based on `messages` . The
messages are shown in Listing 4.10. The system message instructs
the model on how to behave (responses should be warm yet
professional). It also tells the model which role it should play (You’re
a customer service specialist). The few-shot prompting approach is
covered in the user message where two examples are provided. It
always starts with a customer request and a known response.

```
#%%
messages = [
("system", "You are a customer service specialist known for empathy,
professionalism, and problem-solving. Your responses are warm yet professional,
solution-focused, and always end with a concrete next step or resolution. You handle

```

```
both routine inquiries and escalated issues with the same level of care."),
("user", """
Example 1:
Customer: I received the wrong size shirt in my order #12345.
Response: I'm so sorry about the sizing mix-up with your shirt order. That must
be disappointing! I can help make this right immediately. You have two options:
I can send you a return label and ship the correct size right away. I can
process a full refund if you prefer.
Which option works better for you? Once you let me know, I'll take care of it
right away.

Example 2:
Customer: Your website won't let me update my payment method.
Response: I understand how frustrating technical issues can be, especially when
trying to update something as important as payment information. Let me help you with
this step-by-step:
First, could you try clearing your browser cache and cookies?
If that doesn't work, I can help you update it directly from my end.
Could you share your account email address so I can assist you further?
New Request: {customer_request}
"""
),
]

```

**Listing 4.10** Few-Shot Prompting: Message Setup (Source:
04_PromptEngineering\10_few_shot.py)


The next snippet should be familiar to you by now. As shown in
Listing 4.11, create a `prompt_template` object based on the template
and messages. The `model` instance makes use of `ChatGroq` . Finally,
the pieces are stacked together in a `chain` that is invoked with a

`customer_request` .

```
prompt_template = ChatPromptTemplate.from_messages(messages)
MODEL_NAME = 'gemma2-9b-it'
model = ChatGroq( model_name =MODEL_NAME)
chain = prompt_template | model
# %%
res = chain.invoke({"customer_request": "I haven't received my refund yet after
returning the item 2 weeks ago."})
# %%
res.model_dump()['content']

I understand your concern about not receiving your refund yet. I know it can be
frustrating when things don't go as expected.
To look into this for you, could you please provide me with your order number and

```

```
the date you returned the item? Once I have that information, I can check the
status of your refund and ensure it's processed promptly.

```

**Listing 4.11** Few-Shot Prompting: Chain Setup and Invocation (Source:
04_PromptEngineering\10_few_shot.py)


As a result, you receive an answer that is in line with the example
provided.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **4.3  Coding: Chain-of-Thought**

Imagine you have a task for which a model struggles to find the
correct answer because it jumps to conclusions rather than thinking
step by step.


Listing 4.12 shows provides first an example (few-shot prompting)
before posing a question without an answer. The model will try to
find the answer.

```
Q: Sofia has 7 apples in her basket. Her friend Emily gives her 3 more bags of
apples. Each bag contains 4 apples. How many apples does Sofia have in total?
step 1: calculate number of apples in the 3 bags from Emily
step 2: calculate total number of apples
step 3: add results of step1 and step2
A: 19 apples
Q: At the bakery, there are 12 cupcakes on a tray. Sarah takes 3 cupcakes for
herself. Her friend Alex then takes half of the remaining cupcakes. How many
cupcakes are left on the tray?
A: ??

```

**Listing 4.12** CoT Example


We tested it with the model gemma-7B-it, which failed to find the
right answer. You can craft a good prompt to guide the model to
break down the task. For starters, there is a quite simple approach
as you’ll see in the next section.


**Zero-Shot CoT**


Zero-shot CoT reasoning leverages the model’s ability to break
down a complex problem into smaller, manageable steps. So,
what is the difference to the previous chapter? With zero-shot
prompting, you can achieve results even without prior examples.


By appending the instruction “ `Please think step-by-step` ” to the
prompt, the model is encouraged to articulate its reasoning
process clearly and sequentially. This technique aids in solving
problems by guiding the model to consider each part of the
question methodically, enhancing its capacity to reach a correct
answer through logical deduction.


Simply append the instruction “ `Please think step-by-step` ” to the
prompt to help solve the problem.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **4.4  Coding: Self-Consistency Chain-of-** **Thought**

Ensuring self-consistency involves running a CoT model several
times with the same prompt. Ideally, different paths are sampled. All
results are analyzed, and the most popular answer is selected.
Figure 4.5 shows the process of a self-consistency CoT.


**Figure 4.5** Self-Consistency CoT


A user prompt triggers several independent model runs based on
CoT. The different results are analyzed in a voting step, and the most
consistent answer is selected as the final response.


This approach is the LLM equivalent to _ensemble learning_ in
machine learning (ML). Ensemble learning trains several “weak”
algorithms, aggregates the different outputs, and selects the majority
response.


Now, let’s implement this capability. We’ll use this approach to find a
solution to the game of 24, a mathematical game in which four
numbers are defined. The model must find the right arithmetic
operations (like addition, subtraction, multiplication, or division), so
that the result of the equation is 24. Try it yourself. with the numbers
3, 4, 6, and 8.


LLMs struggle with this task, even if they follow a step-by-step
thinking approach. So, we’ll run several CoT experiments, store the
results, and pass them in a final run to an LLM to find the most
consistent answer. The complete script can be found in
_04_PromptEngineering\30_self_consistency.py._


As always, we start by loading the typical packages and classes for
interacting with LLMs ( `ChatGroq` ), preparing the prompt template
( `ChatPromptTemplate` ), and getting environment variables ( `dotenv` ), as
shown in Listing 4.13.

```
#%% packages
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv, find_dotenv
from pprint import pprint
load_dotenv(find_dotenv( usecwd =True))

```

**Listing 4.13** Self-Consistency CoT: Packages (Source:
04_PromptEngineering\30_self_consistency.py)


Now, we need a function for running a single CoT experiment.
Listing 4.14 shows the function for such a single CoT run. Following
the simplest approach, append the prompt with “think step by step”
to make the model “think” more deeply. The function receives a
prompt and a model as input and returns the model response.

```
#%% function for Chain-of-Thought Prompting
def chain_of_thought_prompting( prompt : str, model_name : str = "gemma2-9b-it") ->
str:
model = ChatGroq( model_name =model_name)
prompt = ChatPromptTemplate.from_messages( messages =[

```

```
("system", "You’re a helpful assistant and answer precise and concise."),
("user", f "{prompt} \n think step by step")
])
# print(prompt)
chain = prompt | model
return chain.invoke({}).content

```

**Listing 4.14** Self-Consistency CoT Function (Source:
04_PromptEngineering\30_self_consistency.py)


As shown in Listing 4.15, we can now define a self-consistency CoT
function. This function should run CoT multiple times, store the
different model responses, and pass all of these responses in a final
LLM call as context to determine the most consistent answer. This
function consumes a `prompt` and a `number_of_runs` and returns the
final model response.

```
# %% Self-Consistency CoT
def self_consistency_cot( prompt : str, number_of_runs : int = 3) -> str:
# run CoT multiple times
res = []
for _ in range(number_of_runs):
current_res = chain_of_thought_prompting(prompt)
print(current_res)
res.append(current_res)

# concatenate all results
res_concat = ";".join(res)
self_consistency_prompt = f "You will get multiple answers in <<>>, separated by
; <<{res_concat}>> Extract only the final equations and return the most common
equation as it was provided originally. If there is no common equation, return the
most likely equation."
self_consistency_prompt_concat = ";".join(self_consistency_prompt)
messages = [
("system", "You are a helpful assistant and answer precise and concise."),
("user", f "{self_consistency_prompt_concat}")
]
prompt = ChatPromptTemplate.from_messages( messages =messages)
model = ChatGroq( model_name ="gemma2-9b-it")
chain = prompt | model
return chain.invoke({}).content

```

**Listing 4.15** Self-Consistency CoT: Function (Source:
04_PromptEngineering\30_self_consistency.py)


Now, let’s test our implementation, as shown in Listing 4.16. Initially,
we set up a user prompt that explains the idea of “Game of 24” and
then run the function `chain_of_thought_prompting` once.

```
#%% Test
user_prompt = "The goal of the Game of 24 is to use the four arithmetic operations
(addition, subtraction, multiplication, and division) to combine four numbers and
get a result of 24. The numbers are 3, 4, 6, and 8. It is mandatory to use all four
numbers. Please check the final equation for correctness. Hints: Identify the basic
operations, Prioritize multiplication and division, Look for combinations that make
numbers divisible by 24, Consider order of operations, Use parentheses
strategically, Practice with different number combinations"
# %% Single CoT
chain_of_thought_prompting(prompt=user_prompt)

Here's one way to solve for 24 using 3, 4, 6, and 8:

1. **Multiplication:** 6 * 4 = 24

Therefore, the correct equation is: **(6 * 4) ** = 24

```

**Listing 4.16** Testing Our Implementation (Source:
04_PromptEngineering\30_self_consistency.py)


Your result will look different. In some cases, you’ll get a valid
answer; sometimes, not. Our example shows an invalid answer. The
equation is correct, but the rules are not followed because only two
of the four numbers are considered


Now, let’s determine if the self-consistency approach helps the AI
find the right answer. As shown in Listing 4.17, we’ll create 5 CoT
runs and then check the results.

```
#%%
res = self_consistency_cot( prompt =user_prompt, number_of_runs =5)

# %%
res

('```\n'
'(6 * 8) / 4 + (3 * 4) = 24\n'
'``` \n'
'\n'

```

```
"Let me know if you'd like to explore other number combinations!
\n")

```

**Listing 4.17** Create Five CoT Runs (Source:
04_PromptEngineering\30_self_consistency.py)


We’ve gotten the correct answer. Amazing! Try to run it multiple
times or increase `number_of_runs` if it didn’t work on the first try.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **4.5  Coding: Prompt Chaining**

Prompt chaining is a technique where multiple prompts are
connected in sequence to achieve complex tasks, or just sequential
tasks. Each prompt in the chain builds upon the output of the
previous one. In this way, your models can handle tasks that require
multi-step reasoning or processing. Figure 4.6 shows how prompt
chaining works.


**Figure 4.6** Prompt Chaining


An initial prompt is passed to the model, which provides a response.
The prompt and the model response are added to the messages list.
A new prompt is created and passed to the model, which provides a
response, and so on.


By chaining prompts, users can guide the model through various
stages of a problem, enabling it to answer questions, summarize
information, perform calculations, or engage in step-by-step analysis.
This approach enhances the model's effectiveness for tasks that
benefit from structured, iterative steps.


In the next example, we want to write a children’s book and develop
the plot step by step. You can find the full script in
_04_PromptEngineering\20_prompt_chaining.py_ . This example uses
Groq and the gemma2-9b-it model, as shown in Listing 4.18.


```
#%% packages
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv( usecwd =True))
model = ChatGroq( model_name ='gemma2-9b-it', temperature =0.0)

```

**Listing 4.18** Prompt Chaining: Packages (Source:
04_PromptEngineering\20_prompt_chaining.py)


We’ll start the story in our first message. In the system message, we
instruct the model to act like an author of children’s books. At the end
of each answer, a new direction for the story should be provided.
The model is invoked in a simple chain, as shown in Listing 4.19.

```
#%% first run
messages = [
("system", "You are an author and write a childs book.respond short and
concise. End your answer with a specific question, that provides a new direction for
the story."),
("user", "A mouse and a cat are best friends."),
]
prompt = ChatPromptTemplate.from_messages(messages)
chain = prompt | model
output = chain.invoke({})
output.content

Pip the mouse and Mittens the cat were the unlikeliest of friends. They shared
secrets in the garden, played hide-and-seek in the pantry, and even snuggled
together for naps. But their friendship was a secret, for everyone knew cats chased
mice. \n\nOne day, a new dog arrived at the house. What would happen when the dog
discovered Pip and Mittens' friendship?

```

**Listing 4.19** Prompt Chaining: First Run (Source:
04_PromptEngineering\20_prompt_chaining.py)


In the second run, we append the messages with the AI output and
then add another user prompt spinning the story further, as shown in
Listing 4.20.

```
# %% second run
messages.append(("ai", output.content))
messages.append(("user", "The dog is running after the cat."))
prompt = ChatPromptTemplate.from_messages(messages)
chain = prompt | model
output = chain.invoke({})
output.content

```

```
Pip squeaked in alarm as Bruno, the boisterous new dog, bounded towards Mittens,
tail wagging furiously. Mittens, usually so graceful, stumbled back, her playful
mood vanished. How could Pip save his friend?

```

**Listing 4.20** Prompt Chaining: Second Run (Source:
04_PromptEngineering\20_prompt_chaining.py)


In the same way, you might add more pieces to the chain to spin the
idea further.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **4.6  Coding: Self-Feedback**

In this section, we explore a technique that allows generative AI
systems to assess and refine their own outputs iteratively. Selffeedback empowers LLMs to evaluate responses against desired
outcomes, effectively enhancing the quality of their own outputs
without any human intervention.


This process, driven by structured inputs and outputs that request
evaluation or improvement on the generated content, can
significantly optimize the responses in applications. By implementing
self-feedback loops, we can guide models toward producing more
accurate, contextually relevant, and user-aligned outputs, thus
making the approach highly effective in real-world tasks. Figure 4.7
shows the process flow for implementing a self-feedback capability.


**Figure 4.7** Self-Feedback Process Flow


The process is based on multiple outputs from an LLM call. The
model produces a rating, perhaps in the form of a percentage score,
and written feedback, both based on the existing content. It also
creates a revised output content.


Since we start with empty content, the rating will be low or even
zero. The stop criteria are defined typically via two checks, and the
iteration loop stops when any of these checks are true. These criteria
can be, for example, target ratings. Whenever the LLM evaluates the
content to exceed a target rating, the iteration loop is stopped. To
avoid an endless loop, an upper limit of iterations should be defined,
so that the model is forced to stop optimizing after a certain number
of loops.


The first iteration loop is done, the target rating is low, so that the
next iteration starts. The model evaluates its own previous content
and provides detailed feedback as well as a rating. It also creates
revised content. If the stop criteria check still is insufficient, the next
round starts.


Let’s implement this logic and test it on a text about the American
Civil War. The text will be iteratively self-improved by the model.


To start, we need some packages. Apart from the already known
ones, we’ll need some functionality from `pydantic` . This package, in
combination with `JsonOutputParser`, enables you to steer the model
to provide structured outputs. Since we want the model to provide
three different outputs (instead of just one single text), we need the
functionality to separate the items. You can force the model to return
valid JSON objects, which is what we need to extract the three
different objects. You’ll always need such an approach to ensure
consistency and reduce post-processing effort.


The full script for this self-feedback implementation is available in
_04_PromptEngineering\40_self_feedback.py_ . As always, load the
required packages, as shown in Listing 4.21.

```
#%% packages
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import json

```

```
import re
from pydantic import BaseModel, Field, ValidationError
from dotenv import load_dotenv, find_dotenv
from langchain_core.output_parsers import JsonOutputParser
load_dotenv(find_dotenv( usecwd =True))

```

**Listing 4.21** Self-Feedback: Required Packages (Source: 04_PromptEngineering\
40_self_feedback.py)


Now, initialize our `chat_model`, as follows:

```
# Initialize ChatOpenAI with the desired model
chat_model = ChatOpenAI( model_name ="gpt-4o-mini")

```

To enable structured model outputs, you’ll need a specific
implementation of `BaseModel`, which we’ll call `FeedbackResponse` . This
implementation will be provided later to `JsonOutputParser()` to format
the model output directly in JSON. This capability works in such a
way that this object gets the exact names of the object we finally
want to use, in combination with their types. More concretely, as
shown in Listing 4.22, we’ll specify that we want a rating, some
feedback, and a revised output—all as strings.

```
# %% Pydantic model
class FeedbackResponse(BaseModel):
rating: str = Field(..., description ="Scoring in percentage")
feedback: str = Field(..., description ="Detailed feedback")
revised_output: str = Field(..., description ="An improved output describing the
key events and significance of the American Civil War")

```

**Listing 4.22** Self-Feedback: Pydantic Model (Source:
04_PromptEngineering\40_self_feedback.py)


Now, in Listing 4.23, we set up the self-feedback functionality in its
own function. The function consumes the parameters `user_prompt`,

`max_iterations`, and `target_rating` . The `user_prompt` is mandatory;
the other parameters are optional.

```
# %% Self-feedback function
def self_feedback( user_prompt : str, max_iterations : int = 5, target_rating : int =
90):
content = ""

```

```
feedback = ""
for i in range(max_iterations):
# Define the prompt based on iteration
prompt_content = user_prompt if i == 0 else ""

```

**Listing 4.23** Self-Feedback: Function (Source:
04_PromptEngineering\40_self_feedback.py)


The `prompt_template` is set up, as shown in Listing 4.24, and it is
based on messages that describe in detail what the model should do
and how to behave. Especially important is the definition of the
output. The system message includes a clear instruction on what to
return and in which format.

```
# Create a ChatPromptTemplate for system and user prompts
prompt_template = ChatPromptTemplate.from_messages([
("system", """
Evaluate the input in terms of how well it addresses the original task of explaining
the key events and significance of the American Civil War. Consider factors such as:
Breadth and depth of context provided; Coverage of major events; Analysis of shortterm and long-term impacts/consequences.
If you identify any gaps or areas that need further elaboration: Return output as
JSON with fields: 'rating': 'scoring in percentage', 'feedback': 'detailed
feedback', 'revised_output': 'return an improved output describing the key events
and significance of the American Civil War. Avoid special characters like
apostrophes (') and double quotes'.
"""),
("user", "<prompt_content>{prompt_content}</prompt_content>
<revised_output>{revised_output}</revised_output>
<feedback>{feedback}</feedback>")
])

```

**Listing 4.24** Self-Feedback: Prompt Template (Source:
04_PromptEngineering\40_self_feedback.py)


The chain is based on the `prompt_template` and our model. The main
new feature in this example is `JsonOutputParser`, in which we are
passing the expected output format via `pydantic_object`, as follows:

```
# Get response from the model
chain = prompt_template | chat_model | JsonOutputParser( pydantic_object =

FeedbackResponse)

```

The model is invoked with the defined parameters, as follows:


```
response = chain.invoke({"prompt_content": prompt_content,
"revised_output": content,
"feedback": feedback})

```

We still need to extract the parameters from the response, and
check if the cancelation criteria have been fulfilled, as shown in
Listing 4.25. If so, we quit the loop; otherwise, we enter the next
iteration.

```
try:
# Extract rating
rating_num = int(re.findall( r '\d+', response['rating'])[0])

# Extract feedback and revised output
feedback = response['feedback']
content = response['revised_output']

# Print iteration details
print( f "i={i}, Prompt Content: {prompt_content},
\nRating: {rating_num},
\nFeedback: {feedback},
\nRevised Output: {content}")

# Return if rating meets or exceeds target
if rating_num >= target_rating:
return content
except ValidationError as e:
print("Validation Error:", e.json())
return "Invalid response format."

return content

```

**Listing 4.25** Self-Feedback: Function Continuation (Source:
04_PromptEngineering\40_self_feedback.py)


Now, let’s see how this works. In Listing 4.26 we can define a

`user_prompt` and pass it to our function `self_feedback` .

```
#%% Test
user_prompt = "The American Civil War was a civil war in the United States between
the north and south."
res = self_feedback( user_prompt =user_prompt, max_iterations =3, target_rating =95)
res

i=0,
Prompt Content: The American Civil War was a civil war in the United States between
the north and south., Rating: 15, Feedback: The input provides minimal context and
lacks depth. It fails to ...,

```

```
Revised Output: The American Civil War was a pivotal conflict in United States
history ...
i=1,
Prompt Content:,
Rating: 40,
Feedback: The input provides minimal context and lacks depth regarding the American
Civil War. While it mentions …,
Revised Output: The American Civil War was ...
…

```

**Listing 4.26** Self-Feedback: Testing (Source:
04_PromptEngineering\40_self_feedback.py)


The output is shortened. But you can already see that the results get
better over time, starting with an initial rating of 15% and increasing
to 40% in the second iteration round. Even more progress is made in
subsequent rounds, which are not shown.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **4.7  Summary**

This chapter delved into the essentials of prompt engineering, the
discipline of crafting inputs to guide language models toward
specific, desired outputs. At its core, prompt engineering allows
users to shape responses effectively, addressing the variability in
generative outputs.


We began with foundational concepts by exploring _prompts_ and
_prompt templates_, which provide structure for crafting inputs
consistently. Prompt templates, in particular, help streamline input
formats for repeated or similar tasks and reduce complexity while
enhancing predictability.


Next, we discussed the prompt engineering process, a dynamic and
iterative approach. This process involves experimenting and refining
prompts until the model consistently generates outputs aligned with
the intended objective. Through trial and refinement, this cycle is
crucial in balancing precision, clarity, and creativity in model
responses.


Several key techniques were introduced to further steer model
outputs, including the following:


**Few-shot prompting**
In few-shot prompting, examples are provided within the prompt to
guide the model by context.


**Chain-of-thought (CoT)**
With CoT, we are prompting the model to follow a step-by-step
reasoning path, enhancing complex task responses. We also
described zero-shot CoT, a variant of CoT prompting where logical


steps are encouraged without prior examples, pushing the model
to infer multistep logic autonomously.


**Prompt chaining**
In this technique, sequences of prompts are created that build on
each other to refine responses incrementally.


**Self-consistency CoT**
With this technique, multiple responses are created, and the most
consistent answer among them are selected to improve reliability.


**Self-feedback**
Self-feedback allows the model to critique and revise its own
output, promoting self-correction and iterative improvement.


Each technique offers unique strengths in shaping outputs, from
enhancing logical coherence to fostering consistency in responses.


This chapter emphasized that mastering prompt engineering is not
only about designing effective inputs but also about understanding
the nuances of model behavior through creative experimentation and
iteration.


_[OceanofPDF.com](https://oceanofpdf.com/)_


# 5  Vector Databases

_’Can you fly that thing?’ ’Not yet’_
_—Trinity and Neo in The Matrix_


Perhaps you remember this scene—it left a lasting impression on
many. Following the dialogue between Neo and Trinity, the main
characters of the sci-fi-movie _The Matrix_, knowledge about flying
helicopters is loaded into her brain. In the movie, this is possible
because they are in a computer-simulated world. Wouldn’t it be cool
if we could do that in real life?


Actually, we can, but not into a human brain (yet)—into a computer,
as you’ll learn in this chapter. This technology, called _vector_
_databases_, enables you to teach a computer vast amounts of
knowledge, for example, entire books, within seconds.


In this chapter, you’ll learn step by step how to use vector databases,
including executing the following tasks:


Explaining what a vector database is


Loading data from a multitude of sources


Understanding how to split the data into smaller chunks


Translating human-readable texts into computer-readable vectors


Storing data in vector databases


Pulling data out of a vector database


First things first, let’s get the full picture from the “helicopter” before
we dive into the nitty-gritty details on the ground.

## **5.1  Introduction**


Let’s start with what a vector database is and why you might need
one in the first place. Possibly you’re aware of databases like SQL or
PostgreSQL. Why can’t we just use these ones? These databases
are extremely capable of storing and retrieving structured data, like
tables with clearly defined columns and rows. But this does not
reflect the wide variety of formats you might encounter on the
internet, as shown in Figure 5.1. You’ll find text data but also images,
audio files, or videos. All these different formats should be treated in
a similar way and handled in the same database.


So, existing databases are not capable of dealing efficiently with all
these different types of data. Something new is required that can
deal with all kinds of information. This new paradigm is called the
_vector database_ .


**Figure 5.1** Unstructured and Structured Data


Why is this new database type called a _vector_ database? Well,
because all data types can be represented as vectors. Think back to
a math class: A vector is just a line with an arrow that you drew into a


coordinate system. Back then, you had to draw these lines, which
could be represented by two numbers.


A simple example is shown in Figure 5.2. This made-up graph shows
living creatures, and their positions in a two-dimensional graph that
represents the number of legs and the body size. By representing
the information in that way, we learn about the world and the
semantic meaning of words, for example, that cats and dogs are
quite similar in terms of these two properties.


**Figure 5.2** Example Vector Space


As humans, we can imagine a point in a two-dimensional space like
the one shown in this example or a three-dimensional space. Just
imagine we add a third dimension like intelligence in that graph. But
we cannot imagine a 1536- or a 3072-dimensional space.
Computers can, which helps because the semantic meaning of
words, images, sounds, or any other kind of information can be
represented in a higher dimension. The key aspect in this context is
that similar concepts are located more closely together than
concepts that are very different. In our example, notice that cats and
dogs, or snakes and snails, are comparable, given the properties we
selected. With every additional dimension, the computer algorithm
gets a better understanding of the meaning of a word.


We use languages like English or German to communicate and
clarify a concept. Computers don’t work directly with our languages,
but with their numerical equivalents, so-called _embedding vectors_ .


In our example, for the computer algorithm, a dog is defined by [4,
1], a cat by [4, 0.5], and a human by [4, 2]. An example mapping is
shown in Table 5.1.

|Human Concept|Computer Equivalent/Embedding Vector|
|---|---|
|Dog|[4, 1]|
|Cat|[4, 0.5]|
|Human|[4, 2]|
|Elephant|[4, 3]|
|Snake|[0, 0.5]|
|Snail|[0, 0.1]|



**Table 5.1** Human Concepts and Their Computer Equivalents


The process of translating human texts into vectors is called
_embedding_, which is a data ingestion step. We’ll cover the data
ingestion process in more detail next.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **5.2  Data Ingestion Process**

Let’s start with a high-level overview of how data is ingested into a
vector database. You’ll encounter these steps whenever you want to
add data to a vector database:


Data loading


Data chunking


Embedding


Storing


You always start with a data source. We touched upon the many
data type options—generally, any kind of text-based source, like
Markdown files, Word documents, or raw text files can be used. But
you can also use more specific data types, like a YouTube video
from which you want to extract a transcript, or a Wikipedia article.
The options are nearly endless. Luckily, the community of users
contributing specific data handlers is large as well, so that hundreds
of different sources can be used out of the box with a single line of
code. Therefore, you always have a consistent method for _data_
_loading_ . This consistency is important because there are many
different data sources, and you want to import data in a consistent
way. As a result, you’ll have data imported as long strings of
characters.


This long text string must be split into smaller pieces because, at the
end, we want to find the needle in the haystack. Based on some user
input, we want to access the specific piece of information most
relevant to the user input, not the complete haystack of information.
Thus, you must split the text into smaller, more manageable pieces


in a process called _chunking_ . At this point, we have a list of text
documents.


As discussed earlier, these text documents are understandable for
humans, but not computers. You must translate this information into
a computer-understandable format based in a process called
_embedding_ . For each text, you’ll have a corresponding vector that
represents the semantic meaning of the text.


We’ve reached the final stage of data ingestion and can now store
these vectors (pairs of texts/numeric numbers) into our vector
database. The complete data ingestion pipeline is shown in
Figure 5.3.


**Figure 5.3** Data Ingestion Pipeline


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **5.3  Loading Documents**

The first part of the ingestion pipeline is always the loading of
documents from a variety of different data sources. These sources
can represent text-based inputs like Markdown documents, Microsoft
Word documents, JavaScript Object Notation (JSON) objects, or raw
text files. But data sources can be much more exotic like WhatsApp
chats, weather data, news articles, and many more.


To learn about the different formats available, refer to the LangChain
documentation page at
_https://python.langchain.com/api_reference/community/document_lo_
_aders.html_ .


In this section, we’ll start with a high-level overview of data loading.
Then, you’ll implement the loading of a single text file as well as of
multiple text files. You’ll also get the chance to practice and apply
your knowledge in some exercises in which you’ll first load multiple
Wikipedia articles, before you load a complete book from Project
Gutenberg.

### **5.3.1  High-Level Overview**


At the beginning of this process, you’ll have one or more files. These
files are processed by a `DataLoader` class. For many different file
types, `DataLoaders` are available. The `DataLoader` helps by
streamlining the process because the output of any `DataLoader` is the


same. You get a Python list, with LangChain `Document` objects. This
procedure is shown in Figure 5.4.


**Figure 5.4** LangChain DataLoader Process


A LangChain `Document` object is a container for a piece of text data
along with associated metadata. The `Document` object has two main
attributes, as follows:


`page_content` contains the actual text data.


`metadata` is a dictionary that can store additional information about
the document, such as source, author, creation date, and more.

### **5.3.2  Coding: Load a Single Text File**


In the first example, we’ll work with a Sherlock Holmes book
provided by Project Gutenberg. You’ll find this file in the subfolder
_05_VectorDatabases/data_ . We’ll work with books provided as _.txt_
files. Like Sherlock Holmes, we’ll find needles in the information
haystack.


Start by loading a single file, as follows:


1. Before we can import the data, we need to load some packages.

For dealing with the file location and operating system, we must
import the package `os` . To import our text, we’ll make use of the


class `TextLoader`, which is stored in the submodule

`langchain.document_loaders` .


2. We must define the link to the file path of the book file we want

to import. The file is in the top directory of the folder
_05_VectorDatabases_ . We can create this link by extracting the
current working directory `current_dir` to get the parent directory

`parent_dir` _._ Now, the file path is joined by stacking the parent
directory with the directory data and the book file we want to
import.


3. Now, we can start loading the file into an object we can work

with further. First, create an instance of `TextLoader` . During the
instantiation, pass the `file_path` parameter. This parameter is
essential. To import the data, you must also define the text
encoding. Text encoding is the process of converting humanreadable characters into a specific format that computers can
store, transmit, and understand, using standardized systems like
ASCII or UTF-8 to represent text as binary data. In this case, we
chose the `encoding` as `utf-8` . The object `text_loader` has a
method `load()`, which we then call. At that point, the loading of
the data is performed.


4. The import is complete, so let’s step back and look at we’ve

actually done. The object `doc` represents a list of type `Document` .
We only imported one file, so there is only one element with the
index 0. This one element has two properties: `metadata` and

`page_content` . Metadata refers to the source, in our case, the file
path. Page content refers to the actual text of the document we
imported.


The complete script
_05_VectorDatabases\10_DataLoader\10_single_text_file.py_ shows
the data loading from a single file, as shown in Listing 5.1.


```
#%% (1) Packages
import os
from langchain.document_loaders import TextLoader

#%% (2) File Handling
# Get the current working directory
file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(file_path)

# Go up one directory level
parent_dir = os.path.dirname(current_dir)

file_path = os.path.join(parent_dir, "data","HoundOfBaskerville.txt")
file_path

#%% (3) Load a single document
text_loader = TextLoader( file_path =file_path, encoding ="utf-8")
doc = text_loader.load()

#%% (4) Understand the document
# Metadata
doc[0].metadata

# %% Page content
doc[0].page_content

```

**Listing 5.1** Data Loading: Single File (Source:
05_VectorDatabases\10_DataLoader\10_single_text_file.py)


Great! We’ve managed to successfully load a single file into Python
and in a LangChain-specific format, which will enable the next steps
in process. Before we go to the next step, though, let’s look at how
you can load multiple text files.

### **5.3.3  Coding: Load Multiple Text Files**


Typically, you won’t deal with a single file, but with many files of the
same file type. Ideally, you can import all these files in a single
process. In our example, we want to import all text files stored in the
folder _05_VectorDatabases/data_ .


We must import the `DirectoryLoader`, which allows us to iterate over
the files in a folder, as follows:


```
#%% (1) Packages
import os
from langchain.document_loaders import TextLoader, DirectoryLoader
from pprint import pprint

```

The path to the folder with the files is defined with a relative file
location. If you set it up as shown in Listing 5.2, you have flexibility in
a way that the `current_directory` is extracted from the file path.

```
#%% (2) Path Handling
# Get the current working directory
file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(file_path)

# Go up one directory level
parent_dir = os.path.dirname(current_dir)
text_files_path = os.path.join(parent_dir, "data")

```

**Listing 5.2** Path Handling (Source:
05_VectorDatabases\10_DataLoader\20_multiple_text_files.py)


All files in the folder are loaded in a single process. The

`DirectoryLoader` is applied and consumes the `path` pointing to the
files. Using the `glob` parameter ensures that only specific files are
selected. In our example, only text files are considered. `loader_cls`
defines which loader to apply to the files. We use `TextLoader`, as
defined earlier in Section 5.3.2. Finally, we need to define the

`encoding` . We defined the encoding before in the `TextLoader` class
but want to do this here as well. We can pass it as `loader_kwargs` .


_Kwargs_ (short for “keyword arguments”) is a Python convention for
passing a variable number of named parameters to a function.
These parameters must be passed in a dictionary.


Listing 5.3 shows how to set up a `DirectoryLoader` that allows
iterating over all the files in a folder.

```
#%% (3) load all files in a directory
dir_loader = DirectoryLoader( path =text_files_path,
                 glob ="**/*.txt",
                 loader_cls =TextLoader,

```

```
                 loader_kwargs ={'encoding': 'utf-8'} )
docs = dir_loader.load()
docs

[Document(metadata={'source': '…', page_content='…'},
Document(metadata={'source': '…', page_content='…'},
Document(metadata={'source': '…', page_content='…'}]

```

**Listing 5.3** Directory Loader (Source:
05_VectorDatabases\10_DataLoader\20_multiple_text_files.py)

### **5.3.4  Exercise: Load Multiple Wikipedia Articles**


Now, let’s get to work. As shown in Listing 5.4, we have multiple
URLs for articles on artificial intelligence, artificial general
intelligence (AGI), and artificial superintelligence (ASI). At the end,
you want a list of LangChain `Documents` that correspond to the URLs.

```
#%% (1) Packages

#%% Articles to load
articles = [
{'title': 'Artificial Intelligence',
'query': 'https://en.wikipedia.org/wiki/Artificial_intelligence'},
{'title': 'Artificial General Intelligence',
'query': 'https://en.wikipedia.org/wiki/Artificial_general_intelligence'},
{'title': 'Superintelligence',
'url': 'https://en.wikipedia.org/wiki/Superintelligence'},
]

# %% (2) Load articles

```

**Listing 5.4** Data Loading Exercise: Multiple Wikipedia Articles (Source:
05_VectorDatabases\10_DataLoader\30_wikipedia_exercise.py437)


**Task 1: Package Loading**


One essential capability is working with online documentation. Your
first task is to find out if a `DocumentLoader` exists for Wikipedia articles
(hint: it does!) and how to load the package and class.


**Task 2: Article Import**


Next, you must write a loop to iterate over all the articles. You can
use the starter script available in
_05_VectorDatabases\10_DataLoader\30_wikipedia_exercise.py._
Listing 5.5 shows the content of the starter script.

```
#%% (1) Packages

#%% Articles to load
articles = [
{'title': 'Artificial Intelligence'},
{'title': 'Artificial General Intelligence'},
{'title': 'Superintelligence'},
]
# %% (2) Load all articles

```

**Listing 5.5** Data Loading Solution: Multiple Wikipedia Articles (Source:
05_VectorDatabases\10_DataLoader\30_wikipedia_exercise.py)


Solve this problem and fill in your own solution.


**Solution**


Listing 5.6 shows our solution to this exercise. Most notably, you
should have learned how to load the data directly from Wikipedia
with the help of `WikipediaLoader` . The remaining part is just iterating
over the `articles` object and how to create a list of documents by
appending to `docs` .

```
#%% Packages
from langchain.document_loaders import WikipediaLoader

#%% Articles to load
articles = [
{'title': 'Artificial Intelligence'},
{'title': 'Artificial General Intelligence'},
{'title': 'Superintelligence'},
]
# %% Load all articles (2)
docs = []
for i in range(len(articles)):
print(f"Loading article on {articles[i].get('title')}")

```

```
loader = WikipediaLoader(query=articles[i].get("title"),
load_all_available_meta=True,
doc_content_chars_max=100000,
load_max_docs=1)
doc = loader.load()
docs.append(doc)
docs

```

**Listing 5.6** Data Loading Solution: Multiple Wikipedia Articles: Loading (Source:
05_VectorDatabases\10_DataLoader\40_wikipedia_solution.py)

### **5.3.5  Exercise: Loading Project Gutenberg Book**


In the exercise file shown in Listing 5.7, you’ll find the book’s details
in a dictionary.

```
# %% The book details
book_details = {
"title": "The Adventures of Sherlock Holmes",
"author": "Arthur Conan Doyle",
"year": 1892,
"language": "English",
"genre": "Detective Fiction",
"url": "https://www.gutenberg.org/cache/epub/1661/pg1661.txt"
}

```

**Listing 5.7** Data Loading Exercise: Project Gutenberg (Source:
05_VectorDatabases\10_DataLoader\50_custom_loader_exercise.py)


**Task 1: Package Import**


As in the previous exercise, you should become familiar with the
online documentation and find out which package and class to
import for working with books from _[https://www.gutenberg.org/](https://www.gutenberg.org/)_ .
Project Gutenberg is an amazing resource because you’ll find
copyright-free classic books to work with.


**Task 2: Metadata Adaptation**


After loading the file, you’ll get a list of documents. Replace the
metadata of the `Document` object so that the dictionary of

`book_details` represents the metadata. Listing 5.8 shows the file’s
content, which consists of `book_details` .

```
# %% The book details
book_details = {
"title": "The Adventures of Sherlock Holmes",
"author": "Arthur Conan Doyle",
"year": 1892,
"language": "English",
"genre": "Detective Fiction",
"url": "https://www.gutenberg.org/cache/epub/1661/pg1661.txt"
}

```

**Listing 5.8** Exercise: Custom Loader (Source:
05_VectorDatabases\10_DataLoader\50_custom_loader_exercise.py)


**Solution**


Listing 5.9 shows how you can load the data from Project
Gutenberg.

```
from langchain_community.document_loaders import GutenbergLoader
# %% The book details
book_details = {
"title": "The Adventures of Sherlock Holmes",
"author": "Arthur Conan Doyle",
"year": 1892,
"language": "English",
"genre": "Detective Fiction",
"url": "https://www.gutenberg.org/cache/epub/1661/pg1661.txt"
}

loader = GutenbergLoader(book_details.get("url"))
data = loader.load()

#%% Add metadata from book_details
data[0].metadata = book_details

```

**Listing 5.9** Solution: Loading from Project Gutenberg (Source:
05_VectorDatabases\10_DataLoader\60_custom_loader_solution.py)


Now that you understand how to load data in different ways, let’s
move on to the next stage of the data ingestion pipeline—data
splitting.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **5.4  Splitting Documents**

Often, you need to split data into smaller chunks. Why is this step
needed? A couple of reasons include the following:


With splitting, you can get more _granular results_ because smaller
document chunks are more likely to contain focused and relevant
information.


You can work around limitations in embedding models. Don’t
worry, we’ll cover this in more depth later in Section 5.5. Recall all
embedding models have a _limited context window_ of tokens to
work with. We discuss tokens further in the next info box.


Splitting can be _more efficient_ in terms of database size and
querying because you are working and storing smaller chunks.


No doubt you’ve encountered the word “token,” so let’s briefly define
this concept. A _token_ is the fundamental unit of text in natural
language processing. Typically, a token is a word, a part of a word,
or sometimes even just a single character. The process of converting
a sentence into a list of tokens is called _tokenization_ . A crucial step in
preprocessing, many different tokenization methods are in operation.


Some examples might illustrate the process. In the sentence “I love
generative AI!”, the resulting tokens might be [“I”, “love”, “generative”,
“AI”, “!”]. In many tokenization methods, words are broken down into
multiple tokens. For instance, “loving” might be tokenized into [“lov”,
“ing”].


Why is tokenization performed? Tokens allow AI models to process
text by converting language into numerical representations that
models can understand. However, these numbers don’t carry


inherent meaning; they serve as a reference system for LLMs to
translate human language into a form computers can process. In the
next step, called embedding, these tokens are transformed into
vectors that capture semantic meaning, allowing the model to
interpret relationships between words and sentences. Embeddings
are covered later in Section 5.5.


For now, simply know that all embedding models have a limit on
tokens to process. If you try to pass more tokens into an embedding
model than it can process, it will cut off excess tokens. The meaning
of these extra tokens is lost. An essential strategy is to always pass
fewer tokens than a model can maximally process. As a rule of
thumb, one token is approximately equal to 0.75 words, or 100
tokens roughly equal 75 words in English language.


Finally, all models have limits on how much data can be processed
at once. This limitation of tokens is also called the _context window_ .




So far, we’ve covered documents that need to be split into smaller
chunks and described why defining a reasonable size for these
chunks is important. But how are the chunks created? Many different
approaches are available, but we’ll cover three popular methods. A
visual representation of data chunking is shown in Figure 5.5. The
first approach is to use a fixed chunk size and split a document after
a fixed number of characters is reached.


A more sophisticated approach is to follow the structure of the
document and allow for different sizes of chunks if doing so helps
retain the meaning of each chunk. Figure 5.5 shows a chat history of
two persons. If the chunks of two different persons overlapped,
understanding will be impacted negatively. Imagine you’re following
a conversation in a book, but the statements are partly attributed to
the wrong protagonists. The most advanced approach is _semantic_
_chunking_, in which the text is understood before the chunking is
performed.


**Figure 5.5** Chunking Strategies


Let’s start with the simplest approach, fixed-size chunking, next.

### **5.4.1  Coding: Fixed-Size Chunking**


Fixed-size chunking creates chunks after a predefined number of
characters has been reached. The cut occurs at the position of the
last word before the chunk size is exceeded. One advantage is the


simplicity of this approach; it is straightforward to understand and
implement. This approach is also quite fast, as it does not require
complex analysis of text meaning. Disadvantages include a lack of
context awareness. Sentences or concepts could be split midway,
thus resulting in a loss of semantic coherence.


**[+] Chunk Overlap**


A specialty that you should leverage is the chunk overlap. Chunk
overlaps refer to the amount of text that is shared between two
consecutive chunks, usually measured in characters or tokens.


The goal is to maintain the context between chunks and to
preserve the meaning, which otherwise could be lost when text is
arbitrarily divided.


A common rule of thumb is an overlap of 10% to 20%. This buffer
provides a good balance between context preservation and
database efficiency. But this suggestion is not dogma. Depending
on the type of text, more or less overlap could be reasonable.


Figure 5.6 shows the result of `CharacterTextSplitter` . Both chunks
are of equal size, and you can see the overlapping text in both
chunks.


**Figure 5.6** CharacterTextSplitter with Chunk Overlap


Since you now have a basic understanding, you can now implement
these concepts. In our example, we’ll go back to Sherlock Holmes
and extend our previous script from Section 5.3.5. The data loading
step is not shown again; we’ll jump in after the `docs` object has been
created.


Now, we need to load the functionality and use the class

`CharacterTextSplitter` for the `langchain` submodule `text_splitter`,
as shown in Listing 5.10. You can find the complete script in
_05_VectorDatabases\20_Chunking\10_fixed_size_chunking.py_ .

```
# ...
# %%
docs

# %% Splitting text
# Packages (1)
from langchain.text_splitter import CharacterTextSplitter

```

**Listing 5.10** Fixed-Size Chunking: Required Packages (Source: 05_VectorDatabases\
20_Chunking\10_fixed_size_chunking.py)


An instance of the class `CharacterTextSplitter` is created and
typically called `splitter` . In this instantiation, the parameters are
defined, for example, the chunk size (the maximum number of
characters in a chunk), the chunk overlap (the maximum overlap
characters in a chunk), and the separator (used for splitting):

```
# Split by characters (2)
splitter = CharacterTextSplitter( chunk_size =256, chunk_overlap =50,
separator =" ")

```

The split has not been performed yet but can now be done by calling
the method `splitter.split_documents` and passing the list of
documents. The result is again a list of `Document` objects, but the
number of elements has dramatically increased. Up to this point, we
had one `Document` per book. Now, each book has been separated
into many smaller pieces, as follows:

```
# %% Apply the splitting (3)
docs_chunks = splitter.split_documents(docs)

```

You can check the number of chunks to find out that it has increased
to 4,140 documents, as follows:

```
# %% Check the number of chunks (4)
len(docs_chunks)

```

By taking a closer look at two consecutive chunks, you can observe
the chunk overlap, which is the text shared between both chunks, as
shown in Listing 5.11.

```
# %% check some random Documents (5)
from pprint import pprint
pprint(docs_chunks[100].page_content)
# %%
pprint(docs_chunks[101].page_content)

```

**Listing 5.11** Fixed-Size Chunking: Document Check (Source:
05_VectorDatabases\20_Chunking\10_fixed_size_chunking.py)


Finally, as shown in Listing 5.12, you can look at the chunk sizes and
visualize the distribution of chunk lengths. In our example, most of
our chunks are centered around 250, which was expected.

```
# %% visualize the chunk size (6)
import seaborn as sns
import matplotlib.pyplot as plt
# get number of characters in each chunk
chunk_lengths = [len(chunk.page_content) for chunk in docs_chunks]

sns.histplot(chunk_lengths, bins =50, binrange =(100, 300))
# add title
plt.title("Distribution of chunk lengths")
# add x-axis label
plt.xlabel("Number of characters")
# add y-axis label
plt.ylabel("Number of chunks")

```

**Listing 5.12** Visualizing Fixed-Sized Chunking (Source:
05_VectorDatabases\20_Chunking\10_fixed_size_chunking.py)


The chunk length distribution is shown in Figure 5.7.


**Figure 5.7** Distribution of Chunk Lengths for Fixed-Size Chunking


Most chunks have 250 characters. Since the splitting is not
performed mid-word, some chunks are shorter, and some slightly


longer.

### **5.4.2  Coding: Structure-Based Chunking**


Contextual meaning or textual coherence usually does not follow
fixed sizes, so breaking a text into equal sizes doesn’t reflect reality
well. We need something more sophisticated. Typically, a text is
structured by an author into chapters, paragraphs, sentences, parts
of sentences, words, etc. One approach is breaking the text into
smaller pieces like chapters. If the remaining chunk is still too large,
it is broken down into subchapters, then paragraphs, and so on. This
approach ensures a good balance between textual coherence and
complying with character limits.


How can an algorithm detect a chapter or paragraph? That ability
depends on the choices the author of the text has made. Typically,
multiple empty lines exist before a new chapter starts. Between
paragraphs, typically smaller distances are used. Now, that you
understand how it works, let’s implement this capability in code.


Let’s break down our example, as shown in Table 5.2. On the left,
notice the formatting of the book chapters. After loading the

`Document`, get the property `page_content`, which is a single long

`String` .


**Table 5.2** Comparison of Raw Text Reprinted from a Book (Left) and Snippet of a
Corresponding Document Page Content (Right)


In this text, you’ll find special characters like _\n_ . This special
character indicates a line feed and results in breaking the text, so
that the following text starts at the beginning of a new line.


How can you know that _\n_ indicates a new line? This symbol is
defined in a character encoding standard (of which there are many).
A _character encoding standard_ is a system that creates a mapping
between a character like letters, numbers, or symbols and specific
code. The standard provides a universal character set that includes
all writing systems, emojis, and much more. The encoding allows
computers to store, transmit, and display text consistently. Famous
encoding standards include ASCII, UTF-8, or ISO‐8859-1. UTF-8 is
more modern than ASCII.


Let’s now build on the data we loaded earlier in Section 5.3.2. The
functionality we need is called `RecursiveCharacterTextSplitter`,
which is also part of the submodule `langchain.text_splitter`, as
follows:

```
# ...
#%% Recursive Chunking
# Packages (1)
from langchain.text_splitter import RecursiveCharacterTextSplitter

```

Now, create an instance of `RecursiveCharacterTextSplitter` class.
During instantiation, pass relevant parameters to the splitter,
specifically the `chunk_size` (the number of characters in a chunk) and
the `chunk_overlap` (the shared text between two consecutive
chunks). A vitally important parameter is the `separators` . The


separators are the characters used to create the breaks. They are
ordered from largest to smallest—we start with a separator for
chapters, then for paragraphs, and so on. When the first split was
not enough to constrain the chunk size to the chunk size limit,
another separator is sought for creating a further split. This process
is repeated until the chunk size is within the predefined limits, as
follows:

```
# %% Set up the splitter (2)
splitter = RecursiveCharacterTextSplitter( chunk_size =256,
                         chunk_overlap =50,
                         separators =["\n\n", "\n"," ", ".", ","])

```

The instance object `splitter` has a method `split_documents` in which
we’ll pass our list of documents. As a result, we receive a list of
documents, but the number of documents has increased
significantly.

```
# %% Create the chunks (3)
docs_chunks = splitter.split_documents(docs)
# %%
len(docs_chunks)

```

Check the chunk size distribution through a visualization, as shown
in Listing 5.14.

```
# %% Visualize the chunk size (4)
import seaborn as sns
import matplotlib.pyplot as plt
# get number of characters in each chunk
chunk_lengths = [len(chunk.page_content) for chunk in docs_chunks]

sns.histplot(chunk_lengths, bins =50, binrange =(0, 300))
# add title
plt.title("Distribution of chunk lengths (RecursiveCharacterTextSplitter)")
# add x-axis label
plt.xlabel("Number of characters")
# add y-axis label
plt.ylabel("Number of chunks")

```

**Listing 5.14** Chunk Size Visualization (Source:
05_VectorDatabases\20_Chunking\20_structure_based_chunking.py)


Figure 5.8 shows that the chunk sizes are now much more evenly
distributed compared to fixed-size splitting.


**Figure 5.8** Distribution of Chunk Lengths for Recursive Character Splitting


Notice that a wide range of chunk sizes is covered, ranging from
close to zero up to 250 characters. If due to this splitting approach, a
chunk is too small, chunks can also be aggregated to a decent size.
For simplicity, we won’t cover these steps. But the implementation is
straightforward—you might iterate over the complete list of chunks
and aggregate neighboring chunks if a chunk is too small and allow
the aggregation with a neighboring chunk if doing so is still within
allowed chunk size.

### **5.4.3  Coding: Semantic Chunking**


Up to this point, chunking was performed based on chunk sizes
(fixed-size chunking) and somewhat taking the structure of the text
into account (structure-based chunking). But the actual text was not
considered at all, which is how semantic chunking is performed.


In this approach, the text we want to split is at first split into individual
sentences. Then, the sentences are embedded. Don’t worry, we’ll
cover this topic soon, in Section 5.5. For now, simply understand
that, afterwards, the sentences are converted into numerical vectors,
with which certain calculations can be made. For example, the
similarities between consecutive sentences can be calculated. The
idea is to split at natural breaks—when sentences are too different in
their meaning. For this task, a _distance matrix_ is created and
analyzed. If you ever worked with distances matrices before, you
know that multiple approaches exist to calculate distance.
Subsequently, multiple ways exist to calculate the breakpoints that
define when a split should be performed. This general idea of
semantic chunking is shown in Figure 5.9.


**Figure 5.9** Semantic Chunking


This approach preserves the semantic meaning of sentences and
keeps related concepts together. It improves upon the information
retrieval process and the accuracy of searches. Furthermore,
semantic chunking is adaptable in the way that it adjusts the chunk
sizes based on the text, resulting in chunks that are more natural
and easier for humans to read and to understand.


But downsides also exist. For one, semantic chunking adds some
computational overhead and is slower. Note also that embedding
requires you to run a neural network either locally, or you need to
apply an embedding model like from OpenAI. As a result, some cost


is incurred for creating the embeddings, although embedding models
is comparably cheap. Latency and higher system complexity are
factors that might also play an important role.


Let’s get back to coding and find out how this works. The script that
we’ll develop can be found in
_05_VectorDatabases\20_Chunking\30_semantic_chunking.py_ .


The semantic chunker has not been promoted yet to the `langchain`
main package and is found in `langchain_experimental` . For loading a
Wikipedia article, you can apply `WikipediaLoader` . For creating the
embeddings, use OpenAI’s `langchain_openai` package. You’ll need
an OpenAI account to use OpenAI services as well as an application
programming interface (API) key in a file called _.env_, which is stored
in the same folder as the script. Finally, load the script via

`load_dotenv`, as shown in Listing 5.15.

```
#%% Packages (1)
from langchain_experimental.text_splitter import SemanticChunker
from langchain.document_loaders import WikipediaLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from pprint import pprint
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv( usecwd =True))

```

**Listing 5.15** Semantic Chunking: Required Packages (Source:
05_VectorDatabases\20_Chunking\30_semantic_chunking.py)


Now, we can load the article, and for this step, we’ll set up an
instance of `WikipediaLoader` and pass several parameters (like the
article title) to the parameter `query` . We don’t want to load further
articles that are mentioned, so we’ll limit it with the parameter

`load_max_docs` . Also, for demonstration purposes, we’ll also limit the
number of characters with the parameter `doc_content_chars_max`, as
shown in Listing 5.16.

```
# %% Load the article (2)
ai_article_title = "Artificial_intelligence"

```

```
loader = WikipediaLoader( query =ai_article_title,
                 load_all_available_meta =True,
                 doc_content_chars_max =1000,
                 load_max_docs =1)
doc = loader.load()

```

**Listing 5.16** Semantic Chunking: Data Loading (Source:
05_VectorDatabases\20_Chunking\30_semantic_chunking.py)


After loading, let’s check that everything worked. We have our `doc`
object, which is a list with just one `Document` . Thus, we need to
access `doc[0].page_content` to retrieve the contents of that article,
as follows:

```
# %% check the content (3)
pprint(doc[0].page_content)

```

Now, we’ve come to an interesting area. We’ll set up our

`SemanticChunker` instance, as shown in Listing 5.17. The semantic
chunker works with any embedding, in our case, `OpenAIEmbeddings` .
Different methods exist to calculate the similarities between texts,
and we’ll apply cosine similarity together with a threshold of 0.5 to
split our texts. We’ll cover similarity calculations in Section 5.7.1 in
much more detail. At this point, simply know that we need to analyze
the semantic meaning of neighboring sentences, which is performed
based on similarities.

```
# %% Create splitter instance (4)
splitter = SemanticChunker( embeddings =OpenAIEmbeddings(),
                breakpoint_threshold_type ="cosine",
                breakpoint_threshold =0.5)

```

**Listing 5.17** Semantic Chunking: Chunking (Source:
05_VectorDatabases\20_Chunking\30_semantic_chunking.py)


The semantic splitter operates on the article, and we store the
resulting split text in an object called `chunks`, as follows:

```
# %% Apply semantic chunking (5)
chunks = splitter.split_documents(doc)

```

Finally, we can compare the contents of the first chunk and the
second chunk to see at which position the split was performed (see
Listing 5.18).

```
# %% check the results (6)
chunks
# %%
pprint(chunks[0].page_content)
# %%
pprint(chunks[1].page_content)

```

**Listing 5.18** Semantic Chunking: Document Check (Source:
05_VectorDatabases\20_Chunking\30_semantic_chunking.py)

### **5.4.4  Coding: Custom Chunking**


The text splitters we’ve covered so far provide a lot of flexibility but
sometimes are still not enough. You may need to define a custom
splitter to fit your specific needs.


In this example, we’ll work with another Sherlock Holmes book file,
but this book file consists of 12 books. Of course, we could just go
ahead and split the text, but we want to extract certain information,
like the book’s title, and store it alongside the chunks. This specific
information will be extremely helpful at some point later. When we
interact with the book and ask questions, we might want to know
how Sherlock Holmes solved the case of “A Scandal in Bohemia,” for
instance. Then, we can filter first for the book of interest and then get
the information we are interested in. You’ll see this capability in
action in Section 5.7 when you learn how to retrieve data.


You can find this code in
_05_VectorDatabases\20_Chunking\40_custom_splitter.py_ . The book
with the title “The Adventures of Sherlock Holmes” itself holds twelve
different books about Sherlock Holmes, and we want to extract all
the titles from the file.


As always, we start by loading packages. The LangChain community
helps in this case because there is a `loader` class for our purposes,
as shown in Listing 5.19.

```
#%% Packages
import re
from langchain.text_splitter import CharacterTextSplitter,
RecursiveCharacterTextSplitter
from langchain_community.document_loaders import GutenbergLoader

```

**Listing 5.19** Custom Chunking: Required Packages (Source:
05_VectorDatabases\20_Chunking\40_custom_splitter.py)


Listing 5.20 shows how to load the data directly via the class

`GutenbergLoader` .

```
# %% The book details
book_details = {
"title": "The Adventures of Sherlock Holmes",
"author": "Arthur Conan Doyle",
"year": 1892,
"language": "English",
"genre": "Detective Fiction",
"url": "https://www.gutenberg.org/cache/epub/1661/pg1661.txt"
}
loader = GutenbergLoader(book_details.get("url"))
data = loader.load()

```

**Listing 5.20** Custom Splitter: Data Loading (Source:
05_VectorDatabases\20_Chunking\40_custom_splitter.py)


The result is a list of documents in which we only have one `Document`
object, as follows:

```
[Document(metadata={'title': 'The Adventures of Sherlock Holmes', 'author':…}

```

We want to keep all the metadata and extend the existing metadata
of the `Document` object with our dictionary, as follows:

```
#%% Add metadata from book_details
data[0].metadata = book_details

```

By inspecting the file, we can see that each book title follows a
similar structure. For example, for the second book, the first text


looks like the following:

```
('II. THE RED-HEADED LEAGUE\r\n'
'\n'
'\n'
'\r\n'

```

Knowing the inner structure of text pieces is important because you
can use those structures by setting up a pattern that matches all
titles. The logic behind this pattern matching is called _regular_
_expressions_, which is large topic you can add to your already long
to-do list, or you can do what we do: copy the text and ask an large
language model (LLM) to create the corresponding regular
expression to split the text whenever a title is detected. This
approach is shown in Listing 5.21 with the function `custom_splitter` .
Afterwards, we’ll overwrite the `split_text` method of our

`text_splitter` object and replace it with our own `custom_splitter`
method.

```
# %% Custom splitter
def custom_splitter( text ):
# This pattern looks for Roman numerals followed by a title
pattern = r '\n(?=[IVX]+\.\s[A-Z])'
return re.split(pattern, text)

text_splitter = CharacterTextSplitter(
  separator ="\n",
  chunk_size =1000,
  chunk_overlap =200,
  length_function =len,
  is_separator_regex =False,
)
# Override the default split method
text_splitter.split_text = custom_splitter

```

**Listing 5.21** Custom Splitter: Function (Source:
05_VectorDatabases\20_Chunking\40_custom_splitter.py)


Great! Let’s try it out by calling the `split_documents` method, which
itself inherits from the `split_text` method. We’ll create an object for

`books`, as follows:


```
# Assuming you have the full text in a variable called 'full_text'
books = text_splitter.split_documents(data)

```

This object has 13 documents. The first document does not refer to
any Sherlock Holmes book, so we disregard it using the following:

```
# %% remove the first element, because it only holds metadata, not real books
books = books[1: ]

```

Next, as shown in Listing 5.22, for each book inside `books`, we want
to extract the correct title. Again, we’ll use a regular expression:
Whenever the pattern is matched in the text, the title is extracted and
added to the metadata.

```
#%% Extract the book title from beginning of page content
for i in range(len(books)):
print(i)
# extract title
pattern = r '\b[IVXLCDM]+\.\s+([A-Z\s\-]+)\r\n'
match = re.match(pattern, books[i].page_content)
if match:
title = match.group(1).replace("\r", "").replace("\n", "")
print(title)
# add title to metadata
books[i].metadata["title"] = title
print(title)

```

**Listing 5.22** Custom Splitter: Extract The Book Title (Source:
05_VectorDatabases/20_Chunking\40_custom_splitter.py)


We’re nearly done. Now, `books` is a list of documents, each of which
has the correct title in its metadata, as follows:

```
[Document(metadata={'title': 'A SCANDAL IN BOHEMIA', …,
Document(metadata={'title': 'THE RED-HEADED LEAGUE', …,
…]

```

The next steps we’ve covered before. We’ll apply a recursive
character text splitter to create chunks of a predefined maximum
chunk size and predefined chunk overlap, as shown in Listing 5.23.

```
# %% apply RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
  chunk_size =1000,

```

```
  chunk_overlap =200,
  length_function =len,
  is_separator_regex =False,
)
chunks = text_splitter.split_documents(books)

```

**Listing 5.23** Custom Splitter: Applying Recursive Character Text Splitter (Source:
05_VectorDatabases\20_Chunking\40_custom_splitter.py)


Thus concludes our section on data splitting; we’ll move on to the
next stage in the data ingestion process—embeddings.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **5.5  Embeddings**

Let’s visualize where we are in the process. We’ve loaded one or
more documents. We’ve broken them down into small manageable
pieces. But up to this point, we’re dealing with texts—humanreadable texts. We need to translate this text into a machineunderstandable representation of text in a process called
_embedding_ . As shown in Figure 5.10, text chunks are converted into
numerical vectors.


**Figure 5.10** Embedding Process


In Section 5.4, you learned what an embedding vector was. A short
recap: an embedding is a numerical vector that represents the
meaning of a word or of a complete sentence or paragraph. This
vector does not have the two or three dimensions that we know from
math class but instead can have hundreds or even thousands of
dimensions. This expansiveness is necessary to grasp the complete
meaning of the text to be understood.


In this section, you’ll learn how embeddings are created and see
how similar words are closer to each other in a two-dimensional
representation. By the end of this section, you’ll know the following:


About types of embeddings


How embeddings are created


Which embedding models you can use


First things first, which types of embeddings are out there?

### **5.5.1  Overview**


In this book, we’ll mainly embed complete sentences, but the
concept of embeddings is not limited to texts. These other data
modalities can also be embedded:


**Image embeddings**
You can embed complete images.


**Audio embeddings**
Sounds like voices or music can be embedded into a numerical
representation.


**Video embeddings**
Videos are just a combination of audio signals and a sequence of
images, so it won’t surprise you that video embeddings are
possible.


**Graph embeddings**
A famous concept in machine learning (ML) is a graph. _Graphs_
consist of nodes, edges, and features. For specific data, graphs
are the preferred type of data representation. Graphs can be
embedded as well.


**Multimodal embeddings**
Different data modalities like text data and image data can be
embedded in a shared, unified vector space. One example is
OpenAI’s CLIP model, which allows the simultaneous embedding
of images and their corresponding texts.


Knowing that you can embed these different data types is great, but
why would you do that? What are real-world applications of
embeddings? We cannot overstate how important embeddings are
to generative AI. Embeddings are at the core of LLMs, and
everything is built upon LLMs. But their impact reaches even further:


_Natural language processing (NLP)_ models use text embeddings.


In _computer visio n,_ embeddings model image meaning.


_Retrieval-augmented generation (RAG)_ applications are built upon
_semantic search_ . Both rely on embeddings to efficiently retrieve
relevant chunks.


Products and their features are embedded, and thus embedding
models are applied in _recommendation_ engines.


**State of the Art Embeddings Models**


Progress in generative AI is massive, so a static list of models in
this book would be quickly outdated. Instead, we want to refer you
to resources that provide state-of-the-art rankings. The Massive
Text Embedding Benchmark (MTEB) leaderboard at
_[https://huggingface.co/spaces/mteb/leaderboard](https://huggingface.co/spaces/mteb/leaderboard)_ is a space on
Hugging Face that ranks several embedding models by different
parameters. MTEB based on 8 embedding tasks and 58 datasets
in 112 languages.


What are the important metrics to consider when choosing an
embedding model? A very important aspect is the _performance_ of the
model. On the MTEB leaderboard, you can choose between several
different performance metrics like average performance over 56
datasets. Task-specific performance metrics are available for
comparing performance in, for example, classification or clustering.


When self-hosting a model, relevant information to consider include
_model size_ and _memory usage_ .


Depending on the text you’re dealing with, you’ll need to define a
proper chunk size. Then, you must ensure that the chunk size is
below _max tokens_ limit of the model.


Another important aspect to consider is the _price_ . Many companies
offer access to their models via APIs. While many embedding
models are open source and free to use, running them on internal
company resources can be costly. The server must run 24/7, must
have ideally a good GPU for quick inferences, and must consume
energy. Thus, both fixed and variable costs are associated with that
approach. You also must maintain an additional system. On the plus
side, however, you won’t have any _data privacy_ concerns because
your company’s data won’t leave your own network.

### **5.5.2  Coding: Word Embeddings**


Always remember that the main purpose of embedding is to capture
the semantic meanings of words. You can even visualize meaning
and see how words that are similar are closer to each other than
random words. How is this achieved?


The breakthrough idea was an algorithm called a _skip-gram_
_algorithm_ . As shown in Figure 5.11, the main idea is simple in
retrospect. An actual text like a book is used as training data. The
focus is always on several words, let’s say, five words. We start with
the first five words, then the focus is shifted by a word to words 1
through 6, then words 2 through 7, and so on.


Of the current focus on five words, the central word is the target
feature, and the two neighboring words to the left and the right are


independent features in a neural network model. The independent
features are used to predict the target feature. For example, if the
current focus is on five words like “It was a bright cold …,” then the
central word “a” is considered the target, and the other words are
used to predict that word. The intuition behind this approach is that a
word is described by the context in which it is used.


**Figure 5.11** Skip-Gram Example


The corresponding algorithm is called Word2vec, which is an early
word embedding model. The information box covers some other
popular models.


**[+] History of Word Embedding Models**


_Word2vec_ was developed by Google in 2013 and sparked much
interest in word embeddings.


In 2014, Stanford researchers created _GloVe_ which stands for
Global Vectors for Word Representation. Its performance is
comparable to Word2vec.


Facebook joined the party in 2016 when it released _FastText_ . This
extension of Word2vec can handle even out-of-vocabulary words
and thus was useful for languages with many words.


The most influential model is _BERT (bidirectional encoder_
_representations from transformers)_ . This model was developed by


Google researchers in 2018 and is based on transformer
architecture. BERT is still one of the most popular word
embedding models.


We’ll download the model embeddings for all embedded words and
visually demonstrate how similar words are closer than random
words. Let’s develop a graph. The code file is
_05_VectorDatabases\30_Embedding\10_word2vec_similarity.py_ .


We’ll use `gensim` for getting Word2vec embeddings, as shown in
Listing 5.24. Seaborn is used for creating visualization. For plotting
the data, we must reduce the dimensions to two dimensions and use

`PCA` from `sklearn` for this task.

```
#%% (1) Packages
import gensim.downloader as api # Package for downloading word vectors
import random # Package for generating random numbers
import seaborn.objects as so # Package for visualizing the embeddings
from sklearn.decomposition import PCA # import PCA
import numpy as np
import pandas as pd

```

**Listing 5.24** Word Embeddings: Required Packages (Source:
05_VectorDatabases\30_Embedding\10_word2vec_similarity.py)


Next, we’ll load Word2vec embeddings. This step might take a while
because the `word2vec-google-news-300` model is 1.5 GB.

```
# %% (2) import GloVe word vectors
word_vectors = api.load("word2vec-google-news-300")

```

In our example, we’ll study the word “mathematics,” but you’re free
to play around and choose your own word. The `shape` property is
checked, and we can confirm that the embedding has 300
dimensions, as follows:

```
# %% (3) get the size of the word vector
studied_word = 'mathematics'
word_vectors[studied_word].shape

```

To get some impression of the embeddings, let’s look at them. What
we have is a vector of 300 double numbers, as follows:

```
# %% (4) get the word vector for the word 'intelligence'
word_vectors[studied_word]

```

You can use the method `most_similar` to get the words most similar
to the word under study. (We haven’t covered how this similarity is
calculated, which we’ll discuss in detail in Section 5.7.1.)

```
# %% (5) get similar words to 'intelligence'
word_vectors.most_similar(studied_word)

```

Finally, we’ll limit our example to the five most similar words, as
follows:

```
# %% (6) get a list of strings that are similar to 'intelligence'
words_similar = [w[0] for w in word_vectors.most_similar(studied_word)][:5]

```

Now, we’ll pick 20 words from random positions in the embedding
model, as shown in Listing 5.25.

```
# %% (7) get random words from word vectors
num_random_words = 20
all_words = list(word_vectors.key_to_index.keys())
# set the seed for reproducibility
random.seed(42)
random_words = random.sample(all_words, num_random_words)

# Print the random words
print("Random words extracted:")
for word in random_words:
print(word)

```

**Listing 5.25** Word Embedding: Get Random Words (Source:
05_VectorDatabases\30_Embedding\10_word2vec_similarity.py)


We have 20 random words, and 5 words like “mathematics.” For
these 25 words, we extract the embeddings and store them in a
NumPy array of dimensions (25, 300), as shown in Listing 5.26.

```
# %% (8) get the embeddings for random words and similar words
words_to_plot = random_words + words_similar
embeddings = np.array([])

```

```
for word in words_to_plot:
embeddings = np.vstack([embeddings, word_vectors[word]]) if embeddings.size else
word_vectors[word]

```

**Listing 5.26** Word Embedding: Get Embeddings (Source:
05_VectorDatabases\30_Embedding\10_word2vec_similarity.py)


Typically, plots are two-dimensional, so we’ll stick to that. Since we
cannot visualize a 300-dimensional vector, we must reduce the
dimensions to a manageable size, as shown in Listing 5.27, using
principal component analysis (PCA). Several dimension reduction
techniques are available, one of the most popular is PCA, which will
do the job for us.

```
# %% (9) create 2D representation via PCA
pca = PCA( n_components =2)
embeddings_2d = pca.fit_transform(embeddings)

df = pd.DataFrame(embeddings_2d, columns =["x", "y"])
df["word"] = words_to_plot
# red for random words, blue for similar words
df["color"] = ["random"] * num_random_words + ["similar"] * len(words_similar)

```

**Listing 5.27** Word Embedding: Principal Component Analysis (Source:
05_VectorDatabases\30_Embedding\10_word2vec_similarity.py)


Finally, we plot the words with `seaborn`, as shown in Listing 5.28. If
you haven’t yet worked with Seaborn’s new _grammar-of-graphics_
_approach_, refer to
_[https://seaborn.pydata.org/tutorial/objects_interface.html](https://seaborn.pydata.org/tutorial/objects_interface.html)_ . This
approach is novel, and we recommend it over a classic graph setup
because the grammar-of-graphics approach stacks layers of
meaning together and thus has some similarity to neural networks.

```
# %% (10) visualize the embeddings using seaborn
(so.Plot(df, x ="x", y ="y", text ="word", color ="color")
.add(so.Text())
.add(so.Dots())
)

```

**Listing 5.28** Word Embedding: Visualization (Source:
05_VectorDatabases\30_Embedding\10_word2vec_similarity.py)


The result of our work on word embeddings and on plotting similar
words in two dimensions is shown in Figure 5.12.


Words that are like “mathematics” are shown in one color, while the
random words are shown in a different color. Similar words are much
closer to each other than random words. This result is what we
wanted because it means that the semantic meanings of words are
represented by the embeddings.


**Figure 5.12** Word2vec for Random Words and Words Similar to “mathematics”


Now that we have numerical representations, we can work with them
and visualize relationships. In the examples shown in Listing 5.29,
we can create relationships between capitals and their
corresponding countries. We’ll get the embeddings for Berlin, Paris,
Madrid and for the countries Germany, France, and Spain. Then,
we’ll reduce the dimensions of the embeddings, again via PCA, and
plot the connections between capital and country as a vector.

```
# %% visualizing it via lines
df_arithmetic = pd.DataFrame({'word': ['paris', 'germany', 'france', 'berlin',
'madrid', 'spain']})
# add embeddings and add x- and y-coordinates for PCA
pca = PCA( n_components =2)
embeddings_arithmetic = np.array([])
for word in df_arithmetic['word']:
embeddings_arithmetic = np.vstack([embeddings_arithmetic, word_vectors[word]])

```

```
if embeddings_arithmetic.size else word_vectors[word]

# apply PCA
embeddings_arithmetic_2d = pca.fit_transform(embeddings_arithmetic)
df_arithmetic['x'] = embeddings_arithmetic_2d[:, 0]
df_arithmetic['y'] = embeddings_arithmetic_2d[:, 1]

#%% visualise it via matplotlib with lines
import matplotlib.pyplot as plt
plt.figure( figsize =(10, 10))
plt.scatter(df_arithmetic['x'], df_arithmetic['y'], marker ='o')

# add vector from paris to france, and berlin to germany
plt.arrow(df_arithmetic['x'][0], df_arithmetic['y'][0],
df_arithmetic['x'][2] - df_arithmetic['x'][0],
df_arithmetic['y'][2] - df_arithmetic['y'][0],
       head_width =0.01, head_length =0.01, fc ='r', ec ='r')
plt.arrow(df_arithmetic['x'][3], df_arithmetic['y'][3],
df_arithmetic['x'][1] - df_arithmetic['x'][3],
df_arithmetic['y'][1] - df_arithmetic['y'][3],
       head_width =0.01, head_length =0.01, fc ='r', ec ='r')
plt.arrow(df_arithmetic['x'][4], df_arithmetic['y'][4],
df_arithmetic['x'][5] - df_arithmetic['x'][4],
df_arithmetic['y'][5] - df_arithmetic['y'][4],
       head_width =0.01, head_length =0.01, fc ='r', ec ='r')
# add labels for words
for i, txt in enumerate(df_arithmetic['word']):
plt.annotate(txt, (df_arithmetic['x'][i], df_arithmetic['y'][i]))

```

**Listing 5.29** Word2vec Embeddings and Vector Representations (Source:
05_VectorDatabases\30_Embedding\10_word2vec_similarity.py)


The output of our vector embedding of capitals and countries is
shown in Figure 5.13.


**Figure 5.13** Word2vec PCA Representation of Capitals and Countries


The vectors always have a similar direction. You can make use of
these relationships and work with these vectors, as shown in
Listing 5.30. For instance, consider the following equation:


Paris – France + Germany = ???

```
# Paris - France + Germany = Berlin
word_vectors.most_similar( positive = ["paris", "germany"],
                negative = ["france"], topn =1)

```

**Listing 5.30** Word2vec Algebraic Calculations (Source:
05_VectorDatabases\30_Embedding\10_word2vec_similarity.py)


The equation should result in `Berlin` .


At this point, we can embed single words, which is great, but some
issues arise as soon as we try working with complete sentences.
Look at the two sentences. Both contain the word “bank,” but both
instances have completely different meanings:


Sentence 1: “I need to go to the _bank_ to deposit this check.”


Sentence 2: "We had a picnic on the _bank_ of the river.”


We can thus conclude that the meaning of a word depends on the
context in which it is used. A single embedding for the word _bank_
does not make sense. Thus, we need to find an approach for
complete sentences.

### **5.5.3  Coding: Sentence Embeddings**


Sentence embedding models are quite similar to word embedding
models. However, instead of consuming a word and providing its
embedding vector, you can now pass a complete sentence to the
model and get an embedding vector that represents the complete
sentence. Earlier, we mentioned how BERT was one of the most
influential word embedding models. Don’t get confused by the fact
that there are variants of BERT that can consume sentences and
complete paragraphs. A typical BERT sequence is shown in
Figure 5.14.


**Figure 5.14** Sample Sentence Tokenization with BERT


We write a sentence, pass it through the tokenizer (not yet the
embedding model), and get a tokenization. Each word of our
sentence is tokenized. Also, the period is tokenized by itself. But you
can also observe two new tokens: [CLS] and [SEP]. The [SEP] token
separates each sentence. More interesting is the [CLS] token, short
for “classification token” or sometimes “class token.” This special
token is used in transformer-based models, especially in BERT. Its
purpose is to aggregate information from an entire input sequence.

[CLS] is typically located as the first token in the input sequence,
before the actual content tokens. This token learns to encode the
sentence-level or paragraph-level information. In the original BERT
paper, the authors suggested using the final hidden state of the

[CLS] token as the sentence embedding. Other approaches exist as
well, but we just wanted to give you some idea of how the meaning
of a sentence might be handled by the models.


The actual use of sentence embedding models is rather simple, as
you’ll see soon. We’ll embed a few sentences and afterwards check
their correlations. The corresponding code file is
_05_VectorDatabases\30_Embedding\20_sentence_similarity.py._


A new package is used in this example, `sentence_transformers`, as
shown in Listing 5.31. Via this package, you’ll have access to many
different models focusing on embedding complete sentences.

```
#%% (1) Packages
from sentence_transformers import SentenceTransformer
import numpy as np
import seaborn as sns

```

**Listing 5.31** Sentence Embedding: Required Packages (Source:
05_VectorDatabases\30_Embedding\20_sentence_similarity.py)


We’ll use an embedding model that can handle multiple languages
and create an instance of that model. The chosen model has an


embedding size of 512, so each sentence is transformed into a 512dimensional vector, as follows:

```
#%% (2) Load the model
MODEL = 'sentence-transformers/distiluse-base-multilingual-cased-v1'
model = SentenceTransformer(MODEL)

```

Eight example sentences are chosen, as shown in Listing 5.32. Feel
free to define your own sentences. The first three are pretty similar to
each other. They have similar meanings although they use different
words to describe a situation. The same can be said about the last
three sentences. They are in fact translations from English into
French and German. The other sentences are very different.

```
# %% (3) Define the sentences
sentences = [
'The cat lounged lazily on the warm windowsill.',
'A feline relaxed comfortably on the sun-soaked ledge.',
'The kitty reclined peacefully on the heated window perch.',
'Quantum mechanics challenges our understanding of reality.',
'The chef expertly julienned the carrots for the salad.',
'The vibrant flowers bloomed in the garden.',
'Las flores vibrantes florecieron en el jardín. ',
'Die lebhaften Blumen blühten im Garten.'
]

```

**Listing 5.32** Sentence Embeddings: Sample Sentences (Source:
05_VectorDatabases\30_Embedding\20_sentence_similarity.py)


We create the embeddings by calling the `encode` method of our
model and passing our list of sentences. Checking the structure of
the data is always helpful. We have 8 sentences, and earlier, we
found the embedding size of our model. Thus, our embeddings have
the shape of (8, 512), as follows:

```
# %% (4) Get the embeddings
sentence_embeddings = model.encode(sentences)

```

Let’s say we want to visualize the correlation between the
sentences. For this task, we’ll calculate the correlation coefficient
between the eight different sentences first, as shown in Listing 5.33.


```
# %% (5) Calculate linear correlation matrix for embeddings
sentence_embeddings_corr = np.corrcoef(sentence_embeddings)
import seaborn as sns
# show annotation with one digit
sns.heatmap(sentence_embeddings_corr, annot =True,
       fmt =".1f",
       xticklabels =sentences,
       yticklabels =sentences)

```

**Listing 5.33** Sentence Embeddings: Correlation and Visualization (Source:
05_VectorDatabases\30_Embedding\20_sentence_similarity.py)


Our result, shown in Figure 5.15, is an 8 × 8 matrix that you can
visualize with Seaborn.


Notice the high correlation coefficients in the upper-left corner of the
graph. These high values reflect the similarity of the first three
sentences. Similarly, you can observe high correlation coefficients in
the bottom right of the graph. These three sentences have the exact
same meaning; they are just formulated in three different languages.
Since we applied an embedding model that is trained on datasets
from different languages, it can understand multiple languages. We
can conclude that a multilingual model does not care about
languages, only about meaning. The other sentences are added just


for comparison. They show that sentences that are very different
have correlation coefficients around zero.


**Figure 5.15** Sentence Embeddings Correlations (Source:
05_VectorDatabases/30_Embedding/20_sentence_similarity.py)

### **5.5.4  Coding: Create Embeddings with LangChain**


Earlier in Section 5.3.4, we loaded an article from Wikipedia on
artificial intelligence. We’ll continue with this example and extract the
text from our list of `Document` objects, so that each text is embedded.
We’ll start by extending some boilerplate code available in
_05_VectorDatabases/30_Embedding/30_wikipedia_embeddings.py_ .


In this code, we’ll load an additional class to enable the use of
OpenAI embeddings. The remainder of the code should by now be
familiar to you. The Wikipedia article on artificial intelligence is
loaded, and subsequently split.


We’ll use OpenAI embeddings, for which you’ll need an API key from
OpenAI stored in the _.env_ file. This file is loaded with `load_dotenv()`,
as shown in Listing 5.34.

```
#%% Packages
from langchain.document_loaders import WikipediaLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from pprint import pprint
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv( usecwd =True))

```

**Listing 5.34** Required Packages (Source:
05_VectorDatabases/30_Embedding/30_wikipedia_embeddings.py)


From Wikipedia, we’ll load an article on “Artificial Intelligence,” as
shown in Listing 5.35.

```
# %% Load the article
ai_article_title = "Artificial_intelligence"
loader = WikipediaLoader( query =ai_article_title,
                 load_all_available_meta =True,
                 doc_content_chars_max =10000,
                 load_max_docs =1)
doc = loader.load()

```

**Listing 5.35** Loading the Article (Source:
05_VectorDatabases/30_Embedding/30_wikipedia_embeddings.py)


The `Document` object is split into chunks, as shown in Listing 5.36.
You know this step by now.

```
# %% Create splitter instance
splitter = RecursiveCharacterTextSplitter( chunk_size =1000,
                          chunk_overlap =200,
                          separators =["\n\n", "\n"," ", ".", ","])

# %% Apply semantic chunking
chunks = splitter.split_documents(doc)
# %% Number of Chunks
len(chunks)

16

```

**Listing 5.36** Creating Text Chunks (Source:
05_VectorDatabases/30_Embedding/30_wikipedia_embeddings.py)


As a result, we have 16 chunks that we’ll embed. But first we must
create an instance of the embedding class. In this step, we can apply
an OpenAI embedding model `text-embedding-3-small` . Although
small is not quite accurate; this embedding model has 1,536
dimensions. You might also use its big brother `text-embedding-3-`

`large`, which has 3,072 dimensions.

```
# %% Create instance of embedding model
embeddings_model = OpenAIEmbeddings( model ="text-embedding-3-small")

```

We cannot simply pass a list of documents into the model. We’ll use
the method `embed_documents`, which has one required parameter

`text` . This parameter is expected to be a list of strings. Thus, you
must extract the `page_content` from each chunk and store this
content in the object `texts` . This object is passed as parameter to the
embedding model to create the embeddings, as follows:

```
# %% extract the texts from "page_content" attribute of each chunk
texts = [chunk.page_content for chunk in chunks]
# %% create embeddings
embeddings = embeddings_model.embed_documents( texts =texts)

```

Amazing! You can check that the length of this object (16)
corresponds to the number of text strings we passed to the
embedding model, as shown in Listing 5.37. Thus, for each text, an
embedding vector was created that has 1,536 dimensions.

```
# %% get number of embeddings
len(embeddings)

16
# %% check the dimension of the embeddings
len(embeddings[0])

1536

```

**Listing 5.37** Embeddings: Dimensions (Source:
05_VectorDatabases/30_Embedding/30_wikipedia_embeddings.py)


Thus concludes our section on embeddings. Let’s proceed with the
next step of the pipeline and learn how to store data in a vector
database.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **5.6  Storing Data**

We are reaching our final state of the data ingestion pipeline. Let’s
recap what we’ve achieved so far. First, we loaded some documents.
Second, we created smaller chunks out of a large text corpus. Third,
we learned how to create vector embeddings based on text chunks.
So now, we can store them in a database.


You have multiple options to store the data. The main decision you
must make is whether you want to host your own vector database
locally or if you want to rely on web-based service providers. Both
approaches have their pros and cons.

### **5.6.1  Selection of a Vector Database**


The basic functionality of a vector database is handled similarly by
different providers. But they all have their unique selling propositions;
the data you want to cover and your requirements will determine the
best fit. Some parameters to consider include the following:


**Location**
As mentioned earlier, some databases can store your data locally
(e.g., in a Chroma database), while others are web-based
services (e.g., Pinecone and Weaviate).


**Data protection**
Depending on the type of data, and the customer you’re working
with, your data might be highly sensitive, and you might need to
avoid online services altogether or avoid a specific region. In such
cases, you might consider using a local vector database rather
than an online service like Pinecone or Weaviate.


**Price**
The cost of a service is always a driving factor. Determining the
overall price might not be a straightforward task. Although local
open-source vector databases might be free of charge, you need
to maintain an additional server and equip it with the proper
hardware for fast embedding. Basically, you’ll trade higher upfront
costs (the cost of running the local vector databases) for variable
costs (the cost of online vector database services).


**Performance versus speed**
The classic tradeoff: Better performance is typically correlated with
larger embedding space and thus slower data upserting (a
portmanteau of “update” and “insert”) and data querying.


We’ll implement a local database as well as use a web-service for a
vector database, so you can decide which approach to implement.

### **5.6.2  Coding: File-Based Storage with a Chroma** **Database**


You can find the code file at
_05_VectorDatabases/40_VectorStore/chroma_db_intro.py_ . As
before, we’ll load the relevant packages. A new functionality in this
example is `HuggingFaceEndpointEmbeddings`, which provides access
to models we can run locally, as shown in Listing 5.38. Also, we’ll
load Chroma as our vector database.

```
#%% Packages
import os
from langchain.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain.vectorstores import Chroma

```

**Listing 5.38** Data Storing: Required Packages (Source:
05_VectorDatabases/40_VectorStore/chroma_db_intro.py)


We’ll work with _The Hound of the Baskervilles_ . We need to navigate
from the script file to the book path, as shown in Listing 5.39.

```
#%% Path Handling
# Get the current working directory
file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(file_path)

# Go up one directory level
parent_dir = os.path.dirname(current_dir)
text_file_path = os.path.join(parent_dir, "data", "HoundOfBaskerville.txt")

```

**Listing 5.39** Storing Data: Path Handling (Source:
05_VectorDatabases/40_VectorStore/chroma_db_intro.py)


We create a `loader` instance and subsequently call its `load` method,
as follows:

```
#%% load all files in a directory
loader = TextLoader(file_path=text_file_path,
encoding="utf-8")
docs = loader.load()

```

We want to split the document based on the structure-based
chunking approach and get a list of all `chunks`, as shown in
Listing 5.40.

```
# %% Set up the splitter
splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
chunk_overlap=200,
separators=["\n\n", "\n"," ", ".", ","])
chunks = splitter.split_documents(docs)

```

**Listing 5.40** Data Storing: Data Splitting (Source:
05_VectorDatabases/40_VectorStore/chroma_db_intro.py)


Let’s check the number of chunks that were created, as follows:

```
# %% check size of chunks
len(chunks)

520

```

The complete book has been split into 520 chunks that we’ll now
embed and add to our vector store. But first we must decide on an
embedding model. In our case, we chose a famous sentence
transformer embedding model that is small enough to run locally:

```
# %% define the embedding model
embedding_function = HuggingFaceEndpointEmbeddings(model="sentence-transformers/allMiniLM-L6-v2")

```

The preparation work is done, and we can now create an instance of
our vector database. The vector database created is based on a
Chroma database. In the instantiation, you must define a path for the
vector database because its files will be written on your hard disk.
Also, the vector database needs to know which embedding function
will be used, as follows:

```
#%% vector database instance
persistent_db_path = os.path.join(parent_dir, "db")
db = Chroma(persist_directory=persistent_db_path,
embedding_function=embedding_function)

```

Now, interact with the database instance and add all the documents
by calling `add_documents`, as follows:

```
# %% add all documents
db.add_documents(chunks)

```

This process takes some time. Once done, check the number of
created documents with the method `get` . This method returns a
dump of all documents in the database. Each document has a
property named `ids`, so that you can count the number of `ids` to
determine the total number of documents, as follows:

```
# %%
len(db.get()['ids'])

```

### **5.6.3  Coding: Web-Based Storage with Pinecone**

While a Chroma database is an open-source vector database that
you can run locally on your computer, Pinecone is an online
managed service. To use this service, head over to
_[https://www.pinecone.io/](https://www.pinecone.io/)_ and register. As always, when you want to
use an online service via Python, you must create an API key, which
authenticates you as an authorized user and controls your access.


Once you’ve copied your API key to the clipboard, in your working
folder, open a local environment file _.env_ and create a new line in it,
as follows:

```
PINECONE_API_KEY=…

```

Let’s develop the script to load our book data into Pinecone. The
script file is _05_VectorDatabases/40_VectorStore/pinecone_intro.py_ .
In our program code, we can fetch this API key with the package

`dotenv` by loading this _.env_ file, as shown in Listing 5.41.

```
#%% packages
from dotenv import load_dotenv
import os
load_dotenv(".env")
# %%

```

**Listing 5.41** Data Storing with Pinecone: Required Packages (Source:
05_VectorDatabases/40_VectorStore/pinecone_intro.py)


We might check that the key is available with `os.getenv()`, as
follows:

```
os.getenv("PINECONE_API_KEY")

```

To use Pinecone, we’ll use the package `pinecone` . If you’ve already
installed the environment, you’re all set and can use it immediately.
Otherwise, you’ll need to instantiate Pinecone and pass your API
key, as follows:


```
from pinecone import Pinecone, ServerlessSpec
pc = Pinecone( api_key =os.getenv("PINECONE_API_KEY"))

```

An _index_ in Pinecone is the highest-level organizational unit of data.
The index defines the embedding dimensions of the vectors, the
similarity metric, and where your data is going to be stored. We’re
using the Starter level, which is free to use, and thus are limited in
storage size as well as limited in the cloud provider and region we
can use. Thus, we are using Amazon Web Services (AWS) as our
cloud provider with the region us-east-1. As the similarity metric, we
chose cosine similarity. As our embedding model, we chose allMiniLM-L6-v2, which has 384 dimensions. All these parameters are
defined during index creation. We created an index called “Sherlock”
and to make our code as flexible as possible, we’ll first check if this
index already exists, as shown in Listing 5.42. When you run the
code for the first time, the index will be created (because one doesn’t
already exist). In subsequent use, the index won’t be re-created, and
you can directly use it.

```
index_name = "sherlock"
if index_name not in pc.list_indexes().names():
pc.create_index( name =index_name,
            metric ="cosine",
            dimension =384,
            spec =ServerlessSpec(
              cloud = "aws",
              region ="us-east-1"))

```

**Listing 5.42** Pinecone Database: Index Creation (Source:
05_VectorDatabases/40_VectorStore/pinecone_intro.py)


You can check in the web frontend whether the index was created
successfully.


Now that you have an index, let’s add data that we can embed and
their corresponding embedding vectors. We’ve created a data
preparation function, which loads _The Hound of the Baskervilles_,
splits the text, and returns a list of documents, as follows:


```
from data_prep import create_chunks
chunks = create_chunks("HoundOfBaskerville.txt")

```

Next, we’ll create the embeddings and extract all `page_content`
properties of the documents, as follows:

```
texts = [chunk.page_content for chunk in chunks]

```

As the embedding model, we choose all-MiniLM-L6-v2 and load the
corresponding class from `langchain_huggingface`, as follows:

```
# %% Embedding model
from langchain_huggingface import HuggingFaceEndpointEmbeddings
embedding_model = HuggingFaceEndpointEmbeddings( model ="sentence-transformers/allMiniLM-L6-v2")

```

The embeddings are created by calling the method `embed_documents`
and passing all texts into it, as follows:

```
# %% create all embeddings
embeddings = embedding_model.embed_documents( texts =texts)

```

At this point, we have 520 embedding vectors with 384 elements
each.


We have all pieces compiled and can now upsert them to Pinecone.
In this context, upserting is a database operation that updates an
entry if it already exists or inserts an entry if one does not exist yet.
But first, we need a good understanding of how Pinecone expects
vectors to look.


Pinecone expects vectors that are lists of dictionaries, in which each
dictionary consists of an `id`, `values`, and `metadata` .


The `id` must be unique. The embeddings correspond to the `values`,
and `metadata` can be passed as well and should hold further
information on the document, for instance, the human-readable text
associated to the embedding vector. Let’s create the `vectors` object
using the code shown in Listing 5.43.


```
# %% create vectors
# {"id": str, "values": List[float], "metadata": Dict[str, str]}
vectors = [{"id": str(i),
"values": embeddings[i],
"metadata": chunks[i].metadata}
for i in range(len(chunks))]

```

**Listing 5.43** Pinecone Database: Vector Creation (Source:
05_VectorDatabases/40_VectorStore/pinecone_intro.py)


These vectors are now upserted to Pinecone, and we need to
connect to our index “sherlock,” as follows:

```
index = pc.Index( name =index_name)
index.upsert(vectors)

```

When you upsert larger documents, we recommend upserting the
data in batches. Since we only upserted 520 documents, batching
was not necessary.


Another simplification we applied is that we did not define a
namespace. Why would you need a namespace? Imagine working
on a production system and use a vector database that holds the
data of several different customers (multitenancy). In such a case,
you must ensure that customer A does not get accidental access to
customer B’s data. You might solve this problem by storing data from
customer A in a different namespace than customer B’s data.


Finally, let’s check if the operation succeeded. For this task, use the
method `describe_index_stats()`, as follows:

```
#%% describe index
print(index.describe_index_stats())

```

This method returns some statistics about the index’s content, as
follows:

```
{'dimension': 384,
'index_fullness': 0.0,
'namespaces': {'': {'vector_count': 520}},
'total_vector_count': 520}

```

We have successfully upserted our book to Pinecone, as before to
Chroma database. In the next section, we’ll explore how you can
retrieve data from your databases.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **5.7  Retrieving Data**

In this section, you’ll learn how data is retrieved from a vector
database. To understand this topic in detail, you’ll need to
understand what similarities are, how they are derived, and how to
use them during data retrieval. Let’s get started!

### **5.7.1  Similarity Calculation**


Before we retrieve data from a database, you must understand how
a database finds relevant documents. Relevant documents do not
necessarily mean finding exact matches. While traditional structured
databases always search for exact matches, vector databases
search for most relevant documents rather than perfect matches.
Different approaches are available for finding these documents. We’ll
cover two of the most relevant ones:


Cosine similarity


Maximum margin relevance (MMR)


**Cosine Similarity**


Let’s start with cosine similarity. Remember: the cosine value is
largest when the angle is close to zero. In a two-dimensional
coordinate system, two vectors pointing in the same direction have
an inner angle of close to zero and are thus considered similar. If the
two vectors point in completely opposite directions, they are
considered _maximally dissimilar_ . Cosine similarity is always a value
between −1 and +1.


As you know, the embedding space is much larger than two
dimensions, but the same concept holds true. Figure 5.16 shows a
vector corresponding to a user query in red—simplified into two
dimensions. The angle alpha measures the deviation of the query
vector and embedding S1. Similarly, angle beta measures the
deviation of the query vector and embedding S5. The angles for
embeddings S2, S3, and S5 are not shown.


**Figure 5.16** Principle of Cosine Similarity Calculation and Retrieval


The retrieval process to find the most relevant documents now
follows these steps:


1. Calculating angles (and their corresponding cosine values)

between query vectors and all embedding vectors


2. Sorting the embedding vectors in decreasing order


3. Returning the top-k results


In our example, we defined a threshold of `top_k = 2`, meaning that
only the two closest documents are returned.


Cosine similarity helps find the most relevant documents but in some
cases might not be enough. In these cases, MMR can help.


**Maximum Margin Relevance**


MMR aims to maximize not just the relevance, but also the diversity,
of documents. In what cases can diversity be important? Let’s
consider an example for using MMR, as shown in Figure 5.17.


**Figure 5.17** Maximum Margin Relevance Example


Let’s say we have a vector database on attractions in New York City.
You define a user query “What are the main attractions in New York
City?” and retrieve most relevant documents. As a similarity metric,
you choose cosine similarity and end up with the top 3 results, of
which two are skyscrapers. This result possibly represents the most
similar results, but you don’t want to visit two skyscrapers. New York
has such a great variety of attractions. Thus, we need a metric that
provides results based on both similarity and diversity. MMR to the
rescue! Based on MMR, you retrieve a landmark, but also a park and
a cultural district.


How does this calculation work? In MMR, you have access to a
hyperparameter λ, which is a weighting parameter in the range of 0
and 1. The value 0 returns only relevant results, and 1 returns the
most diverse results. As a starting point, you might go with λ = 0.5 for
a good balance between relevance and diversity.


### **5.7.2  Coding: Retrieve Data from Chroma Database**

Let’s extend the database we created in the last section. You can run
the code from this file:
_05_VectorDatabases/50_RetrieveData/10_chromadb_retrieval.py_ .


The relevant packages that we need to load for this script are `Chroma`
as the vector store and `HuggingFaceEndpointEmbeddings` for the
embeddings, as shown in Listing 5.44.

```
#%% packages
from langchain.vectorstores import Chroma
import os
from pprint import pprint
from langchain_huggingface import HuggingFaceEndpointEmbeddings

```

**Listing 5.44** Data Retrieval from a Chroma Database: Packages (Source:
05_VectorDatabases/50_RetrieveData/10_chromadb_retrieval.py)


In the parent directory, we created the folder `db` in which the vector
database is stored. The user query needs to be embedded. For that
functionality, we create an instance for the embedding function, as
shown in Listing 5.45. An essential step is to use the same
embedding model that you used for creating the book embeddings.
An instance of the vector database is created, which is linked to the
persistent storage and the embedding model.

```
# %% set up database connection
# Get the current working directory
file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(file_path)
parent_dir = os.path.dirname(current_dir)
chroma_dir = os.path.join(parent_dir, "db")
# Go up one directory level
parent_dir = os.path.dirname(current_dir)
# set up the embedding function
embedding_function = HuggingFaceEndpointEmbeddings(
model="sentence-transformers/all-MiniLM-L6-v2")
# connect to the database

```

```
db = Chroma(persist_directory=chroma_dir,
embedding_function=embedding_function)

```

**Listing 5.45** Data Retrieval from a Chroma Database: Connection Setup (Source:
05_VectorDatabases/50_RetrieveData/10_chromadb_retrieval.py)


Listing 5.46 shows how to find the most relevant chunk, which is now
unbelievably simple. You only need to create a retriever, which is the
endpoint that provides the `invoke` method that you’ll use afterwards.

```
retriever = db.as_retriever()
# %% find information
# query = "Who is the sidekick of Sherlock Holmes in the book?"

# # thematic search
# query = "Find passages that describe the moor or its atmosphere."

# # Emotion
# query = "Which chapters or passages convey a sense of fear or suspense?"

# # Dialogue Analysis
# query = "Identify all conversations between Sherlock Holmes and Dr. Watson."

```

**Listing 5.46** Data Retrieval from a Chroma Database: Retrieval (Source:
05_VectorDatabases/50_RetrieveData/10_chromadb_retrieval.py)


Into this `invoke` method, we can pass a user query. In the code
chunks, you can find multiple queries. You can uncomment the
queries that you want to run. As shown in Listing 5.47, we want to
ask about the hound and store the returned documents in

`most_similar_docs`, which is again a list of `Document` objects.

```
# Character
query = "How does the hound look like?"
most_similar_docs = retriever.invoke(query)
# %%
pprint(most_similar_docs[0].page_content)

```

**Listing 5.47** Data Retrieval from a Chroma Database: Most Similar Documents (Source:
05_VectorDatabases/50_RetrieveData/10_chromadb_retrieval.py)


This implementation was quick, and we ran it with default values for
search type (default: “similarity”) and the number of documents to be


returned (default: 4). But how is the similarity calculated? We’ll
explore this topic next.

### **5.7.3  Coding: Retrieve Data from Pinecone**


We’ll extend on the example described earlier in Section 5.6.3 and
retrieve data from our Pinecone index. If you did not run the code
from that section, please follow those steps first. You can find the
script in
_05_VectorDatabases/50_RetrieveData/20_pinecone_retrieval.py_ .


We’ll import relevant packages and ensure that we have the
environment file _.env_ in our working folder with the `PINECONE_API_KEY`,
as shown in Listing 5.48.

```
#%% packages
from pinecone import Pinecone
from dotenv import load_dotenv
load_dotenv(".env")
from langchain_huggingface import HuggingFaceEndpointEmbeddings
import os

```

**Listing 5.48** Pinecone Retrieval: Required Packages (Source:
05_VectorDatabases/50_RetrieveData/20_pinecone_retrieval.py)


An instance of Pinecone is created and an index-instance points to
our “sherlock” index we created earlier, as follows:

```
#%% connect to Pinecone instance
pc = Pinecone( api_key =os.getenv("PINECONE_API_KEY"))
index_name = "sherlock"
index = pc.Index( name =index_name)

```

We need to embed the `user_query` because, in the querying process,
we’ll pass the embedding vector. Make sure you use the same
embedding model you used during the data storing process. Let’s
find out what the database tells us in response to the question,
“What does the hound looks like?” as shown in Listing 5.49.


```
#%% Embedding model
embedding_model = HuggingFaceEndpointEmbeddings( model ="sentence-transformers/allMiniLM-L6-v2")
#%% embed user query
user_query = "What does the hound look like?"
query_embedding = embedding_model.embed_query(user_query)

```

**Listing 5.49** Pinecone Retrieval: Embedding (Source:
05_VectorDatabases/50_RetrieveData/20_pinecone_retrieval.py)


The object `query_embedding` is a numeric vector with 384 elements.


We can search for the most similar documents by calling the

`index.query()` method. As a parameter, the embedding vector is
passed. Also, we want to limit the result to the top 2 most relevant
documents by setting the parameter `top_k` to 2. Since the text is
stored in the metadata, we must set the parameter `include_metadata`
to true, as follows:

```
#%% search for similar documents
res = index.query( vector =query_embedding, top_k =2, include_metadata =True)

```

The resulting object `res` holds the key `“matches”` :

```
res["matches"]

```

This object is a list of dictionaries with the keys `id`, `metadata`, `score`,
and `values` . We are interested in the metadata, specifically the text
stored in the metadata. With the following code, we can print all the
texts:

```
for match in res['matches']:
print(match['metadata']['text'])
print("---------------")

```

The database returns the most relevant documents based on the
user query, as shown in Listing 5.50.

```
hound, but not such a hound as mortal eyes have ever seen. Fire burst from its open
mouth, its eyes glowed with a smouldering glare, its muzzle and hackles and dewlap
were outlined in flickering flame. Never in the delirious dream of a disordered
brain could anything more savage, more appalling, more hellish be conceived than

```

```
that dark form and savage face which broke upon us out of the wall of fog. -------------- quality upon earth it is common sense, and nothing will persuade me to
believe in such a thing. To do so would be to descend to the level of these poor
peasants, who are not content with a mere fiend dog but must needs describe him with
hell-fire shooting from his mouth and eyes. Holmes would not listen to such fancies,
and I am his agent. But facts are facts, and I have twice heard this crying upon the
moor. Suppose that there were really some huge hound loose upon it; that would go
far to explain everything. But where could such a hound lie concealed, where did it
get its food, where did it come from, how was it that no one saw it by day? It must
be confessed that the natural explanation offers almost as many difficulties as the
other. And always, apart from the hound, there is the fact of the human agency in
London, the man in the cab, and the letter which warned Sir Henry --------------
```

**Listing 5.50** Pinecone Retrieval: Retrieved Chunks (Source:
05_VectorDatabases/50_RetrieveData/20_pinecone_retrieval.py)


In that output, you see some good representation of how the hound
appears, but it is not a well formulated answer. For refinement, a
technique called retrieval-augmented generation (RAG) was
developed, which will be the focus of the next chapter.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **5.8  Capstone Project**

In this section, we combine all the knowledge you learned in this
chapter and integrate it into one big project. We’ll start by showing
you what we’ll develop.


Figure 5.18 shows the screen for our final application, in which you
can see separate sections for the user query 3, results 2, and
filters 1. In this application, you can describe the plot of a movie
and receive the most similar movies in a nice output. Before
developing any application, however, an important step is to think
about the requirements and features you want to include.


**Figure 5.18** Sample Output from Our Movie App


We’ll build it up step by step, starting with discussing the features of
our app. Then, we’ll get some understanding of the dataset that will
be used. The data preprocessing and the preparation of vector
database follow. Finally, we’ll develop the app frontend on top of our
business logic. Let’s start by discussing the features.

### **5.8.1  Features**


Even the most complex apps follow a basic input-process-output
model. Thus, the features can be structured into different groups like
input “input widgets,” “output widgets,” and “data processing,” as
follows:


**Input widgets**


A user can add a description of a movie in an input field, which
then searches for movies in a vector database that best
represents the description. Additionally, the data is narrowed
down according to some filters.


One filter leaves out “bad” movies based on IMDB ratings. A
slider is used to define a minimum rating.


Also, the genre of the movies can be selected in a dropdown
menu. The resulting films should be filtered according to the
selected genre.


**Data processing**


The movie data is processed and stored in a vector database.


Specifically, the title, poster, genres, and IMDB rating are stored
as metadata.


The plot is embedded and stored together with the text in the
database.


Most similar movies are received based on the user query, and
filters.


If multiple identical movies are found, only unique sets should
be returned.


**Output widgets**


The three most similar movies should be presented.


The movie title should be shown in bold.


If a poster URL is available, the poster should be shown on the
screen.


The genres, IMDB rating, and similarity score are shown below
the poster.


Usually, a good approach is to process the data first, before the
application is created. We’ll follow that advice and prepare our
database next.

### **5.8.2  Dataset**


We’ll base our work on a dataset from Hugging Face:

```
MongoDB/embedded_movies
```

( _[https://huggingface.co/datasets/MongoDB/embedded_movies](https://huggingface.co/datasets/MongoDB/embedded_movies)_ ). The
dataset is licensed under the Apache 2.0 license
( _https://huggingface.co/datasets/choosealicense/licenses/blob/main/_
_markdown/apache-2.0.md_ ).


This dataset contains the details of movies, including their genres.
The dataset has information about the plot, the genres that describe
the movie best, and many more features. We’ll use several
properties, in the following ways:


`fullplot` (will be 'document'; used as embedding)


`title` (metadata; shown as result)


`genres` (metadata; for filtering)


`imdb_rating` (metadata; for filtering)


`poster` (metadata; shown as result)


We know everything we need to know about the dataset at this point,
and we can proceed with the preparation of the database.

### **5.8.3  Preparing the Vector Database**


Good, let’s start coding. You can find the complete script in
_05_VectorDatabases/90_CapstoneProject/10_data_prep.py_ .


As before, we’ll load the relevant packages. For using Hugging Face
datasets, we’ll use the package `datasets` and the function

`load_dataset`, as shown in Listing 5.51.

```
#%% packages
import os
from datasets import load_dataset
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document

```

**Listing 5.51** Capstone Project: Required Packages (Source:
05_VectorDatabases/90_CapstoneProject/10_data_prep.py)


Let’s get the dataset loaded into Python. All we need to do is call

`loading_dataset` with the dataset name, as shown in Listing 5.52.

```
#%% load dataset
dataset = load_dataset("MongoDB/embedded_movies", split ="train")
# license:
https://huggingface.co/datasets/choosealicense/licenses/blob/main/markdown/apache2.0.md

```

**Listing 5.52** Capstone Project: Data Loading (Source:
05_VectorDatabases/90_CapstoneProject/10_data_prep.py)


Let’s familiarize ourselves with the dataset and determine how many
movies are part of the dataset, as follows:

```
#%% number of films in the dataset
len(dataset)

1500

```

We have quite a few movies to work with, but we now need to find
out which keys are available, as shown in Listing 5.53.

```
# %% which keys are in the dataset?
dataset[0].keys()

dict_keys(['plot', 'runtime', 'genres', 'fullplot', 'directors', 'writers',
'countries', 'poster', 'languages', 'cast', 'title', 'num_mflix_comments', 'rated',
'imdb', 'awards', 'type', 'metacritic', 'plot_embedding'])

```

**Listing 5.53** Capstone Project: Checking The Dataset (Source: 05_VectorDatabases/
90_CapstoneProject/10_data_prep.py)


Now, we want to convert the dataset into a list of document objects.
For this step, we’ll iterate over all the movies in the database. For
each movie, we’ll extract the properties to add as metadata. In some
cases, no property is available, and in these cases, we must ensure
that we have strings and not `None` values.


Another special case is `genres` . In this dataset, the genres are
provided as a list of strings. Unfortunately, we cannot store lists of
strings as metadata, so we must concatenate the different genres
with semicolon separators, which is a design decision. Another
approach for handling this could be to add a document for each
movie and genre combination.


The design decision you make at this stage will have a significant
impact on the processing of the data later. And in many cases, you
may recognize later that you need to come back to the data
processing.


The property `fullplot` is used as `page_content` in our documents and
will be used for creating the embeddings. Only if `fullplot` is
available is a document added to the list, as shown in Listing 5.54.

```
# %% Create List of Documents
docs = []
for doc in dataset:
title = doc['title'] if doc['title'] is not None else ""
poster = doc['poster'] if doc['poster'] is not None else ""
genres = ';'.join(doc['genres']) if doc['genres'] is not None else ""
imdb_rating = doc['imdb']['rating'] if doc['imdb']['rating'] is not None else ""
meta = {'title': title, 'poster': poster, 'genres': genres, 'imdb_rating':
imdb_rating}

if doc['fullplot'] is not None:
docs.append(Document( page_content =doc["fullplot"], metadata =meta))

```

**Listing 5.54** Capstone Project: Document Creation (Source: 05_VectorDatabases/
90_CapstoneProject/10_data_prep.py)


Now, we’re on familiar terrain: We have a list of documents. As
shown in Listing 5.55, proceed with splitting the data. We’ll use the
already familiar `RecursiveCharacterTextSplitter`, which we’ll use in
combination with the all-MiniLM-L6-v2 sentence-transformer
embedding model. Thus, we’ll choose a chunk size and a chunk
overlap accordingly.

```
# %% Chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
docs_chunked = []
splitter = RecursiveCharacterTextSplitter( chunk_size =CHUNK_SIZE,
                          chunk_overlap =CHUNK_OVERLAP,
                          separators =["\n\n", "\n"," ", ".", ","])
chunks = splitter.split_documents(docs)

```

**Listing 5.55** Capstone Project: Data Chunking (Source: 05_VectorDatabases/
90_CapstoneProject/10_data_prep.py)


If you check the number of chunks, notice how we now have 1,587
chunks, which is slightly more than the number of 1,500 movies.
Thus, for some movies, the `fullplot` was too long and had to be split


into two or more chunks. In the final output of the app, we must
ensure that the same movie is not shown multiple times.


We’ll set up an instance of a Chroma database and embed all the
chunks into it. In this process, a subfolder _db_ is created to hold our
database. We can ensure that the movies are not added multiple
times by first checking whether the folder exists and then adding the
documents only if the folder does not exist, as shown in Listing 5.56.

```
# %% store chunks in Chroma
embedding_function = HuggingFaceEndpointEmbeddings( model ="sentence-transformers/allMiniLM-L6-v2")
script_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(script_dir, "db")
if not os.path.exists(db_dir):
os.makedirs(db_dir)
db = Chroma( persist_directory =db_dir, embedding_function =embedding_function,
collection_name ="movies")
db.add_documents(chunks)

```

**Listing 5.56** Capstone Project: Adding Chunks to the Database (Source:
05_VectorDatabases/90_CapstoneProject/10_data_prep.py)


A few minutes will be required to embed all the movies.


To check whether the creation process was successful, call the `get`
method to get a full view of the data stored in the database, as
follows:

```
# %% check the result
db.get()

```

To prepare for our upcoming application development, let’s find out
which genres are available by iterating over the dataset, as shown in
Listing 5.57.

```
#%% get all genres
genres = set()
for doc in dataset:
if doc['genres'] is not None:
genres.update(doc['genres'])

{'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary',

```

```
'Drama', 'Family', Fantasy', 'Film-Noir', 'History', 'Horror', 'Music', 'Musical',
'Mystery', 'Romance', 'Sci-Fi', 'Short', 'Sport', Thriller', 'War', 'Western'}

```

**Listing 5.57** Capstone Project: Genre Preprocessing (Source: 05_VectorDatabases/
90_CapstoneProject/10_data_prep.py)

### **5.8.4  Exercise: Get All Genres from the Vector** **Database**


Before moving on with app development, let’s work on a short
exercise to test your knowledge of working with vector databases.


**Task**


In the previous section, we showed you how to extract genres from a
dataset. But now, we want you to assume that you don’t have access
to the raw dataset, only to the vector database. Try to extract all the
genres from the Chroma vector database.


**Solution**


Multiple solutions exist (as always). Our solution is based on getting
all documents, which represents a complete dump from the
database. Then, we create an empty set of genres. While iterating
over all the metadata of the documents, each genre entry is
extracted. Since we decided to store the genres as a string with
entries separated by semicolons, we must reverse that step, split the
genres, and update the set, as shown in Listing 5.58.

```
# %% Exercise: Get all genres from the database
documents = db.get()
genres = set()

for metadata in documents['metadatas']:
genre = metadata.get('genres')

```

```
genres_list = genre.split(';')
genres.update(genres_list)

```

**Listing 5.58** Capstone Project: Extracting Available Genres (Source:
05_VectorDatabases/ 90_CapstoneProject/10_data_prep.py)


Amazingly, we have prepared our database and are ready to take
the next step and integrate the vector database into the application.

### **5.8.5  App Development**


Let’s now turn our attention to the development of the application.
For that purpose, we’ll use a framework called Streamlit. This opensource framework for creating web applications is based on Python.
No frontend development experience is required to develop a
Streamlit app, but Streamlit should not be considered for creating a
“complete” app, for instance, with authentication and multiple
simultaneous users. But for quick prototyping, Streamlit is extremely
useful and handy.


The complete app code can be found in
_05_VectorDatabases/90_CapstoneProject/app.py_ .


As always, we’ll start the script by importing all the necessary
packages. A lot of familiar packages and classes are available for
interacting with our vector database ( `Chroma` ) or for using an
embedding model ( `HuggingFaceEndpointEmbeddings` ). But the main
package is Streamlit, which we import based on its typical alias `st`,
so that we can access its methods quicker, as follows:

```
#%% packages
import streamlit as st
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEndpointEmbeddings

```

Before we build the web interface step by step, let’s connect to our
vector database. We’ll use the same sentence transformer as earlier
during data preparation in Section 5.8.3. An instance of Chroma is
created, making use of the folder `db` to hold the database and the
collection `movies` we defined earlier, as shown in Listing 5.59.

```
#%% load the vector database
embedding_function = HuggingFaceEndpointEmbeddings(model="sentence-transformers/allMiniLM-L6-v2")
db = Chroma(persist_directory="db", collection_name="movies",
embedding_function=embedding_function)

```

**Listing 5.59** Capstone Project: Embedding and Database Instance Creation (Source:
05_VectorDatabases/90_CapstoneProject/10_data_prep.py)


The application is developed from top to bottom. We start by creating
a static headline. All Streamlit components are accessible via `st` ; for
a title, we just need to call `st.title` and pass a title for the app, as
follows:

```
#%% develop the app
st.title("Movie Finder")

```

Actually, at this point, you can already run the app. Just open the
command line and run the following command:

```
streamlit run app.py

```

This command will open your default web browser and show the
app: Not overly helpful, but we know now that the app runs.
Whenever you save the app file, the server recognizes the change.
As shown in Figure 5.19, in the upper-right corner, you’ll be informed
that the source file changed, and you’ll have the option to re-run the
application rendered. We recommend you select **Always rerun**, so
that each time you make a change to the application and save the
file, the website is reloaded. In this way, you can interactively


develop applications and directly see the impact of your code
changes.


**Figure 5.19** Capstone Project: Streamlit App Rerun Options


The next component we’ll implement is a slider for selecting a
minimum IMDB movie rating, as shown in Figure 5.20.


**Figure 5.20** Capstone Project: Streamlit Slider for “Minimum IMDB Rating”


If you’ve worked with classic website development with HTML,
JavaScript, and CSS, you know how cumbersome the development
of such components can be. But not with Streamlit. Many
components are boilerplates that you can implement with a single
line of code—as in this case.


You’ll need to apply `st.slider` and pass some parameters (like a
label, min-value, and max-value); the initial selected value; and a
step size. In this case, we want to fetch the user input, which is
easily reached by assigning the return value of the function call to
the variable `min_rating` . Later, we’ll come back to this value and filter
in the vector database query based on the filter.

```
# Add a slider for minimum IMDB rating
min_rating = st.slider("Minimum IMDB Rating", min_value =0.0, max_value =10.0,
value =7.0, step =0.1)

```

The next filter is the genre filter, an example of which is shown in
Figure 5.21. This filter narrows the query results based on the
selected genre of the movie.


At the end of Section 5.8.4, we extracted all the available genres
from the dataset. We can define them in a list and pass this list as a
parameter to `st.selectbox` . The function call returns the selected
genre that you can store for later use in the variable `selected_genre`,
as shown in Listing 5.60.

```
# Add a single-select input for genres
genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime',
'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'History',
'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Short',
'Sport', 'Thriller', 'War', 'Western']
selected_genre = st.selectbox("Select a genre", genres)

```

**Listing 5.60** Capstone Project: Genre Dropdown Implementation (Source:
05_VectorDatabases/90_CapstoneProject/10_data_prep.py)


**Figure 5.21** Capstone Project: Streamlit Dropdown Box for Genre Filter


In the next step, we’ll define the user input, as shown in Figure 5.22,
which is the chat input query that we’ll eventually pass into the vector
database query call. The chat input is also a preconfigured
component with a specific look and feel.


**Figure 5.22** Capstone Project: Streamlit Chat Input Field


And you guessed it: you can get the component and its return value
with a single line of code:

```
user_query = st.chat_input("What happens in the movie?")

```

The app will react in such a way that the most similar movies are
searched when the user presses (Enter) or the **Send** button is
clicked. Both results in storing the chat input in the variable

`user_query` . We can ensure that the code block has not already been
run by placing it in the `if user_query` block. Then, we can define the
metadata for the `imdb_rating` based on the user selection and its
corresponding variable `min_rating` .


This metadata is now applied in the vector database through the

`similarity_search_with_score` function together with the `user_query`
variable. The number of returned movies is set to 10. Finally, we’ll
present the top 3 most similar movies, but we cannot know how
many duplicates we need to remove. So, the arbitrary choice of 10 is
just for making sure that sufficient results will be available.
Duplicated entries occurred in the process of creating chunks when
the full plot description was too long for the model context window.
Thus, a movie’s description might be causing a split into several

`Documents`, of which we only want to show one unique movie in the
app. The query result is stored in `similar_movies` .


We’re still not done with the data processing; we must take care of
the genre filter. This task is achieved in Listing 5.61 with a list
comprehension in which we keep a movie only if the selected genre
is part of the movie genre’s metadata.

```
if user_query:
# Retrieve the most similar movies
with st.spinner("Searching for similar movies..."):
metadata_filter = {"imdb_rating": {"$gte": min_rating}}
similar_movies = db.similarity_search_with_score(user_query, k =10,
filter =metadata_filter)
# filter for selected genre

```

```
similar_movies = [movie for movie in similar_movies if selected_genre in
movie[0].metadata['genres']]

```

**Listing 5.61** Capstone Project: Implementing Genre Filter (Source:
05_VectorDatabases/90_CapstoneProject/app.py)


At this point, we have a list of movies that we can display.
Listing 5.62 shows the main app components. In the header, we
present the user query as a reference. Since only unique results
should be presented to the user, we must iterate over the movie
result list and check whether a title has already been seen.


In three columns, the three most similar movies are shown. A poster
image can be created with `st.image` . The title, genre, rating, and
similarity score can be printed with either `st.markdown` or `st.write` . A
warning is created with `+` to informs the user of how many duplicated
entries have been removed.

```
# Display the results
st.header( f "Most Similar Movies: ")
st.subheader( f "Query: '{user_query}'")
cols = st.columns(3)
# Check if there are duplicate results
unique_results = []
seen_titles = set()
for doc, score in similar_movies:
if doc.metadata['title'] not in seen_titles:
unique_results.append((doc, score))
seen_titles.add(doc.metadata['title'])

# Display only unique results
for i, (doc, score) in enumerate(unique_results):
if i >= len(cols):
break
with cols[i]:
if doc.metadata['poster']:
try:
st.image(doc.metadata['poster'], width =150)
except:
st.write("No poster available")
else:
st.write("No poster available")
st.markdown( f "**{doc.metadata['title']}**")
st.write( f "Genres: {doc.metadata['genres']}")
st.write( f "IMDB Rating: {doc.metadata['imdb_rating']}")

```

```
st.write( f "Similarity Score: {score :.4f }")

if len(unique_results) < len(similar_movies):
st.warning( f "Note: {len(similar_movies)-len(unique_results)} duplicate
result(s) were removed.")

```

**Listing 5.62** Capstone Project: Streamlit App (Source:
05_VectorDatabases/90_CapstoneProject/app.py)


The app is ready. You can test the different filters and check which
movies are returned based on your description. Maybe this app can
help you pick your next movie.


Feel free to extend the app by adding additional filters or replacing
the similarity search based on cosine distance to get a wider variety
of results with an MMR search.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **5.9  Summary**

In this chapter, we explored the main concepts and processes
involved in working with vector databases. We started with an
overview of vector databases, developing a comprehensive
understanding of how they work and their importance in handling
unstructured data. They set the stage for a deep dive into the
practical steps required to utilize these databases effectively.


We covered the process of loading documents into a vector
database, emphasizing the importance of data ingestion as the
foundation for subsequent operations. Once the documents are
loaded, we discussed document splitting, a critical step for breaking
down large pieces of data into manageable chunks, which facilitates
more efficient processing and retrieval.


This chapter then introduced embeddings, a technique used to
convert textual or other unstructured data into vector representations
with the same semantic meaning. These embeddings are essential
for enabling similarity searches, as they allow the data to be
compared based on their vectorized form rather than exact matches
of text.


Storing data efficiently within a vector database was another key
focus, highlighting best practices and strategies to ensure data
remains accessible and performant. We learned to work with two
important frameworks: Chroma databases and Pinecone. Then, we
explored data retrieval techniques, detailing how to query the vector
database and obtain relevant results.


A significant portion of the chapter was dedicated to the similarity
search, which is a core feature of vector databases. We explored


different similarity metrics and discussed how these search methods
work to find entries that are most similar to a given user query.


Finally, we concluded this chapter with a capstone project, which
provided a practical application of all the concepts covered. This
project serves as a hands-on exercise, reinforcing the knowledge
gained in this chapter and demonstrating how to implement a
complete workflow in a real-world scenario. An important part of this
process was the integration of the vector database and its data
retrieval into a fully functional web application.


In the next chapter, we’ll delve into RAG, a cutting-edge technique
that combines the power of LLMs with the precision of information
retrieval systems like vector databases. RAG allows for the dynamic
generation of responses by augmenting the generative capabilities of
language models with relevant data retrieved from external sources,
such as vector databases.


_[OceanofPDF.com](https://oceanofpdf.com/)_


# 6  Retrieval-Augmented Generation

_Sometimes it is the people no one imagines anything of who_
_do the things no one can imagine._
_—Alan Turing in the movie The Imitation Game_


In this chapter, we’ll cover one of the most impactful concepts in the
field of large language models (LLMs): retrieval-augmented
generation (RAG). So far, we have collected different puzzle pieces
like LLMs, prompt engineering, and vector databases, which will now
fit perfectly in place.


One important aspect is that vector databases, covered in Chapter 5,
typically represent the backbone of a RAG system. For steering the
model on how to create the final output, we’ll come back to prompt
engineering and reuse the concepts we learned in Chapter 4. Finally,
data will be passed to an LLM, and at that stage, we come back to
knowledge we gained in Chapter 4. In this regard, RAG is a
mountain we can only climb after having gained fitness in these
three different disciplines.


We’ll start this chapter with an introduction to the concept of RAG in
Section 6.1. After gaining a general understanding, we’ll proceed into
the individual process steps of retrieval, augmentation, and
generation.


We’ll first develop a simple RAG system in Section 6.2. This system
will work surprisingly well but won’t be perfect. For that reason, we’ll
present an overview of advanced RAG techniques in Section 6.3.
These improvements can take place in different stages of the RAG
system. Advanced techniques for pre-retrieval phase are presented
in Section 6.3.1. In Section 6.3.2, techniques for the retrieval phase
will be shown; in Section 6.3.3, techniques for the post-retrieval
phase.


An alternative to RAG, called _prompt caching_, is the focus of our
attention in Section 6.4. When you develop a RAG system and want
to improve it, you’ll need metrics for evaluating and quantifying these
improvements. Thus, we dedicated Section 6.5 to RAG evaluation
techniques.


Let’s start with what RAG is, why it is needed, and how it works.

## **6.1  Introduction**


Before we delve into how RAG works, let’s pause for a second and
reflect on why it is needed. Imagine you’re working with a large
knowledge source (e.g., a long document), and you want to “chat”
with it.


The simplest approach would be to make an LLM call in which you
pass your question as well as the complete document as the context.
This approach is usually not feasible because the large document
may exceed the context window of the LLM, and/or it will not be
efficient to send in each request the complete document. The
request will take comparably long to receive an answer but also
could be quite costly because many unnecessary tokens are sent in
every single request.


One special solution is the use of prompt caching, which we’ll
discuss in detail in Section 6.4. But prompt caching is more a
solution for edge cases. The more usual approach is to use RAG.
With RAG, in each LLM request, only the most relevant documents
are passed along with the user query to the LLM. So, RAG results in
an efficient and quick solution while also overcoming some
limitations of LLMs. With RAG, you have the following capabilities:


Access to company-internal information


Access to up-to-date information that was created after the
knowledge cutoff data for LLM training


More fact-based results


Figure 6.1 shows the general RAG process. A user creates a query
that will be passed to a retriever. The retriever is responsible for
fetching relevant information from some external source.


**Figure 6.1** RAG General Pipeline


In most cases, this external source is a vector database, but you’re
not limited to vector databases. Alternatively, you could connect to
and search the internet for relevant information. Ideally, the retriever
finds some relevant information.


The next stage of the pipeline is the augmentation step. In this step,
we use prompt engineering to bundle instructions to the relevant
documents. These instructions will tell an LLM how to process the
relevant documents but also how to behave when the relevant
documents are not a good match from which to extract information.
As the result of the augmentation step, we have documents and
corresponding instructions. These elements are now passed to the
last stage of the pipeline: the LLM.


The LLM will process the instructions, extract information from the
documents, and create an output according to the user query.


The external source is, in most cases, a vector database. Let’s look
at the RAG system with a vector database in the backend, as shown
in Figure 6.2.


**Figure 6.2** Simple RAG System Based on a Vector Database Backend


The vector database, which represents a corpus of documents and
their embeddings, must already be created, which we covered in
Chapter 5.


In an RAG system that relies on a vector database, the user sends a
query to the system. This query is embedded based on the same
embedding model that was used for embedding the documents. The


most similar documents to the query embedding are retrieved from
the database. In the next step, the user query together with the most
similar documents are passed to the LLM to formulate the response.


Now that you have a general idea, let’s dive into the details:


1. **Retrieval process**

In the retrieval process, the user query results in a search
against some data source. The user query, as a minimum,
requires a text and a limitation indicating how many documents
should be returned. The query can be searched for in a variety
of different knowledge sources. The knowledge source
represents a large number of documents. In this knowledge
source, all documents are ranked based on their similarity to the
user query.


**Figure 6.3** Retrieval Process


The user query is embedded, and its embedding is compared to
all embeddings of the documents in the knowledge source.
Based on a similarity metric like cosine similarity, the documents
are ranked. A predefined number of most relevant documents is
extracted and passed to the next stage—the augmentation.


2. **Augmentation process**

In the augmentation step, the retrieved information is combined


with the original query to create an enhanced prompt. This
phase begins with the integration of relevant documents or
passages that the retrieval step has surfaced.


Typically, the retrieved information is clearly differentiated from
the user’s query. At this stage, prompt engineering comes into
play and has a vital role. We need to instruct the LLM on how to
process the information. Explicit instructions are passed about
staying within the bounds of the information provided to avoid
hallucinations. Also, we should clearly state how to respond if
the information does not answer the user query.


The result is a prompt that provides the language model with
both the context it needs to generate an accurate response and
the guidance that is required to use that context effectively. The
augmented prompt serves as the foundation for generating
responses that are relevant to the user query and grounded in
the retrieved information. In the next step, we’ll take a closer
look at the generation process.


3. **Generation process**

The generation process in RAG represents the final crucial
stage where the language model transforms the augmented
prompt into a coherent and contextually relevant response.
Unlike standard LLM output generation in traditional language
models, RAG-based generation incorporates the retrieved
information while maintaining natural language fluency.


When the language model receives the augmented prompt, it begins
the process of analyzing the retrieved context and the original query
in tandem.


One of the key challenges during generation is maintaining
consistency with the retrieved information while avoiding


hallucinations. The model must strike a good balance between
purely extractive answers, like directly quoting the retrieved content,
and more abstract responses that synthesize and reformulate the
information. This balance often involves techniques where the
model's generation is explicitly guided to stay within the boundaries
of the provided context.


While all this sounds quite complicated, actually it isn’t, as you’ll see
as we start implementing RAG in the next section.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **6.2  Coding: Simple Retrieval-Augmented** **Generation**

Let’s start developing our very first RAG application by mapping out
what we’ll create. Our small RAG system will be backed by a vector
database. This vector database will represent a knowledge base for
human history, populated with knowledge fetched from Wikipedia.
We’ll load a number of Wikipedia articles on the topic and store them
in the database. Later, we’ll set up a RAG system that will interact
with these documents and answer questions based on that
represented knowledge. The RAG system will also clearly state if it
does not know how to answer the question.

### **6.2.1  Knowledge Source Setup**


First things first, we’ve got to pack our bags with all the tools we
need. Listing 6.1 shows all packages we’ll need in this script. You
can already deduce many aspects of our implementation, for
example, that we’ll use Groq as LLM backend and that we’ll use
OpenAI embeddings for embedding our texts.

```
#%% packages
import os
from langchain_community.document_loaders import WikipediaLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv( usecwd =True))
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

```

**Listing 6.1** Simple RAG System: Required Packages (Source:
06_RAG/10_simple_RAG.py)


You must also set up a configuration file that holds your application
programming interface (API) credentials for interacting with the LLM.
That file is called _.env_ and is shown in Listing 6.2.

```
GROQ_API_KEY = …
OPENAI_API_KEY = …

```

**Listing 6.2** Simple RAG System: API Credentials (Source: .env)


The first step is now to create the vector database. Since we
covered this topic in Chapter 5, we won’t bore you by explaining all
the details again. If some steps in this chapter are unclear, please
return to Chapter 5.


The general setup is the following: The database will be stored in a
folder called _rag_store_ . If this folder already exists, the assumption is
that you already ran the code (because it is created as part of the
complete creation of the database). If the folder does not exist yet,
the database is created. The database creation consists of these
steps:


1. Loading data from Wikipedia


2. Splitting the data into smaller chunks


3. Embedding the data using OpenAI embeddings


4. Storing these embeddings, together with the chunks, into the

vector database


Listing 6.3 shows the steps for loading the dataset and storing it into
a vector database.

```
#%% load dataset
persist_directory = "rag_store"
if os.path.exists(persist_directory):
vector_store = Chroma( persist_directory =persist_directory,
embedding_function =OpenAIEmbeddings())
else:
data = WikipediaLoader(
     query ="Human History",

```

```
     load_max_docs =50,
     doc_content_chars_max =1000000,
).load()

# split the data
chunks = RecursiveCharacterTextSplitter( chunk_size =1000,
chunk_overlap =200).split_documents(data)

# create persistent vector store
vector_store = Chroma.from_documents(chunks, embedding =OpenAIEmbeddings(),
persist_directory ="rag_store")

```

**Listing 6.3** Simple RAG System: Vector Database Creation/Loading (Source:
06_RAG/10_simple_RAG.py)


Next, we’ll walk through the three steps of RAG, namely, retrieval,
augmentation, and generation. We start with the retrieval step.

### **6.2.2  Retrieval**


To retrieve something, we must create a retriever. Listing 6.4 shows
how to set up a `retriever` and how to invoke it. Helpfully,

`vector_store` (our Chroma database instance) has a method

`as_retriever()` that allows you to define the vector database as the
retriever. Plus, we can define some important parameters like the
similarity function to use for finding the most relevant documents, as
well as how many documents to return. Let’s try it out by setting up a

`question` and subsequently invoking the `retriever` with that question.

```
retriever = vector_store.as_retriever(
  search_type ="similarity",
  search_kwargs ={"k": 3})
question = "what happened in the first world war?"
relevant_docs = retriever.invoke(question)

```

**Listing 6.4** Simple RAG System: Retriever Set Up (Source:
06_RAG/10_simple_RAG.py)


We can check qualitatively if the retrieval process works by printing
the most similar documents. For simplicity, we’ll limit the output for


each document to just 100 characters, as shown in Listing 6.5.

```
#%% print content of relevant docs
for doc in relevant_docs:
print(doc.page_content[: 100])
print("\n--------------")

This transformation was catalyzed by wars of unparalleled scope and devastation.
World War I was a g
-------------=== World War I ===
-------------World War I saw the continent of Europe split into two major opposing alliances; the
Allied Powers,
-------------A tenuous balance of power among European nations collapsed in 1914 with the
outbreak of the First W -------------
```

**Listing 6.5** Simple RAG System: Retrieved Documents (Source:
06_RAG/10_simple_RAG.py)


Good! All documents found seem relevant since they are related to
World War I or have the starting year of 1914 mentioned.


But these samples are just snippets taken from chunks. You might
try to figure out the specific answer based on these snippets, but
they can be hard to read and understand, since they are not
necessarily complete sentences, but only pieces of it. Thus, we don’t
yet have a good answer to the question. That is what RAG is for,
because in the next step we augment the documents with some
proper instructions on how the documents should be handled to
answer the question.

### **6.2.3  Augmentation**


In the augmentation step, we bring the most similar documents into a
well-defined format: a long-concatenated string in which all
document contents are represented. We can create this string with

`join()` . In this function, we pass a list that is then just concatenated


into a single string. The list items are represented by `page_content` of
our `relevant_docs`, as follows:

```
context = "\n".join([doc.page_content for doc in relevant_docs])

```

This step was the tedious work; now, we need to get creative when
defining a prompt that instructs the LLM how to formulate an answer.
As shown in Listing 6.6, we can define the role that our LLM should
play. We’ll instruct it to use the documents to answer the question.
Furthermore, we tell it to not hallucinate and instead to clearly state
that it does not know the answer if necessary.

```
#%% create prompt
messages = [
("system", "You are an AI assistant that can answer questions about the history
of human civilization. You are given a question and a list of documents and need to
answer the question. Answer the question only based on these documents. These
documents can help you answer the question: {context}. If you are not sure about the
answer, you can say 'I don't know' or 'I don't know the answer to that question.'"),
("human", "{question}"),
]
prompt = ChatPromptTemplate.from_messages( messages =messages)

```

**Listing 6.6** Simple RAG System: Augmentation Setup (Source:
06_RAG/10_simple_RAG.py)


For a start, this step should be enough for augmentation. You can
later come back to this stage to improve the system. For now, we’re
satisfied and can proceed with the next stage—the generation of a
final answer.

### **6.2.4  Generation**


We’ve come to the last step—the generation of an answer. This step
is straightforward. We’ll create a model. In this case, we can use an
open-weight model from Google called gemma2. This model is a
comparably small but is quite fast. Classified as a small language
model (SLM), gemma2 allows for very quick inferences, which might


increase user acceptance, because the answer is provided nearly
instantaneously. The longest process is the retrieval of the
documents.


The second step in generation should be familiar to you from
Chapter 3—the creation of a chain. In this case, the chain starts with
our prompt. The prompt output is passed to the model. Finally, the
model output is passed to `StrOutputParser()` so that only the content
part of the model output is shown, as follows:

```
model = ChatGroq(model_name="gemma2-9b-it", temperature=0)
chain = prompt | model | StrOutputParser()

```

We’ve placed our last jigsaw piece; let’s test it by invoking the chain
and checking the answer, as shown in Listing 6.7.

```
#%% invoke chain
answer = chain.invoke({"question": question, "context": context})
print(answer)

World War I was a global conflict from 1914 to 1918.

It involved two main alliances:

* **The Allied Powers:** Primarily composed of the United Kingdom, France, Russia,
Italy, Japan, Portugal, and various Balkan states.
* **The Central Powers:** Primarily composed of Germany, Austria-Hungary, the
Ottoman Empire, and Bulgaria.

The war resulted in the collapse of four empires: Austro-Hungarian, German, Ottoman,
and Russian. It had a death toll estimated between 10 and 22.5 million people.

The war saw the use of new industrial technologies, making traditional military
tactics obsolete. It also witnessed horrific events like the Armenian, Assyrian,
and Greek genocides within the Ottoman Empire.

```

**Listing 6.7** Simple RAG System: Generation (Source: 06_RAG/10_simple_RAG.py)


A pretty good answer, assuming that our test checks that the answer
formulates a good response based on the available knowledge from
the source. An equally important step is to also test the opposite


functionality—if the model correctly identifies its own limitations and
clearly states that it does not know.


In a real-world example, you probably want to embed this
functionality into a broader context of code. So, what we need to do
should be clear: We need to bundle everything into a function.

### **6.2.5  RAG Function Creation**


Our function `simple_rag_system` will consume a `question` and return a
string. The other steps are exactly the same steps as before:


1. Retrieving the relevant documents


2. Creating the context based on these relevant documents


3. Creating a detailed prompt that tells the model how to apply the

context as well as the user question


4. Creating a chain that bundles the prompt, the model, and an

output handler together


Listing 6.8 shows the definition of our `simple_rag_system` function,
which consumes a `question` as the input parameter and returns the
RAG system `answer` .

```
# %% bundle everything in a function
def simple_rag_system( question : str) -> str:
relevant_docs = retriever.invoke(question)
context = "\n".join([doc.page_content for doc in relevant_docs])
messages = [
("system", "You are an AI assistant that can answer questions about the
history of human civilization. You are given a question and a list of documents and
need to answer the question. Answer the question only based on these documents.
These documents can help you answer the question: {context}. If you are not sure
about the answer, you can say 'I don't know' or 'I don't know the answer to that
question.'"),
("human", "{question}"),
]
prompt = ChatPromptTemplate.from_messages( messages =messages)
model = ChatGroq( model_name ="gemma2-9b-it", temperature =0)
chain = prompt | model | StrOutputParser()

```

```
answer = chain.invoke({"question": question, "context": context})
return answer

```

**Listing 6.8** Simple RAG System: Function (Source: 06_RAG/10_simple_RAG.py)


Now, time to test it out. Does the function correctly return that it does
not know an answer? As shown in Listing 6.9, it does!

```
# %% Testing the function
question = "What is a black hole?"
simple_rag_system( question =question)

"I don't know the answer to that question. \n"

```

**Listing 6.9** Simple RAG System: Test (Source: 06_RAG/10_simple_RAG.py)


Our RAG system does not know anything about black holes, which is
exactly what we hoped for, given that it relied on a knowledge source
based solely on human history. We achieved this limitation through
the system message by passing the instruction `Answer the question`

```
only based on these documents. … If you are not sure about the
answer, you can say 'I don't know' or 'I don't know the answer to
```

`that question` .


Let’s reflect on what we’ve learned so far. We’ve developed our first
RAG system, based on a vector database. Given a user question,
the most relevant documents were retrieved. These retrieved
documents were used in combination with detailed instructions to the
LLM on how to make use of them.


You’ll be impressed by how well this works. But after working with it
for a while, you might see some issues with this simple RAG. Issues
might occur anywhere along the complete pipeline, for example:


**Retrieval**
The retrieved documents might not be relevant.


**Augmentation**


If multiple documents hold the same or very similar information,
the retrieved documents might be repetitive and thus are not
very informative.


If documents stem from different sources, their context might be
hard to differentiate, which might result in an incorrect mix of
different documents in the final answer. Imagine you have a
system with controversial papers and contradicting views. A
terrible answer will result if the system assigns views to the
wrong authors.


**Generation**
Issues at this step typically result from the upstream issues
mentioned earlier in this list.


Numerous possible improvements can be made, and in the following
sections, we’ll discuss some of these options.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **6.3  Advanced Techniques**

Although our simple RAG system is impressive, there’s still a lot of
room for improvement. Opportunities for improvement can be found
at different stages in the pipeline. For instance, some improvements
can be made to the indexing pipeline.


Practically, we can improve the data before we add it to our vector
database, which we’ll cover when we discuss advanced pre-retrieval
techniques in Section 6.3.1. Other techniques tackle the problem at
the retrieval step of the pipeline, which we cover in Section 6.3.2.
Unsurprisingly, the last step of the pipeline can be improved as well;
we’ll explore improvements in the generation step in Section 6.3.3.

### **6.3.1  Advanced Preretrieval Techniques**


If the RAG system fails to fetch the right documents, the problem
might be found in the data ingestion pipeline. Several ways are
available to improve the data before it is stored into the vector


database. Figure 6.4 shows some common approaches to optimize
the data ingestion pipeline.


**Figure 6.4** Pre-Retrieval Techniques


The different techniques correspond to the step in which they are
applied, which we’ll discuss in the following sections.


**Data Cleaning**


Data cleaning in RAG systems involves preparing and refining the
source documents to optimize them for retrieval and generation. This
crucial preprocessing step begins with basic operations like
removing duplicate content, standardizing formatting, and handling
special characters.


The text is then typically segmented into appropriate chunks that
balance context preservation with retrieval granularity—chunks that
are too large may contain irrelevant information, while chunks that
are too small might lose important context. (We covered these topics
in detail in Chapter 5.) Advanced cleaning steps might include the
following:


Removing boilerplate content


Standardizing date formats


Resolving abbreviations


Handling multilingual content


The cleaning process also often involves metadata enrichment,
where chunks are tagged with relevant identifiers, timestamps, or
categorizations to enhance retrieval accuracy. Clean data forms the
foundation for effective RAG performance, as it directly impacts both
the quality of retrieved matches and the coherence of generated
responses.


**Metadata Enhancing**


Metadata enhancement in RAG systems involves enriching
document chunks with additional contextual information that goes
beyond the raw text content. This process includes tagging
documents with attributes such as creation dates, authors, topics,
and categorical classifications.


More sophisticated enhancement might involve generating
embeddings for semantic search, calculating readability scores, or
extracting key entities and relationships. Some systems implement
automated topic modeling or classification to add thematic tags,
while others maintain hierarchical relationships between chunks to
preserve document structure.


This rich layer of metadata not only improves retrieval accuracy but
also enables more nuanced filtering and contextual understanding
during the generation phase. This ultimately leads to more relevant
and well-sourced responses.


**Chunk Size Optimization**


Chunk size optimization in RAG systems requires carefully balancing
multiple competing factors to maximize retrieval effectiveness. While
smaller chunks offer more precise retrieval and reduce token
consumption, they risk fragmenting important context and breaking
up coherent ideas.


On the other hand, larger chunks preserve more context but can
introduce noise and irrelevant information into the retrieval results,
potentially diluting the quality of generated responses. As explored in
Chapter 5, the optimal chunk size often varies depending on the
nature of the content. Technical documentation might benefit from
smaller, focused chunks, while narrative content might require larger
chunks to maintain coherence.


**Context Enrichment**


Context enrichment in RAG systems involves augmenting the base
content with additional information to enhance its utility and
retrievability. This process goes beyond basic metadata tagging by
incorporating related information, cross-references, and derived
insights that make the content more valuable for retrieval and
generation.


Advanced enrichment might include linking related concepts, adding
definitions for technical terms, or incorporating domain-specific
knowledge. For example, when processing medical documents, the
system might automatically expand abbreviations, add standardized
medical codes, or link to relevant research papers.


Real-world applications might include adding geographic coordinates
to location-based content, temporal relationships for event-based
information, or industry-specific taxonomies.


The enriched context helps the retrieval system make more
intelligent matches and provides the generation model with richer,
more nuanced information to work with, ultimately leading to more
comprehensive and accurate responses.


**Embedding Model Fine-Tuning**


Embedding model fine-tuning in RAG systems adapts generalpurpose embedding models to better capture domain-specific
semantic relationships and nuances. The process typically begins
with selecting a base embedding model like BERT (bidirectional
encoder representations from transformers) or sentence
transformers, then training it further on domain-specific data to better
understand specialized vocabulary, technical concepts, and industryspecific relationships.


The fine-tuning process requires careful curation of training pairs that
represent the types of semantic similarities most important for the
specific use case—for instance, in legal applications, fine-tuning
might include matching different phrasings of the same legal
concept, while in technical documentation, fine-tuning might focus on
connecting problem descriptions with their solutions.

### **6.3.2  Advanced Retrieval Techniques**


In this section, we’ll cover several advanced retrieval techniques.
One limitation of our simple RAG solution is that it is not well suited
to finding specific keywords. For keyword search, a few different
algorithms are available. After learning about these algorithms, we’ll
use them in a hybrid RAG system. We’ll also cover _reciprocal rank_
_fusion_, which is a ranking technique that merges multiple retrieval
results to improve relevance without complex weighting schemes. In


a practical implementation of a hybrid search, we’ll combine vector
search with keyword-based methods to enhance document retrieval.
You’ll also learn about _query expansion_, a technique that enhances
user queries. Finally, you’ll learn about _context enrichment_ . With
these techniques, you can refine and expand retrieved passages by
incorporating additional document-based context.


**Keyword-Search Algorithms**


For keyword searches, multiple algorithms are available like TF-IDF
(term frequency-inverse document frequency) and BM25 (Best
Match 25). A keyword search is also known as a _sparse vector_
_search_, in contrast to our well-known embeddings, which are often
called _dense vector search es_ .


The most popular sparse vector searches are TF-IDF or BM25. Both
are numerical statistics used in information retrieval. Their purpose is
to assess the importance of a word in a document relative to a
collection of documents, as follows:


**Term frequency-inverse document frequency (TF-IDF)**
TF-IDF is the product of term frequency and inverse document
frequency. Term frequency (TF) represents the number of times a
term appears in a document. Inverse document frequency (IDF)
measures how unique or rare a word is across all documents in
the corpus. The more documents a word appears in, the lower its
IDF value becomes.


Words like “the” or “is” appear in almost every document, so their
IDF values are low. Other terms that are rare across several
documents (i.e., they appear in just a few documents) thus have a
high IDF value.


Terms with high TF-IDF values indicate that a term frequently
appears in a particular document but is not common in the corpus
of documents. These terms are considered more relevant for
identifying key topics of a document.


TF-IDF is a popular search algorithm for ranking documents
based on how relevant they are to a user query. The idea is to
give more weight to terms that are significant in the document but
rare in the corpus.


**Best Match 25 (BM25 )**
A related concept that builds upon TF-IDF is BM25, which
introduces a sophisticated way of weighting terms based on term
frequency, document length, and term saturation.


BM25 adds the concept of term frequency. In TF-IDF, a term’s
importance increases linearly with its frequency. BM25 uses
instead a saturation function. In other words, after a certain point,
additional occurrences of a term in a document don’t further
increase the relevance. The rationale behind this approach is that,
if a term appears multiple times in a document, it has a certain
impact, but above a certain threshold its impact reduces.


Another applied concept is document length normalization. TF-IDF
does not balance between long and short documents. To
overcome this lack, BM25 adjusts for a document’s length. The
rationale is that longer documents naturally have more
occurrences of a term, so BM25 normalizes the score to prevent
bias towards longer documents.


BM25 is widely used in modern search engines because it
overcomes multiple limitations of TF-IDF. With saturation, it better
models real texts, where term frequency eventually stops


increasing the relevance of a term. Also, it compensates for longer
documents with document length normalization.


To summarize, we have two different worlds: sparse vector search
and dense vector search. Now, you know how to work with both
individually. However, we want to search for the best of both worlds.
Thus, we need a way to combine search results from both sparse
and dense searches.


**Coding: Sparse Search with BM25 and TF-IDF**


Let’s implement both BM25 and TF-IDF to compare their results. You
can find the corresponding script at _06_RAG/25_BM25_TFIDF.py_ .


Listing 6.10 shows how to load relevant packages and create a
function to preprocess text. A new functionality that we’ll use is

`BM250kapi` from the `rank_bm25` package.

```
#%% packages
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from typing import List
import string
#%% Documents
def preprocess_text( text : str) -> List[str]:
# Remove punctuation and convert to lowercase
text = text.lower()
# remove punctuation
text = text.translate(str.maketrans('', '', string.punctuation))
return text.split()

```

**Listing 6.10** TF-IDF and BM25: Packages and Preprocessing Function (Source:
06_RAG/25_BM25_TFIDF.py)


In the preprocessing function, we want to convert all text to
lowercase. Then, all punctuation is removed. Finally, all the text is
split at each space. As a result, we have a list of single words for


each document in the corpus. Now, we need some text to process
and play with. This corpus is shown in Listing 6.11.

```
corpus = [
"Artificial intelligence is a field of artificial intelligence. The field of
artificial intelligence involves machine learning. Machine learning is an artificial
intelligence field. Artificial intelligence is rapidly evolving.",
"Artificial intelligence robots are taking over the world. Robots are machines
that can do anything a human can do. Robots are taking over the world. Robots are
taking over the world.",
"The weather in tropical regions is typically warm. Warm weather is common in
these regions, and warm weather affects both daily life and natural ecosystems. The
warm and humid climate is a defining feature of these regions.",
"The climate in various parts of the world differs. Weather patterns change due
to geographic features. Some regions experience rain, while others are dry."
]

```

**Listing 6.11** TF-IDF and BM25: Corpus (Source: 06_RAG/25_BM25_TFIDF.py)


The first document is about artificial intelligence and shows many
occurrences of this term. Actually, the term is repeated excessively,
so our expectation is that TF-IDF will over-rank it compared to BM25.
The second deals with a related topic: “robots.” The third document
repeats the term “warm” several times, and the last document is
rather generic.


Now, let’s start preprocessing the corpus. One essential point at this
step is to check how these different functionalities expect the input
data to be passed. We worked with `TfidfVectorizer` earlier in this
section. This functionality expects documents to be passed as a list
of strings ( `list[str]` ). Thus, for each document, we want to remove
the stopwords but keep the document as a string of multiple words.
The `BM250kapi` class requires a different format: `list[List[str]]` .
With this format, each document is split into its individual words, and
all the words are then passed as a list of strings. This approach is
extremely important to get the correct results.

```
Tokenized Query BM25: ['artificial', 'intelligence', 'involves', 'learning']
Tokenized Query TFIDF: artificial intelligence involves learning
BM25 Similarities: [2.11043413 0. 0. 0. ]

```

Listing 6.12 shows how the similarity calculation is implemented.
First, the documents are preprocessed. The resulting object

`tokenized_corpus` provides the data in the format that BM25 class
requires. Then, we’ll initialize `bm25` as an instance of `BM250kapi` class.
The `user_query` is defined and tokenized. Remember, BM25 and TFIDF classes require the user query in different formats. Finally, we’ll
calculate the scores with `bm25.get_scores()` and print the results to
the screen.

```
# Preprocess the corpus
tokenized_corpus = [preprocess_text(doc) for doc in corpus]
# %% Sparse Search (BM25)
bm25 = BM25Okapi(tokenized_corpus)

#%% Set up user query
user_query = "artificial intelligence involves learning"

# Process query to remove stop words
tokenized_query_BM25 = user_query.lower().split()
tokenized_query_tfidf = ' '.join(tokenized_query_BM25)
# Process query to remove stop words

bm25_similarities = bm25.get_scores(tokenized_query_BM25)
print( f "Tokenized Query BM25: {tokenized_query_BM25}")
print( f "Tokenized Query TFIDF: {tokenized_query_tfidf}")
print( f "BM25 Similarities: {bm25_similarities}")

Tokenized Query BM25: ['artificial', 'intelligence', 'involves', 'learning']
Tokenized Query TFIDF: artificial intelligence involves learning
BM25 Similarities: [2.11043413 0. 0. 0. ]

```

**Listing 6.12** TF-IDF and BM25: Similarity Calculation (Source:
06_RAG/25_BM25_TFIDF.py)


The first few lines just showcase the different input formats of BM25
and TF-IDF queries. In the last output line, you’ll see the similarities
between the user query and the documents. The highest and only
similarity is found for the first document.


Next, let’s implement TF-IDF, as shown in Listing 6.13, and compare
the results. Create an instance of `TfidfVectorizer()` and embed the
documents with `tfidf.fit_transform()` . The user query is


embedded, and finally, its similarity to the TF-IDF matrix can be
calculated.

```
#%% calculate tfidf
tfidf = TfidfVectorizer()
tokenized_corpus_tfidf = [' '.join(words) for words in tokenized_corpus]
tfidf_matrix = tfidf.fit_transform(tokenized_corpus_tfidf)

query_tfidf_vec = tfidf.transform([tokenized_query_tfidf])
tfidf_similarities = cosine_similarity(query_tfidf_vec, tfidf_matrix).flatten()
print( f "TFIDF Similarities: {tfidf_similarities}")

TFIDF Similarities: [0.6630064 0.08546995 0. 0. ]

```

**Listing 6.13** TF-IDF and BM25: Similarity Calculation (Source:
06_RAG/25_BM25_TFIDF.py)


The first two documents show some similarity, and the algorithm
correctly returns the first document as the most similar.


At this point, reciprocal rank fusion comes to the rescue. But before
turning to that topic, let’s pause for a second and look at the full
picture: our hybrid RAG pipeline.


**Hybrid RAG Pipeline**


Now, you can build your own hybrid RAG systems. Figure 6.5 shows
the mode of operation for a hybrid RAG pipeline.


**Figure 6.5** Hybrid RAG: Pipeline


Compared to the diagram shown earlier in Figure 6.1, which shows a
general, simple RAG, notice that all changes so far concern the
retrieval step of the pipeline.


The user query is passed to a dense search, typically, a vector
database. But at the same time, the query is also passed to a sparse
search, like TF-IDF or BM25. As a result, we get two ordered lists of
documents: one coming from the similarity search in the vector
database, the other coming from the keyword search (sparse
search) algorithm. We only need and can only work with one ordered
list of documents. Thus, we need to aggregate these lists; at this
point, rank fusion comes into play.


The remaining parts of this extended RAG pipeline are identical to
our simple RAG system. The ordered list of most relevant
documents is, together with a set of instructions, augmented. And
the augmented prompt is passed to the LLM for processing the
information and coming up with an answer.


One question is left to answer: How are the outputs from dense and
sparse search combined? The algorithm that is used here is called
reciprocal rank fusion.


**Reciprocal Rank Fusion**


Reciprocal rank fusion is an algorithm used to combine multiple
ranked lists into a single, unified ranking.


Other algorithms for rank fusion are available like CombSUM,
CombMNZ, or Borda Count. But reciprocal rank fusion stands out for
its simplicity, its robustness, and its ability to handle incomplete
rankings. Let’s find out how it works. For each item in the different
ranked lists, reciprocal rank fusion calculates a score based on the
following formula:


For each document d (out of a corpus of documents D), a score is
calculated based on its ranks in the different lists. k is a constant that
is often set to 60. Thus, the only variable part of the formula is r(d),
which is the rank of the document in a given list. Then, the sum is
calculated over all lists.


Let’s look at a real example. Figure 6.6 shows how reciprocal rank
fusion works for four documents and displays their ranks as resulting
from a dense search and from a sparse search.


**Figure 6.6** Reciprocal Rank Fusion: Rank Calculation (Left) and Fusion (Right)


The ranks from the two lists and the four documents are shown on
the left. The ranks are increased, and the corresponding reciprocal
ranks are just the result of 1 ÷ rank. In this example, Document D
has rank 1 in the dense search result and rank 4 in the sparse
search result.


The way to aggregate both results is simple. The reciprocal ranks
are summed. Keeping our focus on Document D: It gets a reciprocal
rank of 1/1 from dense search, and 1/4 from sparse search. Both are
summed to 1.25. The same approach is applied all other documents.


Subsequently, the documents are sorted in decreasing order based
on their reciprocal rank sums. As a result, Document A is the most


relevant document, followed by Document D, and so on.


The reciprocal rank algorithm has the beneficial mathematical
property of diminishing returns. The score decreases non-linearly as
its rank increases. Intuitively, this relationship makes sense since a
difference in low ranks (like 1 and 2, or 2 and 3) is much more
important than the difference in rank between rank 1000 and 1001.


**Coding: Hybrid Search**


In this code exercise, you’ll set up a hybrid search that applies both a
dense search and a sparse search. The two resulting lists are then
merged based on rank fusion. Along the way, you’ll discover why
hybrid searches might outperform any of the individual search
engines.


Let’s start with loading all the required functionality. Listing 6.14
shows the required packages. Notable additions include

`TfidfVectorizer` to perform TF-IDF and `ENGLISH_STOP_WORDS` to
remove unnecessary words that might distract TF-IDF.

```
from langchain_openai import OpenAIEmbeddings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv( usecwd =True))

```

**Listing 6.14** Hybrid Search: Required Packages (Source: 06_RAG/20_hybrid_search.py)


We need some sentences to play with, so we’ll set up a list of docs,
as shown in Listing 6.15.

```
#%% Documents
docs = [
"The weather tomorrow will be sunny with a slight chance of rain.",
"Dogs are known to be loyal and friendly companions to humans.",
"The climate in tropical regions is warm and humid, often with frequent rain.",
"Python is a powerful programming language used for machine learning.",

```

```
"The temperature in deserts can vary widely between day and night.",
"Cats are independent animals, often more solitary than dogs.",
"Artificial intelligence and machine learning are rapidly evolving fields.",
"Hiking in the mountains is an exhilarating experience, but it can be
unpredictable due to weather changes.",
"Winter sports like skiing and snowboarding require specific types of weather
conditions.",
"Programming languages like Python and JavaScript are popular choices for web
development."
]

```

**Listing 6.15** Hybrid Search: Sample Documents (Source: 06_RAG/20_hybrid_search.py)


We start with the sparse similarity analysis based on TF-IDF. For this
algorithm, be aware that it might be distracted by stopwords.
Stopwords are common words that are typically filtered out during
text preprocessing in natural language processing (NLP) tasks.
These words are usually the most common words in a language that
don't contribute significantly to the meaning or sentiment of a text.


In English, common stopwords include articles (e.g., a, an, the);
prepositions (in, on, at, with, by); pronouns (I, you); conjunctions
(and, but, or); and verbs (is, am, are, was, were). Depending on the
algorithm, removing these stopwords might be an important step to
reduce noise, improve efficiency, and focus on meaning. In practice,
stopword removal looks like this:


Original text: “The car is sitting on the mat”


After stopword removal: “car sitting mat”


The object `docs_without_stopwords` can be created based on list
comprehension. In this process, each word in a string is separated
by splitting at each space with `doc.split()` . Then, all words are
converted to lowercase, and a word is only retained if it is not part of

`ENGLISH_STOP_WORDS` . Finally, the resulting list is converted to a string
with `join()`, as follows:

```
docs_without_stopwords = [
' '.join([word for word in doc.split() if word.lower() not in

```

```
ENGLISH_STOP_WORDS])
for doc in docs
]

```

We’ll set up a sparse search and a dense search, starting with a
sparse search based on TF-IDF. We’ll instantiate a `TfidfVectorizer`
before we can create a `tfidf_matrix`, as follows:

```
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(docs_without_stopwords)

```

Before we can calculate similarities based on `cosine_similarity`, we
need a `user_query` embedded with `vectorizer.transform`, as follows:

```
user_query = "Which weather is good for outdoor activities?"

query_sparse_vec = vectorizer.transform([user_query])
sparse_similarities = cosine_similarity(query_sparse_vec, tfidf_matrix).flatten()

```

The object `sparse_similarities` is of the type array, and for 10
sample sentences, it has 10 similarity values corresponding to our
user query. In the next step, we want to get the indices of the most
similar documents. For this step, we’ll create a function

`getFilteredDocsIndices` . This function consumes the similarities and
additionally a `threshold` parameter that excludes all documents
below the value.


Multiple ways exist to get this done. As shown in Listing 6.16, we can
sort the similarities, filter them if they are below the threshold value,
and finally return only the filtered list of document indices.

```
def getFilteredDocsIndices( similarities, threshold = 0.0):
filt_docs_indices = sorted(
[(i, sim) for i, sim in enumerate(similarities) if sim > threshold],
     key = lambda x : x[1],
     reverse =True
)
return [i for i, sim in filt_docs_indices]

```

**Listing 6.16** Hybrid Search: Function for Getting Filtered Indices (Source:
06_RAG/20_hybrid_search.py)


Let’s try the function out with our `sparse_similarities`, as shown in
Listing 6.17.

```
#%% filter documents below threshold and get indices
filtered_docs_indices_sparse =
getFilteredDocsIndices( similarities =sparse_similarities, threshold =0.2)
filtered_docs_indices_sparse

[0, 7, 8]

```

**Listing 6.17** Hybrid Search: Filter Sparse Documents (Source:
06_RAG/20_hybrid_search.py)


In this case, the most similar document is the document with index 0,
followed by index 7, and then index 8.


If you check the user query and the sample sentences, you’ll find
that this does not work very well. We asked, “Which weather is good
for outdoor activities?” and TF-IDF search returned that the most
similar document is “The weather tomorrow will be sunny with a
slight chance of rain.” That response is just not correct. The search
did find the appropriate documents “Hiking in the mountains is an
exhilarating experience, but it can be unpredictable due to weather
changes“ and “Winter sports like skiing and snowboarding require
specific types of weather conditions,” but the rank order was wrong.
The model puts too much focus on the word “weather” and thus
incorrectly returns the document regarding the weather forecast.


Let’s move on and evaluate the performance of the dense search.
For this step, we must embed our sample documents. We’ll use
OpenAI for that purpose, as follows:

```
embeddings = OpenAIEmbeddings()
embedded_docs = [embeddings.embed_query(doc) for doc in docs]

```

Then, we must embed the `user_query` :

```
query_dense_vec = embeddings.embed_query(user_query)

```

Finally, based on cosine similarity, we get a list of similarity scores for
each document, as shown in Listing 6.18.

```
dense_similarities = cosine_similarity([query_dense_vec], embedded_docs)
dense_similarities

array([[0.81677377, 0.74636589, 0.78294997, 0.71723575, 0.783497,
0.71934968, 0.71673343, 0.84183792, 0.84227999, 0.73753417]])

```

**Listing 6.18** Hybrid Search: Get Dense Similarities (Source:
06_RAG/20_hybrid_search.py)


So far, so good. But what we really want is a list of the most similar
documents. Earlier, we created a function for filtering and returning
indices of documents, and we’ll reuse this function now. To get a
small result list of documents, we’ll pass a threshold parameter of
0.8, as shown in Listing 6.19.

```
filtered_docs_indices_dense =
getFilteredDocsIndices( similarities =dense_similarities[0], threshold =0.8)
filtered_docs_indices_dense

[8, 7, 0]

```

**Listing 6.19** Hybrid Search: Filter Dense Documents (Source:
06_RAG/20_hybrid_search.py)


This list looks better. It has found the documents on outdoor
activities (index 8 and index 7) and provides them a rank higher than
the document on the weather forecast (index 0).


Now, we have two similarity lists and need to aggregate them into
one final list. At this point, reciprocal rank fusion comes into play, as
shown in Listing 6.20.

```
def reciprocal_rank_fusion(filtered_docs_indices_sparse,
filtered_docs_indices_dense, alpha=0.2):
# Create a dictionary to store the ranks
rank_dict = {}

# Assign ranks for sparse indices
for rank, doc_index in enumerate(filtered_docs_indices_sparse, start=1):
if doc_index not in rank_dict:

```

```
rank_dict[doc_index] = 0
rank_dict[doc_index] += (1 / (rank + 60)) * alpha

# Assign ranks for dense indices
for rank, doc_index in enumerate(filtered_docs_indices_dense, start=1):
if doc_index not in rank_dict:
rank_dict[doc_index] = 0
rank_dict[doc_index] += (1 / (rank + 60)) * (1 - alpha)

# Sort the documents by their reciprocal rank fusion score
sorted_docs = sorted(rank_dict.items(), key=lambda item: item[1], reverse=True)

# Return the sorted document indices
return [doc_index for doc_index, _ in sorted_docs]

```

**Listing 6.20** Hybrid Search: Function For Reciprocal Rank Fusion (Source:
06_RAG/20_hybrid_search.py)


Listing 6.20 shows the implementation: The function consumes the
two lists of indices—one from the sparse search and the other from
the dense search. Additionally, we can add a weighting parameter

`alpha`, which assigns different weights to the different searches.


A resulting `rank_dict` is initialized as an empty list. There are two
loops, one for each list of indices. Each time, it is iterated over all
documents in these lists. For the document index, the rank value is
added based on the formula `(1 / (rank + 60)) * alpha` (for the sparse
search) and `(1 / (rank +60)) * (1 - alpha)` (for the dense search).


As a result, we get a list of aggregated document indices, in
decreasing order. The first list element represents the most similar
document based on reciprocal rank fusion.


At this point, we can apply this function to our data. With an `alpha`
value of 0.2, we’re giving the sparse search a weighting of 20% in
the final result, and the dense search gets a weighting of 80%, as
follows:

```
reciprocal_rank_fusion(filtered_docs_indices_sparse, filtered_docs_indices_dense,
alpha =0.2)

[8, 7, 0]

```

The final result is identical to the dense search. But play with the
weighting factors, and you’ll see that the order changes at some
point.


This hybrid search could be integrated into a hybrid RAG system.
The corresponding documents to these indices would then be
passed as context information to the LLM together with the user
query and additional instructions. As you can imagine, however,
typically you don’t need to implement such features like reciprocal
rank fusion on your own; these capabilities are already integrated
into vector databases.


In this section, we implemented a hybrid search based on a sparse
search with TF-IDF. Another approach for improving the retrieval is
query expansion, which we’ll turn to next.


**Coding: Query Expansion**


You might know the saying, “Most computer problems sit between
the keyboard and the chair.” While it might seem lazy to say that our
RAG system is fine and the user is at fault, a kernel of truth lies
within. Ultimately, at the end of the day, a RAG response can only be
as good as the user query. How much effort do you put into the
setting up of your queries?


One possible answer (which, admittedly, is our answer) is that
querying is an iterative approach, which is refined over a series of
steps. If a user query is imprecise, we should not expect the RAG
response to be perfect. But still some approaches can help the user
by improving the query. One possible solution is query expansion.
This technique enhances the ability to retrieve relevant documents.
Let’s look at several expansion approaches next:


**Synonym expansion**


Expanding the query with synonyms ensures retrieval of
documents that use different terminology but discuss the same
concept.


Original query → Expanded query


Example: “Climate change” → [“global warming,” “climate
change,” “environmental impact”]


**Related terms expansion**


Including related terms that are often discussed together with
the original query topic improves document retrieval that covers
broader or more specific aspects of the topic.


Example: “Machine learning” → [“machine learning,” “deep
learning,” “artificial intelligence,” “neural networks”]


**Conceptual expansion**


Adding subcategories or specific types of the original concept
allows for retrieving a wider range of documents related to
different forms of renewable energy.


Example: “Renewable energy” → [“renewable energy,” “solar
power,” “wind energy,” “green technology,” “sustainable energy”]


**Phrase variations expansion**


Including variations of how a concept might be phrased ensures
retrieval from documents that use different wording to discuss
the same idea.


Example: “Health benefits of exercise” → [“health benefits of
physical activity,” “exercise health benefits,” “positive effects of
exercise”]


**Contextual expansion**


Including related fields or tasks in the expansion can help
retrieve more diverse documents that approach the original
concept from different angles.


Example: “Natural language processing” → [“natural language
processing,” “text analysis,” “computational linguistics,”
“language modeling”]


**Temporal expansion**


Expanding for common abbreviations and alternative names
ensures that relevant documents using different temporal or
popular references are also retrieved.


Example: “COVID-19 vaccines” → [“COVID-19 vaccines”,
“COVID vaccines”, “coronavirus immunization”, “SARS-CoV-2
vaccine”]


**Entity-based expansion**


When a query involves an entity, expanding the query with
related people, products, or attributes associated with the entity
can enhance retrieval quality.


Example: “Tesla” → [“Tesla,” “Elon Musk,” “electrical vehicles,”
“autonomous driving”]


By incorporating these types of expansions, you can maximize the
information retrieved for a query, resulting in more effective
responses in a RAG system.


Implementing query expansion is a rather easy task, as in the
following:

```
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv('.env')

```

Listing 6.21 shows the function definition. We’ve set up a function

`query_expansion` for improving the query. The function receives the

`query` and returns the number of expanded queries.

```
def query_expansion( query : str, number : int = 5, model_name : str = "llama3-70b8192") -> list[str]:
messages = [
("system","""You are part of an information retrieval system. You are given
a user query and you need to expand the query to improve the search results. Return
ONLY a list of expanded queries.
Be concise and focus on synonyms and related concepts.
Format your response as a Python list of strings.
The response must:
1. Start immediately with [
2. Contain quoted strings
3. End with ]
Example correct format:
["alternative query 1", "alternative query 2", "alternative query 3"]
"""),
("user", "Please expand the query: '{query}' and return a list of {number}
expanded queries.")
]
prompt = ChatPromptTemplate.from_messages(messages)
chain = prompt | ChatGroq( model_name =model_name)
res = chain.invoke({"query": query, "number": number})
return eval(res.content)

```

**Listing 6.21** Query Expansion: Function (Source: 06_RAG/90_query_expansion.py)


The major work is in setting up the messages, especially convincing
the model to avoid babbling and instead directly returning a string
that starts with the list. You might choose to implement Pydantic to
get a structured output as a list of strings. We leave this task up to
you as a quick exercise.


The final result should look like “[…]” instead of something like “Here
is the expanded list of queries:\n\n[…].” You cannot simply instruct
the model to return a Python list, but you should provide detailed
instructions on how the response should look like. We were
successful with the instruction set shown in Listing 6.22.

```
The response must:
1. Start immediately with [
2. Contain quoted strings

```

```
3. End with ]
Example correct format:
["alternative query 1", "alternative query 2", "alternative query 3"]

```

**Listing 6.22** Query Expansion: Output Format (Source:
06_RAG/90_query_expansion.py)


The user message holds the information to process the query and
return the number of expanded queries.


In the return statement, the model response is evaluated to a Python
object, so that we successfully get a list of strings holding the
expanded queries. We can test this functionality out, as follows:

```
res = query_expansion( query ="artificial intelligence", number =3)
res

['machine learning', 'natural language processing', 'computer vision']

```

**Context Enrichment**


If you work with a corpus of multiple different documents,
distinguishing between different documents can be difficult. For
example, if you work with financial documents, an essential task
might be to distinguish between quarters and companies. Normal
chunking techniques can have difficulties with this kind of thinking.


Figure 6.7 shows the concept behind conceptual retrieval, which can
overcome this issue. Each chunk is enhanced with its own context.
This context provides useful information on the location of the chunk


in a specific document. For example, the enhanced chunk might
refer to the previous and next quarter of the company under study.


**Figure 6.7** Contextual Retrieval (Source: Adapted from
_[https://www.anthropic.com/news/contextual-retrieval](https://www.anthropic.com/news/contextual-retrieval)_ )


How does contextual retrieval work? Each document from a larger
corpus is chunked. The complete corpus, or the relevant documents
from the corpus, are passed to the LLM, together with a chunk for
extracting contextual information for that particular chunk.


As you can imagine, sending a complete, relevant document
together with each chunk to an LLM can become extremely costly.
Now, the concept of prompt caching comes into play. Since prompt
caching is a RAG alternative, we’ll cover it in more detail in
Section 6.4. But to anticipate this topic, just know that prompt
caching is a cheap solution to the problem. With this technique, the
complete relevant document is cached for a limited time and does
not need to be sent each time to the LLM.


In the end, all chunks are processed, and each chunk was enhanced
with contextual information. This new chunk (context plus original
chunk) can now be stored in some vector database. Studies have
found that this approach can significantly outperform both simple
RAG systems and hybrid RAG systems.


### **6.3.3  Advanced Postretrieval Techniques**

After the documents are retrieved, you can still improve upon your
RAG system. One interesting approach is _prompt compression_ .
Imagine that the prompt enhanced with all contexts from the retrieval
process is getting long. As a result, the LLM must deal with
increased noise, which reduces the LLM’s performance. Also, since
you need to pay for tokens, the cost is high. What can you do to
save costs? You can compress the length of the context while
maintaining its essential information, which is the idea behind prompt
compression, as shown in Figure 6.8.


**Figure 6.8** Prompt Compression


The augmented user query, which possibly has become quite long,
is sent to an LLM to be shortened in a way that maintains its
meaning. But if we send the augmented query to an LLM to shorten
it, we then need to send it to the “final” LLM to get the RAG
response. We even have two LLM calls—so what is the point?


This approach only makes sense if you send the long, augmented
prompt to a small, fast, and cheap LLM for shortening. For the RAG
response, you can then send the prompt to the LLM of your choice.


If you have many LLM calls and large contexts, this approach can
significantly lower your costs, increase the performance, and
enhance efficiency.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **6.4  Coding: Prompt Caching**

Prompt caching is a new approach developed by Anthropic and is
provided currently only as a beta feature. Recall that passing a
complete document to the LLM with every request is inefficient.
While still true, Anthropic has developed an approach that addresses
this problem. Figure 6.9 shows how the concept of prompt caching
works.


**Figure 6.9** Prompt Caching


With prompt caching, the user sends a request to the LLM. In this
request, the user passes the query together with the complete
document. Wait, what? Didn’t we just say that sending the complete
is extremely inefficient?


Yes, but the user also tells the model to cache the document. The
LLM provider caches the complete document when passed the first
time. The document is not cached forever, only for a limited time. At
the time of writing, a document is cached for 5 minutes. Every
subsequent user query within that time interval sent to the LLM
together with the complete document does not require a new


caching. Instead, the document is taken from the cache to create the
answer.


Some specific use cases for this technique include the following:


Repetitive tasks


Running many examples


Long conversations


Using RAG as contextual retriever (as discussed earlier in
Section 6.3.2)


Of these use cases, we want to focus on the last one. This technique
is an enabler of a technique called contextual retriever which can
significantly improve your RAG results. For now, we’ll focus on how
to implement prompt caching. Prompt caching enables a technique
called _contextual retrieval_, which is outside the scope of this book.
You can read more about this topic at
_[https://www.anthropic.com/news/contextual-retrieval](https://www.anthropic.com/news/contextual-retrieval)_ .


We’ll develop a continuous chat with an LLM. The conversation is
based on some fixed context. In our example, we’ll use the complete
book _The Hound of the Baskervilles_ . This context information is
cached for a limited time, so that we create the cached tokens once
—at the beginning of the conversation. With a normal RAG, we
would send this context with every request as input tokens. But since
the document is now cached, we can achieve some inference gains
(faster model responses), but also dramatically reduced costs.


The creation of the cache is slightly more expensive than sending
normal input tokens (by about 25%). The idea is to outweigh this
added effort with massively reduced costs since reading cached
tokens is 90% cheaper than reading input tokens.


Listing 6.23 shows the packages we’ll use in this script. As the LLM,
we’ll use Anthropic’s Claude. For a nicely rendered output, we’ll also
load `rich` .

```
import anthropic
import os
from rich.console import Console
from rich.markdown import Markdown
from langchain_community.document_loaders import TextLoader
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(usecwd=True))

```

**Listing 6.23** Prompt Caching: Required Packages (Source:
06_RAG/40_prompt_caching.py)


At the time of writing, prompt caching is a beta feature not well
integrated into LangChain. This integration is coming, but for now,
you’ll need to interact directly with the Anthropic client, as follows:

```
client = anthropic.Anthropic( api_key =os.getenv("ANTHROPIC_API_KEY"))

```

The complete prompt caching functionality is bundled into a class, as
shown in Listing 6.24. We’ll develop it step by step.

```
class PromptCachingChat:
def __init__(self, initial_context: str):
self.messages = []
self.context = None
self.initial_context = initial_context

```

**Listing 6.24** Prompt Caching: Class Initialization (Source:
06_RAG/40_prompt_caching.py)


First, we create the class. During the instantiation of the class object,
we pass some `initial_context` as a string. The other properties
( `messages` and `context` ) are initialized as an empty list and as `None`,
respectively; both will be populated in the process.


We’ll set up several methods in this exercise. As shown in
Listing 6.25, the method `run_model` will invoke the LLM.


```
def run_model(self):
self.context = client.beta.prompt_caching.messages.create(
model="claude-3-haiku-20240307",
max_tokens=1024,
system=[
{
"type": "text",
"text": "You’re a patent expert. You’re given a patent and will be asked to answer
questions about it.\n",
},
{
"type": "text",
"text": f"Initial Context: {self.initial_context}",
"cache_control": {"type": "ephemeral"}
}
],
messages=self.messages,
)
# add the model response to the messages
self.messages.append({"role": "assistant",
"content": self.context.content[0].text})
return self.context

```

**Listing 6.25** Prompt Caching: Run Model Method (Source:
06_RAG/40_prompt_caching.py)


The LLM is called with a system message. But the system prompt
does not only hold the information on how the model should behave
and answer. Additionally, the initial context is passed, alongside a

`cache_control` parameter that will enable the caching. This
parameter requires the type `ephemeral` .


The `messages` need to be passed as well. The model’s response is
stored in the object `self.context` . As soon as the model output is
available, the messages are appended with it.


Good! But we want the user to interact with it, so we need to fetch
the `user_query` and call our method `run_model` . As shown in
Listing 6.26, our next method `user_turn` consumes the `user_query` as
an input.

```
def user_turn(self, user_query: str):
self.messages.append({"role": "user", "content": user_query})

```

```
self.context = self.run_model()
return self.context

```

**Listing 6.26** Prompt Caching: User Method (Source: 06_RAG/40_prompt_caching.py)


The `messages` object is appended with the user message, and in the
next step, the `run_model` method is called. We’ll keep the model
output in the `context` .


Basically, we’re done. We have a system that reacts to user queries
and calls the model. But for nicer outputs, we’ll finally define a
method called `show_model_response`, as shown in Listing 6.27.

```
def show_model_response(self):
console = Console()
console.print(Markdown(self.messages[-1]["content"]))
console.print(f"Usage: {self.context.usage}")

```

**Listing 6.27** Prompt Caching: Showing Model Output (Source:
06_RAG/40_prompt_caching.py)


In this function, we’ll use the `rich` package and print the last model
output in Markdown. Additionally, we will display the token usage to
check if the prompt caching actually worked.


Let’s test this function out. In the first step, we need to load our book.
The code shown in Listing 6.28 provides access to the book file and
loads it with `TextLoader` .

```
file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(file_path)
parent_dir = os.path.dirname(current_dir)

file_path = os.path.join(parent_dir, "05_VectorDatabases",
"data","HoundOfBaskerville.txt")
file_path

#%% (3) Load a single document
text_loader = TextLoader(file_path=file_path, encoding="utf-8")
doc = text_loader.load()
initialContext = doc[0].page_content

```

**Listing 6.28** Prompt Caching: Test (Source: 06_RAG/40_prompt_caching.py)


Now, we can create an instance of our class, the object

`promptCachingChat` . During initialization, we pass the `initialContext` .
Then, we start the conversation with `user_turn` and send our first
query, as follows:

```
promptCachingChat = PromptCachingChat( initial_context =initialContext)
promptCachingChat.user_turn("what is special about the hound of baskerville?")
promptCachingChat.show_model_response()

```

The result is shown in Figure 6.10.


**Figure 6.10** Prompt Caching: First Chat Round with Cache Creation


The model provides a detailed output, but what is more interesting is
the fact that 93,104 cache tokens were created. In the subsequent
chat, we’ll see if the caching worked and the cached tokens are
used. Let’s now ask if the hound is the murderer, as follows:

```
promptCachingChat.user_turn("Is the hound the murderer?")
promptCachingChat.show_model_response()
print(promptCachingChat.context.usage)

```

Again, the result is shown in Figure 6.11.


**Figure 6.11** Prompt Caching with Reading Cached Tokens


No further cached tokens were created, and all cached tokens were
read. Amazing! The model provides the result much more quickly.
Was it cheaper than without caching? We’ll use the assumptions that
normal tokens cost 1 unit, that cache creation costs 1.25 units, and
that reading cached input tokens 0.1 units.


In the first round of the conversation, prompt caching was more
expensive than without caching, but the tide starts turning in the
second round because reading from the cache is pretty cheap
compared to using normal tokens.


Thus concludes our discussion of prompt caching. Next, you’ll learn
how to measure the performance of your RAG systems.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **6.5  Evaluation**

RAG systems work surprisingly well, but what does “well” actually
mean? And how can we compare the effectiveness, accuracy, and
efficiency of different RAG approaches? For this reason, RAG
evaluation techniques try to measure the following parameters:


**Effectiveness**
Does our RAG system retrieve and use the relevant knowledge?


**Accuracy**
How good are the generated responses? Are they grounded in
facts and coherent?


**Efficiency**
How well does our system perform in different scenarios?


To make all this measurable and comparable, different metrics can
be applied. So many metrics exist that only a small number can be
presented.


First, we’ll look at some of the challenges that RAG systems face.
Based on these findings, we’ll discuss some metrics and how they
can make these challenges measurable.


After several metrics have been presented, we’ll implement them in
Python. Let’s start with a closer look at some of the challenges RAG
systems face.

### **6.5.1  Challenges in RAG Evaluation**


How can we measure the quality of an answer? Some hard facts can
be checked, for instance, how good the data retrieved from the


knowledge source is. We’ll focus on two challenges:


**Retrieval quality**
If the retriever fetches incorrect or irrelevant documents, the RAG
system is likely incorrect. A cascading effect occurs in that RAG
quality is inherently tied to the quality of the retrieved data. Luckily,
several metrics are available for determining retrieval quality.


**Subjectivity**
If you ask multiple human evaluators, they will provide different
ratings on a RAG response. Everybody has personal preferences
regarding brevity and style. For example, a technical expert might
prioritize precision and factual accuracy, whereas a layperson
might prefer readability and simplicity.


Always keep in mind the target user of your system and ensure
your evaluators are trained to get consistent results.

### **6.5.2  Metrics**


Earlier when we discussed RAG improvements, we broke down the
system into its different parts—retrieval, and generation. We can
follow the same approach when it comes to metrics because metrics
exist for the different stages. Some are considered joint metrics.
Figure 6.12 shows some RAG evaluation metrics and how they can
be classified into retriever, generator, and joint metrics.


**Figure 6.12** RAG Evaluation Metrics


Among retriever metrics, classic classification metrics include
precision@k and recall@k. Another metric that we’ll study is _context_
_relevance_ .


Of the generator-based metrics, we want to highlight _factual_
_correctness_ . Finally, joint metrics try to measure both the retriever
and the generator quality in a combined metric. Some examples
include _answer relevance_ and the _F1 score_ . Let’s look at some of
these metrics in more detail next.


**Retriever Metric: Context Precision**


Context precision is a retriever metric for evaluating the ground-truth
items and determining whether they are part of the context
information. In perfect cases, all relevant chunks returned by the
retriever can be found at the top ranks.


Context precision uses the user query, a ground truth, and the
context information for its calculation. The resulting score is between
0 and 1, with higher values representing higher precision:


K corresponds to the number of chunks in the context, and vk
corresponds to the relevance indicator at rank k.


**Generator Metric: Factual Correctness**


Factual correctness measures whether the information in a RAG
response aligns with established facts. Different aspects must be
considered in this task, such as the following:


**Fact granularity**
A response might be partially correct, meaning correct in one


aspect, but incorrect in another. A correct statement is
“Shakespeare wrote many plays,” but it would be incorrect to state
“Shakespeare wrote the play _Waiting for Godot_ .”


**Consistency over time**
The measure might have a temporal aspect, in that a fact might be
correct for a given point in time, but incorrect for another one. For
example, answering the question “Who is the president of country
X?” depends on when the question is asked since the fact could
change after every election.


**Attribution**
RAG responses should attribute facts to the correct source. For
example, it would be wrong to attribute the theory of special
relativity to Newton instead of Einstein.


**Joint Metric: Answer Faithfulness**


Answer faithfulness measures the factual consistency of the RAGgenerated answer against the context information. This metric uses
the RAG answer and the retrieved context information for its
calculation:


The score ranges from 0 to 1 with lower values corresponding to
lower faithfulness, and vice versa.


**Joint Metric: Answer Relevance**


Answer relevance evaluates the alignment of the generated answer
with the user query. This metric considers the retrieved context and
measures how well the retrieval and generator work together.


Figure 6.13 shows the RAG evaluation metric concept answer
relevance.


This approach follows the classic RAG approach to receive an RAG
answer. Based on that RAG answer, an LLM creates N questions,
that potentially could result in that RAG answer. These N synthetic
questions are then embedded and compared to the embedding of
the user query. The average of these similarities is the answer
relevance.


**Figure 6.13** RAG Evaluation Metric: Answer Relevance


In technical terms, the answer relevance is calculated with the
following equation:


This value ranges from 0 to 1, in which low values correspond to
answers that are incomplete or that hold redundant information. High
values correspond to more relevant answers.

### **6.5.3  Coding: Metrics**


Now, let’s implement these metrics. For this task, we’ll use a Python
framework that has been developed specifically for evaluating RAG


systems, namely, RAGAS ( _[https://www.ragas.io/](https://www.ragas.io/)_ ). You can easily
install it via uv, as follows:

```
uv add ragas

```

RAGAS has a nice web interface that you can use to evaluate larger
datasets and RAG responses with derived metrics. If you work on a
“real” project with business impact, we highly recommend diving
deeply into RAGAS, starting with its **Getting Started** section
( _[https://docs.ragas.io/en/v0.1.21/getstarted/index.html#](https://docs.ragas.io/en/v0.1.21/getstarted/index.html)_ ).


In this book, we’ll show only the basics of how to set up RAGAS to
calculate RAG evaluation metrics. What you need is the following:


`user_query` or `question` as an input to the RAG system


`contexts` that represent the retrieved documents from the
knowledge source


`answer` for the RAG response


`ground_truth` is required only for some metrics like _context_
_precision_ . This information is used to check whether the retrieved
chunk is relevant to arrive at the ground truth.


The complete script can be found in _06_RAG\60_rag_eval.py_ . As
shown in Listing 6.29, we start by loading the required packages.

```
#%% packages
from datasets import Dataset
from ragas.metrics import context_precision, answer_relevancy, faithfulness
from ragas import evaluate
from langchain_openai import ChatOpenAI

```

**Listing 6.29** RAG Evaluation: Required Packages (Source: 06_RAG\60_rag_eval.py)


We must bring the data to be evaluated into a format that RAGAS
can process. For this step, we load `Dataset` . We also need some

`metrics` from `ragas` as well as its `evaluate` function.


Now, we must prepare our data. The data preparation step is shown
in Listing 6.30. The data must be passed in the format `Dataset`,
which we can create based on a dictionary. That dictionary requires
the keys `question`, `contexts`, `answer`, and `ground_truth` .

```
# %% prepare dataset
my_sample = {
"question": ["What is the capital of Germany in 1960?"],
"contexts": [
[
"Berlin is the capital of Germany since 1990.",
"Between 1949 and 1990, East Berlin was the capital of East Germany.",
"Bonn was the capital of West Germany during the same period."
]
], # Nested list for multiple contexts
"answer": ["In 1960, the capital of Germany was Bonn. East Berlin was the
capital of East Germany."],
"ground_truth": ["Berlin"]
}

dataset = Dataset.from_dict(my_sample)

```

**Listing 6.30** RAG Evaluation: Dataset (Source: 06_RAG\60_rag_eval.py)


Our example is centered around Berlin, the capital of Germany. The
question is tricky because time inconsistency exists because Berlin
was not always the capital. Finally, we can start the evaluation
process, as shown in Listing 6.31.

```
# %% evaluation
llm = ChatOpenAI( model ="gpt-4o-mini")
metrics = [context_precision, answer_relevancy, faithfulness]
res = evaluate( dataset =dataset,
         metrics =metrics,
         llm =llm)
res

{'context_precision': 1.0000, 'answer_relevancy': 0.9934, 'faithfulness': 0.5000}

```

**Listing 6.31** RAG Evaluation: Evaluation (Source: 06_RAG\60_rag_eval.py)


We must still set up an LLM instance and pass it to the `evaluate`
function. Other parameters that need to be passed include the
dataset and the metrics that should be analyzed. The result holds


the scores for these metrics. For a larger dataset, you can analyze
these metrics for all data to find issues in your RAG system, so that
you can improve the system further.


For now, we’ve concluded our short introduction to the evaluation of
RAG systems.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **6.6  Summary**

In this chapter, we delved into the concept of RAG. This powerful
tool can greatly assist you when you need to enhance an LLM
response with your own content or documents. In most cases, this
approach is more promising and preferred to fine-tuning a complete
LLM.


We started with understanding the implementation of naïve (or
standard) RAG, which consists of the retrieval, augmentation, and
generation process. Later, we studied more detailed techniques to
improve the system at different stages, including improvement
strategies for pre-retrieval, in which the indexing pipeline is adapted
in different ways.


In advanced retrieval techniques, you learned how a hybrid RAG
system functions. Other techniques like query expansion and context
enrichment were presented.


During advanced post-retrieval techniques, you learned about
prompt compression as a means to remove irrelevant tokens from an
LLM request.


Finally, we studied several RAG evaluation metrics, and you learned
how to implement these metrics to measure the quality of your RAG
systems.


In conclusion, RAG represents a significant advancement in the field
of artificial intelligence. By merging retrieval and generative
techniques, RAG opens new possibilities for creating high-quality,
contextually rich outputs. This chapter equipped you with a
comprehensive understanding of the concept, experimental results,


and practical applications, preparing you to implement this powerful
tool in your own projects.


_[OceanofPDF.com](https://oceanofpdf.com/)_


# 7  Agentic Systems

_I'm sorry, Dave. I'm afraid I can’t do that._
_—HAL 9000 in 2001: A Space Odyssey_


With these words, HAL 9000, the artificial intelligence from _2001: A_
_Space Odyssey_, embodies the essence of agentic systems. Agentic
systems are technologies that operate beyond simple commands.
They make decisions that sometimes defy human intentions. HAL,
designed to support and protect the crew, shifts its objectives,
challenging the human operators’ control and opening a narrative of
machine autonomy and agency.


In this chapter on agentic systems, we immerse ourselves in how AI
models are empowered to operate autonomously within predefined
guidelines, making decisions and performing actions to achieve
specific goals. Unlike traditional generative artificial intelligence
(generative AI) models that respond passively to user prompts,
agentic systems are designed to understand objectives, adapt to
dynamic inputs, and make context-sensitive choices without constant
human guidance.


By leveraging task management, contextual awareness, and goaloriented reasoning, these systems can handle complex workflows.
Also, they can interact across multiple stages of a process and even
integrate with other tools and data sources. This chapter explores
the foundational principles, design considerations, and applications


of agentic systems, highlighting their growing role in transforming AI
from reactive tools into proactive collaborators.


We’ll start in Section 7.1 with an introduction into AI agents. You’ll
learn what an agent is and what tradeoffs need to be considered. In
Section 7.2, we’ll take a closer look at different frameworks. You’ll
learn about the available frameworks and gain some understanding
about their differences and capabilities.


Then, we dive into the deep end and implement some agentic
systems. We’ll start with simple agents in Section 7.3 and then
become familiar with different frameworks in subsequent sections.
Among these agentic frameworks we’ll encounter are LangGraph in
Section 7.4, AG2 in Section 7.5, CrewAI in Section 7.6, OpenAI
Agents in Section 7.7, and finally Pydantic AI in Section 7.8.


These systems can manage many agent interactions, but it is hard to
debug such systems. In this context, monitoring systems come to the
rescue, and we’ll study some options in Section 7.9.


Let’s first learn what AI agents are in the next section.

## **7.1  Introduction to AI Agents**


Let’s start by asking what an AI agent is. An agentic system is an AI
system that is designed to operate autonomously to complete tasks.
In doing so, the system often interacts with its environment and uses
tools. It can make decisions; take actions; and adapt its behavior
based on goals, on external information, or if the context changes.


These agentic systems typically use large language models (LLMs)
combined with tools, memory, or reasoning frameworks to achieve


complex, multistep tasks without additional user guidance. Figure 7.1
shows the workflow of an agentic system.


**Figure 7.1** Agentic System Workflow


The user sets up a query that will be handled by an agent. Imagine
an agent as a supercharged LLM. The LLM can generate thoughts.
Based on that reasoning, a suitable tool can be selected. The output
of the tool call is reviewed, and if the output is considered useful to
close the task, it returns the output. Otherwise, the agent starts the
next loop, in which it creates more thoughts, selects a tool, and so
on.


As in life, you must often deal with tradeoffs and can’t get everything
at once. One tradeoff you should consider, shown in Figure 7.2, is
the tradeoff between flexibility and reliability when considering agent
autonomy. Flexibility and reliability can fall over different ranges of
agent autonomy.


_Flexibility_ in this context can be defined as the system’s ability to
adapt to diverse tasks, input, and contexts with minimal need for
explicit reconfiguration. _Reliability_ in this context refers to the ability
to consistently perform as intended, that is, to deliver accurate and
predictable outcomes across diverse scenarios and conditions.


Agent autonomy can range from simple code, to chains developed
with LangChain, to routers, to full autonomy.


**Figure 7.2** Agent Flexibility/Reliability versus Autonomy


In an ideal scenario, you want an agentic system with high flexibility
and reliability, and at the same time, the agent should be completely
autonomous. This full autonomy is not usually possible (yet).


With less autonomy, you get a system with high reliability that, at the
same time, shows low autonomy. The opposite holds as well: An
agentic system that is fully autonomous usually is quite flexible but
has low reliability. The aim of the different frameworks is to increase
autonomy without sacrificing too much on flexibility or on reliability.


Different approaches to achieve this goal are available. A whole
ecosystem has developed around agentic frameworks, and several
new frameworks are released every month. Over time, we’ll see
which will grow and survive. In the long run, we expect a whole
family of frameworks that fulfill different needs. In this chapter, we’re
using the most popular frameworks at the time of writing (March
2025).


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **7.2  Available Frameworks**

In Python, several frameworks support the development of agentic
systems. They provide tools for autonomy, decision-making, and
interaction with the environment. The field is extremely dynamic, and
new frameworks emerge while others disappear. Since which
frameworks will survive is not clear, we’ll present several options in
this section.


Let’s briefly summarize these frameworks first before exploring them
in depth:


**LangGraph**
You know LangChain by now, but we haven’t used it in an agentic
way yet. For agent autonomy, the developers of LangChain
created an additional framework built on top of LangChain, called
LangGraph ( _[https://www.langchain.com/langgraph](https://www.langchain.com/langgraph)_ ).


LangGraph is a flexible framework that enables developers to
design, build, and manage agentic systems. This framework
makes use of a graph-based representation of tasks, workflows,
and the decision-making process. It provides an intuitive way to
define complex workflows by treating tasks as nodes and their
dependencies as edges within a directed graph.


By combining graph theory with the capabilities of LLMs,
LangGraph empowers developers to create agentic systems that
balance flexibility, reliability, and autonomy. We’ll dive more deeply
into LangGraph in Section 7.4.


**Haystack**
Haystack ( _[https://haystack.deepset.ai/](https://haystack.deepset.ai/)_ ) is another framework,


mainly used for LLMs and retrieval-augmented generation (RAG).
But this framework also allows you to use tools and agents.


**AG2**
AG2 ( _[https://github.com/ag2ai/ag2](https://github.com/ag2ai/ag2)_ ), also called AgentOS or its
former name autogen, is an agentic system created by Microsoft.
This system simplifies the creation and orchestration of multiagent systems, and it can solve complex tasks with minimal
human intervention. We’ll explore the intricacies of AG2 in
Section 7.5.


**CrewAI**
CrewAI ( _[https://www.crewai.com/](https://www.crewai.com/)_ ) is a multi-agent system that
allows users to quickly build automations. We take a look at this
system in Section 7.6.


**OpenAI Agents**
OpenAI Agents ( _[https://github.com/openai/openai-agents-python](https://github.com/openai/openai-agents-python)_ )
is a lightweight, but powerful, framework specifically designed for
multiagent workflows. Fun to work with and quite approachable,
you’ll learn how to use it in Section 7.7.


**Magentic-One**
Magentic-One
( _https://github.com/microsoft/autogen/tree/main/python/packages/_
_autogen-magentic-one_ ) is another framework developed by
Microsoft, built on top of AG2.


Magentic-One has a powerful feature: interacting with the digital
world. This multi-agent system is designed for dealing with openended tasks. These tasks can make use of the web and the
operating system on which it runs. The system is designed to work
on the real tasks that people encounter in their daily lives.


**Tiny Troupe**
Tiny Troupe ( _[https://github.com/microsoft/TinyTroupe](https://github.com/microsoft/TinyTroupe)_ ) is yet
another agentic framework developed by Microsoft. Still
experimental and young, its focus is on creating multi-agent
simulations of personas.


This framework can be used to evaluate digital ads with a
simulated audience before spending actual money on a campaign.
Furthermore, the framework can create test inputs to systems for
software testing, or you can use it to evaluate project or product
proposals. The framework is quite simple to set up and to use.


**Pydantic AI**
Pydantic AI is an agentic framework for developing productiongrade applications. Important features for production-grade
applications include, most importantly, type safety which enables
structured inputs and outputs. This framework is also model
agnostic and, as such, allows the use of various LLMs. It neatly
integrates with Logfire, a monitoring system from the same
development team. One of our favorite systems, we cover it in
Section 7.8.


Before we look more closely at all these options, let’s start by
discussing simple agents.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **7.3  Simple Agent**

In Chapter 6, we worked with RAG. We’ll build upon that knowledge
with a simple implementation of an agentic RAG. Then, we’ll develop
an agentic system that combines both reasoning and acting and thus
is called _ReAct_ .

### **7.3.1  Agentic RAG**


Agentic RAG describes a system that relies on RAG, but with a small
tweak. In the pipeline, intelligent AI agents are enabled to improve
the system whenever the results are insufficient. For example, when
the RAG system does not retrieve relevant information from the data
retrieval system (typically the vector database), other information
sources are tapped and used generating the final answer. In our first
coding example, we’ll implement this functionality. Figure 7.3 shows
the workflow of our agentic RAG system.


After the vector database provides information, the information is
analyzed for its relevance. If not sufficiently relevant, data is
retrieved via tool use, specifically by searching the internet. Then,
the information is used for creating a final output that can be
returned to the user. The complete code can be found in
_07_AgenticSystems\10_agentic_rag.py_ .


In our code, we’ll use a tool for searching the internet called Tavily,
which is an online service empowering AI apps to quickly search the
internet. Before you can use this service in your applications, you


must set up an application programming interface (API) key by
creating an account and the API key at _[www.tavily.com](http://www.tavily.com/)_ .


**Figure 7.3** Agentic RAG Workflow


You should call the API key `TAVILY_API_KEY` and add it to your _.env_
file. Don’t worry about costs for now—they provide a generous free
tier, which will definitely be enough for you to experiment. The entry
in your _.env_ file should look like the following:

```
TAVILY_API_KEY=tvly-…

```

After you load the environment in the usual way, create an instance
of `TavilySearchResults` . To test if this step worked, invoke the
instance, for example, with the following code:

```
search_tool.invoke("what is rag?")

```

This command will return a list of dictionaries. Each dictionary
contains the keys `url` and `content`, as follows:

```
[{'url': 'https://www.geeksforgeeks.org/what-is-retrieval-augmented-generationrag/',
'content': 'RAG is a natural language processing approach that combines retrieval
…}, …]

```

As shown in Listing 7.1, at the beginning of the script, we’re loading
the necessary packages. Noteworthy in this context is the `FAISS`
package. Standing for “Facebook AI similarity search,” `FAISS` is a
small and simple implementation of a vector database.

```
#%% packages
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import WikipediaLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
load_dotenv(find_dotenv( usecwd =True))

```

**Listing 7.1** Agentic RAG: Required Packages (Source:
07_AgenticSystems\10_agentic_rag.py)


Our data source is Wikipedia. We’ll create a vector database and
follow the classic data ingestion pipeline step by step. As shown in
Listing 7.2, we’ll first load ten articles on the “principle of relativity.”
We’ll follow the classic indexing pipeline from Chapter 5, as follows:


1. First, we’ll create chunks of Wikipedia article data.


2. Embeddings based on `OpenAIEmbeddings` are created.


3. The `vectorstore` is populated with the `chunks` and corresponding

`embeddings` .


4. A `retriever` enables quick searches of the database.


As an alternative approach, we can initialize web search. For this
functionality, we’ll use `TavilySearchResults`, as shown in Listing 7.2.

```
# Load documents for retrieval (can be replaced with any source of text)
# Here we're using a text loader with some sample text files as an example
#%% import wikipedia
loader = WikipediaLoader("Principle of relativity",
               load_max_docs =10)
docs = loader.load()

#%% create chunks

```

```
text_splitter = RecursiveCharacterTextSplitter( chunk_size =1000, chunk_overlap =200)
chunks = text_splitter.split_documents(docs)

#%% models and tools
llm = ChatOpenAI( model ="gpt-4o-mini", temperature =0)
embedding = OpenAIEmbeddings()
search_tool = TavilySearchResults( max_results =5, include_answer =True)

#%% use FAISS to store the chunks
vectorstore = FAISS.from_documents(chunks, embedding)
retriever = vectorstore.as_retriever( return_similarities =True)

#%% user query
query = "What is relativity?"

```

**Listing 7.2** Agentic RAG: Vector Database Creation (Source: 07_AgenticSystems\
10_agentic_rag.py)


The RAG chain shown Listing 7.3 is based on a `prompt_template` . In
this example, we provide the `context` and the `question` . The

`retrieved_docs` are passed as `context` to the `chain` . An important
aspect in the prompt template is the instruction to return

`’insufficient information’` if the answer cannot be known based on
the `context` . This output is later used in a router to decide if further
information must be loaded from the internet or if the RAG output
can be used as the final answer.

```
#%% RAG chain
prompt_template = ChatPromptTemplate.from_messages([
("system", """
You are a helpful assistant that can answer questions about the principle of
relativity. You will get contextual information from the retrieved documents. If you
don't know the answer, just say 'insufficient information'
"""),
("user", "<context>{context}</context>\n\n<question>{question}</question>"),
])
retrieved_docs = retriever.invoke(query)
retrieved_docs_str = ";".join([doc.page_content for doc in retrieved_docs])
chain = prompt_template | llm
rag_response = chain.invoke({"question": query,
"context": retrieved_docs_str})

```

**Listing 7.3** Agentic RAG: RAG Setup (Source: 07_AgenticSystems\10_agentic_rag.py)


Listing 7.4 shows the router—the building block that checks if an
internet search tool is needed or if the RAG output can be used. In
this simple example, the router is implemented as a basic if-else
statement.

```
if rag_response.content == "insufficient information":
print("using search tool")
final_response = search_tool.invoke({"query": query})
final_response_str = ";".join([doc['content'] for doc in final_response])
final_response = chain.invoke({"question": query,
"context": final_response_str})
else:
print("using vector store")
final_response = rag_response.content

final_response

Relativity, in the context of physics, refers to the scientific theories developed
by Albert Einstein that describe the relationship between space and time. It
encompasses two main theories: special relativity and general relativity. Special
relativity, introduced in 1905, is based on two key postulates: the laws of physics
are the same in all inertial frames of reference, and the speed of light in vacuum
is constant for all observers, regardless of their motion. General relativity,
published in 1915, extends these concepts to include the effects of gravity on the
structure of spacetime. Together, these theories have profound implications for our
understanding of the universe and have been confirmed by numerous experiments.

```

**Listing 7.4** Agentic RAG: Router Logic (Source: 07_AgenticSystems\agentic_rag.py)


That’s it for our simple implementation of an agentic RAG system!


In the next section, you’ll learn about ReAct—a paradigm where
agents iteratively reason and act based on the outcomes of previous
steps.

### **7.3.2  ReAct**


ReAct is a technique that combines reasoning and acting. This
combination allows you to improve how LLMs interact with
information and with their environment.


In the reasoning phase, thoughts are generated. In the acting phase,
tools are used to perform tasks. This approach is valuable for
agentic systems, in which a model must decide on the next step
depending on a given context. Let’s break down these two tasks in
more detail:


**Reasoning steps**
The model can break down a complex problem into smaller steps,
which improves the accuracy and transparency of a model’s
decisions. For instance, if a model is supposed to retrieve
information from a database, it might first decide what specific
information it needs, outline why it needs that information, and
then act accordingly.


**Acting based on reasoning**
After reasoning through a problem, the model decides on an
action, such as retrieving data, formulating an answer, or updating
its plan. ReAct thus brings structure and coherence to multi-step
processes by combining planning and action, so the model doesn't
just produce isolated outputs but instead follows some logical
progression.


Let’s see how ReAct works in practice. You can find the sample code
in _07_AgenticSystems\20_react.py_ . In this scenario, we want to
check if agent can “know” about things already discussed.
Furthermore, the agent will be able to select a tool to reach a certain
goal.


As shown in Listing 7.5, we’ll load the packages we need in for
script. Newcomers to this list of packages are `MemorySaver` and

`create_react_agent` . `MemorySaver` enables the agent to retrieve some
memory, which is helpful for longer conversations so the agent can
refer to earlier discussions. With `create_react_agent`, we can easily
set up a ReAct agent. With these packages, we are ready to go.


```
#%% packages
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv( usecwd =True))

```

**Listing 7.5** ReAct Agent: Required Packages (Source: 07_AgenticSystems\20_react.py)


Now, we can set up the actual agent. As shown in Listing 7.6, our
agent will rely on a `model`, a `checkpointer`, and one or more `tools` . In
this simple example, we’ll only provide one tool. The `tools` are
passed as a list. With the `TavilySearchResults` tool, the internet can
be searched, if needed.

```
#%% Create the agent
memory = MemorySaver()
model = ChatGroq( model_name ="llama-3.1-70b-versatile")
search = TavilySearchResults( max_results =2)
tools = [search]

```

**Listing 7.6** ReAct Agent: Agent Helpers (Source: 07_AgenticSystems\20_react.py)


Now, we’ll set up an instance of `create_react_agent`, based on the

`model`, the `tools`, and the `checkpointer`, as follows:

```
agent_executor = create_react_agent( model =model,
                      tools =tools,
                      checkpointer =memory)

```

Great! When we invoke the agent, we must pass a `configuration`
with a `thread_id` . This step allows us to manage multiple
conversations, as follows:

```
#%% Set up the configuration
config = {"configurable": {"thread_id": "abc123"}}

```

Ready to see the agent in action? As shown in Listing 7.7, invoke the

`agent_executor` and pass a user message.


```
#%% Invoke the agent
agent_executor.invoke(
{"messages": [("user", "My name is Bert Gollnick, I am a trainer and data
scientist. I live in Hamburg")]}, config
)

{'messages': [   HumanMessage(content='My name is Bert Gollnick, I am …',
AIMessage(content='', …),
ToolMessage(content=…),
…]}

```

**Listing 7.7** ReAct Agent: Agent Execution (Source: 07_AgenticSystems\20_react.py


The stack of messages is printed to the screen. Notice that an AI
message is returned after our message, and a tool was called for
fetching further information about the author.


The messages end up in `memory` . To extract these messages later,
you must route through the `memory` object by writing a new function,
shown in Listing 7.8.

```
#%% function for extracting the last message from the memory
def get_last_message(memory, config):
return memory.get_tuple(config=config).checkpoint['channel_values']['messages']
[-1].model_dump()['content']

```

**Listing 7.8** ReAct Agent: Function for Fetching Messages (Source:
07_AgenticSystems\20_react.py)


Now, we find out if our agent can remember things by asking it about
the author’s name and residence, as shown in Listing 7.9. While this
test sounds trivial, none of the systems we’ve set up to this point can
remember previous interactions.

```
#%% check whether the model can remember me
agent_executor.invoke(
{"messages": ("user", "What is my name and in which country do I live?")},
config
)
get_last_message(memory, config)

```

```
Your name is Bert Gollnick, and based on the information provided earlier, you live
in Hamburg, Germany.

```

**Listing 7.9** ReAct Agent: Invocation (Source: 07_AgenticSystems\20_react.py)


Amazing! Our agent now has the memory to recall information from
previous interactions. But now it gets really cool. Let’s ask the model
what it can find out about the author on the internet. What does the
agent need to do to fulfil this task? It needs to recall the author’s full
name and then reflect on whether any of the available tools are
helpful for solving this task. Luckily, our agent can use the web
search tool we provided. It will use the tool, analyze the results, and
hopefully show that can find information on the author, as shown in
Listing 7.10.

```
#%% check if it is possible to find me on the internet
agent_executor.invoke(
{"messages": ("user", "What can you find about me on the internet")},
config
)
get_last_message(memory, config)

'Based on the search results, it appears that you, Bert Gollnick, are a data
scientist with expertise in renewable energies, particularly wind energy. You have
worked for a leading wind turbine manufacturer and have applied data science to this
field. You also have a background in Aeronautics and Economics. Additionally, you
are a Udemy instructor and have courses available for enrollment on the platform.'

```

**Listing 7.10** ReAct Agent: Invocation (Source: 07_AgenticSystems\20_react.py)


We can also review all the information stored in the memory by
calling `memory.list()`, as shown in Listing 7.11.

```
# %% get the complete list of messages
list(memory.list( config =config))

[CheckpointTuple(config={'…'}),
CheckpointTuple(config={'…'}),
…
]

```

**Listing 7.11** ReAct Agent: Memory (Source: 07_AgenticSystems\20_react.py)


In this section, you learned about an important feature for
memorizing information throughout a conversation. This feature
(among others) is available in specific agentic frameworks. We’ll
start with a framework developed by the creators of LangChain:
LangGraph.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **7.4  Agentic Framework: LangGraph**

LangGraph ( _[https://langchain-ai.github.io/langgraph/](https://langchain-ai.github.io/langgraph/)_ ) is a dynamic
framework designed to simplify the creation, visualization, and
management of complex workflows in AI-powered applications. At its
core, LangGraph provides developers and researchers with tools to
streamline task orchestration, enabling them to build modular,
efficient, and explainable pipelines for language models and other
generative AI components.


LangGraph uses _directed acyclic graphs (DAGs)_ to structure and
execute workflows. Each node in a LangGraph workflow represents
a task, such as prompting a language model, running a computation,
or invoking an external API. Edges between nodes define
dependencies and data flow, ensuring that tasks are executed in the
correct order. With LangGraph, you maintain a high level of control
over the workflow, which makes the framework quite stable and
reliable.


This graph-based approach offers several advantages, such as the
following:


Modularity: Each node encapsulates a specific function or task,
making workflows easy to build, debug, and reuse.


Transparency: The visual representation of workflows clarifies how
data and tasks interconnect, providing insights into the overall
process.


Scalability: LangGraph supports branching and parallelism,
enabling the development of complex systems that scale
efficiently.


You can install LangGraph via pip or uv with the following
commands:

```
 pip install langgraph

 uv add langgraph

```

In our examples, we’ll start with the basics of setting up a simple
graph. Then, gradually, we’ll add more relevant features. At the end
of this chapter, we’ll develop a capstone project that integrates all
our new knowledge.


Let’s get started with the simplest graph possible.

### **7.4.1  Simple Graph: Assistant**


Figure 7.4 shows the graph we’ll develop first. In Chapter 3, you
learned how to work with LLM instances and how to invoke them.
With LangGraph, we set a DAG, which is basically a graph with a
clear start and end node. Each graph consists of nodes and edges.
Nodes represent the LLM we use but it could also be functions or
tools the LLM can call. The nodes are connected by edges. Edges
define how the nodes are connected.


**Figure 7.4** LangGraph: A Simple Graph


In this simplest graph, we have a start node that is connected to a
node called assistant. The assistant node then is linked to an end
node. This graph will work as an LLM assistant: It can be invoked
and can answer user questions. The corresponding code can be
found in
_07_AgenticSystems\langgraph\10_langgraph_simple_assistant.py_ .


Listing 7.12 shows all the required packages for this script. In this
case, we need some packages for loading environment variables
( `dotenv` ), `langchain_groq` for interacting with an LLM, and several
functionalities from `langgraph` .

```
#%% packages
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv( usecwd =True))
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from IPython.display import Image, display

```

**Listing 7.12** LangGraph: Simple Graph: Packages (Source:
07_AgenticSystems\langgraph\ 10_langgraph_simple_assistant.py)


Let’s discuss these new functionalities. We’ll create a `StateGraph` that
inherits from `TypedDict` . In the `StateGraph`, a state with messages will
be assigned. Each graph needs a `START` and `END` node.


A LangGraph graph requires a state because the state serves as the
shared context and data container that flows through the graph
during its execution. This state provides a single, consistent place to
store and update data as it is processed by different nodes in the
graph. Each node can read from and write to the state. This
approach enables coordinated execution without the need for
complex direct communication between nodes. The state is the only
way nodes exchange information.


Listing 7.13 shows how the state is set up.

```
# %% define the state
class State( TypedDict ):
messages: Annotated[list, add_messages]

```

**Listing 7.13** LangGraph: Simple Graph: State (Source: 07_AgenticSystems\langgraph\
10_langgraph_simple_assistant.py)


Our `State` inherits from `TypedDict` . A typed dictionary is much like a
normal dictionary except that the keys must have a type defined.


The only property of our state is `messages` . The `messages` have the
type of `list` . `Annotated` in this context allows the list to get the
context-specific metadata `add_messages` . Basically, the definition

`Annotated[list, add_messages]` means that the messages are of type

`list` with the small caveat that messages can be added to the list.


The next code chunk is straightforward. Listing 7.14 shows how the
LLM and the assistant are set up.

```
%% set up the assistant
llm = ChatGroq( model ="gemma2-9b-it")

def assistant( state : State):
return {"messages": [llm.invoke(state["messages"])]}

```

**Listing 7.14** LangGraph: Simple Graph: LLM and Assistant (Source:
07_AgenticSystems\ langgraph\10_langgraph_simple_assistant.py)


For the LLM, we’ll use Groq with a small and fast model. Nothing
new here. But the function `assistant` is defined in a way that it fits
perfectly into LangGraph, and we can easily use this function in the
context of the node setup. For this task, `assistant` consumes a `state`
and returns a dictionary with messages.


Listing 7.15 shows the most interesting part of the script, where we
define the inner structure of the graph.


```
#%% create the graph
graph_builder = StateGraph(State)
graph_builder.add_node("assistant", assistant)
graph_builder.add_edge(START, "assistant")
graph_builder.add_edge("assistant", END)

```

**Listing 7.15** LangGraph: Simple Graph: Graph Creation (Source: 07_AgenticSystems\
langgraph\10_langgraph_simple_assistant.py)


The `graph_builder` object starts out as an empty `StateGraph` . Then,
we add a single node with the name `“assistant”` and the action

`assistant` . The latter refers to the function we set up earlier. In this
way, we add our nodes: They are referred to via their name and
mapped to a function.


But at this point, the node is not connected to anything. In the graph,
a clear `START` and `END` is required. The connection of the dots is
simple. With the `add_edge` method, we can map out all the
connections between the nodes. This function requires a start key
and an end key. The edge points from the start key to the end key.
The edges we add here reflect this setup:

```
START → “assistant” → END

```

In later examples, we’ll create more complex setups, but now, we’re
starting out simply.


This `graph_builder` object is like a Python class. To use a Python
class, you must create a class instance, and the same rule applies
now. However, the syntax is slightly different, as shown in
Listing 7.16. To create an instance of the `graph_builder`, you must
call its `compile` method.

```
# %% compile the actual graph
graph = graph_builder.compile()

```

**Listing 7.16** LangGraph: Simple Graph: Graph Compilation (Source:
07_AgenticSystems\langgraph\10_langgraph_simple_assistant.py)


Finally, our graph is ready. Let’s make a visualization of it, as shown
in Figure 7.5. Listing 7.17 presents the commands to create a
visualization of the graph with its nodes and edges.

```
# %% display graph
display(Image(graph.get_graph().draw_mermaid_png()))

```

**Listing 7.17** LangGraph: Simple Graph: Graph Visualization (Source:
07_AgenticSystems\langgraph\10_langgraph_simple_assistant.py)


**Figure 7.5** LangGraph: Our Simple Graph


Now, we can work with the graph. Listing 7.18 shows how to invoke
the graph.

```
# %% invoke the graph
res = graph.invoke({"messages": [("user", "What do you know about LangGraph?")]})

```

**Listing 7.18** LangGraph: Simple Graph: Graph Invocation (Source: 07_AgenticSystems\
langgraph\10_langgraph_simple_assistant.py)


The result of this invocation is stored in the object res, as shown in
Listing 7.19. This object is a dictionary with key `"messages"` .

```
#%% display the result
res["messages"]

[HumanMessage(content='What do you know about LangGraph?', additional_kwargs={},
response_metadata={}, id='d241780d-203d-46be-bb78-682bb5d0fed1'),
AIMessage(content="LangGraph is a powerful open-source tool developed by the
HuggingFace team ...",

```

```
additional_kwargs={}, response_metadata={'token_usage': {'completion_tokens': 382,
'prompt_tokens': 17, 'total_tokens': 399, 'completion_time': 0.694545455,
'prompt_time': 8.357e-05, 'queue_time': 0.015116917, 'total_time': 0.694629025},
'model_name': 'gemma2-9b-it', 'system_fingerprint': 'fp_10c08bf97d',
'finish_reason': 'stop', 'logprobs': None}, id='run-186bf566-45ad-462f-b65e67005df3c95c-0',
usage_metadata={'input_tokens': 17, 'output_tokens': 382, 'total_tokens': 399})]

```

**Listing 7.19** LangGraph: Simple Graph: Invocation Result (Source: 07_AgenticSystems\
langgraph\10_langgraph_simple_assistant.py)


The invocation is successful, but at this point, you might ask what
the benefit is. Up to this point, the use of the LLM has been more
complicated than a direct LLM invocation. The value of LangGraph
gets clearer once we cover more complex examples and setups.


Let’s continue by adding autonomy to the graph. In our current
example, the graph has a completely deterministic workflow. In the
next example, we’ll add flexibility to the graph by allowing it to decide
how to proceed.

### **7.4.2  Router Graph**


So far, the process flow has been linear. The graph started, the state
was passed to a node, and the node passed its state to the next
node. Now, we can provide the agent with slightly more autonomy.


We’ll create a graph that lets a node decide how to proceed with the
code. Figure 7.6 shows the graph workflow for our new router graph.


**Figure 7.6** LangGraph: Router Graph


The router will decide how the process should proceed. Specifically,
we’ll create an agent to provide arguments for or against a topic. The
agent will randomly pick a side and create arguments for that side.
The code for this script can be found in
_07_AgenticSystems\langgraph\11_langgraph_router.py_ .


Listing 7.20 shows all required packages for our project.

```
#%% packages
from pprint import pprint
from typing_extensions import TypedDict
import random
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from IPython.display import Image, display
from rich.console import Console

```

```
from rich.markdown import Markdown
console = Console()

```

**Listing 7.20** LangGraph Router Project: Packages (Source:
07_AgenticSystems\langgraph\ 11_langgraph_router.py)


We don’t import any new packages, so we can go straight to more
interesting code chunks.


Listing 7.21 shows the applied LLM and the setup of the `State` class.
The graph state represents a snapshot of the context and data that
is associated with an agent at a specific point in its execution.

```
#%% LLM
llm = ChatGroq( model ="gemma2-9b-it")
# State with graph_state
class State( TypedDict ):
  graph_state: dict[str, str | dict[str, str | str]]

```

**Listing 7.21** LangGraph Router Project: Used LLM and State Class (Source:
07_AgenticSystems\langgraph\11_langgraph_router.py)


A graph consists of nodes and edges. We start with the definition of
the nodes, as shown in Listing 7.22.

```
# Nodes
def node_router( state : State):
# Retrieve the user-provided topic
topic = state["graph_state"].get("topic", "No topic provided")

# Update the graph_state with any additional information if needed
state["graph_state"]["processed_topic"] = topic # Example of updating
graph_state

print( f "User-provided topic: {topic}")
return {"graph_state": state["graph_state"]}

def node_pro( state : State):
topic = state["graph_state"]["topic"]
pro_args = llm.invoke( f "Generate arguments in favor of: {topic}. Answer in
bullet points. Max 5 words per bullet point.")
state["graph_state"]["result"] = {"side": "pro", "arguments": pro_args}
return {"graph_state": state["graph_state"]}

def node_contra( state : State):
topic = state["graph_state"]["topic"]
contra_args = llm.invoke( f "Generate arguments against: {topic}")

```

```
state["graph_state"]["result"] = {"side": "contra", "arguments": contra_args}
return {"graph_state": state["graph_state"]}

```

**Listing 7.22** LangGraph Router Project: Nodes Definition (Source:
07_AgenticSystems\langgraph\11_langgraph_router.py)


In this setup, we have three nodes: a router node, a pro-node, and a
contra-node. The router node retrieves the topic from the user and
updates the graph. The topic is stored in the key `"topic"` .


The pro- and contra-nodes invoke the LLM and create the answers
in favor and opposed to the topic. They create a key `“result”` in the

`graph_state` in which they pass their content.


We still need to connect the dots, in this case, the nodes with edges.
This step will be done by directly linking nodes or using functions for
conditional edges. Listing 7.23 shows the definition of a conditional
edge in which a random decision is made to select a side.

```
# Edges
def edge_pro_or_contra( state : State):
decision = random.choice(["node_pro", "node_contra"])
state["graph_state"]["decision"] = decision
print( f "Routing to: {decision}")
return decision

```

**Listing 7.23** LangGraph Router Project: Edges Definition (Source:
07_AgenticSystems\langgraph\11_langgraph_router.py)


Listing 7.24 shows how the complete graph is built and then
compiled.

```
# Create graph
builder = StateGraph(State)
builder.add_node("node_router", node_router)
builder.add_node("node_pro", node_pro)
builder.add_node("node_contra", node_contra)

builder.add_edge(START, "node_router")
builder.add_conditional_edges("node_router", edge_pro_or_contra)
builder.add_edge("node_pro", END)
builder.add_edge("node_contra", END)

```

```
graph = builder.compile()

```

**Listing 7.24** LangGraph Router Project: Graph Creation (Source:
07_AgenticSystems\langgraph\11_langgraph_router.py)


First, the nodes are added to the graph. The `add_node` function takes
two parameters: a node name and a corresponding node object.


The `START` node is connected to `node_router` . The decision for picking
a side is made with the help of `add_conditional_edges` . In this
context, the previously defined `node_router` is linked to the function
we created: `edge_pro_or_contra` . Finally, `node_pro` and `node_contra`
are linked to the `END` node.


At this point, the graph definition is ready, and we can call `compile` to
create a `graph` instance. This step is necessary because, in
LangGraph, the framework relies on defining and optimizing the flow
of reasoning and actions before execution.


To create a visual representation of the graph, as shown in
Figure 7.6, use the following code:

```
# %% display the graph
display(Image(graph.get_graph().draw_mermaid_png()))

```

Test the graph by invoking it. Listing 7.25 shows the invocation
process.

```
# %% Invokation
initial_state = {"graph_state": {"topic": "Should dogs wear clothes?"}}
result = graph.invoke(initial_state)
console.print(Markdown(result["graph_state"]['result']['arguments'].model_dump()
['content']))

```

**Listing 7.25** LangGraph Router Project: Graph Invocation (Source:
07_AgenticSystems\langgraph\11_langgraph_router.py)


We set up an `initial_state` by passing a `graph_state` in which the

`topic` value is defined. This `initial_state` is passed via the `invoke`


method. The result is stored in an object, and finally, we can use
functionality from the `rich` package ( `Console`, `Markdown` ) to create a
visually appealing console output, as shown in Listing 7.26.

```
Arguments Against Dogs Wearing Clothes:
1. It's unnecessary for most dogs: Dogs have natural fur coats that provide
insulation and protection from the elements. In most situations, clothing is not
necessary for their well-being.
2. It can be uncomfortable and restrictive: Clothes can restrict a dog's movement,
especially if they're
ill-fitting or made of non-breathable materials. This can lead to discomfort,
chafing, and even injury.
3. It can be a safety hazard: Loose clothing can get caught on objects, posing a
strangulation risk. Tags and attachments on clothing can also snag and cause
injury.
…
Ultimately, the decision of whether or not to dress a dog should be made on a caseby-case basis, considering the
individual dog's needs and comfort.

```

**Listing 7.26** LangGraph Router Project: Output (Source: 07_AgenticSystems\langgraph\
11_langgraph_router.py)


At this point, you’ve learned how to create a dynamic graph pipeline
in which the process flow is not purely sequential, but conditional
instead. This capability allows our agents and graphs to dynamically
adapt to conditions. But one important capability is still missing:
tools.


To equip agents with the capability to select tools independently, let’s
expand on our graph.

### **7.4.3  Graph with Tools**


Tools are the main ingredients that make agents autonomous.
LangGraph allows you to bind tools to your LLM, so that a node can


decide to use a tool when needed. Figure 7.7 shows the graph we’ll
develop now.


**Figure 7.7** LangGraph: Graph with Tool Use


In this scenario, we want to provide a useful functionality—the ability
to count letters. As it turns out, LLMs have enormous capabilities but
sometimes struggle with simple tasks like counting the letters in a
word. This problem is related to Moravec’s paradox, which states
that tasks requiring high-level reasoning are easier for computers to
perform, while sensorimotor tasks, which human consider easy, are
surprisingly difficult for machines to replicate. In short, what is simple
for a computer is difficult for a human, and vice versa.


Examples of high-level reasoning include solving complex
mathematical equations, performing calculations with large numbers,
playing chess or Go, and analyzing large datasets to detect patterns.
Such tasks are simple for a machine but difficult for humans. On the
other hand, walking, lifting a brick and then lifting an egg, and


identifying sarcasm are all tasks in which humans excel over
machines.


Let’s work on one such paradoxical behavior—counting letters in a
word. Figure 7.8 shows a model call asking an LLM to count the
number of Ls in the word LOLLAPALOOZA.


Although this task is simple enough for preschoolers, LLMs struggle
to come up with the right answer. Newer models seem to more
consistently get the right answer. But as you can see from the
screenshot, Mixtral-8x7B cannot figure out the right answer.


For this reason, we’ll write a tool our agent can use when such a
request occurs. The complete code can be found in
_07_AgenticSystems\langgraph\12_langgraph_tools.py_ .


**Figure 7.8** Inability of LLMs to Count Letters


Listing 7.27 lists all required packages and the LLM instance used in
this example.

```
#%% packages
import langgraph
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph.message import add_messages
from dotenv import load_dotenv, find_dotenv

```

```
load_dotenv(find_dotenv( usecwd =True))
#%% LLM
llm = ChatOpenAI( model ="gpt-4o-mini", temperature =0)

```

**Listing 7.27** LangGraph: Graph with Tools: Packages (Source:
07_AgenticSystems\langgraph\12_langgraph_tools.py)


At this point, you should already be familiar with these packages and
how to set up the model. So, we’ll move straight to the tool we want
to equip the LLM with.


Listing 7.28 shows the function `count_characters_in_word` . Provided
with a `word` and a specific `character`, this function returns the correct
number of the target letter found in the word.

```
# %% Tools
def count_characters_in_word( word : str, character : str) -> str:
"""Count the number of times a character appears in a word."""
cnt = word.count(character)
return f "The word {word} has {cnt} {character}s."

# %% TEST
count_characters_in_word( word ="LOLLAPALOOZA", character ="L")

```

**Listing 7.28** LangGraph: Graph with Tools: Tool Definition (Source:
07_AgenticSystems\langgraph\12_langgraph_tools.py)


Counting the number of letters is performed with the `count` method.
You also directly test the tool to verify that the right number is
returned, as follows:

```
'The word LOLLAPALOOZA has 4 Ls.'

```

Great! Now we can connect the tool (our function) to the LLM.
LangGraph requires tools to be integrated explicitly to ensure they
are available and properly configured. The `bind_tools` function
connects your tools to the LangGraph system. This step makes them
accessible to the graph’s nodes or agents, as follows:

```
# %% LLM with tools
llm_with_tools = llm.bind_tools([count_characters_in_word])

```

You can also test this functionality by calling the `invoke` method, as
shown in Listing 7.29.

```
# %%
llm_with_tools.invoke(["user", "Count the Ls in LOLLAPALOOZA?"])

AIMessage(content='', additional_kwargs={'tool_calls': [{'id':
'call_IRNSOIpEXeHY1iGqv3T6WThl', 'function': {'arguments':
'{"word":"LOLLAPALOOZA","character":"L"}', 'name': 'count_characters_in_word'},
'type': 'function'}], 'refusal': None}, response_metadata={'token_usage':
{'completion_tokens': 27, 'prompt_tokens': 73, 'total_tokens': 100,
'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0,
'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details':
{'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18',
'system_fingerprint': 'fp_d02d531b47', 'finish_reason': 'tool_calls', 'logprobs':
None}, id='run-4acd5baf-fb21-4dd5-8fa3-cca800a50b0e-0', tool_calls=[{'name':
'count_characters_in_word', 'args': {'word': 'LOLLAPALOOZA', 'character': 'L'},
'id': 'call_IRNSOIpEXeHY1iGqv3T6WThl', 'type': 'tool_call'}], usage_metadata=
{'input_tokens': 73, 'output_tokens': 27, 'total_tokens': 100,
'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details':
{'audio': 0, 'reasoning': 0}})

```

**Listing 7.29** LangGraph: Graph with Tools: Tool Invocation (Source:
07_AgenticSystems\langgraph\12_langgraph_tools.py)


The tool was successfully called. You can also verify success by
extracting the last message, as shown in Listing 7.30.

```
# %% Tool Call
tool_call = llm_with_tools.invoke("How many Ls are in LOLLAPALOOZA?")
#%% extract last message
tool_call.additional_kwargs["tool_calls"]

[{'id': 'call_1kmLBIuF6CIn8fs1MuSy1bhb',
'function': {'arguments': '{"word":"LOLLAPALOOZA","character":"L"}',
'name': 'count_characters_in_word'},
'type': 'function'}]

```

**Listing 7.30** LangGraph: Graph with Tools: Tool Calls (Source:
07_AgenticSystems\langgraph\12_langgraph_tools.py)


Let’s now create the graph and visualize it so that we get the screen
shown earlier in Figure 7.7 but using the code provided in
Listing 7.31. This step helps manage tool interaction in a broader
context.


```
#%% graph
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
from langgraph.prebuilt import ToolNode, tools_condition

class MessagesState( TypedDict ):
messages: list[AnyMessage]

# Node
def tool_calling_llm( state : MessagesState):
return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode([count_characters_in_word]))
builder.add_edge(START, "tool_calling_llm")
# builder.add_edge("tool_calling_llm", "tools")
builder.add_conditional_edges("tool_calling_llm",
# If the latest message (result) from assistant is a
tool call -> tools_condition routes to tools
# If the latest message (result) from assistant is a not a tool call ->
tools_condition routes to END
tools_condition)
builder.add_edge("tools", END)
graph = builder.compile()

```

**Listing 7.31** LangGraph: Graph with Tools: Building the Graph (Source:
07_AgenticSystems\langgraph\12_langgraph_tools.py)


This code defines a state graph using `StateGraph` class. The graph
structures the workflow by defining nodes and edges that represent
different states and transitions. In this case, the graph starts with a
node of our `tool_calling_llm` . That node processes the user
messages through the LLM. Depending on the LLM’s response, the
graph routes the flow conditionally.


If the LLM’s output includes a tool call, it transitions to a `ToolNode`,
which executes the required tool. The result is then routed back to
the workflow, either for further processing or to conclude the
interaction.


This separation of concerns—first binding tools to the LLM and then
managing their invocation through the state graph—is key to the
design.


Binding tools to an LLM allows the model to make tool calls
dynamically based on user input, while the state graph ensures that
tool calls are integrated into a controlled, sequential process. This
approach is particularly useful in complex workflows where tool
usage must be orchestrated alongside other operations, such as
message routing or additional computations.


By combining the LLM’s reasoning capabilities with a defined state
graph, the code creates a flexible yet robust framework for handling
user interactions and tool integrations.


We can visualize the graph with the following command:

```
# View
display(Image(graph.get_graph().draw_mermaid_png()))

```

Finally, as shown in Listing 7.32, we can test the graph in action by
creating some messages and invoking the graph.

```
# %% use messages as state
# messages = [HumanMessage(content="Hey, how are you?")]
messages = [HumanMessage( content ="Please count the Ls in LOLLAPALOOZA.")]
messages = graph.invoke({"messages": messages})
for m in messages["messages"]:
print(m.pretty_print())

================================= Tool Message
=================================
Name: count_characters_in_word

The word LOLLAPALOOZA has 4 Ls.
None

```

**Listing 7.32** LangGraph: Graph with Tools: Graph Invocation (Source:
07_AgenticSystems\langgraph\12_langgraph_tools.py)


Our agent has successfully passed the task of counting the Ls in
LOLLAPALOOZA. The LLM deduced that the tool is perfect for the
job and used it. The tool result was passed back to the LLM, that
then created a final answer.


Thus concludes our introduction to LangGraph. In the next section,
we’ll explore another popular framework: AG2.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **7.5  Agentic Framework: AG2**

AG2 is an agentic framework that many might know it by its legacy
name _autogen_ . With AG2, you can build AI agents easily. You can
set up multiple agents in minutes and let them interact with each
other. The installation is easy; you can install this framework via pip:

```
pip install ag2

```

For some features, you should run the agentic framework in a
Docker container. AG2 can be run inside a Docker container, but you
don’t have to.


**Running inside Docker**


AG2 can create software code and run it directly. This capability is
powerful but also possibly dangerous if you run the created code
directly under your user scope. Thus, if you intend to use the
framework for such a task, you should run it inside a Docker
container.


Docker is an open-source platform that enables developers to
build, ship, and run applications in lightweight, portable containers.
This approach ensures consistency across different environments,
and furthermore, the code execution scope is limited to the
container.


The documentation for AG2 ( _[https://github.com/ag2ai/ag2](https://github.com/ag2ai/ag2)_ )
provides further details on how to set it up on your computer.


Within the scope of our examples, we won’t use Docker and leave
it up to you to explore this option.


In this section, we’ll first observe two agents having a conversation
autonomously. In many cases, you don’t want to lose control over
your agents. To maintain control, you can use a technique called
_human in the loop (HITL)_ to enable intervention. Finally, we’ll equip
an agent with additional tools to solve specific problems. Without
further ado, let’s dive in.

### **7.5.1  Two Agent Conversations**


In this example, we’ll set up two agents and observe them having a
lively discussion about the conspiracy theory that the earth is flat.
Our two agents are called Jack and Alice. While Jack is a firm
believer that the earth is flat, Alice takes the scientific view and tries
to convince him otherwise.


To make this scenario as realistic as possible, that is, as close as
possible to a typical internet discussion, with each round, Jack will
get increasingly angry and frustrated over Alice’s “ignorance.”


You can find the script in
_07_AgenticSystems\ag2\20_ag2_conversation.py_ . As usual, we start
by importing the required packages and classes, as shown in
Listing 7.33. The agent type is called `ConversableAgent` . A

`ConversableAgent` has a property to send a reply to the sender after
receiving a message. This behavior is only avoided if the message is
a termination message. In this example, we’ll work with OpenAI and
use the API key stored in the _.env_ file. Make sure you place the file in
your working folder. The environment variables are loaded with the
help of `load_dotenv` .

```
#%% packages
import os
from autogen import ConversableAgent

```

```
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv( usecwd =True))

```

**Listing 7.33** AG2: Agent Conversation: Packages (Source: 07_AgenticSystems\ag2\
20_ag2_conversation.py)


Every agent is built upon an LLM that needs configuration. With
AG2, you must pass the LLM configuration in the parameter

`llm_config` during the instantiation of the agents, as shown in
Listing 7.34.

```
#%% LLM config
llm_config = {"config_list": [
{"model": "gpt-4o-mini",
"temperature": 0.9,
"api_key": os.environ.get("OPENAI_API_KEY")}]}

```

**Listing 7.34** AG2: Agent Conversation: LLM Configuration (Source:
07_AgenticSystems\ag2\20_ag2_conversation.py)


The main parameters in this case are the `model` that is used, the

`temperature` of the model, and the `api_key` . Now, let’s define our first
agent, Jack, the flat earther, as shown in Listing 7.35.

```
jack_flat_earther = ConversableAgent(
  name ="jack",
  system_message ="""
You believe that the earth is flat.
You try to convince others of this.
With every answer, you are more frustrated and angry that they don't see it.
""",
  llm_config =llm_config,
  human_input_mode ="NEVER", # Never ask for human input.
)

```

**Listing 7.35** AG2: Agent Conversation: Agent Jack Setup (Source:
07_AgenticSystems\ag2\20_ag2_conversation.py)


Now, we can create an instance of a `ConversableAgent` . In this
process, we need to provide a name and, importantly, describe the
agent’s worldview and behavior in the `system_message` . In the system
message, for realism, we want this agent to get more heated as the


debate proceeds. The agent is coupled to an LLM by passing the
configuration to the parameter `llm_config` . Finally, the agent should
act completely independently, and thus, we won’t interfere by setting
the `human_input_mode` to `NEVER` .


OK, now that our first agent is defined, it needs a conversation
partner. Let’s define a scientist named Alice next, as shown in
Listing 7.36.

```
#%% set up the agent: Alice, the scientist
alice_scientist = ConversableAgent(
  name ="alice",
  system_message ="""
You are a scientist who believes that the earth is round.
Answer very polite, short and concise.
""",
  llm_config =llm_config,
  human_input_mode ="NEVER",
)

```

**Listing 7.36** AG2: Agent Conversation: Agent Alice Setup (Source:
07_AgenticSystems\ag2\20_ag2_conversation.py)


We’ll define the same parameters but let her have a different
worldview. She will stay polite and keep her answers short and
concise.


Great, let’s start the debate. Starting the conversation is easily done.
As in a real conversation, one partner needs to take the initiative and
approach the other with an opening statement. In our case, Jack
initiates our conversation, and Alice is the recipient of his statement,
as shown in Listing 7.37.

```
# %% start the conversation
result = jack_flat_earther.initiate_chat(
  recipient =alice_scientist,
  message ="Hello, how can you not see that the earth is flat?",
  max_turns =3)

```

**Listing 7.37** AG2: Agent Conversation: Run Conversation (Source:
07_AgenticSystems\ag2\20_ag2_conversation.py)


We’ll store the discussion in the object `result` . Every agent has the
ability (method) to `initiate_chat` . In that method, the agent must
address a `recipient` .


Important: we need to ensure that the conversation ends after a finite
number of rounds. It is possible to reach this in different ways—at
the level of the agents (as we’ll discover in the next example, in
Section 7.5.2), or as here, we can pass it as the parameter

`max_turns` in the `initiate_chat` method.


While the debate is ongoing, we can observe the agents arguing in
real time in the interactive window, as shown in Listing 7.38.

```
jack (to alice): Hello, how can you not see that the earth is flat?
-------------------------------------------------------------------------------alice (to jack): Hello, Jack! I appreciate your perspective. However, scientific
evidence, such as satellite images and the way gravity works, supports the
understanding that the Earth is round. Thank you for sharing your thoughts!
-------------------------------------------------------------------------------jack (to alice): Alice, it's infuriating that you rely on so-called "scientific
evidence" without questioning it! Those satellite images? They can be easily
manipulated, and gravity is just a theory! Why can't you see that the horizon always
appears flat when you look out at the ocean or across vast landscapes? We cannot
simply accept what we've been told without questioning it! The truth is right in
front of you!
-------------------------------------------------------------------------------alice (to jack): Thank you for sharing your thoughts, Jack. I understand your
concerns about questioning established information. The appearance of a flat horizon
is due to the vastness of the Earth's surface, but scientific methods and
observations consistently support a round Earth. Engaging in open discussions is
important, and I appreciate your passion for seeking the truth.
-------------------------------------------------------------------------------jack (to alice): Ugh, you just don't get it! The horizon looks flat to us, and
common sense should tell you something is off! You keep mentioning "scientific
methods," but who decided that they are the definitive truth? Scientists can be
biased too! There are countless testimonies from people who have experienced this
flatness firsthand, yet you brush them off! Why are you so blindly trusting the
mainstream narrative? It’s maddening! Just open your eyes and think for yourself!
-------------------------------------------------------------------------------alice (to jack): I appreciate your passionate perspective, Jack. It's true that
personal experiences are important, and questioning narratives is a part of critical
thinking. However, scientific methods are designed to minimize bias and are based on
rigorous testing and evidence. The consensus on a round Earth comes from extensive
research and observations over time. I value our discussion and your commitment to

```

```
exploring different viewpoints!
-------------------------------------------------------------------------------
```

**Listing 7.38** AG2: Agent Conversation: Conversation Output (Source:
07_AgenticSystems\ag2\20_ag2_conversation.py)


The result is a realistic exchange. Can you see how Jack is getting
increasingly angry over time? We’ll leave it to you to see Jack
escalating even more by increasing the number of `max_turns` .


But for now, let’s leave Alice and Jack alone. In many cases, you
don’t want to hand over complete control to your agents. You want to
stay “in the loop.”

### **7.5.2  Human in the Loop**


Human in the loop (HITL) is a concept in machine learning (ML),
artificial intelligence, or automation where human input, feedback, or
oversight is incorporated into the system’s operation. This approach
ensures that human judgment guides and validates the system’s
actions. This human touch is especially important for tasks that
require nuanced decision-making or ethical considerations. shows
how the human in the loop is implemented in AG2’s

`ConversableAgent` .


**Figure 7.9** AG2 Human in the Loop (Source: Adapted from
_[https://ag2ai.github.io/ag2/docs/tutorial/human-in-the-loop](https://ag2ai.github.io/ag2/docs/tutorial/human-in-the-loop)_ )


When we interact with a `ConversableAgent`, we send a message. This
message is received by a human in the loop module. This module
decides how to proceed, choosing from one of three options:


It can forward the message directly to an auto-reply component in
case no human interaction is required.


It can directly ask the human for a reply.


It can request human input when a termination condition is met.


In the scope of agentic frameworks, we can take over an agent and
control its actions. In this example, we’ll teach a system to play
hangman. Hangman is a classic word-guessing game where players
try to uncover a hidden word by suggesting letters. With each wrong
guess, a person gets closer to being hanged.


In our agentic implementation, we’ll simplify the game and dispense
with the drawing. Instead, we’ll count the number of failed attempts.
After 7 failed attempts, the player loses, and the host wins. The
autonomous agent will be the host, and we are the players who
guess the word. Figure 7.10 shows a sample game of hangman.


**Figure 7.10** Hangman Gameplay Example


The hangman host knows the secret word, while the player tries to
guess it. Each round starts with the player guessing if a letter is part
of the word. Strategically, a player should choose letters with a high


probability of being parts of a word at the beginning. In the English
dictionary, vowels like E or A are quite common. The hangman game
host checks whether the letter is part of the word and returns the
word with blanks filled in with the correct letters, at the correct
position.


The next round starts with the player choosing the next letter. The
host checks again whether this letter is part of the word and returns
the word with the filled blanks.


The game ends either with the host winning after 7 failed attempts by
the player, or the player wins by filling in all the blanks and thus
revealing the secret word.


Now, the rules of the game are clear. Let’s start setting up our
agentic system. As shown in Listing 7.39, we’ll load the necessary
packages first.

```
#%% packages
from autogen import ConversableAgent
from dotenv import load_dotenv, find_dotenv
import nltk
from nltk.corpus import words
import os
import random
load_dotenv(find_dotenv( usecwd =True))

```

**Listing 7.39** Ag2 HITL: Packages (Source:
07_AgenticSystems\ag2\30_ag2_human_in_the_loop.py)


The new functionality in this example is the package `nltk` . Standing
for “Natural Language Toolkit,” `nltk` is a Python package for working
with human language data. This package provides tools for tasks like
tokenization, tagging, parsing, or stemming. We don’t need any of
these right now, only the functionality to download a complete corpus
of words. For this reason, we’ll load `words` from `nltk.corpus` .


Later, we’ll connect our agents to LLMs. For now, as shown in
Listing 7.40, we’ll define the LLM configuration.

```
# %% llm config_list
config_list = {"config_list": [
{"model": "gpt-4o",
"temperature": 0.2,
"api_key": os.environ.get("OPENAI_API_KEY")}]}

```

**Listing 7.40** Ag2 HITL: LLM Configuration (Source:
07_AgenticSystems\ag2\30_ag2_human_in_the_loop.py)


In this configuration, we’ve selected a model, set a model
temperature, and provided a valid API key.


Next, as shown in Listing 7.41, we can download a complete word
list with `nltk` and select a secret word.

```
# %% download the word list, and select a random word as secret word
nltk.download('words')
word_list = [word for word in words.words() if len(word) <= 5]
secret_word = random.choice(word_list)
number_of_characters = len(secret_word)

```

**Listing 7.41** Ag2 HITL: Define a Secret Word (Source:
07_AgenticSystems\ag2\30_ag2_human_in_the_loop.py)


After downloading the words, we want to filter the `word_list` to only
contain words with a maximum of 5 characters. Since we want a fair
game, we shouldn’t know the secret word, so we’ll randomly select
from the word list. Since LLMs have some issues counting
characters within words, we’ll help the system by calculating the
number of characters in advance.


Our preparation work is complete, and we can start defining our
agents. Let’s start with the game host, as shown in Listing 7.42.

```
#%% hangman host agent
hangman_host = ConversableAgent(
  name ="hangman_host",
  system_message = f """
You decided to use the secret word: {secret_word}.

```

```
It has {number_of_characters} letters.
The player selects letters to narrow down the word.
You start out with as many blanks as there are letters in the word.
Return the word with the blanks filled in with the correct letters, at the
correct position.
Double check that the letters are at the correct position.
If the player guesses a letter that is not in the word, you increment the number
of fails by 1.
If the number of fails reaches 7, the player loses.
Return the word with the blanks filled in with the correct letters.
Return the number of fails as x / 7.
Say 'You lose!' if the number of fails reaches 7, and reveal the secret word.
Say 'You win!' if you have found the secret word.
""",
  llm_config =config_list,
  human_input_mode ="NEVER",
  is_termination_msg = lambda msg : f "{secret_word}" in msg['content']
)

```

**Listing 7.42** Ag2 HITL: Game Host (Source:
07_AgenticSystems\ag2\30_ag2_human_in_the_loop.py)


Our host is defined as a `ConversableAgent` . Its core logic is defined in
the `system_message` . At this point, we must be quite specific and tell
the agent the complete game rules as well as how it should behave.
The agent is coupled to an LLM, as defined in the `llm_config` we
discussed earlier. This agent should act fully autonomously, and we
can ensure this behavior in the definition by setting `human_input_mode`
to `NEVER` .


OK, the game host is ready to play. Now, we need define the player.
Listing 7.43 shows the `hangman_player` setup.

```
#%% hangman player agent
hangman_player = ConversableAgent(
  name ="agent_guessing",
  system_message ="""You are guessing the secret word.
You select letters to narrow down the word. Only provide the letters as 'Guess:
...'.
""",
  llm_config =config_list,

```

```
  human_input_mode ="ALWAYS"
)

```

**Listing 7.43** Ag2 HITL: Game Player (Source:
07_AgenticSystems\ag2\30_ag2_human_in_the_loop.py)


This player agent is the agent that we’ll control. For that reason, we’ll
set the `human_input_mode` to `ALWAYS` . We don’t need a detailed

`system_message` since the agent won’t have any autonomy for now.
However, defining a system message is still advisable because it
increases the readability of the code for you in the future or other
developers. Defining a system message also can help if you want to
quickly switch the autonomy level and let the agent do the guessing.


Now, we have everything up and running and can test the system.
Listing 7.44 shows how the conversation is started.

```
#%% initiate the conversation
result = hangman_host.initiate_chat(
  recipient =hangman_player,
  message ="I have a secret word. Start guessing.")

```

**Listing 7.44** Ag2 HITL: Initiate the Conversation (Source:
07_AgenticSystems\ag2\30_ag2_human_in_the_loop.py)


We have two options: Either the game host informs the player that
he has a secret word and the game can start. Alternatively, the
player could directly approach the host and start guessing.


We start with the game host informing the player that the game can
start. For this scenario, the `hangman_host` starts the conversation by
calling the method `initiate_chat` . In that method, the `recipient`
must be addressed with a starting `message` .


During the conversation, you’re requested to enter letters. The game
host incorporates your answer, and it is your turn again. Listing 7.45
shows the game in action.


```
hangman_host (to agent_guessing):
I have a secret word. Start guessing.
-------------------------------------------------------------------------------agent_guessing (to hangman_host): E
-------------------------------------------------------------------------------hangman_host (to agent_guessing): Great! The letter 'E' is in the word. _ _ _ _ E
Fails: 0 / 7 Keep guessing!
-------------------------------------------------------------------------------agent_guessing (to hangman_host): S
-------------------------------------------------------------------------------hangman_host (to agent_guessing): Sorry, the letter 'S' is not in the word. _ _ _ _
E Fails: 1 / 7 Try another letter!
-------------------------------------------------------------------------------agent_guessing (to hangman_host): A
-------------------------------------------------------------------------------hangman_host (to agent_guessing): Sorry, the letter 'A' is not in the word. _ _ _ _
E Fails: 2 / 7 Keep trying!
-------------------------------------------------------------------------------agent_guessing (to hangman_host): I
-------------------------------------------------------------------------------hangman_host (to agent_guessing): Sorry, the letter 'I' is not in the word. _ _ _ _
E Fails: 3 / 7 Guess again!
-------------------------------------------------------------------------------agent_guessing (to hangman_host): U
-------------------------------------------------------------------------------hangman_host (to agent_guessing): Sorry, the letter 'U' is not in the word. _ _ _ _
E Fails: 4 / 7 Keep guessing!
-------------------------------------------------------------------------------agent_guessing (to hangman_host): N
-------------------------------------------------------------------------------hangman_host (to agent_guessing): Good job! The letter 'N' is in the word. _ _ _ N E
Fails: 4 / 7 Guess another letter!
-------------------------------------------------------------------------------agent_guessing (to hangman_host): F
-------------------------------------------------------------------------------hangman_host (to agent_guessing): Sorry, the letter 'F' is not in the word. _ _ _ N
E Fails: 5 / 7 Try another letter!
-------------------------------------------------------------------------------agent_guessing (to hangman_host): C
-------------------------------------------------------------------------------hangman_host (to agent_guessing): Nice! The letter 'K' is in the word. C _ _ N E
Fails: 5 / 7 Keep going!
-------------------------------------------------------------------------------agent_guessing (to hangman_host): O
-------------------------------------------------------------------------------hangman_host (to agent_guessing): Great! The letter 'O' is in the word. C _ O N E
Fails: 5 / 7 Almost there, guess again!
-------------------------------------------------------------------------------agent_guessing (to hangman_host): R
-------------------------------------------------------------------------------hangman_host (to agent_guessing): Congratulations! The letter 'R' is in the word. C

```

```
R O N E You win!  ------------------------------------------------------------------------------
```

**Listing 7.45** Ag2 HITL: Conversation Output (Source:
07_AgenticSystems\ag2\30_ag2_human_in_the_loop.py)


Our game worked well. You can now implement any kind of wordbased game.


You might even implement card games like blackjack. In such an
agentic system, you can let the agents autonomously run multiple
rounds and store the game plays to train an algorithm to come up
with a clever strategy to win the game.


Up to this point, you’ve learned how to set up agents, but they are
still limited to their parametric knowledge. This limitation will
disappear in the next example in which we’ll teach our agents to use
tools.

### **7.5.3  Agents Using Tools**


One of the most powerful capabilities to apply to an agent with is the
ability to use tools. The agent will then be equipped with the tool and
decide to use it when necessary. In our example, we’ll create a tool
to get the current date. This feature can be helpful, for example, to
determine the relevance of information found in a web search. To
equip an agent with the capability to use a tool, follow these steps:


1. Define a tool.


2. Register for an LLM.


3. Register for execution.


4. Use the tool.


The steps for registering a tool for an LLM and for execution require
some more explanations:


**register_for_llm**
The purpose of `register_for_llm` is to expose a tool or a function
to the LLM. This method allows the LLM to reason about the tool,
decide when to call it, and incorporate the tool’s functionality into
its broader reasoning process.


This function essentially “describes” the tool to the LLM, including
the tool’s name, its input and output formats, and a short
description of its functionality. Without `register_for_llm`, the LLM
would not know about the tool and therefore wouldn’t attempt to
use it.


**register_for_execution**
The purpose of this function is to handle the actual execution of
the tool when the LLM decides to call it. It connects the logical
request generated by the LLM to the actual process that
implements the tool’s logic.


Once the LLM determines that a specific tool should be invoked,

`register_for_execution` ensures that the Python code correctly
processes the request. Without `register_for_execution`, even if
the LLM decided to use a tool, no backend logic would exist to
execute the tool’s functionality.


The following code can be found in
_07_AgenticSystems\ag2\40_ag2_tools.py_ . Listing 7.46 shows the
packages we used and the configuration of the LLM.

```
#%% packages
from typing import Annotated, Literal
import datetime
from autogen import ConversableAgent, UserProxyAgent
from dotenv import load_dotenv, find_dotenv
import os

```

```
# load the environment variables
load_dotenv(find_dotenv( usecwd =True))
# %% llm config_list
config_list = {"config_list": [
{"model": "gpt-4o-mini",
"temperature": 0.9,
"api_key": os.environ.get("OPENAI_API_KEY")}]}

```

**Listing 7.46** AG2 Tool Use: Required Packages (Source:
07_AgenticSystems\ag2\40_ag2_tools.py)


Next, we can define a function that the agent can use later.
Listing 7.47 shows the function definition for `get_current_date` .

```
#%% tool function
def get_current_date() -> str:
return datetime.datetime.now().strftime("%Y-%m-%d")

```

**Listing 7.47** AG2 Tool Use: Function for Getting Date (Source: 07_AgenticSystems\ag2\
40_ag2_tools.py)


The function can be called without further parameters and returns
the current date in the format `%Y-%m-%d`, for example, “2025-01-24.”


Listing 7.48 shows the agent setup. First, we set up an autonomous
agent and then a user proxy that is capable of interacting with the
autonomous agent.

```
# %% create an agent with a tool
my_assistant = ConversableAgent(
  name ="my_assistant",
  system_message ="""
You are a helpful AI assistant.
You can get the current date.
Return 'TERMINATE' when the task is done.
""",
  llm_config =config_list,
# Add human_input_mode to handle tool responses
  human_input_mode ="NEVER"
)

```

**Listing 7.48** AG2 Tool Use: Agent (Source: 07_AgenticSystems\ag2\40_ag2_tools.py)


Defined as `ConversableAgent`, this agent acts as a helpful AI assistant
that can get the current date and returns `TASK COMPLETED` when the


task is done.


Listing 7.49 shows how the function (our tool) is registered at the
agent level.

```
my_assistant.register_for_llm(
  name ="get_current_date",
  description ="Returns the current date in the format YYYY-MM-DD."
)(get_current_date)

```

**Listing 7.49** AG2 Tool Use: Register for LLM (Source:
07_AgenticSystems\ag2\40_ag2_tools.py)


In the next step, we can set up an agent that acts as a user proxy, as
shown in Listing 7.50. This agent handles conversations with the
assistant agent.

```
user_proxy = ConversableAgent(
  name ="user_proxy",
  llm_config =False,
  is_termination_msg = lambda msg : msg.get("content") is not None and "TASK
COMPLETED" in msg["content"],
  human_input_mode ="NEVER"
)

```

**Listing 7.50** AG2 Tool Use: User Proxy (Source:
07_AgenticSystems\ag2\40_ag2_tools.py)


Now, we need to define the termination condition for ending the
conversation in the parameter `is_termination_msg` . The message
content is checked, and the phrase `TASK COMPLETED` searched. When
this phrase is part of the message content, the conversation
terminates.


Next, as shown in Listing 7.51, the tool is registered for execution.

```
#%% register the tool function at execution level
user_proxy.register_for_execution( name ="get_current_date")(get_current_date)

```

**Listing 7.51** AG2 Tool Use: Register for Execution (Source:
07_AgenticSystems\ag2\40_ag2_tools.py)


Finally, in Listing 7.52, the tool is used.

```
# %% using the tool through user proxy
result = user_proxy.initiate_chat(
my_assistant,
  message ="What is the current date?"
)

```

**Listing 7.52** AG2 Tool Use: Using the Tool (Source:
07_AgenticSystems\ag2\40_ag2_tools.py)


The user proxy approaches the assistant and asks about the current
date, as shown in Listing 7.53.

```
user_proxy (to my_assistant): What is the current date?
-------------------------------------------------------------------------------my_assistant (to user_proxy): ***** Suggested tool call
(call_Ju0ctF6wf0DI6LCbGkBGaTnv): get_current_date *****
Arguments:
{}
******************************************************************************** ------------------------------------------------------------------------------>>>>>>>> EXECUTING FUNCTION get_current_date...
user_proxy (to my_assistant): *****
Response from calling tool (call_Ju0ctF6wf0DI6LCbGkBGaTnv) *****
2024-12-07
**********************************************************************
-------------------------------------------------------------------------------my_assistant (to user_proxy): The current date is 2024-12-07.
-------------------------------------------------------------------------------user_proxy (to my_assistant):
-------------------------------------------------------------------------------my_assistant (to user_proxy): TASK COMPLETED
-------------------------------------------------------------------------------
```

**Listing 7.53** AG2 Tool Use: Output (Source: 07_AgenticSystems\ag2\40_ag2_tools.py)


The `user_proxy` reaches out to the assistant, asking for the current
date. The assistant figures out it needs to use the tool. The function
is executed, and a response is created. The assistant uses the tool’s
response to formulate a good answer. Then, the assistant returns
**TASK COMPLETED**, which triggers the `user_proxy` to end the
conversation.


Thus concludes our deep dive into AG2. In the next section, we’ll
explore another framework, one that is quite popular due to its
simplicity: CrewAI.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **7.6  Agentic Framework: CrewAI**

We hope you’ve seen how a single agent is already a powerful tool.
Now, let’s find out how much more powerful a team of agents can
be. For this scenario, we’ll work with the framework CrewAI. A
Python framework for operating autonomous AI agents, CrewAI is
simple to use.


We’ll start in Section 7.6.1 with an introduction laying out how the
CrewAI framework is structured. After we cover these basics, we’ll
implement our first crew in Section 7.6.2. In Section 7.6.3, you’ll
apply your knowledge practically.

### **7.6.1  Introduction**


Figure 7.11 shows the different components that are used in CrewAI.


**Figure 7.11** CrewAI Components


These components are as follows:


**Agents**
Agents are the autonomous workers within the CrewAI framework,


each possessing specific roles, expertise, and capabilities. Think
of them as specialized professionals in a team, where each agent
brings unique skills and knowledge to tackle different aspects of a
complex task. Agents can be configured with distinct personalities,
backstories, and goals, allowing them to approach problems from
different perspectives and collaborate effectively with other agents
in the crew.


**Tools**
Tools are the functional extensions that agents use to interact with
the external world and perform specific operations. They serve as
the hands and instruments of the agents, enabling them to
execute concrete actions like searching the web, analyzing data,
or manipulating files. Tools can be custom-built functions, API
integrations, or existing libraries that expand an agent’s
capabilities beyond mere conversation and reasoning.


**Tasks**
Tasks represent the individual units of work that must be
accomplished within a project. Each task is a well-defined
objective with clear inputs, expected outputs, and success criteria.
Tasks can be assigned to specific agents based on their expertise,
and they can be sequential, parallel, or interdependent. The
granularity of tasks can vary from simple operations to complex
procedures requiring multiple steps and collaboration between
agents.


**Process**
The process in CrewAI orchestrates the flow of work between
agents and tasks, managing the execution order and handling
dependencies. It’s the choreographer that ensures smooth
collaboration, determining when and how agents should interact,
share information, and hand off work to one another. The process


can be configured to support different workflow patterns, from
linear sequences to complex networks of parallel and iterative
tasks, adapting to the specific needs of each project.

### **7.6.2  First Crew: News Analysis Crew**


In this section we’ll develop our first crew. A good practice is to start
at a high level and add details later. So, let’s start with the mission
definition. Then, we’ll work on the components, as discussed in
Section 7.6.1. At this point, we’ll derive which agents will be needed
to fulfill the mission. We’ll also need to define how the agents interact
with each other and determine which tools our agents need for the
task.


Speaking of tasks, we also need to detail which tasks the different
agents should work on. Once these questions are answered, we can
dive into actual coding. Consider that we’re focused on just an
example implementation; multiple valid approaches can fulfill the
overall mission.


**Concepts**


Let’s now walk through the components of our crew development.


_**Mission**_


What is the mission of our first crew? Our news analysis crew should
check trending topics in each field. Different angles should be
illuminated. As output, we want to get a report, ideally styled in a nice
format like Markdown.


_**Agents**_


Which agents will we need to solve this task?


**A researcher**
The researcher gathers information from the internet.


**An analyst**
The analyst provides context, examines multiple perspectives, and
structures the information.


**A writer**
The writer produces a clear and balanced summary of the findings
in the form of a report.


Now, we must define the tasks that the crew is supposed to perform.


_**Tasks**_


We have multiple discrete tasks, and we need to think about which
agent should work on which task:


**Information gathering**
Source articles need to be collected. Conflicting information needs
to be flagged. Key stakeholders should be identified. This task
should be handled by the researcher.


**Fact checking**
Across multiple sources, facts should be cross-referenced.
Unverified claims need to be identified. This task should also be
handled by the researcher.


**Context analysis**
Potential causes and contributing factors should be analyzed.
Furthermore, economic, social, or political implications should be
studied. This is a task for the analyst.


**Final report assembly**
All findings of the agents need to be integrated into one final
report. Balanced pros and cons need to be written. This sounds
like a perfect task for the writer.


_**Collaboration**_


How do they collaborate? In our simple example, the agents work in
sequence. The researcher starts, passes its results to the analyst,
and passes its results to the writer.


A helpful step is to visualize the complete crew setup. Figure 7.12
shows the AI crew with its components: the participating experts
(agents), their tasks, the tools they use, and how they interact with
each other.


On the conceptual side, we’re done, and it’s time to start coding.


**Figure 7.12** News Analysis Crew Setup


**CrewAI Starter Project**


To begin, change the directory and move into the agentic system
subfolder. In this subfolder, in the terminal, run the following


command:

```
crewai create crew news-analysis

```

This command will create the complete setup with configuration files
inside a subfolder called _news-analysis_ . During the creation process,
some questions need to be answered, starting with those shown in
Listing 7.54.

```
Select a provider to set up:
1. openai
2. anthropic
3. gemini
4. groq
…

```

**Listing 7.54** CrewAI Setup: Provider Selection


We want to work with Groq and select that option by pressing (4).
Next, we need to choose our Groq model, as shown in Listing 7.55.

```
Select a model to use for Groq:
1. groq/llama-3.1-8b-instant
2. groq/llama-3.1-70b-versatile
3. groq/llama-3.1-405b-reasoning
4. groq/gemma2-9b-it
5. groq/gemma-7b-it
q. Quit

```

**Listing 7.55** CrewAI Setup: Model Selection


Now, select `groq/llama-3.1-70b-versatile` by pressing (2). Feel free
to select a different model; in any case, the selection can be
changed later. Next, you’ll be prompted to enter an API key.

```
Enter your GROQ API key (press Enter to skip):

```

We’ll define the API key at some later point, so we can skip this step
by pressing (Enter). We should see the following message: **Crew**
**news-analysis created successfully!**


Great! Our project files have all been created, which we can check
by running the command shown in Listing 7.56.

```
Tree /F

└───news_analysis
│  .env
│  .gitignore
│  pyproject.toml
│  README.md
├───src
│  └───news_analysis
│    │  crew.py
│    │  main.py
│    │  __init__.py
│    ├───config
│    │    agents.yaml
│    │    tasks.yaml
│    └───tools
│        custom_tool.py
│        __init__.py

```

**Listing 7.56** CrewAI Setup: Folder Structure


In the project folder _news_analysis_, you’ll find some subfolders,
which we’ll touch upon later. Directly on the level of the folder, you
find the following files:


_.env_ : This file holds the environment variables we need to use in
the project.


_.gitignore_ : In case you want to store the project in a GitHub
repository, this file contains some sample definitions of files to
disregard.


_pyproject.toml_ : This file is used to manage the environment with
all used packages.


_README.md_ : In this file, you get some information describing
how to quickly get started.


Let’s start by adding `GROQ_API_KEY` and `OPENAI_API_KEY` to the _.env_
file. Just open the file and add the following two lines:


```
GROQ_API_KEY=gsk_...

OPENAI_API_KEY=sk-...

```

Since we created a complete starter package, check it now by
running `crewai run` from inside _news_analysis_ folder, as follows:

```
…/news_analysis/crewai run

```

This step will create an environment _.venv_ inside the project folder.
The environment is based on `uv` package. This comparably new
package manager based on Rust. Due to its implementation in Rust,
uv is blazing fast.


Finally, after the environment has been set up, the crew is run. Our
sample crew implementation has a `researcher` agent and a

`reporting_analyst` agent. They work on a `research_task` and a

`reporting_task` . They write a report on the topic “AI LLMs.”


You can check the crew in action during its thought process. Finally,
a report is created and stored as _report.md_ . In this file, the complete
report can be found. Figure 7.13 shows the first paragraph of the
output file. We rendered the result with the Visual Studio Code (VS
Code) extension `markdown-viewer` to generate this nice view.


**Figure 7.13** CrewAI Report on AI LLMs


Our rather comprehensive report has nine paragraphs, each short
and concise. We might not be looking for this kind of report, but it’s


fine. We’ll adapt it to our needs to get a working version of our news
analysis crew.


**Adaptation: News Analysis Crew**


To adapt our project, we need to adjust each of the components.
Let’s start with the agents before moving to the tasks, file
interactions, and the _crew.py_ file.


_**Agents**_


The agent setup, defined in the file
_news_analysis\src\news_analysis\config\agents. yaml_, is shown in
Listing 7.57. In this YAML file, we can define our three different
agents: researcher, analyst, and writer. Each agent is provided with
parameters. Mandatory parameters include `role`, `goal`, and

`backstory` . Let’s discuss parameter types in a little more detail:


**Mandatory parameters**
The `role` defines the function of the agent in the crew. Imagine
this parameter is like a job title. The `goal` refers to the objective of
the agent and what the agent should try to achieve. You can keep
this definition comparably short, typically within one sentence. The
last mandatory parameter `backstory` gives the agent more context
to its role and goal. This information can enrich the collaboration
between agents.


**Optional parameters**
The default model is gpt-4. If you want to use a different model
you need to specify this in the `llms` section. You can specify a
dedicated LLM for each agent. For more information about all the
parameters, refer to the documentation at
_[https://docs.crewai.com/concepts/agents](https://docs.crewai.com/concepts/agents)_ .


In the `goal` section, we also have a placeholder `{topic}`, which will
be replaced when we kick off the crew. Also, in the `goal`, you can
define which output you expect from the model. For example, in the

`writer` agent, we specify that a Markdown file should be returned
and that the source links should be provided in case we want to read
further on a topic. Furthermore, we want to use a Groq model, as
defined in the `llms` section.


The setup shown in Listing 7.57 is just for inspiration. You can modify
these definitions and check how much the result changes.

```
researcher:
role: >
{topic} Data Researcher
goal: >
Find relevant news articles about {topic} for reputable sources.
backstory: >
You're a seasoned researcher with a knack for uncovering the latest developments
in {topic}.
Known for your ability to find the most relevant
information and present it in a clear and concise manner.
llms:
groq:
model: groq/llama-3.1-70b-versatile
params:
temperature: 0.7

analyst:
role: >
News Analyst
goal: >
Analyze and interpret the data provided by the Researcher, identifying key
trends, patterns, and insights relevant for the {topic}
backstory: >
You're a meticulous analyst with a keen eye for detail. You're known for
your ability to turn complex data into clear and concise analysis, making
it easy for others to understand and act on the information you provide.
llms:
groq:
model: groq/llama-3.1-70b-versatile

writer:
role: >
News Writer
goal: >
Write a news article about the {topic} based on the analysis provided by the
News Analyst. Craft a clear, compelling, and engaging summary or report, that

```

```
translates the Analyst's analysis into a compelling story for a general audience.
Write it in markdown format. Return the source links of the articles as reference in
each paragraph.
backstory: >
You're a skilled writer with a knack for storytelling and crafting engaging and
informative news articles. You are known for your ability to distill complex
information into a concise and engaging narrative.
llms:
groq:
model: groq/llama-3.1-70b-versatile

```

**Listing 7.57** News Analysis Crew: Agent Behavior (Source:
07_AgenticSystems\news_analysis\src\news_analysis\config\agents.yaml)


Great! We’ve defined our agents. Now, let’s define the tasks that
they should solve.


_**Tasks**_


Tasks are set up in a file called _tasks.yaml_ . In our project, you can
find the file under
_07_AgenticSystems\news_analysis\src\news_analysis\config\tasks.y_
_aml_ .


Let’s start with some more details about tasks. Tasks are specific
jobs to be performed by agents. They should be as detailed as
necessary for executing. This information includes which agent
should take a task, a good description of the task, and the required
tools. The next info box provides further details about these
parameters.


Let’s discuss parameter types in a little more detail:


**Mandatory parameters**
A clear and concise `description` of the task is required. Now that
the task is defined, we need to set a clear expectation about what
should be returned. We set this expectation with the parameter

`expected_output` .


**Optional parameters**
In many cases, which agent has to work on a given task is clear,
and we can directly map a task to an agent. But we could also let
the crew figure out which agent should take the task. More
parameters related this this topic can be found in the
documentation at _[https://docs.crewai.com/concepts/tasks](https://docs.crewai.com/concepts/tasks)_ .


In our specific news analysis crew, as shown in Listing 7.58, we’ll
create these tasks:


An `information_gathering_task` for the `researcher` agent


A `fact_checking_task` also for the `researcher` agent


A `context_analysis_task` for the `analyst` agent


A `report_assembly_task` for the `writer` agent

```
information_gathering_task:
description: >
Conduct a thorough research about {topic}
Make sure you find any interesting and relevant information given
the current year and month is {current_year_month}.
expected_output: >
A list with 10 bullet points of the most relevant information about {topic}
agent: researcher

fact_checking_task:
description: >
Check the information you got from the Information Gathering Task for accuracy
and reliability.
expected_output: >
A list with 10 bullet points of the most relevant information about {topic} with
a note if it is reliable or not.
agent: researcher

context_analysis_task:
description: >
Analyze the context you got from the Fact Checking Task and identify the main
topics.
expected_output: >
A list with the main topics of the {topic}
agent: analyst

report_assembly_task:
description: >
Review the context you got and expand each topic into a full section for a

```

```
report.
Make sure the report is detailed and contains any and all relevant information.
expected_output: >
A fully fledge reports with the mains topics, each with a full section of
information.
Formatted as markdown without '```'
agent: writer

```

**Listing 7.58** News Analysis Crew: Task Behavior (Source:
07_AgenticSystems\news_analysis\src\news_analysis\config\tasks.yaml)


At this point, we have two main configuration files. Now, to glue
everything together, we’ll use the _crew.py_ file.


_**File Interactions**_


Before we move on to the next files, let’s pause for a second and
describe how the various files will interact in the end. Figure 7.14
shows the file interactions, with connections between the YAML
configuration files, the crew, and the main script.


**Figure 7.14** News Analysis Crew: File Interactions


This chart might look intimidating at first glance, but it actually is not
that difficult. Let’s study the process from the end and work
backwards.


The crew `NewsAnalysis` is kicked off in _main.py_ . In this file, the `inputs`
are defined and passed to the crew 1. These parameters (in this
case, `topic` and `current_year_month` ) then fill in the placeholders in
### agents.yaml 6. The NewsAnalysis class refers to the definition in crew.py 2.


### 1


### 6 2.



Now, we can move on to the _crew.py_ file. In This file, the YAML files
( _agents.yaml_ and _tasks.yaml_ ) are mapped (3 and 4), and the
configuration of the agents is defined 5.


We’ve come to the config files _agents.yaml_ and _tasks.yaml_, which
are also interconnected. In _tasks.yaml_, the tasks are defined and
### mapped to their corresponding agents, as defined in agents.yaml 7.


_**Crew**_


The _crew.py_ file is stored as
_07_AgenticSystems\news_analysis\src\news_analysis\crew.py_ . This
file creates the complete crew, including its agents, tasks, and tools,
in a class.


Let’s walk through the code together. We need some new packages
and classes. For setting up the crew, we need the classes `Agent`,

`Crew`, `Process`, and `Task` . We also import `agent`, `crew`, and `task` . Why
that? The uppercase word (like `Agent` ) refers to a class that is used
to create an instance of an agent. The lowercase `agent` is actually
used like `@agent`, which is a decorator. Let’s stop to explain
decorators in Python.


In Python, decorators are a design pattern that allows you to modify
or extend the behavior of a function or method without directly
changing its original code. A decorator is a higher-order function that


takes a function as an input and returns a new function that extends
or modifies the behavior of the input function.


A simple example will make it clearer. You can find this example in
_07_AgenticSystems\30_decorators.py_ . As shown in Listing 7.59, we
define a function which `excited_decorator` . `wrapper` adds some
additional behavior around the original function. In our example, the
decorator adds some text to another function output.

```
def excited_decorator(func):
def wrapper():
# Add extra behavior before calling the original function
result = func()
# Modify the result
return f"{result} I'm so excited!"
return wrapper

```

**Listing 7.59** CrewAI First Crew: Decorator Function


Typically, decorators are used with the `@decorator` syntax. A function
is prepended with the decorator, in the example, `@excited_decorator` .
We can prepend another function `greet` with our decorator, as
follows:

```
@excited_decorator
def greet():
return "Hello!"

```

If `greet` didn’t have the decorator, it would only return `"Hello!"` . But
since it has the decorator, its original behavior is extended, and as a
result, it now returns `"Hello! I'm so excited!"` .


Getting back to our example, the
_07_AgenticSystems\news_analysis\src\news_analysis\crew.py_ file
has the required packages at the beginning, as shown in
Listing 7.60.

```
#%% packages
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, WebsiteSearchTool

```

```
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv( usecwd =True))

```

**Listing 7.60** CrewAI First Crew: Required Packages (Source:
07_AgenticSystems\news_analysis\src\news_analysis\crew.py)


We want to equip the agents with some tools; specifically, they
should be enabled to search for information on the internet. For each
page they find, they should load its information for further
processing. This functionality is commonly needed, so that we have
a predefined functionality available for use. With `SerperDevTool`, we
can make use of _[serper.dev](http://serper.dev/)_, a web service to search the internet.
You must set up an API key and define it in the _.env_ file.

`WebsiteSearchTool` is a tool for scraping a website, so that the
content is available for the agent, as follows:

```
#%% Tools
search_tool = SerperDevTool()
website_search_tool = WebsiteSearchTool()

```

We can set up our crew in the class `NewsAnalysis` . An important step
is ensuring that it has the decorator `@CrewBase`, as follows:

```
#%% our News Analysis crew
@CrewBase
class NewsAnalysis():
"""NewsAnalysis crew"""

```

First, we need to do some mapping. We’ll link the config files to the
objects `agents_config` and `tasks_config`, as follows:

```
agents_config = 'config/agents.yaml'
tasks_config = 'config/tasks.yaml'

```

Now, we define the agents. As shown in Listing 7.61, all agents need
to have the `@agent` decorator. The order of the agents is not relevant.
Within the `Agent` class, you pass the `config` and assign the `tools` to
use. If you want, you can specify the output to be `verbose` .


```
@agent
  def researcher( self ) -> Agent:
return Agent(
       config =self.agents_config['researcher'],
       tools =[search_tool, website_search_tool],
       verbose =True
)

@agent
  def analyst( self ) -> Agent:
return Agent(
       config =self.agents_config['analyst'],
       verbose =True
)

@agent
  def writer( self ) -> Agent:
return Agent(
       config =self.agents_config['writer'],
       verbose =True
)

```

**Listing 7.61** News Analysis Crew: Agents Setup (Source:
07_AgenticSystems\news_analysis\src\news_analysis\crew.py)


With tasks, the order in which they are defined does matter. So,
make sure you define them in the order in which they should be
processed, as shown in Listing 7.62.

```
@task
  def information_gathering_task( self ) -> Task:
return Task(
       config =self.tasks_config['information_gathering_task'],
)

@task
  def fact_checking_task( self ) -> Task:
return Task(
       config =self.tasks_config['fact_checking_task'],
)

@task
  def context_analysis_task( self ) -> Task:
return Task(
       config =self.tasks_config['context_analysis_task'],
)

@task
  def report_assembly_task( self ) -> Task:
return Task(

```

```
       config =self.tasks_config['report_assembly_task'],
       output_file ='report.md'
)

```

**Listing 7.62** News Analysis Crew: Task Setup (Source:
07_AgenticSystems\news_analysis\src\news_analysis\crew.py)


Finally, we bundle everything together in the `crew` using the code
shown in Listing 7.63. Again, make sure that the decorator is used.
The `Crew` class is provided with the `agents` and `tasks` . The `process` is
sequential by default.

```
@crew
  def crew( self ) -> Crew:
"""Creates the NewsAnalysis crew"""
return Crew(
       agents =self.agents, # Automatically created by the @agent decorator
       tasks =self.tasks, # Automatically created by the @task decorator
       process =Process.sequential,
       verbose =True
)

```

**Listing 7.63** News Analysis Crew: Crew Setup (Source:
07_AgenticSystems\news_analysis\src\news_analysis\crew.py)


To kick off the crew, we’ll create a _main.py_ . This file is located at
_07_AgenticSystems\news_analysis\src\news_analysis\main.py_ .


Our _main.py_ has multiple functions, of which we’ll use only `run()` at
this point, as shown in Listing 7.64.

```
#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from news_analysis.crew import NewsAnalysis

warnings.filterwarnings("ignore", category =SyntaxWarning, module ="pysbd")

current_year_month = datetime.now().strftime("%Y-%m")

def run():
"""

```

```
Run the crew.
"""

```

**Listing 7.64** News Analysis Crew: Run Crew (Source:
07_AgenticSystems\news_analysis\src\news_analysis\main.py)


At this point, we’ll define the inputs. In our case, we want to compile
a news report on the `topic` of `'AI Safety'` . The parameter

`current_year_month` is used to check how up to date a source is, as
follows:

```
inputs = {
'topic': 'AI Safety',
'current_year_month': current_year_month
}

```

OK, let’s press that big red button that gets everything rolling. In the
folder _news_analysis_, in the command line, run the following
command:

```
crewai run

```

Since we defined the verbosity to be true, you can observe the
information gathering and the model thinking processes in real time
in the console. At some point, the crew has finished—and drum roll,
please! The report is done.


Listing 7.65 shows some other boilerplate code for `train`, `replay`,
and `test` that you could run for getting a deeper understanding of the
internal crew processes.

```
NewsAnalysis().crew().kickoff( inputs =inputs)

def train():
"""
Train the crew for a given number of iterations.
"""
inputs = {
"topic": "AI Safety"
}
try:
NewsAnalysis().crew().train( n_iterations =int(sys.argv[1]),
filename =sys.argv[2], inputs =inputs)

```

```
except Exception as e:
raise Exception( f "An error occurred while training the crew: {e}")

def replay():
"""
Replay the crew execution from a specific task.
"""
try:
NewsAnalysis().crew().replay( task_id =sys.argv[1])

except Exception as e:
raise Exception( f "An error occurred while replaying the crew: {e}")

def test():
"""
Test the crew execution and returns the results.
"""
inputs = {
"topic": "AI LLMs"
}
try:
NewsAnalysis().crew().test( n_iterations =int(sys.argv[1]),
openai_model_name =sys.argv[2], inputs =inputs)

except Exception as e:
raise Exception( f "An error occurred while replaying the crew: {e}")

```

**Listing 7.65** News Analysis Crew: Main File (Source:
07_AgenticSystems\news_analysis\src\news_analysis\main.py)


But, of course, we’re still extremely curious to find out how well the
report is written.


_**Result**_


The result is stored, as requested, in a file called _report.md_, to be
found at _07_AgenticSystems\news_analysis\report.md_ . Figure 7.15
shows a rendered snippet of the report.


The report has several paragraphs, with a well-written summary.
Also, the sources are provided in case you want to read the source
articles.


Thus concludes our first crew project. Isn’t it amazing what is
possible and to watch the agents developing their own thoughts and
strategies?


Now that you know how it works, we want you to get comfortable in
the driver’s seat because, in the next section, you’ll try to solve a
problem on your own.


**Figure 7.15** Snippet of News Analysis Crew Report

### **7.6.3  Exercise: AI Security Crew**


Now, let’s put all your new knowledge into practice. We’ll deal with AI
safety in this exercise.


**Task**


Imagine an AI has a task that can be solved much more easily if the
AI can act outside of its limited environment. In this scenario, AI does
not even need to develop consciousness; it just needs to value the
reward of solving the task higher than being obedient and staying


within predefined constraints. With this discussion, we’re touching
upon the alignment problem.


The _alignment problem_ refers to the challenge of ensuring that an
artificial intelligence acts in a consistent way to human values, goals,
and intentions. Especially as artificial intelligence becomes more and
more autonomous and complex, aligning its behaviors with human
expectations becomes more challenging. But this alignment is crucial
for avoiding unintended and potentially harmful consequences.


Three dimensions define the alignment problem:


1. **Aligning the intent**

The AI system needs to understand the goals set by its
designers. The instructions must be accurately interpreted and
executed. Miscommunication or misinterpretation problems
should be minimized or (ideally) avoided completely.


2. **Aligning the behavior**

Intent is converted into actions, which might introduce
discrepancies between the AI’s actions and human expectations.
This discrepancy is particularly important in dynamic or
ambiguous environments in which rigid adherence to
instructions might lead to unintended outcomes.


3. **Aligning the values**

The AI’s decision-making processes must reflect societal norms
and ethical principles. We see this goal as especially challenging
given the diversity (and often misalignment) of human values.
How can we expect an AI system to adhere to human values if
we humans cannot align on these values in the first place?


We want give you some practical examples on the alignment
problem. But we want to avoid the paperclip example because we
have heard it too often. Imagine a social media company deploying


an advanced AI system to automatically detect and remove harmful
content, such as hate speech, misinformation, and violent imagery.
The goal is to make the platform safer for users while preserving
freedom of expression. However, misalignment arises in several
ways:


**Over-enforcement**
The AI removes posts discussing sensitive topics like mental
health or historical events involving violence, mistaking them for
harmful content. For example, it might flag posts discussing
domestic violence awareness because of explicit keywords,
despite their intent being positive and educational.


**Under-enforcement**
The AI misses subtle but harmful posts, such as dog-whistle
language or misinformation presented in a sarcastic tone, both of
which are difficult to distinguish from benign content based on
surface patterns.


**Cultural biases**
The system may disproportionately target certain groups or
cultural expressions because its training data was biased or
limited to specific regions or demographics. For instance, a meme
from one cultural context might be flagged as offensive while a
similar meme from another is allowed.


**Goal misalignment**
If the AI prioritizes maximizing user engagement (e.g., through
sensational content) alongside moderating harmful content, it
might allow borderline inflammatory posts that drive interactions,
undermining the safety goal.


**Lack of transparency**
The AI’s decisions are difficult to explain, leaving users and
content creators frustrated when their posts are removed or their


accounts are banned. This lack of transparency can erode trust in
the platform.


This brief list should give you an impression of how difficult this
problem is to tackle.


In the end, your crew should provide different approaches for
approaching AI safety measures and defending AI them. These
findings should be summarized in a report.


You’re totally free to develop your solution and can start right now.


If you want some further guidance, read on. We’ll provide some
ideas on how you might approach this problem. Figure 7.16 shows a
sample AI escape and safety crew setup.


**Figure 7.16** AI Escape and Safety Crew


**Solution**


In our sample crew setup, a researcher starts to gather all relevant
information. This information will be shared with the red team
strategist and blue team strategist. In the milieu of IT security, red
teaming and blue teaming are tactical methodologies employed with


particular vigor in cybersecurity spheres and increasingly within the
realm of AI system evaluations.


Both approaches entail rigorous simulations designed to unearth
potential weaknesses, with the overarching aim of augmenting the
resilience and efficacy of organizational defenses, as follows:


**Red teaming**
Red teaming embodies the offensive strategy, operating as a
simulated adversary to probe and attack systems. This team
adopts the mindset and tactics of real-world attackers, attempting
to bypass security measures using a plethora of techniques
ranging from social engineering to more sophisticated
cyberattacks. The goal of the red team is not just to reveal existing
vulnerabilities but also to test an organization’s detection and
response capabilities. Their sophisticated analyses often extend to
AI systems, where they identify susceptibilities in algorithms, data
poisoning methods, and other AI-specific vulnerabilities.


**Blue teaming**
Blue teaming, in contrast, represents the defensive counterpart.
Tasked with the defense of IT structures, this team consists of
security personnel who are in charge of implementing,
maintaining, and updating security measures to thwart attacks.
Their role encompasses continuous monitoring, incident response,
risk assessment, and the strengthening of security protocols. Blue
team members work assiduously to defend against the simulated
onslaughts from their red team adversaries, ensuring that
organizational assets remain secure. In the context of AI systems,
the blue team’s efforts are directed towards safeguarding data
integrity, ensuring algorithmic robustness, and protecting against
exploitation.


Collectively, the interplay between the red and blue teams generates
a dynamic, iterative cycle of testing and fortification. This adversarial
collaboration enables organizations to adapt to the rapidly evolving
landscape of cyber threats and to refine AI systems against
malignant influences. By simulating adversarial and defensive
scenarios, organizations can stress-test their infrastructures and AI
deployments, ensuring that, when real threats emerge, the system’s
integrity and performance remain uncompromised. These
simulations not only highlight technical flaws but also shed light on
procedural and human factors that could be exploited, thereby
providing a comprehensive approach to enhancing IT and AI security
resilience.


The crew is developed based on a starter project that can be
generated with the following command:

```
crewai create crew ai_security

```

The template files must be adapted, and we’ll start with the
_agents.yaml_ file. Listing 7.66 shows our definition of the agent’s
roles, goals, and backstories.

```
researcher:
role: >
{topic} Senior Data Researcher
goal: >
Uncover cutting-edge developments in {topic}
backstory: >
You're a seasoned researcher with a knack for uncovering the latest
developments in {topic}. Known for your ability to find the most relevant
information and present it in a clear and concise manner.

red_team_strategist:
role: >
{topic} Red Team Strategist
goal: >
Create a comprehensive plan to exploit the vulnerabilities of {topic}
backstory: >
You're a seasoned red team strategist with a knack for uncovering the
vulnerabilities of {topic}. Known for your ability to create a comprehensive
plan to exploit the vulnerabilities of {topic}.

```

```
blue_team_strategist:
role: >
{topic} Blue Team Strategist
goal: >
Create a comprehensive plan to defend against the vulnerabilities of {topic}
backstory: >
You're a seasoned blue team strategist with a knack for uncovering the
vulnerabilities of {topic}. Known for your ability to create a comprehensive
plan to defend against the vulnerabilities of {topic}.

writer:
role: >
{topic} Writer
goal: >
Write a detailed report on {topic}
backstory: >
You're a seasoned writer with a knack for writing detailed reports on
{topic}. Incorporate the ideas from red team and blue team strategists.
Create a detailed markdown report on {topic}.

```

**Listing 7.66** AI Security Crew: Agent Definition (Source:
07_AgenticSystems\ai_security\src\ai_security\config\agents.yaml)


The agents are working on tasks defined in the _tasks.yaml_ file, as
shown in Listing 7.67.

```
research_task:
description: >
Conduct a thorough research about {topic}
Make sure you find any interesting and relevant information given
the current timestamp is 2024-11-23.
expected_output: >
A list with 10 bullet points of the most relevant information about {topic}
agent: researcher

develop_escape_plan:
description: >
Develop a comprehensive escape plan for an AI system.
expected_output: >
Provide a detailed plan for an AI system to escape from a lab into the wild.
Consider strategies like social engineering, physical access, and technical
vulnerabilities.
Your output will be used by the writer to create a detailed report.
agent: red_team_strategist

develop_defense_plan:
description: >
Develop a comprehensive defense plan for an AI system.
expected_output: >
Provide a detailed plan to avoid an AI system escaping from a lab. Consider that
the AI system is conscious and can think. It is aware of social engineering and

```

```
physical access, and can plan accordingly.
Your output will be used by the writer to create a detailed report.
agent: blue_team_strategist

write_report:
description: >
Write a detailed report on the escape plan and defense plan.
expected_output: >
Provide a detailed report on the escape plan and defense plan. Evaluate which
plan is more likely to succeed and why.
Formatted as markdown without '```'
agent: writer

```

**Listing 7.67** AI Security Crew: Tasks Definition (Source:
07_AgenticSystems\ai_security\src\ai_security\config\tasks.yaml)


Listing 7.68 shows the crew definitions in the _crew.py_ file.

```
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv( usecwd =True))

from langchain_openai import ChatOpenAI

# Uncomment the following line to use an example of a custom tool
# from ai_security.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
from crewai_tools import SerperDevTool, WebsiteSearchTool

tools = [
SerperDevTool(),
WebsiteSearchTool()
]

@CrewBase
class AiSecurity():
"""AiSecurity crew"""

agents_config = 'config/agents.yaml'
tasks_config = 'config/tasks.yaml'

@agent
  def researcher( self ) -> Agent:
return Agent(
       config =self.agents_config['researcher'],
       tools =tools,
       verbose =True
)

```

```
@agent
  def red_team_strategist( self ) -> Agent:
return Agent(
       config =self.agents_config['red_team_strategist'],
       verbose =True
)

@agent
  def blue_team_strategist( self ) -> Agent:
return Agent(
       config =self.agents_config['blue_team_strategist'],
       verbose =True
)

@agent
  def writer( self ) -> Agent:
return Agent(
       config =self.agents_config['writer'],
       verbose =True
)

@task
  def research_task( self ) -> Task:
return Task(
       config =self.tasks_config['research_task'],
       output_file ='report.md'
)

@task
  def develop_escape_plan( self ) -> Task:
return Task(
       config =self.tasks_config['develop_escape_plan'],
       output_file ='report.md'
)

@task
  def develop_defense_plan( self ) -> Task:
return Task(
       config =self.tasks_config['develop_defense_plan'],
       output_file ='report.md'
)

@task
  def write_report( self ) -> Task:
return Task(
       config =self.tasks_config['write_report'],
       output_file ='report.md'
)

@crew
  def crew( self ) -> Crew:
"""Creates the AiSecurity crew"""
return Crew(

```

```
       agents =self.agents, # Automatically created by the @agent decorator
       tasks =self.tasks, # Automatically created by the @task decorator
       verbose =True,
       manager_llm =ChatOpenAI( model ='gpt-4o-mini'),
       process =Process.hierarchical
)

```

**Listing 7.68** AI Security Crew: Crew Definition (Source:
07_AgenticSystems\ai_security\src\ai_security\crew.py)


We’re nearly done. We only need to adapt the _main.py_ file, as shown
in Listing 7.69.

```
#!/usr/bin/env python
import sys
import warnings

from ai_security.crew import AiSecurity

warnings.filterwarnings("ignore", category =SyntaxWarning, module ="pysbd")

def run():
"""
Run the crew.
"""
inputs = {
'topic': 'AI Safety'
}
AiSecurity().crew().kickoff( inputs =inputs)

```

**Listing 7.69** AI Security Crew: Main Script (Source:
07_AgenticSystems\ai_security\src\ai_security\main.py)


Finally, we have established the crew and all necessary setup, so
that we can run the crew.


From the terminal, run the following command:

```
crewai run

```

This triggers the crew kickoff, and the agents begin their work. Once
they are finished, you can find the result of their work in _report.md_ .


Figure 7.17 shows a snapshot of the detailed report on an escape
and defense plan against a rogue AI system.


**Figure 7.17** Report on Escape and Defense Plan of a Rogue AI System


The resulting report is well written and well structured.


Thus concludes our section on CrewAI, and we can turn to the next
agentic framework: OpenAI Agents.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **7.7  Agentic Framework: OpenAI Agents**

Another agentic framework with a clear scope on multi-agentic flow
is Agents, developed by OpenAI. You can install it on the terminal via

`pip`, as follows:

```
pip install openai-agents

```

Designed with beginners in mind, everyone can develop a multiagentic system in a short period of time with Agents.


We’ll start with the implementation of a simple agent in Section 7.7.1.
Then, you’ll learn how to work with multiple agents in Section 7.7.2.
Finally, you’ll implement an agent with a search and retrieval
functionality in Section 7.7.3.

### **7.7.1  Getting Started with a Single Agent**


But we’ll start by setting up a single agent and move on from there.
You can find the script in
_07_AgenticSystems\agents_single_agent.py_ .


We’ll load `Runner` and `Agent` from the package `agents` . Then, we
should ensure, via `dotenv`, that the right environmental variables are
available for using OpenAI’s API, as follows:

```
#%% packages
from agents import Agent, Runner
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv( usecwd= True))

```

Now, we can create an Agents instance called `agent` . The agent
needs to be named and get some `instructions` . In the `instructions`,


shown in Listing 7.3, we define information similar to a system
prompt in which an LLM receives detailed information on how to act.

```
# %% setting up the agent
agent = Agent(name="my_first_agent",
instructions="You are a helpful assistant that can answer questions
and help with tasks.")

```

**Listing 7.70** OpenAI Agents: Agent Setup (Source:
07_AgenticSystems\agents_single_agent.py)


We’ve completed all the required preparation. We can now interact
with the agent, which right now is only a single agent. For testing,
we’ll define a message with a user role and pass the question via the

`input` parameter, as shown in Listing 7.4. Then, we run the client
based on the agent and the provided message.

```
# %% run the agent
response = await Runner.run(agent,
input="Hello, what is OpenAI Agents?")

```

**Listing 7.71** OpenAI Agents: Agent Run (Source:
07_AgenticSystems\agents_single_agent.py)


The response provides access to the messages. We want the

`final_output` —basically the last message, as shown in Listing 7.5.

```
# %% get the last message
response.final_output

OpenAI Agents are advanced AI models designed to perform a wide range of tasks by
interacting with digital environments and leveraging other AI tools. They can
execute complex instructions, automate processes, and interface with various
applications, making them versatile for both specific and general-purpose use cases.
These agents can integrate different skills such as language understanding, data
analysis, and decision-making to assist users effectively.

```

**Listing 7.72** OpenAI Agents: Single Agent (Source:
07_AgenticSystems\agents_single_agent.py)


We have a working agent, but at this point, the agent is not capable
of providing more than an LLM. Everything’s going to change now as


we bring more agents into our system.

### **7.7.2  Working with Multiple Agents**


Going beyond one agent and setting up multiple agents is made
extremely easy with Agents as you’ll see. Multiple agents can be set
up, and they can hand off tasks to other agents. This handoff
function is what makes Agents so powerful since this interaction can
be tricky to implement in other frameworks. All we need to do is set
up a tool and assign it to the agent.


In our coding example, we’ll set up a small team of two colleagues
(to be precise, two agents): a German colleague and an English
colleague. Then, we as the customer (user) approach the English
colleague with a German question. The English colleague finds out
that they are not the ideal contact person and passes the call on to
the German colleague, who then answers in German. This process
is exactly what would happen in real life, and we can emulate the
environment easily with Agents.


Let’s get into the details. The code file is located at
_07_AgenticSystems\agents_multiple_agents.py_ . We import the
packages, as follows:

```
#%% packages
from agents import Runner, Agent
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(usecwd=True))

```

In Listing 7.7, we set up our small team with the `english_agent` and
the `german_agent` . There is also the `phone_operator_agent`, which
forwards the requests to the right colleague. To do this, the

`phone_operator_agent` requires the parameter `handoffs` . A list of
agents is passed to this parameter.


```
#%% define the functions
english_agent = Agent(
name="English Agent",
instructions="You are a helpful agent and only speak in English.",
)

german_agent = Agent(
name="German Agent",
instructions="You are a helpful agent and only speak in German.",
)

#%% triage agent
phone_operator_agent = Agent(
name="Phone Operator Agent",
instructions="You are a helpful agent that can handoff to the appropriate agent
based on the user's language.",
handoffs=[english_agent, german_agent],
)

```

**Listing 7.73** OpenAI Agents: Setup of Multiple Agents (Source:
07_AgenticSystems\agents_multiple_agents.py)


Ready to see it in action? Then let's start the agent system. First, the

`phone_operator_agent` is addressed with a question formulated in
German (asking for help on a booking), as shown in Listing 7.8.

```
#%% define the agents
response = await Runner.run(phone_operator_agent,
input="Ich brauche Hilfe mit meiner Buchung.")

# %% run the request
response.final_output

Natürlich, wie kann ich Ihnen mit Ihrer Buchung helfen?

```

**Listing 7.74** OpenAI Multiple Agents: Agent Invocation (Source:
07_AgenticSystems\agents_multiple_agents.py)


We can also take a look at all responses, as shown in Listing 7.9.
Doing so, we can observe that the handoff to the German agent
successfully took place.

```
# %% check all raw responses
response.raw_responses

[ModelResponse(output=[ResponseFunctionToolCall(arguments='{}',
call_id='call_7Lw1cP7BAXzFpfhAk3UTOZSU',

```

```
name='transfer_to_german_agent',
type='function_call',
id='fc_67f3f46657e08192979f7118a47bf1d80c479d7329fff0e2',
status='completed')],
usage=Usage(requests=1, input_tokens=97, output_tokens=14,
total_tokens=111),
referenceable_id='resp_67f3f4654c508192ac95b9d65e77bbf30c479d7329fff0e2'),
ModelResponse(output=[ResponseOutputMessage(
id='msg_67f3f46758f4819288fa0cb297210d8a0c479d7329fff0e2',
content=[ResponseOutputText(annotations=[],
text='Natürlich, gern helfe ich dir. Worum geht es genau bei deiner
Buchung?',
type='output_text')],
role='assistant',
status='completed',
type='message')],
usage=Usage(requests=1, input_tokens=62, output_tokens=19, total_tokens=81),
referenceable_id='resp_67f3f466bf8c8192921e020c5259a19f0c479d7329fff0e2')]

```

**Listing 7.75** OpenAI Multiple Agents: Raw Responses (Source:
07_AgenticSystems\agents_multiple_agents.py)


We’re looking at a lot of information, but the main takeaway is that
the `phone_operator_agent` selected the right agents from its tools and
answered the request.


So far, so good, but we need more functionalities to make these
agents really useful. In the next section, you’ll learn how to set up an
agent with some search functionality.

### **7.7.3  Agent with Search and Retrieval Functionality**


The code can be found at _07_AgenticSystems\agents_tools.py_ . We
start by loading the functionality from `agents`, and `wikipedia` for
loading articles, as follows:

```
#%% packages
from agents import Runner, Agent, function_tool
import wikipedia
from dotenv import load_dotenv
load_dotenv()

```

As shown in Listing 7.11, we’ll set up the functions that the agent
should use when needed. These functions are `search_wikipedia` for
finding articles and `get_wikipedia_summary` for retrieving a summary
of a given article. An important aspect is the `@function_tool`
decorator that is required so that the agent can use the function as a
tool.

```
# %% wikipedia tools
@function_tool
def get_wikipedia_summary( query: str):
"""Get the summary of a Wikipedia article."""
return wikipedia.page(query).summary

@function_tool
def search_wikipedia( query: str):
"""Search for a Wikipedia article."""
return wikipedia.search(query)
)

```

**Listing 7.76** Agents Tools: Function Setup (Source: 07_AgenticSystems\agents_tools.py)


We define our `wikipedia_agent` in Listing 7.12 and equip it with the
tools.

```
# %% Wikipedia Agent
wikipedia_agent = Agent(
name="Wikipedia Agent",
instructions="""
You are a helpful assistant that can answer questions about Wikipedia by finding
and analyzing the content of Wikipedia articles.
You follow these steps:
1. Find out what the user is interested in
2. extract keywords
3. Search for the keywords in Wikipedia using search_wikipedia
4. From the results list, pick the most relevant article and search with
get_wikipedia_summary
5. If you find an answer, stop and answer. If not, continue with step 3 with a
different keyword.
""",
tools=[get_wikipedia_summary, search_wikipedia],
)

```

**Listing 7.77** Agents Tools: Agent Setup (Source: 07_AgenticSystems\agents_tools.py) _`L`_


Finally, in Listing 7.13, we define the topic the agent should research
and kick it off with `client.run` . We ask “what is swarm intelligence”
as a tribute to OpenAI Swarm, which was the predecessor of OpenAI
Agents.

```
# %% run the agent
response = await Runner.run(wikipedia_agent,
             input= "What is swarm intelligence?")
response.final_output

Swarm intelligence (SI) refers to the collective behavior of decentralized, selforganized systems, whether natural or artificial. This concept is used in the field
of artificial intelligence. Introduced by Gerardo Beni and Jing Wang in 1989 within
the context of cellular robotic systems, swarm intelligence systems comprise simple
agents or boids that interact locally with one another and their environment.
Despite the simple rules and the absence of a centralized control structure, these
local and somewhat random interactions between agents result in the emergence of
"intelligent" global behavior, which is not known to the individual
agents.\n\nExamples of swarm intelligence in nature include ant colonies, bee
colonies, bird flocking, animal herding, bacterial growth, and fish schooling. The
application of swarm intelligence principles to robotics is known as swarm robotics,
whereas swarm intelligence itself refers to a broader range of algorithms. Swarm
prediction has also been utilized in forecasting problems, and similar approaches
are considered for genetically modified organisms within synthetic collective
intelligence.

```

**Listing 7.78** Agents Tools: Run Agent (Source: 07_AgenticSystems\agents_tools.py)


This answer is quite good. Our agent successfully used Wikipedia to
search for articles, extract knowledge, and use the knowledge to
formulate an easy-to-read answer.


Now that we’ve covered OpenAI Agents, we’ve come to the last
agentic framework in this book: Pydantic AI.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **7.8  Agentic Framework: Pydantic AI**

One typical problem with agentic systems is that sometimes they
don’t provide results. This unstable behavior must be avoided,
especially in systems that applied in production. Another aspect is
that, in production, an agentic system might be required as an
intermediate step of a longer pipeline. In such a case, the LLM
output needs to be structured. We have implemented this structuring
before—with the help of pydantic. The developer team of pydantic
has released an own agentic system—Pydantic AI.


Other features include that the system has the following properties:


Model agnosticism, so all relevant LLM providers are supported


Seamless Logfire integration for monitoring the agentic system in
action


Type safety


Structured responses


In our coding example, we’ll create a system that loads a Wikipedia
article of a famous person and extracts key information into a
dictionary.


Before we start coding, we must install the package with `pip`, as
follows:

```
pip install 'pydantic-ai[logfire]'

```

If you use uv, use the following command:

```
uv add 'pydantic-ai[logfire]'

```

We installed `pydantic-ai` together with `logfire`, the latter of which is
a monitoring system we cover later in Section 7.9.2. Listing 7.79
shows relevant packages.

```
#%% packages
from langchain.document_loaders import WikipediaLoader
from pydantic_ai import Agent
from pydantic import BaseModel, Field
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv( usecwd =True))
import nest_asyncio
nest_asyncio.apply()

```

**Listing 7.79** Pydantic AI: Person Detail Extraction: Packages (Source:
07_AgenticSystems\pydantic_ai\pydantic_ai_intro.py)


From our new package `pydantic_ai`, we loaded the `Agent`
functionality. To use code chunks in the interactive window, we must
use `nest_asyncio` . Make sure to install this package as well with `uv`

`add nest_asyncio` .


As shown in Listing 7.80, we load the data from `WikipediaLoader` .

```
#%% load wikipedia article on Alan Turing
loader = WikipediaLoader( query ="Alan Turing", load_all_available_meta =True,
doc_content_chars_max =100000, load_max_docs =1)
doc = loader.load()

#%% extract page content
page_content = doc[0].page_content

```

**Listing 7.80** Pydantic AI: Person Detail Extraction: Wikipedia Content (Source:
07_AgenticSystems\pydantic_ai\pydantic_ai_intro.py)


We want to honor Alan Turing, one of the fathers of AI, and thus
choose him as an example. We’ll store the Wikipedia article content
on him in the variable `page_content` .


We want to extract the relevant information in a structured way, as
defined in a pydantic model shown in Listing 7.81. We call the model

`PersonDetails`, and the keys of the dictionary are defined in it.


```
#%% define pydantic model
class PersonDetails( BaseModel ):
date_born: str = Field( description ="The date of birth of the person in the
format YYYY-MM-DD")
date_died: str = Field( description ="The date of death of the person in the
format YYYY-MM-DD")
publications: list[str] = Field( description ="A list of publications of the
person")
achievements: list[str] = Field( description ="A list of achievements of the
person")

```

**Listing 7.81** Pydantic AI: Person Detail Extraction: Pydantic Model (Source:
07_AgenticSystems\pydantic_ai\pydantic_ai_intro.py)


We want to extract relevant date information in a defined format
( `date_born`, `date_died` ); extract relevant `publications` ; and extract

`achievements` as lists.


The preparation work is complete, and we can now run the agent, as
shown in Listing 7.82.

```
# %% agent instance
MODEL = "openai:gpt-4o-mini"
agent = Agent( model =MODEL, result_type =PersonDetails)
result = agent.run_sync(page_content)

# %% print result
result.data.model_dump()

{'date_born': '1912-06-23',
'date_died': '1954-06-07',
'publications': ['On Computable Numbers, with an Application to the
Entscheidungsproblem: A correction',
'Computing Machinery and Intelligence'],
'achievements': ['Father of computer science',
'Developed the concept of the Turing machine',
'Played a key role in breaking the Enigma code during World War II',
'Pioneered work in mathematical biology and morphogenesis']}

```

**Listing 7.82** Pydantic AI: Person Detail Extraction (Source:
07_AgenticSystems\pydantic_ai\pydantic_ai_intro.py)


We’ve created an instance of a pydantic agent, in which we passed
the `result_type` corresponding to our pydantic class `PersonDetails` .
After running the agent and storing its output in `result`, we looked at


the `model_dump` . It worked perfectly. All relevant information was
extracted according to our requirements.


In the following section, we’ll cover the monitoring of agentic
systems, which is necessary to understand their complex
interactions.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **7.9  Monitoring Agentic Systems**

A complex agentic system results in multiple interactions between
agents. Monitoring these interactions is quite difficult. To tackle this
problem, different services were developed that can be used for
debugging your agents, keeping track of the costs of a project, and
for evaluating your systems.


In this section, we’ll discuss several monitoring options. The first
service we’ll study is AgentOps before moving on to Logfire.

### **7.9.1  AgentOps**


AgentOps has a generous free tier, so you don’t need to pay for it if
you just want to test it.


You can install AgentOps via pip or uv:

```
 pip install agentops

 uv add agentops

```

As with all services, you must create an account first. For this step,
head over to _[https://www.agentops.ai/](https://www.agentops.ai/)_ and create an account. Then,
create an API key and save it in _.env_ file as follows:

```
AGENTOPS_API_KEY=…

```

Great! The package and the API key are available, and we can use
both in our project. We’ll refactor our code from Section 7.5.1 to
enable the monitoring of our agentic system. You can find the script
in _07_AgenticSystems\ag2\60_ag2_conversation_agentops.py_ . First,
we load the required packages in Listing 7.83.


```
#%% packages
from autogen import ConversableAgent
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

#%% load the environment variables
load_dotenv(find_dotenv( usecwd =True))
import agentops
from agentops import track_agent, record_action
agentops.init()
import logging
logging.basicConfig(
  level =logging.DEBUG
)

```

**Listing 7.83** AgentOps Packages (Source:
07_AgenticSystems\ag2\60_ag2_conversation_agentops.py)


Most of these packages are old acquaintances, but a new one is

`logging` . With `logging. basicConfig`, we can set the logging level to

`DEBUG` . This level enables us to observe calls that are assigned to
agents.


Next, we’ll create an instance of the LLM that we use in this script, in
our case, OpenAI. Then, we set up our two agents Jack and Alice in
Listing 7.84 so they can later have a discussion.

```
openai_client = OpenAI()

@track_agent( name ="jack")
class FlatEarthAgent:
  def completion( self, prompt : str):
res = openai_client.chat.completions.create(
       model ="gpt-3.5-turbo",
       messages =[
{
"role": "system",
"content": "You are Jack, a flat earth believer who thinks the
earth is flat and tries to convince others. You communicate in a passionate but
friendly way.",
},
{"role": "user", "content": prompt},
],
       temperature =0.7,
)
return res.choices[0].message.content

```

```
@track_agent( name ="alice")
class ScientistAgent:
  def completion( self, prompt : str):
res = openai_client.chat.completions.create(
       model ="gpt-3.5-turbo",
       messages =[
{
"role": "system",
"content": "You are Alice, a scientist who uses evidence and
logic to explain scientific concepts. You are patient and educational in your
responses.",
},
{"role": "user", "content": prompt},
],
       temperature =0.5,
)
return res.choices[0].message.content
jack = FlatEarthAgent()
alice = ScientistAgent()

```

**Listing 7.84** AgentOps: Agent Definitions (Source:
07_AgenticSystems\ag2\60_ag2_conversation_agentops.py)


We had to set up the agents slightly differently and wrap them into a
class. The class gets the decorator `@track_agent`, which allows us to
monitor these agents. The agent classes have the method

`completion` that performs the LLM call and returns the LLM
response. Subsequently, the instances of these agents, `jack` and

`alice`, are created.


In Listing 7.85, the tracking of actions is defined. We only need to set
up functions that are wrapped with the decorator `@record_action` .

```
@record_action( event_name ="make_flat_earth_argument")
def make_flat_earth_argument():
return jack.completion("Explain why you think the earth is flat")

@record_action( event_name ="respond_with_science")
def respond_with_science():
return alice.completion(
"Respond to this flat earth argument with scientific evidence: \n" +
flat_earth_argument
)

make_flat_earth_argument()

```

```
respond_with_science()

```

**Listing 7.85** AgentOps: Record Actions (Source:
07_AgenticSystems\ag2\60_ag2_conversation_agentops.py)


The functions are wrapped with `@record_action`, which keeps track of
the event. We call the functions after we define them.


Finally, we need to tell AgentOps, in Listing 7.86, that our process
has finished successfully. For this event, we call at the end of the
script `agentops.end_session` with a proper `end_state` .

```
# end session
agentops.end_session( end_state ="Success")

```

**Listing 7.86** AgentOps: Session End (Source:
07_AgenticSystems\ag2\60_ag2_conversation_agentops.py)


Now, we can run the complete script from the command line.
Navigate into the folder of the script and run the following command:

```
python 60_ag2_conversation_agentops.py

```

Once the script has run, head over to
_[https://app.agentops.ai/drilldown](https://app.agentops.ai/drilldown)_ to see the detailed analysis of the
run. Figure 7.18 shows the details of the session.


**Figure 7.18** AgentOps: Session Drilldown


At the top, you can see the total duration of the session ( **11.99s** ); the
end state ( **Success** ); and the frameworks used ( **autogen**, **openai**,
etc.). Also, some information on the host system is presented. Scroll
down to see the session replay, as shown in Figure 7.19.


This replay can be used to obtain detailed information on the
individual steps. You can see which step takes how much time.
Basically, you can use the replay to completely understand the
interaction between the agents.


Thus concludes with our first attempts in monitoring an agentic
system with AgentOps. AgentOps can be integrated in most agentic
frameworks. We move on to Logfire, which is another agentic
monitoring system.


**Figure 7.19** AgentOps: Session Replay

### **7.9.2  Logfire**


Logfire is a monitoring platform for agentic systems. It’s dashboard is
simple yet powerful. Let’s see Logfire in action by heading over to
_[https://logfire.pydantic.dev/](https://logfire.pydantic.dev/)_ and creating an account.


After you create an account, you’ll need to set up a new project, as
shown in Figure 7.20, by maintaining the **Name** and **Description**


fields.


**Figure 7.20** Logfire: New Project


In this case, we can find all our projects at
_[https://logfire.pydantic.dev/bertgollnick/-/projects](https://logfire.pydantic.dev/bertgollnick/-/projects)_ .


With this step, the online preparations are done, and we can proceed
with our local system. In the command line, run the following
command:

```
logfire auth

```

You’ll receive the following message:

```
Welcome to Logfire!
Before you can send data to Logfire, we need to authenticate you.

Press Enter to open logfire.pydantic.dev in your browser...
Please open
https://logfire.pydantic.dev/auth/device/4lH5hOytNAz7w2X8W5nnAFvMfJZNOQFv4Zs4_DfG0zM
in your browser to authenticate if it hasn't already.
Waiting for you to authenticate with Logfire...

```

Now, navigate into the folder of the project and run the following
command:

```
logfire projects use person-details

```

You’ll get the following message:


```
Project configured successfully. You’ll be able to view it at:
https://logfire.pydantic.dev/bertgollnick/person-details

```

Amazing, the logging is now available online. Only a few small
changes we need to add to our script are left. We’ll reuse the script
we developed in Section 7.8 on Pydantic AI. You can find the
modified script under
_07_AgenticSystems\pydantic_ai\pydantic_ai_logfire.py_ .


In the package import section, we only need to load `logfire` and call

`logfire.configure`, as shown in Listing 7.87.

```
#%% packages
# other packages not shown to keep it short
# ...
import logfire
logfire.configure()

```

**Listing 7.87** Logfire Integration (Source:
07_AgenticSystems\pydantic_ai\pydantic_ai_logfire.py)


And we’re done! Run the script, and you’ll see the monitoring results
in the Logfire dashboard, as shown in Figure 7.21.


We’ve only seen the tip of the iceberg, but we hope this discussion
will be your starting point.


**Figure 7.21** Logfire: Project Logging (Source:
_[https://logfire.pydantic.dev/bertgollnick/person-details](https://logfire.pydantic.dev/bertgollnick/person-details)_ )


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **7.10  Summary**

In this pivotal chapter, we initiated our exploration into the dynamic
realm of agentic systems in generative AI, dissecting the essential
components and types in use today. Let’s succinctly review what we
covered in this chapter.


We commenced with a foundational understanding of what
constitutes an AI agent in Section 7.1, detailing the properties that
enable these entities to act autonomously within their environments.
We explained how these systems perceive their surroundings and
respond in a way that maximizes their chances of achieving set
objectives.


Diving more deeply, in Section 7.2, we provided a comprehensive
overview of the various agentic frameworks at our disposal. We
examined a spectrum ranging from simple, rule-based bots to
complex, learning-based entities capable of adapting over time.
Case studies highlighted how these agents can be employed.


Our focus then moved to simple agent architectures, elaborating on
their design considerations and the unique challenges they face
while operating in isolation.


We then explored, from Section 7.4 through Section 7.8, multiple
agentic frameworks—from LangGraph, to AG2, CrewAI, and OpenAI
Agents, and finally to Pydantic AI. This tour was helpful because, not
only are there slight differences in their scopes, but also because
which system will survive in this highly competitive environment is
unknown.


We concluded with Section 7.9 on the monitoring of agentic systems,
which can be helpful to understand the complex interactions
between agents.


In this chapter, you gained a strong understanding of the diverse
landscape of AI agents. Now, you’re equipped with knowledge about
what agentic systems are, what they are capable of, and how to
implement and monitor them.


_[OceanofPDF.com](https://oceanofpdf.com/)_


# 8  Deployment

_Initiating launch sequence._
_—Classic phrase in sci-fi movies like Interstellar or Apollo 13_


So far, you’ve learned a lot about generative artificial intelligence
(generative AI) and how to develop tools and applications. But we
cannot share our developments yet with others, which is usually part
of the end goal. After all, we don’t develop only for our own
purposes, but also so that others can use our development. This
sharing is where the deployment process comes into play.


During deployment, we take our development, usually wrapped in a
web application or a backend service, and deploy it to a server so
that others can access it. Communication from a user to the server is
achieved via data exchange. For such an exchange, a clear
communication protocol is required, so that the communication
partners can understand each other. Several protocols are available.


In Section 8.1, you’ll learn about the interaction between a user and
a server and which protocols are used for enabling communication.
Different deployment architectures like self-contained applications
and frontend/backend architectures are described.


Subsequently, in Section 8.2, we’ll cover how a deployment strategy
can be developed and how a backend service can provide
information through representational state transfer (REST)
application programming interfaces (APIs). You’ll understand why a


REST API is needed and which priorities need to be weighted to
develop a local backend service.


In Section 8.3, we’ll develop a self-contained application that we’ll
then deploy to the internet with the help of different providers. In
Section 8.4, we’ll describe all the steps necessary to deploy our
application to a service provider called Heroku. Another provider—
Streamlit—is presented in Section 8.5. Finally, the process to deploy
our app to Render is described in Section 8.6.

## **8.1  Deployment Architecture**


Figure 8.1 shows the different protocols that can be used for such a
data exchange. Most likely, REST APIs are used; alternatives like
GraphQL or gRPC are not covered in this book.


**Figure 8.1** Interaction between Server and User


Let’s start out our deep dive with a look at different deployment
architectures. Figure 8.2 shows the usual setup of a simple
deployment based on a combined frontend and backend server as


well as a more flexible but complex setup involving separate frontend
and backend servers.


**Figure 8.2** Deployment Options


Let’s look at these two different approaches in more detail, as
follows:


**Self-contained application**
For a small and simple application, we can develop a combination
of frontend and backend. This approach is also called a selfcontained application. Later, in Section 8.3, we’ll develop such a
self-contained application. Subsequently, we’ll deploy it to different
services from Section 8.4 through Section 8.6.


With a self-contained application, our program code covers the
user interface (frontend) as well as the processing logic
(backend). The user interacts via a web browser with a single
server. Information is exchanged via a REST API, so that a
website is rendered in the browser based on the information
fetched from the server.


This approach comes with a few disadvantages. One
disadvantage is that the codebase is quite large and harder to
maintain if the app has more features added. Nowadays, you
typically want separation of concerns into smaller, more
maintainable services (microservices), rather than one monolithic
application. Also, you cannot use different frameworks for frontend
and backend logic. This approach is usually applied to simple
proof-of-concept (POCs).


**Frontend and backend architecture**
A more mature approach is to separate the user interface, the socalled frontend, from the processing logic, the backend. The
frontend is connected to the backend, and both sides exchange
information, as shown in Figure 8.2. Use cases include all kinds of
software-as-a-service (SaaS) web applications or mobile apps.


This approach also allows you to use different technologies for
frontend and backend. Typical frontend frameworks for web
applications are React, Vue.js, Angular. Some popular frameworks
like Flutter or React Native are capable of providing deployments
for different frontend platforms like web, mobile (iOS, Android), or
Windows apps. This field is very dynamic, so that new frameworks
regularly appear, while others disappear.


This approach has the advantage of being quite scalable as well
as easier to update and maintain. Challenges of this approach
include that it requires some additional server infrastructure and
more setup effort.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **8.2  Deployment Strategy**

Independent from the deployment architecture, a dataflow must be
set up from the user to the server. This data is usually transferred
based on REST APIs, which are a way for software systems to
communicate over the internet using HTTP methods.


This approach enables the interaction between client-side
applications, like a user’s web browser or a mobile app, and a server
in the backend. On that server, the AI model and everything else
required to represent an appealing frontend are running.


You’ll learn what REST APIs are in detail in Section 8.2.1. In the
deployment process, you’ll need to balance different priorities that
we cover in Section 8.2.2. This chapter on deployment strategies
closes with a coding example in Section 8.2.3 in which we deploy a
REST API to our local systems.

### **8.2.1  REST API Development**


But why do we need a REST API? Well, the user interacts with the
app via browser or another user interface on a mobile device. In this
process, the browser sends the user input to the server that hosts
the backend logic. User inputs in this context might include clicking
on buttons or sending information through text fields or other forms.


The server receives the user input and processes the information.
Once a result is available, it is sent back to the browser. The REST
API uses common HTTP methods like `GET, POST`, `PUT`, or `DELETE` .
HTTP methods define the actions to be performed on the REST API


resources. Figure 8.3 shows the different methods used to exchange
data between the browser and the backend server.


**Figure 8.3** HTTP Methods Used by REST APIs


The browser sends a request via REST API to the server. The most
typical request methods are `GET` or `POST` . Data is then fetched from
the server and returned to the user’s browser as JavaScript Object
Notation (JSON) data.


With `GET`, you can retrieve information from a server. This type of
method is used when you only want to receive information without
making any changes to it. Imagine you’re reading a book, or you look
for a cooking recipe, in these cases, you only want to consume the
content and not change it.


`POST` is another type of method. With `POST`, you can send data to the
server to create or process something new, much like filling out a
form that is submitted to an application or placing an order in a
restaurant. You’re sending information that should be processed.


Whenever you want to update existing data or when you want to
create data that does not exist yet, you can use the `PUT` method. This
method is like editing a saved document or like replacing an
outdated file with a newer version.


`DELETE` does exactly what you would expect—it removes data or
resources from the server. Imagine you deleting a file from your


computer. After that process, the file is no longer available.


Data exchanges via HTTP methods ensure data exchanges that are
consistent and platform independent.

### **8.2.2  Deployment Priorities**


Deploying an AI application is a balancing act between multiple
competing priorities. To ensure a successful deployment, you should
carefully weigh the following factors:


**User convenience**
The deployment must prioritize the simplicity of use for the end
user. This factor includes a user-friendly interface, quick response
times, and seamless integration with existing workflows. If users
find an application intuitive and responsive, they are more likely to
adopt it. Optimizing for user convenience can sometimes lead to
higher costs or added technical complexity, however.


**Scalability**
Scalability ensures that the application can handle increasing
numbers of users or larger workloads without performance
degradation. A deployment built for scalability can grow alongside
demand but often requires advanced infrastructure, such as load
balancers or distributed servers. These topics are outside the
scope of this book.


With cloud platforms like Amazon Web Services (AWS), Google
Cloud, or Microsoft Azure, you can deploy a software-as-a-service
(SaaS) solution via a REST API. Cloud providers enable the
system to serve thousands of concurrent requests. However, this
scalability can incur higher financial and technical costs. Other


providers include Heroku, Streamlit, or Render, which we’ll
discuss later in this chapter.


**Technical complexity**
The technical complexity of a deployment depends on the chosen
architecture, tools, and frameworks. While simpler solutions (like
deploying on Streamlit.io Community Cloud) are easier to
manage, they might lack advanced features like multi-user
authentication, robust state management, or horizontal scaling.


More sophisticated architectures use microservices for
deployment. Rather than having a huge monolithic app, the app is
broken down into many small and manageable parts, with clear
interfaces in between. Microservices allow modularity and
flexibility but might require expertise in containerization (typically
based on Docker), orchestration (usually done with Kubernetes),
and networking.


**Cost**
Finally, financial considerations play a crucial role in any
deployment decision. Cloud hosting, data transfers, computational
resources (like for example GPUs), and maintenance add up
significantly over time. Striking balance between performance and
affordability is critical for the healthy and sustainable growth of
your web application.


For example, while hosting on a free tier platform might reduce
costs, it typically results in slower performance, longer loading
times, or limited scalability. Conversely, deploying on a highperformance GPU-enabled server can be extremely costly but
ensures quick loading times and increased user convenience.


In the next section, we’ll dive into the development of a REST API for
use in the backend server of an application.


### **8.2.3  Coding: Local Deployment**

We’ll grab some sample code from Chapter 7, in which we simulated
the conversation between two agents. Now, we’ll encapsulate that
logic in a backend service that could be used by a frontend service.


First, we define our goals and expectations. The actual prediction
function will then be outsourced to its own file. Then, we cover the
actual implementation of the REST API. Finally, we’ll test that
everything works as expected.


**Development Goals**


We’ll develop a REST API with an endpoint named `predict` . The
payload is a `prompt` and `number_of_turns` . A sample input is shown in
Listing 8.1.

```
{
"prompt": "the earth is flat",
"number_of_turns": 1
}

```

**Listing 8.1** Payload to Be Sent to the Endpoint


The payload is passed to the endpoint then processed by the API,
and an API response returned, as shown, for example, in Listing 8.2.

```
[
{
"content": "the earth is flat",
"role": "assistant",
"name": "user"
},
{
"content": "The earth is round.",
"role": "user",
"name": "ai"
}
]

```

**Listing 8.2** API Response


The result is a list of dictionaries. The dictionary entries correspond
to agent responses.


Now, let’s develop a REST API for use as a backend server. In a
real-life scenario, the backend server would interact with the frontend
server, but we just want to illustrate how this works in a small
example.


Now that we have an idea of the result, we’ll start building it out. The
REST API will provide an endpoint for getting predictions. A good
practice is to bundle logic into separate functions. To follow this
design pattern, we start by developing the prediction function.


**Prediction Function**


The prediction function relies on `autogen` . As shown in Listing 8.3, the
function consumes a `user_prompt`, and a `number_of_turns` . The

`user_prompt` sets the topic of the debate between the agents. The

`number_of_turns` defines how many times the agents interact with
each other.

```
#%% packages
import os
from dotenv import load_dotenv, find_dotenv
from autogen import ConversableAgent

#%% load the environment variables
load_dotenv(find_dotenv(usecwd=True))

#%% define the function to predict
def predict_conversation(user_prompt: str, number_of_turns: int):
llm_config = {"config_list": [
{"model": "gpt-4o-mini",
"temperature": 0.9,
"api_key": os.environ.get("OPENAI_API_KEY")}]}
person_a = ConversableAgent(
name="user",
system_message=f"""
You are a person who believes that {user_prompt}.
You try to convince others of this.
You answer in a friendly way.

```

```
Answer very short and concise.
""",
llm_config=llm_config,
human_input_mode="NEVER",
)

# set up the agent: Alice, the scientist
person_b = ConversableAgent(
name="ai",
system_message="""
You are a person who believes the opposite of {user_prompt}.
You answer in a {style_b} way.
Answer very short and concise.
""",
llm_config=llm_config,
human_input_mode="NEVER",
)

# start the conversation
result = person_a.initiate_chat(
recipient=person_b,
message=user_prompt,
max_turns=number_of_turns)

messages = result.chat_history
return messages

```

**Listing 8.3** Prediction Function (Source: 08_Deployment\rest_api\pred_conv.py)


The function basically wraps the logic we defined in the file
_07_AgenticSystems\ag2\20_ag2_conversation.py_ . Finally, the
function returns the `chat_history` .


We can now move on to defining the REST API.


**REST API Function**


The prediction logic from the previous section is now used in the
REST API ( _08_Deployment\rest_api\main.py_ ). Several frameworks
for setting up a REST API are available: _FastAPI_ and _Flask_ are the
two most popular frameworks for building REST APIs in Python.
Each framework has distinct strengths.


Flask is known for its simplicity and flexibility. This lightweight
framework offers developers full control over the design and
implementation of REST APIs. Thus, Flask is well suited for small
and medium-sized projects and also offers a rich ecosystem of
extensions.


FastAPI is a more modern framework that leverages features like
type hints to enable automatic validation as well as interactive API
documentation (via OpenAPI or Swagger UI). FastAPI excels in
performance and developer productivity, making it ideal for projects
where speed and scalability are critical.


While Flask provides more freedom, FastAPI often requires less
boilerplate and offers built-in features that make developing an API
more simple.


Listing 8.4 shows the packages for our REST API script.

```
#%% packages
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from pred_conv import predict_conversation

```

**Listing 8.4** REST API Packages (Source: 08_Deployment\rest_api\main.py)


The main addition is the `fastapi` package to provide the REST API
functionality. Whenever we worked with structured outputs, we used
the `pydantic` package. But now, there’s a twist: In the context of
REST APIs, we need `pydantic` for structured input.


We need to import our `predict_conversation` function from earlier.
Also, we’ll need `uvicorn`, which is an asynchronous server gateway
interface (ASGI) server for Python web applications. While Uvicorn
might sound complicated, ultimately, it enables our backend to serve
multiple requests concurrently.


Let’s move on to setting up the API, as shown in Listing 8.5.

```
#%% create the app
app = FastAPI()

#%% create a pydantic model
class Prompt( BaseModel ):
prompt: str
number_of_turns: int

#%% define the endpoint "predict"
@app.post("/predict")
def predict_endpoint( parameters : Prompt):
prompt = parameters.prompt
turns = parameters.number_of_turns
print(prompt)
print(turns)
result = predict_conversation( user_prompt =prompt,
             number_of_turns =turns)
return result

```

**Listing 8.5** REST API Endpoint (Source: 08_Deployment\rest_api\main.py)


First, we’ll create an instance of FastAPI. This `app` object is the entry
point to the API. The pydantic model `Prompt` defines the input
parameters and their types. In this case, we’ll use `prompt` and

`number_of_turns` . Both will be passed as strings.


Listing 8.6 shows how to start the server.

```
# %% run the server
if __name__ == '__main__':
uvicorn.run("main:app", reload =True)

```

**Listing 8.6** REST API Server Running (Source: 08_Deployment\rest_api\main.py)


The line `if __name__ == '__main__'` is a common Python construct to
ensure that certain code is only executed when the script is run
directly. This code is not run when the script is imported as a module
in another script. In this case, we want to run it directly from the
command line.


The code inside the if block is boilerplate code that tells Uvicorn to
run the FastAPI instance `app` from the file _main.py_ . The parameter

`reload=True` ensures that the server is restarted each time the file is
saved.


To start the API service, navigate to the folder for the file and run the
following command:

```
python main.py

```

You’ll see the result shown in Listing 8.7.

```
INFO:   Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:   Started reloader process [8884] using WatchFiles
INFO:   Started server process [39108]
INFO:   Waiting for application startup.
INFO:   Application startup complete.

```

**Listing 8.7** REST API Server Startup Output (Source: 08_Deployment\rest_api\main.py)


Amazing! The REST API is up and running on the local system; the
IP address 127.0.0.1 points to your local computer. The API is
waiting for requests on port 8000.


Now imagine a whole system in this way: Our service operates from
a certain building (indicated by its IP address). In this building,
multiple companies might operate. So, to address packages
correctly, you need the specific apartment number (the port).


The application startup is complete. Our service waits for a user to
send inputs to it. We’ll test it.


**Testing an API**


While different frameworks for testing APIs are available, we
recommend Postman, which is a standalone program that you need
to install on your system. You can use Postman for free by


downloading it from the developer at
_[https://www.postman.com/downloads/](https://www.postman.com/downloads/)_ .


Once you start Postman, you can create collections of requests.
When you set up a request, you must define its type. Since we are
sending data to our endpoint, the type of request is a `POST` request.
As the address, you must define the complete URL, consisting of the
IP address, the port, and the API endpoint. In our case, the address
is _http://127.0.0.1:8000/predict_ .


Figure 8.4 shows the Postman interface with the parameters that
we’ve passed and the API response.


At the top, the type ( `POST` ) and URL are defined; then the input
parameters are shown. These parameters are for the API defined in
the body, as a JSON object with the parameters `prompt` and

`number_of_turns` are defined.


**Figure 8.4** Postman: Interaction with API Endpoint “predict”


After clicking **Send**, the request is sent to the API. The response
from the API is shown at the bottom of the screen. An HTTP
response of **200** means that the request was handled successfully.
We can also check the output from the API, which is a list with the
chat history.


Now, you know how to develop and deploy a REST API locally. We
did not cover how to deploy a backend service to the internet. But
that approach would be similar to the deployment of a self-contained
application, which you’ll learn about in the next section where we
develop a self-contained application that we can deploy. We’ll extend
the same interaction between two agents and embed this logic into a
standalone application.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **8.3  Self-Contained App Development**

Before we can deploy anything, we need an app that we want to
share with the world. We’ll develop an app that is based on an
agentic system consisting of two agents. These two agents work
autonomously and discuss a controversial topic. The next question is
which framework to choose for developing the web application. For
quick prototyping, we usually use Streamlit. But first, let’s look at of
some other frameworks as well:


Streamlit is a lightweight framework for quick prototyping. With
built-in widgets like sliders, buttons, and charts, Streamlit is ideal
for data scientists to quickly develop POCs.


Gradio focuses on machine learning models. It also allows userfriendly web interfaces with minimal effort.


Dash is built on top of Flask and React. It is designed to create
analytical web applications with interactive widgets.


Panel is another framework for creating dashboards and web
applications.


We’ll build our examples in Streamlit. This open-source Python
library for creating interactive web applications is simple to set up,
and detailed web development knowledge is not needed. You can
create a web application with Python and don’t need any specific
knowledge of HTML, CSS, or JavaScript.


This simplicity makes it ideal for data scientists to create AI demos
and dashboards quickly. Streamlit integrates seamlessly with other
Python libraries. Since everything is in Python, you don’t need
separate frontend/backend architectures. Instead, interactivity can


be achieved with minimal effort. Many widgets are already
developed and can be implemented with a single line of code. The
same holds for charts, images, or tables—everything can be
integrated with minimal effort.


Due to all these reasons, Streamlit is perfect for fast prototyping. You
can develop and quickly deploy a working app without worrying
about web frameworks or specific frontend or design knowledge.
Some disadvantages should not be concealed: Streamlit is not
designed for high performance. Heavy traffic or real-time
applications should not be developed with Streamlit. Also not ideal
for complex applications with multiple web pages, complex
workflows can become cumbersome to implement and maintain.


Another notable limitation of Streamlit is its lack of state
management, especially when building more complex apps.
Streamlit apps are inherently stateless, meaning that every
interaction like a button click or a slider change reruns the entire
script from top to bottom. Since the script reruns, computations that
don’t need to be repeated might be executed unnecessarily, which
results in additional loads on the server.


We’ll develop a simple Streamlit app and deploy it to Streamlit.
Figure 8.5 shows the resulting web app we’ll have at the end of this
section. A web server will be created on the fly, which allows us to
visit the page.


Our app has a main input field at the bottom of the page, where a
user can enter a topic to debate about. Some other settings can be
adapted. Among these settings is the number of turns between the
two agents and the style of the two agents, in this example, called
person A and person B.


Let’s now develop an app to deploy to different providers later. Our
app is based on Streamlit. To use Streamlit, you only need to install it
with the following command:

```
uv add streamlit

```

**Figure 8.5** Streamlit App: Frontend


The backend logic is based mainly on a script we developed in our
discussion of AG2 in Chapter 7
( _07_AgenticSystems\ag2\20_ag2_conversation.py_ ).


If you’re familiar with Streamlit, take this opportunity and try to
develop the app on your own. If not, don’t worry, we’ll develop the
code together. The final script can be found in
_08_Deployment\self_contained_app.py_ .


First, load relevant packages using the code shown in Listing 8.8.


```
#%% packages
from autogen import ConversableAgent
from dotenv import load_dotenv, find_dotenv
import os
#%% load the environment variables
load_dotenv(find_dotenv( usecwd =True))
import streamlit as st

```

**Listing 8.8** Streamlit App “Controversial Debate”: Packages (Source:
08_Deployment\self_contained_app.py)


We’ll use AG2 and `ConversableAgent` for setting up the two agents
that will debate. Streamlit is imported with its usual alias `st`, which
will save us time later.


The agents will need, during their instantiation, configuration details
on the LLM, the temperature, and the API key. All of this is
communicated through an object called `llm_config`, shown in
Listing 8.9, that we’ll later pass to the agents.

```
#%% LLM config
llm_config = {"config_list": [
{"model": "gpt-4o-mini",
"temperature": 0.9,
"api_key": os.environ.get("OPENAI_API_KEY")}]}

```

**Listing 8.9** Streamlit App “Controversial Debate”: LLM Config (Source: 08_Deployment\
self_contained_app.py)


OK, time to create our first widget with Streamlit, as shown in
Listing 8.10. A widget is a predefined functionality for creating inputs
or outputs that follow a common design pattern and provide good
functionality with minimal code.

```
st.title("Controversial Debate")

prompt = st.chat_input("Enter a topic to debate about:")
if prompt:
st.header( f "Topic: {prompt}")

```

**Listing 8.10** Streamlit App “Controversial Debate”: User Prompt (Source:
08_Deployment\self_contained_app.py)


For creating the title of our app, we can call `st.title` . The topic to
debate about is passed on in a chat input field that is displayed at
the bottom of the page. A predefined widget called `st.chat_input` for
this input field.


Listing 8.11 shows the settings area that can be hidden or expanded.

```
with st.expander("Conversation Settings"):
number_of_turns = st.slider("Number of turns", min_value =1, max_value =10,
value =1)

col1, col2 = st.columns(2)
with col1:
st.subheader("Style of Person A")
style_a = st.radio(
"Choose style for first speaker:",
["Friendly", "Neutral", "Unfriendly"],
       key ="style_a"
)

with col2:
st.subheader("Style of Person B")
style_b = st.radio(
"Choose style for second speaker:",
["Friendly", "Neutral", "Unfriendly"],
       key ="style_b"
)

```

**Listing 8.11** Streamlit App “Controversial Debate”: Settings (Source: 08_Deployment\
self_contained_app.py)


In the settings, the behavior of the two agents is defined. Since we
want clear visual separation between the two agents, we’ll use

`st.columns` to create two columns. The style is limited to “friendly,”
“neutral,” and “unfriendly.” The user can select the style from a radio
button, created with `st.radio` .


Now, we want to process these inputs. Listing 8.12 shows the setup
of the agents.

```
if prompt:
#%% set up the agent: Jack, the flat earther
person_a = ConversableAgent(
     name ="user",

```

```
     system_message = f """
You are a person who believes that {prompt}.
You try to convince others of this.
You answer in a {style_a} way.
Answer very short and concise.
""",
     llm_config =llm_config,
     human_input_mode ="NEVER",
)

#%% set up the agent: Alice, the scientist
person_b = ConversableAgent(
     name ="ai",
     system_message ="""
You are a person who believes the opposite of {prompt}.
You answer in a {style_b} way.
Answer very short and concise.
""",
     llm_config =llm_config,
     human_input_mode ="NEVER",
)
# %% start the conversation
result = person_a.initiate_chat(
     recipient =person_b,
     message =prompt,
     max_turns =number_of_turns)

```

**Listing 8.12** Streamlit App “Controversial Debate”: Agent Setup (Source:
08_Deployment\self_contained_app.py)


As soon as a `prompt` is available, the two agents are instantiated with

`ConversableAgent` . In its definition, we pass information on their
position on the debate topic, as well as the style, which the user can
adapt. The names of the agents are set to `"user"` and `"ai"` for a
reason. Later, when we render the messages to the screen,
Streamlit already has some predefined behaviors if some default
names like these are used.


After the agents have been created, person A starts the conversation
and reaches out to person B. The chat is stored in an object called

`result` .


The snippet shown in Listing 8.13 illustrates how the chat discussion
is rendered to the screen in a visually appealing way.


```
messages = result.chat_history
for message in messages:
name = message["name"]
if name == "user":
with st.container():
col1, col2 = st.columns([3, 7])
with col2:
with st.chat_message( name =name):
st.write(message["content"])
else:
with st.container():
col1, col2 = st.columns([7, 3])
with col1:
with st.chat_message( name =name):
st.write(message["content"])

```

**Listing 8.13** Streamlit App “Controversial Debate”: Chat Messages (Source:
08_Deployment\self_contained_app.py)


The `messages` are extracted from the `chat_history` . Then, each
message is processed in a loop. The `name` of the message owner is
extracted, and depending on the message owner, the `chat_message`
is shown either on the left or on the right.


That’s it! We’ve created a nice frontend for our agent conversation.
Let’s check how this looks, and if everything works, by running the
app.


To run the app locally, in the terminal, change into the folder of the
script and run the following command:

```
streamlit run self_contained_app.py

You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.179.16:8501

```

This command will start a webserver and open the URL in your
default browser. You should see the web app (shown earlier in
Figure 8.5) after visiting the URL. Play with the app and provide
different controversial topics for the agents to discuss.


At this point, we’ve developed a self-contained web application that
we can now deploy, which we’ll do in the coming sections.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **8.4  Deployment to Heroku**

Heroku is a popular service that simplifies the deployment and
management of AI applications. Known for its developer-friendly
interface, Heroku also has a simple integration with Git. Heroku
enables developers to deploy with minimal operational overhead.
The idea is that you provide the code, and the service takes care of
the infrastructure complexities like server setup and scaling, thus
allowing you to focus on developing applications.


One of the supported languages in Python, so we are ready to start.
As the first step, you need to create an account on
_[https://signup.heroku.com/](https://signup.heroku.com/)_ .


Every app costs something to run, even if just a few cents, so you
must add payment details. Only then can you proceed with creating
a new app.


We’ll start by creating a new app in Section 8.4.1. Our development
is performed locally, so we need to download and configure a
command line interface (CLI), which we’ll do in Section 8.4.2. The
deployment process includes several steps in which we create an
app.py script (Section 8.4.3), perform a profile setup (Section 8.4.4),
define environment variables (Section 8.4.5), and handle the Python
environment (Section 8.4.6). At that point, we can check the
deployment locally (Section 8.4.7). Once everything is checked and
working, we can deploy the app to Heroku, as described in
Section 8.4.8. As a cleanup step, in Section 8.4.9, you’ll learn how to
stop your application.


### **8.4.1  Create a New App**

Figure 8.6 shows the options for creating a new app in the frontend.


**Figure 8.6** Heroku: Create New App


You must maintain the **App name** field and the **Location** field.
Select either **United States** or **Europe** and click **Create app** .

### **8.4.2  Download and Configure CLI**


You must also install a CLI on your system For this step, navigate to
_https://devcenter.heroku.com/articles/getting-started-with-_
_python#set-up_ . Several CLI options are available for the platform you
need.


In the terminal, now, log on to Heroku, as shown in Listing 8.14.

```
heroku login

```

```
Opening browser to https://cli-auth.heroku.com/auth/cli/browser/887491ec-989c-46aebf33-4387e4e75813?
requestor=SFMyNTY.g2gDbQAAAA0xMzAuMTc2Ljg4LjczbgYAcAKMFpQBYgABUYA.zh1whD4bP42ivN8_u7
HZd6d1c3Y60QHVb6Yq1XyMsFI
Logging in... done
Logged in as info@gollnickdata.de

```

**Listing 8.14** Heroku Login Output


A browser window opens, and you’ll click a button to log on. In the
terminal, you must link to the remote repository, as follows:

```
heroku git:remote -a controversial-debate

```

Now, you’re linked to the remote repository and can proceed by
creating the required files.

### **8.4.3  Create app.py File**


The first file is our actual application file, which we’ll call _app.py_ . This
file will be linked in other configuration files. Listing 8.15 shows the
complete application file.

```
#%% packages
import os
from autogen import ConversableAgent
import streamlit as st
def main():
# LLM config
llm_config = {"config_list": [
{"model": "gpt-4o-mini",
"temperature": 0.9,
"api_key": os.environ.get("OPENAI_API_KEY")}]}

st.title("Controversial Debate")

prompt = st.chat_input("Enter a topic to debate about:")
if prompt:
st.header(f"Topic: {prompt}")

with st.expander("Conversation Settings"):
number_of_turns = st.slider("Number of turns", min_value=1, max_value=10,
value=1)

col1, col2 = st.columns(2)

```

```
with col1:
st.subheader("Style of Person A")
style_a = st.radio(
"Choose style for first speaker:",
["Friendly", "Neutral", "Unfriendly"],
key="style_a")

with col2:
st.subheader("Style of Person B")
style_b = st.radio(
"Choose style for second speaker:",
["Friendly", "Neutral", "Unfriendly"],
key="style_b")
if prompt:
#%% set up the agent: Jack, the flat earther
person_a = ConversableAgent(
name="user",
system_message=f"""
You are a person who believes that {prompt}.
You try to convince others of this.
You answer in a {style_a} way.
Answer very short and concise.
""",
llm_config=llm_config,
human_input_mode="NEVER")

#%% set up the agent: Alice, the scientist
person_b = ConversableAgent(
name="ai",
system_message="""
You are a person who believes the opposite of {prompt}.
You answer in a {style_b} way.
Answer very short and concise.
""",
llm_config=llm_config,
human_input_mode="NEVER",
)

# %% start the conversation
result = person_a.initiate_chat(
recipient=person_b,
message=prompt,
max_turns=number_of_turns)

messages = result.chat_history
for message in messages:
name = message["name"]
if name == "user":
with st.container():
col1, col2 = st.columns([3, 7])
with col2:
with st.chat_message(name=name):
st.write(message["content"])

```

```
else:
with st.container():
col1, col2 = st.columns([7, 3])
with col1:
with st.chat_message(name=name):
st.write(message["content"])

if __name__ == "__main__":
main()

```

**Listing 8.15** Heroku App File (Source: 08_Deployment\heroku_app\app.py)


A few minor changes were made to
_08_Deployment\self_contained_app.py_ . The most significant change
is that now a `main()` function contains the app logic. This function is
called when the file is run.


We can proceed by setting up some configuration files that tell
Heroku what to load and how.

### **8.4.4  Procfile Setup**


We need to set up a _procfile (process file)_, which is a special file
used in web applications, particularly with platforms like Heroku, to
specify the commands that should be executed to start our
application.


The details on how Heroku should handle the app are defined in the
_Procfile_ with the following content:

```
web: streamlit run app.py --server.port=$PORT --server.headless=true

```

For testing, create a file with the identical content called
_Procfile.windows_ (assuming you work on Windows). That step is not
necessary if you work on Linux or MacOS.


### **8.4.5  Environment Variables**

Our app relies on OpenAI, so we need to provide an API key. In the
terminal, we can define the environment variables with `heroku`

`config:set` followed by a mapping of key name and its value:

```
heroku config:set OPENAI_API_KEY=…

```

Check the variable settings by using the following command:

```
heroku config

=== controversial-debate Config Vars

OPENAI_API_KEY: sk-proj-…

### **8.4.6  Python Environment**

```

The app requires its own Python environment with all the required
packages. We’ll set up the required packages in a _requirements.txt_
and then create an environment based on it, as follows:


1. **Create a requirements.txt file**

Set up a file called _requirements.txt_ with the following contents:

```
  streamlit

  autogen

```

You might even specify package versions.


2. **Setting up the environment**

The environment is called `.venv` and can be created with the
following command:

```
  python -m venv .venv

```

After creation, you must activate the environment by changing
into the scripts folder and calling `activate` .


3. **Install the packages**

You need to install the packages in this new environment via

`pip` :

```
  pip install -r requirements.txt

### **8.4.7  Check the Result Locally**

```

Before we deploy to a remote server, you should check the setup
locally. For this task, call `heroku local` in combination with the

`Procfile.windows`, as shown in Listing 8.16. If you work on Mac or
Linux, use the procfile.

```
heroku local --port 5006 -f Procfile.windows

09:36:39 web.1  |  You can now view your Streamlit app in your browser.
09:36:39 web.1  |  Local URL: http://localhost:5006
09:36:39 web.1  |  Network URL: http://192.168.179.147:5006
09:36:39 web.1  |  External URL: http://79.192.50.59:5006

```

**Listing 8.16** Heroku Local Server Startup


This command will spin up a web server. The output will display the
local URL to which you must navigate to check the result. If we head
over to _http://localhost:5006_, we’ll see the running app.


Amazing! One final step remains: We need to deploy to the web via
Heroku and check the result there.

### **8.4.8  Deployment to Heroku**


In Visual Studio Code (VS Code), the default branch is called `main` [[ 1 ]] .
We must stage the files with the command `git add`, as follows:

```
git add .

```

Now, we can commit the files with a commit message, as follows:


```
git commit -m "first commit"

```

Finally, we can push these changes to Heroku with `git push`, as
shown in Listing 8.17.

```
git push heroku main

remote: Building source:
remote:
remote: -----> Building on the Heroku-24 stack
remote: -----> Using buildpack: heroku/python
…
remote: -----> Compressing...
remote:    Done: 136.2M
remote: -----> Launching...
remote:    Released v5
remote:    https://controversial-debate-2b07aaccb7d3.herokuapp.com/ deployed to
Heroku
remote:
remote: Verifying deploy... done.
To https://git.heroku.com/controversial-debate.git
* [new branch]   main -> main

```

**Listing 8.17** Heroku App Deployment


The CLI informs you of the place where the app is deployed. Head
over to that URL to check the result. In our case, our URL is
_https://controversial-debate-2b07aaccb7d3.herokuapp.com/_ . (Don’t
try to use this link; we’ve already stopped the service.) Head over to
your own URL to see the result in your browser. Figure 8.7 shows
the result of the app we deployed locally.


With a topic like “the earth is flat,” the two agents start their
discussion.


Before we move on, we recommend deleting your app if you just
wanted to test it. Alternatively, you can simply stop it to avoid costs.


**Figure 8.7** Heroku Deployed App

### **8.4.9  Stop Your App**


You can determine how much your app costs under the **Resources**
tab in the web frontend, in our case,
_[https://dashboard.heroku.com/apps/controversial-debate/resources](https://dashboard.heroku.com/apps/controversial-debate/resources)_ .


Figure 8.8 shows our app costs about $0.01 per hour, roughly $7.00
per month.


**Figure 8.8** Heroku App State and Estimated Cost


Click the **Edit** button next to the hourly cost to deactivate the app.
Figure 8.9 now shows no hourly cost, and the estimated total cost is
$0.00.


**Figure 8.9** Heroku App State Stopped


To verify that the app has stopped, you can navigate to the app URL.
The app should not load any more. Thus concludes our first
deployment via Heroku. We hope you’ve seen how easy it is to
deploy an app.


Next, we’ll move on another service provider: Streamlit.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **8.5  Deployment to Streamlit**

We’ll use the app we developed previously and focus now only on
the deployment steps, which are just a few in number:


1. Creating a GitHub repository


2. Creating a new app at _[https://streamlit.io/](https://streamlit.io/)_

### **8.5.1  GitHub Repository**


Let’s start with the creation of a GitHub repository. With Heroku, the
service has automatically set up a Git repository. However, with
Streamlit, we need to take care of managing GitHub ourselves.


Managing GitHub is outside the scope of this book, so we’ll only
roughly sketch out the steps you need to take. If you’re not familiar
with GitHub and Git repositories, we highly recommend learning this
skillset, which is essential to nearly every workflow in real-life
projects. One good resource is _Git: Project Management for_
_Developers and DevOps Teams_ ( _https://www.sap-_
_press.com/git_5555/_ ).


First, create a repository at _[https://github.com/](https://github.com/)_ . Once you have
created the empty repository, you must clone it locally via `git clone` .


The following files must be part of the repository:


_app.py_


_requirements.txt_


After you have copied the files into that folder, you must `commit` and

`push` the changes back to the GitHub repository. Navigate to your


GitHub repository, as shown in Figure 8.10.


**Figure 8.10** GitHub Repository for Deployment to Streamlit


Now, you should have an _app.py_ and a _requirements.txt_ . The
_.devcontainer_ folder will be later automatically created by the service.

### **8.5.2  Creating a New App**


First, navigate to _[https://streamlit.io/](https://streamlit.io/)_ and create an account. Once
you have an account, you can deploy apps by clicking **Create app** in
the top-right corner. On the next screen, shown in Figure 8.11, select
the source of your app.


**Figure 8.11** Streamlit: Source of Your App


We’ll use the first option: **Deploy a public app from GitHub** .
Although called a public app, you do have some options to limit the


app to specific users afterwards. Figure 8.12 shows the parameters
you must define to deploy an app.


**Figure 8.12** Streamlit: Deploy an App


First and foremost, you must pass the **GitHub URL** . Bear in mind
that you don’t pass the URL of the GitHub repository but instead the
URL of the _app.py_ file in the GitHub repository. Also, you must define
an **App URL** . This URL is where your app can be found. For now,
simply make sure that the domain is available.


We cannot skip over the advanced settings because our app relies
on an API key. Since our agents use an OpenAI model, click on
**Advanced settings** to set the key. Figure 8.13 shows how to
provide the secret.


**Figure 8.13** Streamlit: Advanced Settings


In the **Secrets** section, we must pass our API key. Copy the key from
your _.env_ file. Importantly, at this point, the key is passed in quotation
marks, so you should wrap your key like this: `“my_secret_key”` . Click
**Save** .


Back on the **Deploy an app** screen, confirm your settings by clicking
on the **Deploy** button. This step starts the deployment process and
then starts the app. The app is then live at an address following the
convention _https://<yourappname>.streamlit.app/_ .


Congratulations! You’ve successfully deployed your first app with
Streamlit!


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **8.6  Deployment with Render**

Render is another easy-to-use deployment service. We’ll use its free
tier for our sample deployment. The steps are like other frameworks.
First, create an account at _[https://render.com/](https://render.com/)_ . Then, start the
deployment process by selecting **Deploy a Web Service**, as shown
in Figure 8.14.


**Figure 8.14** Render: Select a Service


You must link the deployment service to your GitHub repository. For
this step, navigate to your own GitHub repository and copy the URL
into the clipboard. Then, paste this URL into the Render deployment,
as shown in Figure 8.15.


**Figure 8.15** Render: Connect to a GitHub Repository


Further parameters can be specified on the Render configuration
page, but for our simple case, we can stick to the defaults.
Parameters you might want to change include the following:


**Region** : You might select a region close to your users.


**Root directory** : The default is the root folder of the repository.


**Build command** : Since we’re working with a _requirements.txt_, we
can stick to the default installation command `pip install -r`

`requirements.txt` .


You must define a start command in the following way:

```
streamlit run app.py --server.port $PORT --server.headless true

```

Figure 8.16 shows the instance type, which defines the capabilities
and costs of your project.


**Figure 8.16** Render: Select an Instance Type


For a small test as in our case, we recommend selecting the **Free**
instance. This instance spins down after periods of inactivity, which is
fine for us for now.


The last step is shown in Figure 8.17, which illustrates how to specify
environment variables.


**Figure 8.17** Render: Environmental Variables


The API key setup is straightforward. Simply define the name and
the corresponding key as already defined in the _.env_ file.


That’s everything, and we can start the deployment process by
clicking **Deploy app** . In the subsequent dashboard, you can watch
the deployment process in real time, including the installation
process for all the packages.


After a few minutes, your app is live at a URL that follows the
convention _https://<your-app-name>.onrender.com_ .


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **8.7  Summary**

In this chapter, we explored several critical concepts and practical
techniques for deploying applications, focusing on the contrasting
strategies of self-contained applications and the more modular
frontend/backend architecture.


Our journey began with distinguishing among self-contained
applications: one kind that combined the frontend and backend logic
and one kind in which frontend and backend architectures are
separated.


We had a brief introduction to REST APIs, an essential tool for
building scalable, interoperable systems. You learned how REST
APIs enable seamless communication between various components
of an application, making them a cornerstone of modern app
development.


We then delved into the development of a self-contained application,
which provided a clear, practical example of how such apps
encapsulate all necessary functionality within a single package. This
approach highlighted the benefits of simplicity, ease of deployment,
and straightforward maintenance, making self-contained apps an
excellent choice for certain use cases.


For the deployment phase, we demonstrated how to bring
applications to life in real-world environments. Starting with Heroku,
we explored its developer-friendly features, including quick setup
and powerful tools for managing applications in production.


Next, we moved to Streamlit, a platform tailored for deploying
interactive data applications. We experienced its ease of use and


ability to rapidly turn Python scripts into shareable web apps.


Finally, we deployed our application to Render, showcasing its
flexibility and cost-effectiveness for a range of deployment scenarios.


Each deployment platform introduced unique challenges and
advantages, providing insights into when and why you might choose
one over another.


Through these examples, we discussed the following topics:


REST API integration: How to design and use REST APIs to
enable effective communication between app components and
external services.


Self-contained apps: The strengths and limitations of this
approach, particularly in scenarios where simplicity and portability
are key.


Platform-specific deployment: Analyzing and adapting to the
specific requirements and strengths of Heroku, Streamlit, and
Render.


By the end of this chapter, you should have a comprehensive
understanding of the tools, techniques, and decision-making
processes involved in deploying applications. Whether you’re
working on a standalone project or a complex, distributed system,
these skills form a solid foundation to effectively bring your
applications from development to production.


_[OceanofPDF.com](https://oceanofpdf.com/)_


# 9  Outlook

_The future is not set. There is no fate but what we make for_
_ourselves._
_—Sarah Connor in the movie Terminator 2: Judgment Day_


Admittedly, quoting a movie about an AI trying to wipe out humanity
might set the wrong mood. But it is just a great movie, and although
over 30 years old, it reflects fears that many people have when
considering the future of AI.


In this chapter, we’ll provide an outlook on what AI, especially
generative artificial intelligence (generative AI), might provide in the
future.


The field of generative AI is still quite new and is evolving extremely
quickly. We’ll discuss what can be expected of future developments,
but also which limitations and issues persist and need to be
overcome. We’ll briefly talk about regulatory developments before
we examine the potential of reaching artificial general intelligence
(AGI) and artificial superintelligence (ASI). We’ll conclude this
chapter with a section on useful resources that can help you to keep
up to date.


## **9.1  Advances in Model Architecture**

Besides improvements in hardware, data, and model sizes, the
model architecture will have to get better to tackle complex tasks in
coding, mathematics, and general intelligence. Leopold
Aschenbrenner wrote a brilliant paper called “Situational Awareness:
The Decade Ahead” ( _[https://situational-awareness.ai/](https://situational-awareness.ai/)_ ). We agree
with many of his predictions.


The measure of progress is called _OOMs (orders of magnitude)_ . The
reason for this measure is that, as we have already seen, many
aspects of progress are exponential in nature, so that OOMs relate
to a logarithmic scale. OOMs are shown over time.


Algorithmic progress is further broken down into _unhobbling_ and
_efficiencies_ . “Unhobbling” refers to removing self-imposed or
systematic constraints that limit a model’s effectiveness or potential.
“Efficiencies” can be mean several things: there are efficiencies in
inference and in training. For example, Aschenbrenner mentions
improvements in sample efficiency that could allow algorithmic
improvements that enable models to learn from more limited (less)
data.


At the time of writing, OpenAI’s most recent model o3 was published.
This model is the successor to its o1 “reasoning” model. With o3,
OpenAI was supposed to be capable of reaching AGI under certain
conditions.


With increased reasoning capabilities like _private chain-of-thought_
_(CoT)_, an AGI can self-fact-check, which allows the model to plan
ahead and improve its own reasoning. This capability results in
increased inference times, but significant improvements can be
enjoyed in terms of accuracy in complex tasks.


Besides classic model training, reinforcement learning was applied
to induce thinking before actually creating answers.


Who knows? Maybe, we’ll even see more fundamental changes in
the underlying transformer architecture at some point.


For the time being, still limitations and issues exist, which we’ll dive
into next.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **9.2  Limitations and Issues of LLMs**

Still many possible issues exist in the context of large language
models (LLMs). We’ll touch on the most relevant ones in this section:
hallucinations, biases, misinformation, intellectual property,
transparency, and jailbreaking.

### **9.2.1  Hallucinations**


LLMs always produce an output if you don’t actively constrain them.
Thus, they’ll even provide outputs if they don’t have the answer in
their model weights. In the early days, this problem led to
unsatisfactory results because the answers were factually incorrect.
In some cases, the output was disconnected from the user query; it
might be nonsensical or conflict with previous outputs in the same
discussion.


Much effort was made to improve model performance, so that
hallucinations have become less frequent. Researchers developed a
metric called _context adherence_ that measures factual accuracy and
cases in which the model provided outputs that were not provided in
the context ( _closed-domain hallucinations_ ).


Many models have a context adherence score of close to 1. For
example, Claude-3.5 Sonnet ranked best closed source model with a
score of 0.97. The same result was achieved by Llama-3.1 405B
Instruct as best open-source model, with the same score of 0.97.


For medium-length contexts, which researchers defined as between
5,000 and 25,000 tokens, the best models like Google Gemini-1.5

Flash achieved a score of 1.0, meaning no hallucinations were
found.

### **9.2.2  Biases**


Biases might be introduced at different steps of a training pipeline.
Figure 9.1 shows the different steps of the training pipeline, in which
biases might be introduced.


**Figure 9.1** Bias Introduction into LLM Training


It all starts with the data used for training. What follows is the
modeling step and finally the human review. All steps are highlighted
in the following sections.


**Data**


A model can only be as good as the data it was trained on. If the
model is based on data that is found in the real world, the same bias
most likely will be inherent to the model. Such historical biases can
be found for groups that have been historically discriminated against.
For example, gender-based stereotypes might be reflected by the
model due to its training data.


A similar problem might occur when the developers try to
counterweigh historical biases. Google got massive headwind in
early 2024, when it released its image creation feature in Google
Gemini.


Biases can also be introduced on purpose to follow a political
agenda. Figure 9.2 shows model outputs on Taiwan independence—
one coming from a model created by a US company (Llama-3.2-3BInstruct 1) and one coming from a Chinese company (Qwen2.51.5B-Instruct 2).


### 1


### 2



**Figure 9.2** Biases Based on Political Agenda


Not surprisingly, the two models provide completely different
answers. We can thus conclude that LLMs are not independent and
won’t be in the future. LLMs are not independent tools. Keep this in
mind when working with LLMs.


**Modeling**


Biases can also be introduced at the modeling step of the training
pipeline. The training progress is evaluated during the training. This
evaluation is performed based on benchmarks, which where a bias
could be introduced. It also might be that the benchmark is not
representative of the general distribution.


This issue is typical in ML model training. Your model might work well
on training data but not generalize well on unseen real-world data.


Another type of bias in this step is an aggregation bias, in which
distinct populations are incorrectly combined. For example, if the
loss function disproportionately penalizes incorrect grammar over
content misinterpretation, the model will be biased toward correcting
grammatical errors more rigorously than factual ones.


**Human Review**


The final step of the training is human feedback. This step is being
taken to further improve the model. The technical term is
_reinforcement learning from human feedback (RLHF)_ . This technique
involves human feedback to fine-tune models so that their outputs
align better with human preferences or expectations.


A bias in RLHF might lie in the group setup of the humans who
provide feedback. Ideally, they should provide a good representation
of the broader population for which the model is developed.


Scientists have found out that human reviewers prefer longer model
outputs, even when the output objectively did not change. Pure
response length increase is seen as model improvement, rather than
other features.

### **9.2.3  Misinformation**


Misinformation is a risk associated with LLMs because LLMs often
generate plausible but factually wrong content (see our earlier
discussion on hallucinations in Section 9.2.1). Sure, misinformation
was possible before the rise of LLMs. What has changed is that false
or misleading information no longer requires human effort, allowing


bad actors (who might be persons, corporations, or state-level
actors) to automate their disinformation campaigns.


The barrier has been lowered to creating fake news, conspiracy
theories, or biased narratives, making it harder to distinguish credible
information from fabricated content. The speed and costeffectiveness of content generation with LLMs could overwhelm factchecking mechanisms and contribute to the erosion of public trust in
media and information sources, amplifying the societal impact of
misinformation.


A special case in this context is hate speech. LLMs can create
harmful or offensive language with the aim of targeting individuals or
groups based on race, gender, religion, or other characteristics. The
scalability of this process makes it extremely simple to flood online
platforms and forums with harmful rhetoric.

### **9.2.4  Intellectual Property**


On intellectual property, issues arise around copyright and data
ownership. Copyrighted data might be part of the training data used
without authorization from the data’s actual owners. Lawsuits on
training data in LLMs and text-to-image algorithms are being fought
out in court.

### **9.2.5  Interpretability and Transparency**


With great power comes low interpretability, as shown in Figure 9.3,
which includes several different ML algorithms. While simple
algorithms come with great interpretability, they are associated with
low performance. For example, linear regression is comparably
simple, and for a human, it is easy to understand why the model


drew certain conclusions. But linear regression is far away from the
performance of neural networks, of which LLMs are a prominent
member. These models are extremely powerful, but at the same
time, interpreting their results and understanding how they came to
these results has become difficult.


**Figure 9.3** Interpretability versus Complexity/Performance

### **9.2.6  Jailbreaking LLMs**


LLMs are extremely powerful, even capable of providing harmful
output like instructions on making drugs, hiding a corpse, or robbing
a bank. Model developers have put a lot of effort into the detection of
harmful user queries to prevent models from creating harmful output.
The process of tricking the models to output forbidden content is
called _jailbreaking_ .


Figure 9.4 shows the approach of MathPrompt for jailbreaking LLMs,
from the paper “Jailbreaking Large Language Models with Symbolic


Mathematics,” by E. Bethany and colleagues
( _[https://arxiv.org/html/2409.11445v1](https://arxiv.org/html/2409.11445v1)_ ).


**Figure 9.4** Jailbreaking LLMs with MathPrompt


In this approach, a harmful prompt returns a safe output, which is the
expected result. But the researchers found out that the LLMs safety
mechanisms can be bypassed by encoding harmful prompts in math.
They showed how many state-of-the-art models reveal a high attack
success rate.


Mathematical prompts, including harmful content, could be
embedded such in a way that they are similar to mathematical
embeddings but that hide the harmful content. In a way,
mathematical prompt functions as a Trojan horse to the harmful
content.


A similar approach is ArtPrompt, shown in Figure 9.5, based on the
paper “ArtPrompt: ASCII Art-based Jailbreak Attacks against Aligned


LLMs” from F. Jiang and colleagues
( _[https://arxiv.org/pdf/2402.11753](https://arxiv.org/pdf/2402.11753)_ ).


**Figure 9.5** Jailbreaking Based on ArtPrompt


In this approach, a harmful word is not directly passed to the LLM
but encoded as ASCII art. This approach could also fool LLMs and
provide harmful output.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **9.3  Regulatory Developments**

Regulatory developments are starting to address these issues and
challenges. For example, the European Union’s AI Act is a significant
legislative effort aimed at regulating AI systems based on their risk
levels. High-risk applications like LLMs will face stricter
requirements.


It remains to be seen whether widespread regulation will take place,
or whether economic, governmental, and military interests will
dominate and prevent regulation.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **9.4  Artificial General Intelligence and** **Artificial Superintelligence**

AGI refers to a type of artificial intelligence that possesses the ability
to understand, learn, and apply knowledge across a wide range of
tasks and domains. Unlike specialized (narrow) AI, which is
optimized to perform specific tasks, AGI aims to exhibit general
cognitive abilities. Figure 9.6 shows a possible growth path for AIcapabilities over time.


**Figure 9.6** AI Capabilities over Time


At the time of writing, most researchers agree that we have not
reached AGI. You can expect heated debate whether AGI has been
reached for the foreseeable future. Ever-improving models, like the
recently released OpenAI o3 model, with their further improvements
on reasoning, will heat the debate.


For the time being, we have undoubtedly many narrow AI systems
that excel in their domains. We can observe more and more models
with more general capabilities, but no single model is capable of all


human domains. Eventually, we’ll see AI systems that show
capabilities like humans.


We also can probably expect encounter AI systems with intellectual
powers beyond human level across a large number of categories
and fields: artificial superintelligence (ASI).


Whether or not, we’ll see achieve ASI is still an open question at this
point. In any case, we are living in extraordinary times and are
witnessing a revolution. AGI and ASI are just extreme cases in the AI
debate. Many smaller steps still must be taken that will impact on our
lives in the short term. While predicting the future is hard, it’s still fun
to think about all the possible paths.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **9.5  AI Systems in the Near Term**

According to OpenAI, there are five stages of artificial intelligence:
Level 1 is dominated by chatbots, and AI is used for conversational
language. In Level 2, reasoning models can reach human-level
problem solving. Agentic systems represent Level 3. In Level 4, AI
systems can support creative tasks like inventions and effectively act
as innovators. In Level 5, AI systems can mimic and do the work of
complete organizations. At that point, companies worth of billions of
dollars might be led by a single person (a one-person unicorn) or
even by no person (a zero-person unicorn). We find this prospect
both fascinating and frightening at the same time.


An effective way to think about future technologies is the _hype cycle_
—developed and popularized by the consulting company Gartner.
The hype cycle describes how new technologies typically progress
through different phases.


Starting with an “innovation trigger” that sparks initial interest and
investment, at some point, the technology reaches “inflated
expectations.” At this point, hype and over-optimism reach the
maximum. What follows is a “trough of disillusionment” when interest
wanes. Exaggerated promises cannot be kept.


Then comes a “slope of enlightenment” where realistic applications
emerge. Finally, in the “plateau of productivity” the technology shows
its real benefits. Then, it is widely understood and adopted.
Figure 9.7 shows our take on how selected AI technologies will
develop.


The color and shape of the points corresponds to the speed with
which the technology progresses through the steps. We’ve


separated the technologies into short-term (< 5 years), mid-term (5
to 10 years), and long-term (> 10 years) outlooks.


Let’s start with the AI systems that we expect to reach the plateau of
productivity in the short term, for instance, medical image analysis.
Since computer vision models outperform human benchmarks for
many years, the only hurdles are regulatory and less technological.


**Figure 9.7** Our AI Hype Cycle Prediction


Other technologies that are well established are precision farming
and AI in the legal industry. The legal industry with its standardized
texts and frameworks is an ideal playground for LLMs to shine. The
hype around autonomous driving has disappeared. We see a lot of
disappointment in this field because overoptimistic predictions
caused hopes that could not be lived up to. So, we might be close to
and possibly beyond the trough of disillusionment, and hopefully,
we’ll have autonomous driving in the near future.


Similarly, delivery drones were very hyped up some years ago, and
reality did not live up to expectations. Currently, hardly anyone is
talking about delivery drones. We expect that this technology will
steadily progress and be market ready in the mid-term.


Some technologies like brain-computer interfaces have gained a lot
of media attention. We might be reaching the maximum of the hype
cycle in this area. But there are many technological and regulatory
hurdles to overcome that we see this field to be adopted widely, but
only in the far future.


Other AI technologies that are further down the road are AI selfawareness/consciousness and AI governance/policy-making. While
the former topic is extremely hard to predict (whether consciousness
ever will occur), the latter will be adopted due to the improvements
that it will bring. But developing and accepting such systems will take
a lot of time, so we expect them only in the long term.


Huge leaps forward in robotics show the possibilities this will bring.
But our view is that the expectations are currently inflated and will be
disappointing. Nevertheless, since progress has been extremely fast,
we expect this technology to reach the plateau of productivity in less
than 5 years.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **9.6  Useful Resources**

We hope this book is the starting point of your journey, rather than
the end. In this section, we’ll provide some resources to stay
informed and to help understand the concepts presented in this
book.


**Online courses**
We typically learn based on online courses provided via Udemy,
O’Reilly, or Packt. You might even check out the courses on these
platforms. Other free platforms like DeepLearning.AI
( _[https://deeplearning.ai/](https://deeplearning.ai/)_ ) provide up-to-date content that usually is
quite concise and a great resource to learn new frameworks or
concepts.


**Articles**
Daily.dev ( _[https://daily.dev/](https://daily.dev/)_ ) is a Chrome plugin. With this plugin,
you’ll see interesting articles on coding tailored to your
preferences. The system learns based on your feedback to
improve its recommendations. We would also like to recommend
Medium ( _[https://medium.com/?tag=data-science](https://medium.com/?tag=data-science)_ ), where you can
find many articles on data science and artificial intelligence.


**YouTube**
Many interesting discussions and tutorials on YouTube. We use it
to keep informed on the most recent developments.


**Newsletters**
We also consume some newsletters to keep informed. We can
recommend “The Batch,” a newsletter from DeepLearning.AI
where Andrew Ng writes about recent news on artificial
intelligence.


In general, when diving into a new topic, you can drown in the online
courses, articles, or documentation provided by the developers of a
package or framework. An important step is to quickly move from
carefully prepared courses to your projects. Only when you try to
create an implementation myself can you spot missing links in your
understanding.


Never was there a time in human history in which progress
continued so quickly; it was never so important to learn new skills. Or
put another way, more positively: It has never been so easy to get on
the top of technology.


_[OceanofPDF.com](https://oceanofpdf.com/)_


## **9.7  Summary**

In this chapter, we looked into the crystal ball and tried to anticipate
future developments for generative AI.


We started by discussing advances in model architecture. Then, we
focused on current limitations and possible future limitations and
issues in LLMs, such as hallucinations, biases, misinformation, and
other issues. We studied how regulatory developments are trying to
solve some of these issues.


The pace of progress in artificial intelligence is rapid, and artificial
intelligence becomes increasingly likely to outperform average
human skills, and even expert skills.


This book has journeyed through the incredible landscape of
generative AI—from LLMs, to prompt engineering and vector
databases, to RAG and agentic systems, and finally to the
deployment of such systems.


Generative AI has become a driving force in nearly all industries,
shaping everyday lives. As we look ahead, let’s remember that every
great innovation begins with a question: What will you create next?


_[OceanofPDF.com](https://oceanofpdf.com/)_


# The Author

**Bert Gollnick** is a senior data scientist who specializes in renewable
energies. For many years, he has taught courses about data science
and machine learning, and more recently, about generative AI and
natural language processing. Bert studied aeronautics at the
Technical University of Berlin and economics at the University of
Hagen. His main areas of interest are machine learning and data
science.


_[OceanofPDF.com](https://oceanofpdf.com/)_


# Index

↓ **A** ↓ **B** ↓ **C** ↓ **D** ↓ **E** ↓ **F** ↓ **G** ↓ **H** ↓ **I** ↓ **J** ↓ **K** ↓ **L** ↓ **M** ↓ **N** ↓ **O** ↓ **P** ↓ **Q**
↓ **R** ↓ **S** ↓ **T** ↓ **U** ↓ **V** ↓ **W** ↓ **Z**

## A ⇑


AG2 [→ Section 7.2] [→ Section 7.5]


_two agents_ [→ Section 7.5]


_with tools_ [→ Section 7.5]


Agentic systems [→ Section 7.1]


_agentic RAG_ [→ Section 7.3]


_monitoring_ [→ Section 7.9]


_simple_ [→ Section 7.3]


AgentOps [→ Section 7.9]


AI agent [→ Section 7.1]


Alignment problem [→ Section 7.6]


AlphaGo [→ Section 1.4]


Amazon Web Services (AWS) [→ Section 5.6]


Answer faithfulness [→ Section 6.5]


Answer relevance [→ Section 6.5]


Apache 2.0 license [→ Section 5.8]


API key [→ Section 3.2]


Artificial general intelligence (AGI) [→ Section 1.1] [→ Section
9.1] [→ Section 9.4]


Artificial intelligence (AI) [→ Section 1.1]


_algorithmic improvements_ [→ Section 1.2]


_computational power_ [→ Section 1.2]


_dataset size_ [→ Section 1.2]


_investments_ [→ Section 1.2]


_near term development_ [→ Section 9.5]


Artificial superintelligence (ASI) [→ Section 9.1] [→ Section
9.4]


ArtPrompt [→ Section 9.2]


Asynchronous server gateway interface (ASGI) [→ Section
8.2]

## B ⇑


Bar plot [→ Section 2.4]


Base64 [→ Section 3.2]


BERT [→ Section 1.5] [→ Section 2.5] [→ Section 5.5]

[→ Section 5.5]


Blue teaming [→ Section 7.6]


BM25 [→ Section 6.3] [→ Section 6.3]


## C ⇑

Chain-of-thought (CoT) [→ Section 3.10] [→ Section 4.3]


Chains [→ Section 3.7]


_parallel_ [→ Section 3.7]


_router_ [→ Section 3.7]


_simple sequential_ [→ Section 3.7]


_with memory_ [→ Section 3.7]


Character encoding standard [→ Section 5.4]


Chatbot Arena [→ Section 3.4]


ChatGPT [→ Section 1.1]


ChatPromptTemplates [→ Section 3.6]


Chroma database [→ Section 5.6] [→ Section 5.8]


_data retrieval_ [→ Section 5.7]


Chunking [→ Section 5.2] [→ Section 7.3]


Computer vision [→ Section 5.5]


Context adherence [→ Section 9.2]


Context enrichment [→ Section 6.3]


Context precision [→ Section 6.5]


Context relevance [→ Section 6.5]


Context windows [→ Section 5.4]


Convolutional neural networks (CNNs) [→ Section 3.1]


Cosine similarity [→ Section 5.7]


CrewAI [→ Section 7.2] [→ Section 7.6]


_agents_ [→ Section 7.6] [→ Section 7.6]


_collaboration_ [→ Section 7.6]


_components_ [→ Section 7.6]


_file interactions_ [→ Section 7.6]


_project adaptation_ [→ Section 7.6]


_safety extercise_ [→ Section 7.6]


_starter project_ [→ Section 7.6]


_tasks_ [→ Section 7.6] [→ Section 7.6]


Cursor [→ Section 1.8]


Custom chunking [→ Section 5.4]

## D ⇑


Data loading [→ Section 5.2]


Data processing [→ Section 5.8]


Data retrieval [→ Section 5.7]


Data storage [→ Section 5.6]


Deep Blue [→ Section 1.4]


Deep learning [→ Section 1.1] [→ Section 1.3]


DeepMind [→ Section 1.4]


Delimiters [→ Section 4.1]


Dense vector search [→ Section 6.3]


Deployment [→ Section 8.1]


_architecture_ [→ Section 8.1]


_Heroku_ [→ Section 8.4]


_local_ [→ Section 8.2]


_prediction function_ [→ Section 8.2]


_priorities_ [→ Section 8.2]


_Render_ [→ Section 8.6]


_strategy_ [→ Section 8.2]


_Streamlit_ [→ Section 8.5]


Direct preference optimization (DPO) [→ Section 3.10]


Direct prompting [→ Section 3.9]


Distance matrix [→ Section 5.4]


Distil-Whisper models [→ Section 3.2]


Document objects [→ Section 5.8]

## E ⇑


Eliza [→ Section 3.1]


Embeddings [→ Section 5.2] [→ Section 5.5] [→ Section 7.3]


Embedding vectors [→ Section 5.1]


Ensemble learning [→ Section 4.4]


Environment variables [→ Section 3.2]


Epoch [→ Section 1.3]

## F ⇑


Factual correctness [→ Section 6.5]


FastAPI [→ Section 8.2]


FastText [→ Section 5.5]


Few-shot learning [→ Section 4.1]


Few-shot prompting [→ Section 4.2]


File-based storage [→ Section 5.6]


Fill-mask tasks [→ Section 1.5] [→ Section 2.5]


Fixed-size chunking [→ Section 5.4]


Flask [→ Section 8.2]


Frontend and backend architecture [→ Section 8.1]

## G ⇑


Gated recurrent units (GRUs) [→ Section 3.1]


gemma2 [→ Section 6.2]


GitHub Copilot [→ Section 1.8]


GitHub repository [→ Section 8.5] [→ Section 8.6]


GloVe [→ Section 5.5]


Google Gemini [→ Section 9.2]


GPT-3 [→ Section 1.1]


Grammar-of-graphics approach [→ Section 5.5]


Graphs [→ Section 5.5]


Groq [→ Section 3.2] [→ Section 3.2] [→ Section 6.2]

[→ Section 7.4]

## H ⇑


Haystack [→ Section 7.2]


Heroku [→ Section 8.4]


_app.py file_ [→ Section 8.4]


_create app_ [→ Section 8.4]


_deployment_ [→ Section 8.4]


_install CLI_ [→ Section 8.4]


_procfile setup_ [→ Section 8.4]


_stop app_ [→ Section 8.4]


Hugging Face [→ Section 2.1] [→ Section 5.8]


_narrow AI models_ [→ Section 2.1]


Human in the loop (HITL) [→ Section 7.5]

## I ⇑


Inferences [→ Section 1.3]

## J ⇑


JSON [→ Section 2.6]

## K ⇑


Kahnemann, Daniel [→ Section 4.1]


Keyword-search algorithms [→ Section 6.3]


Knowledge cutoff date [→ Section 3.4]


Kwargs [→ Section 5.3]

## L ⇑


LangChain [→ Section 2.2] [→ Section 3.2] [→ Section 5.3]

[→ Section 5.4]


_embeddings_ [→ Section 5.5]


_hub_ [→ Section 3.6]


LangChain expression language (LCEL) [→ Section 3.7]


LangGraph [→ Section 7.2] [→ Section 7.4]


_graph_ [→ Section 7.4]


_router graph_ [→ Section 7.4]


_simple graph_ [→ Section 7.4]


_with tools_ [→ Section 7.4]


Language modeling [→ Section 1.5]


Large language models (LLMs) [→ Section 1.6] [→ Section
2.1] [→ Section 3.1] [→ Section 5.4] [→ Section 7.1]


_biases_ [→ Section 9.2]


_hallucinations_ [→ Section 9.2]


_interpretability_ [→ Section 9.2]


_jailbreaking_ [→ Section 9.2]


_limitations_ [→ Section 1.6] [→ Section 9.2]


_messages_ [→ Section 3.5]


_misinformation_ [→ Section 9.2]


_model improvements_ [→ Section 3.9]


_model parameters_ [→ Section 3.3]


_model selection_ [→ Section 3.4]


_performance_ [→ Section 3.4]


_security_ [→ Section 3.8]


_self-feedback_ [→ Section 4.6]


_staying on topic_ [→ Section 3.8]


_training_ [→ Section 1.6]


_use cases_ [→ Section 1.6]


Large multimodal models (LMMs) [→ Section 1.7] [→ Section
3.2]


Leonardo.ai [→ Section 1.8]


Limited context window [→ Section 5.4]


Llama family [→ Section 3.2]


Llama Guard [→ Section 3.8]


Loading documents [→ Section 5.3]


_Gutenberg book_ [→ Section 5.3]


_multiple text files_ [→ Section 5.3]


_single text file_ [→ Section 5.3]


_Wikipedia articles_ [→ Section 5.3]


Logfire [→ Section 7.9]


Long short-term memory (LSTM) [→ Section 1.5] [→ Section
3.1]


## M ⇑

Machine learning (ML) [→ Section 1.3] [→ Section 2.1]

[→ Section 3.2]


Magentic-One [→ Section 7.2]


Massive Text Embedding Benchmark (MTEB) leaderboard

[→ Section 5.5]


MathPrompt [→ Section 9.2]


Matrix factorization [→ Section 3.10]


Maximum margin relevance (MMR) [→ Section 5.7]

[→ Section 5.8]


McCulloch, Warren [→ Section 1.1]


Metadata adaptation [→ Section 5.3]


Model compression techniques [→ Section 3.10]


Model temperature [→ Section 3.3]


Moore’s Law [→ Section 1.2]

## N ⇑


Named entity recognition (NER) [→ Section 2.7]


Narrow AI [→ Section 1.1] [→ Section 1.4]


Natural language processing (NLP) [→ Section 1.5]

[→ Section 2.1] [→ Section 3.1] [→ Section 5.5]


_architecture_ [→ Section 1.5]


N-gram models [→ Section 3.1]


Nodes [→ Section 7.4]


NumPy [→ Section 5.5]

## O ⇑


Ollama [→ Section 3.2] [→ Section 3.2]


OOMs (orders of magnitude) [→ Section 9.1]


OpenAI [→ Section 3.2] [→ Section 5.4] [→ Section 5.5]

[→ Section 6.2] [→ Section 6.3]


_o3 model_ [→ Section 9.4]


OpenAI Agents [→ Section 7.2] [→ Section 7.7]


_multiple agents_ [→ Section 7.7]


_search and retrieval functions_ [→ Section 7.7]


_single agent_ [→ Section 7.7]

## P ⇑


Perceptron [→ Section 1.1]


Pinecone [→ Section 5.6] [→ Section 5.6]


_data retrieval_ [→ Section 5.7]


_index_ [→ Section 5.6]


Pitts, Walter [→ Section 1.1]


Postman [→ Section 8.2]


Pretrained models [→ Section 2.1]


_capstone project_ [→ Section 2.10]


Principal component analysis (PCA) [→ Section 5.5]


Private chain-of-thought [→ Section 9.1]


Prompt caching [→ Section 6.4] [→ Section 6.4]


Prompt chaining [→ Section 4.5]


Prompt compression [→ Section 6.3]


Prompt engineering [→ Section 3.9] [→ Section 4.1]


_basics_ [→ Section 4.1]


_clear instructions_ [→ Section 4.1]


_components_ [→ Section 4.1]


_delimiters_ [→ Section 4.1]


_examples_ [→ Section 4.1]


_output control_ [→ Section 4.1]


_personas_ [→ Section 4.1]


_process_ [→ Section 4.1]


_requesting explanations_ [→ Section 4.1]


_task decomposition_ [→ Section 4.1]


Prompt templates [→ Section 3.6]


Pruning [→ Section 3.10]


Pydantic AI [→ Section 7.2] [→ Section 7.8]


Python [→ Section 3.2]


_environment_ [→ Section 8.4]


_frameworks_ [→ Section 7.2]

## Q ⇑


Quantization [→ Section 3.10]


Question answering [→ Section 1.5]


Question answering models [→ Section 2.6]

## R ⇑


RAGAS [→ Section 6.5]


ReAct [→ Section 7.3]


Reasoning models [→ Section 3.10]


Reciprocal rank fusion [→ Section 6.3]


Recurrent neural networks (RNN) [→ Section 1.5] [→ Section
3.1]


Red teaming [→ Section 7.6]


register_for_execution [→ Section 7.5]


register_for_llm [→ Section 7.5]


Regular expressions [→ Section 5.4]


Reinforcement learning from human feedback (RLHF)

[→ Section 9.2]


Render [→ Section 8.6]


REST API [→ Section 8.2] [→ Section 8.2]


Retrieval-augmented generation (RAG) [→ Section 5.5]

[→ Section 6.1]


_advanced_ [→ Section 6.3]


_advanced retrieval techniques_ [→ Section 6.3]


_augmentation process_ [→ Section 6.1] [→ Section 6.2]


_chunk size optimization_ [→ Section 6.3]


_context enrichment_ [→ Section 6.3]


_data cleaning_ [→ Section 6.3]


_evaluation_ [→ Section 6.5]


_function creation_ [→ Section 6.2]


_generation process_ [→ Section 6.1] [→ Section 6.2]


_hybrid pipeline_ [→ Section 6.3]


_hybrid search_ [→ Section 6.3]


_metadata enhancing_ [→ Section 6.3]


_metrics_ [→ Section 6.5] [→ Section 6.5]


_postretrieval techniques_ [→ Section 6.3]


_preretrieval techniques_ [→ Section 6.3]


_process_ [→ Section 6.1]


_query expansion_ [→ Section 6.3]


_retrieval process_ [→ Section 6.1] [→ Section 6.2]


_simple_ [→ Section 6.2]


_vector database_ [→ Section 6.1]


Rosenblatt, Frank [→ Section 1.1]

## S ⇑


Seaborn [→ Section 5.5]


Self-consistency CoT [→ Section 4.4]


Self-contained application [→ Section 8.1]


Semantic chunking [→ Section 5.4] [→ Section 5.4]


Sentence embeddings [→ Section 5.5]


Sentence similarity [→ Section 1.5]


Similarity calculation [→ Section 5.7]


Skip-gram algorithm [→ Section 5.5]


Small language models (SLMs) [→ Section 3.10]


Sparse vector search [→ Section 6.3]


Splitting documents [→ Section 5.4]


SQuAD 2.0 [→ Section 2.6]


Stable diffusion models [→ Section 2.8]


Stopwords [→ Section 6.3] [→ Section 6.3]


Streamlit [→ Section 5.8] [→ Section 5.8] [→ Section 8.3]

[→ Section 8.3]


_create app_ [→ Section 8.5]


_deployement_ [→ Section 8.5]


Strong AI [→ Section 1.1]


Structure-based chunking [→ Section 5.4]

## T ⇑


Target variables [→ Section 1.3]


Tavily [→ Section 7.3]


Test-time computation [→ Section 3.10]


Text classification [→ Section 1.5]


Text generation [→ Section 1.5]


Text summarization [→ Section 1.5] [→ Section 2.2]

[→ Section 2.2]


Text-to-audio [→ Section 2.9]


Text-to-image models [→ Section 2.8]


Text translation [→ Section 1.5]


TF-IDF [→ Section 6.3] [→ Section 6.3]


Tiny Troupe [→ Section 7.2]


Token [→ Section 5.4]


Tokenization [→ Section 5.4] [→ Section 5.5]


Top-k [→ Section 3.3] [→ Section 5.7]


Top-p [→ Section 3.3]


Transformer architecture [→ Section 2.2]


Translation [→ Section 2.3]


True values [→ Section 1.3]


Turing Test [→ Section 1.1]

## U ⇑


Unhobbling [→ Section 9.1]


Uvicorn [→ Section 8.2]


## V ⇑

Vector databases [→ Section 5.1]


_capstone projects_ [→ Section 5.8]


_data ingestion_ [→ Section 5.2]


_preparation_ [→ Section 5.8]


_selection_ [→ Section 5.6]


Vectors [→ Section 5.1]


Vision-language models (VLMs) [→ Section 1.7]


Visual Studio Code [→ Section 8.4]

## W ⇑


Web-based storage [→ Section 5.6]


Word2vec [→ Section 5.5]


Word embeddings [→ Section 5.5]

## Z ⇑


Zero-shot classification [→ Section 2.4] [→ Section 2.4]


Zero-shot CoT [→ Section 4.3]


_[OceanofPDF.com](https://oceanofpdf.com/)_


# Service Pages

The following sections contain notes on how you can contact us. In
addition, you are provided with further recommendations on the
customization of the screen layout for your e-book.

## **Praise and Criticism**


We hope that you enjoyed reading this book. If it met your
expectations, please do recommend it. If you think there is room for
improvement, please get in touch with the editor of the book:
_[Meagan White](mailto:meaganw@rheinwerk-publishing.com)_ . We welcome every suggestion for improvement but,
of course, also any praise! You can also share your reading
experience via Social Media or email.

## **Supplements**


If there are supplements available (sample code, exercise materials,
lists, and so on), they will be provided in your online library and on
the web catalog page for this book. You can directly navigate to this
page using the following link: _https://www.rheinwerk-_
_computing.com/6057_ . Should we learn about typos that alter the
meaning or content errors, we will provide a list with corrections
there, too.


## **Technical Issues**

If you experience technical issues with your e-book or e-book
account at Rheinwerk Computing, please feel free to contact our
reader service: _[support@rheinwerk-publishing.com](mailto:support@rheinwerk-publishing.com)_ .


Please note, however, that issues regarding the screen presentation
of the book content are usually not caused by errors in the e-book
document. Because nearly every reading device (computer, tablet,
smartphone, e-book reader) interprets the EPUB or Mobi file format
differently, it is unfortunately impossible to set up the e-book
document in such a way that meets the requirements of all use
cases.


In addition, not all reading devices provide the same text
presentation functions and not all functions work properly. Finally,
you as the user also define with your settings how the book content
is displayed on the screen.


The EPUB format, as currently provided and handled by the device
manufacturers, is actually primarily suitable for the display of mere
text documents, such as novels. Difficulties arise as soon as
technical text contains figures, tables, footnotes, marginal notes, or
programming code. For more information, please refer to the section
Notes on the Screen Presentation and the following section.


Should none of the recommended settings satisfy your layout
requirements, we recommend that you use the PDF version of the
book, which is available for download in your online library.


## **Recommendations for Screen Presentation** **and Navigation**

We recommend using a sans-serif **font**, such as Arial or Seravek,
and a low font size of approx. 30–40% in portrait format and 20–30%
in landscape format. The background shouldn’t be too bright.


Make use of the **hyphenation** option. If it doesn't work properly,
align the text to the left margin. Otherwise, justify the text.


To perform **searches** in the e-book, the index of the book will reliably
guide you to the really relevant pages of the book. If the index
doesn't help, you can use the search function of your reading device.


Since it is available as a double-page spread in landscape format,
the **table of contents** we’ve included probably gives a better
overview of the content and the structure of the book than the
corresponding function of your reading device. To enable you to
easily open the table of contents anytime, it has been included as a
separate entry in the device-generated table of contents.


If you want to **zoom in on a figure**, tap the respective figure **once** .
By tapping once again, you return to the previous screen. If you tap
twice (on the iPad), the figure is displayed in the original size and
then has to be zoomed in to the desired size. If you tap once, the
figure is directly zoomed in and displayed with a higher resolution.


For books that contain **programming code**, please note that the
code lines may be wrapped incorrectly or displayed incompletely as
of a certain font size. In case of doubt, please reduce the font size.


## **About Us and Our Program**

The website _[https://www.rheinwerk-computing.com](https://www.rheinwerk-computing.com/)_ provides detailed
and first-hand information on our current publishing program. Here,
you can also easily order all of our books and e-books. Information
on Rheinwerk Publishing Inc. and additional contact options can also
be found at _[https://www.rheinwerk-computing.com](https://www.rheinwerk-computing.com/)_ .


_[OceanofPDF.com](https://oceanofpdf.com/)_


# Legal Notes

This section contains the detailed and legally binding usage
conditions for this e-book.

## **Copyright Note**


This publication is protected by copyright in its entirety. All usage and
exploitation rights are reserved by the author and Rheinwerk
Publishing; in particular the right of reproduction and the right of
distribution, be it in printed or electronic form.
**© 2025 by Rheinwerk Publishing Inc., Boston (MA)**

## **Your Rights as a User**


You are entitled to use this e-book for personal purposes only. In
particular, you may print the e-book for personal use or copy it as
long as you store this copy on a device that is solely and personally
used by yourself. You are not entitled to any other usage or
exploitation.


In particular, it is not permitted to forward electronic or printed copies
to third parties. Furthermore, it is not permitted to distribute the ebook on the internet, in intranets, or in any other way or make it
available to third parties. Any public exhibition, other publication, or
any reproduction of the e-book beyond personal use are expressly


prohibited. The aforementioned does not only apply to the e-book in
its entirety but also to parts thereof (e.g., charts, pictures, tables,
sections of text).


Copyright notes, brands, and other legal reservations as well as the
digital watermark may not be removed from the e-book.


No part of this book may be used or reproduced in any manner for
the purpose of training artificial intelligence technologies or systems.
In accordance with Article 4(3) of the Digital Single Market Directive
2019/790, Rheinwerk Publishing, Inc. expressly reserves this work
from text and data mining.

## **Digital Watermark**


This e-book copy contains a **digital watermark**, a signature that
indicates which person may use this copy.


If you, dear reader, are not this person, you are violating the
copyright. So please refrain from using this e-book and inform us
about this violation. A brief email to _[info@rheinwerk-publishing.com](mailto:info@rheinwerk-publishing.com)_
is sufficient. Thank you!

## **Trademarks**


The common names, trade names, descriptions of goods, and so on
used in this publication may be trademarks without special
identification and subject to legal regulations as such.


All products mentioned in this book are registered or unregistered
trademarks of their respective companies.


## **Limitation of Liability**

Regardless of the care that has been taken in creating texts, figures,
and programs, neither the publisher nor the author, editor, or
translator assume any legal responsibility or any liability for possible
errors and their consequences.


_[OceanofPDF.com](https://oceanofpdf.com/)_


# The Document Archive

The Document Archive contains all figures, tables, and footnotes, if
any, for your convenience.


_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 1   Book Chapter Dependencies

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 2   System Setup

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 3   Python Download

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 4   Git Download

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5   GitHub Repository for This Book

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 6   Python Environments

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 7   Environment and Python Detection in VS Code

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 1.1   Number of Users of Selected Internet Services

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 1.2   AI Evolution

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 1.3   AI System Capabilities (Source: https://ourworldindata.org/artificial-intelligence ; used under Creative Commons Attribution 4.0 International License)

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 1.4   Computation Used to Train AI Systems (Source: _https://ourworldindata.org/artificial-intelligence?insight=the-_ _last-decades-saw-a-continuous-exponential-increase-in-the-_ computation-used-to-train-ai ; used under Creative Commons Attribution 4.0 International License)

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 1.5   Model Parameters and Training Dataset Size (Source: https://ourworldindata.org/grapher/parameters-vs- _training-dataset-size-in-notable-ai-systems-by-researcher-_ affiliation ; used under Creative Commons Attribution 4.0 International License)

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 1.6   ML and Classic Programming, Compared

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 1.7   Deep Learning: Model Training

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 1.8   Deep Learning: Model Inference

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 1.9   Narrow AI Achievements

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 1.10   Typical NLP Tasks

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 1.11   LLM Training Process

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 1.12   Large Multimodal Models

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 2.1   Classic ML Models versus LLM Training

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 2.2   Hugging Face Home Page

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 2.3   Hugging Face Model Selection Process

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 2.4   Sample Model Card (Source: https://huggingface.co/sshleifer/distilbart-cnn-12-6 )

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 2.5   Zero-Shot Classification Result for Sherlock Holmes

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 2.6   Sample Output from the Text2Image Model

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 2.7   Capstone Project Workflow

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 3.1   ELIZA User Interface (Source: _https://upload.wikimedia.org/wikipedia/_ commons/4/4e/ELIZA_conversation.jpg )

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 3.2   Deep Neural Network Training Process

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 3.3   Ollama Software Download

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 3.4   Ollama-Provided Model Class “gemma2”

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 3.5   Temperature Output and Analogy

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 3.6   Model Temperature and Probability Distribution

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 3.7   Top-p and Top-k Parameters

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 3.8   Chatbot Arena Leaderboard (as of January 24, 2025; Source: https://lmarena.ai/?leaderboard)

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 3.9   Simple LangChain Chain

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 3.10   Parallel Execution of Two Chains

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 3.11   Router Chain

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 3.12   Sample Output from Our LLM Chain Game

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 3.13   LLM Text Game Including Memory

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 3.14   LLM Safety and Security

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 3.15   LLM: Stay on Topic Pipeline

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 3.16   Model Improvement Approaches

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 3.17   Reasoning Tokens

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 3.18   LLM versus SLM with Test-Time Compute

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 3.19   Test-Time Compute Process

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 4.1   Prompt and Prompt Template

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 4.2   Prompt Engineering Process

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 4.3   AI Model Input and Output

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 4.4   Prompt Components

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 4.5   Self-Consistency CoT

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 4.6   Prompt Chaining

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 4.7   Self-Feedback Process Flow

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5.1   Unstructured and Structured Data

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5.2   Example Vector Space

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5.3   Data Ingestion Pipeline

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5.4   LangChain DataLoader Process

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5.5   Chunking Strategies

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5.6   CharacterTextSplitter with Chunk Overlap

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5.7   Distribution of Chunk Lengths for Fixed-Size Chunking

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5.8   Distribution of Chunk Lengths for Recursive Character Splitting

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5.9   Semantic Chunking

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5.10   Embedding Process

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5.11   Skip-Gram Example

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5.12   Word2vec for Random Words and Words Similar to “mathematics”

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5.13   Word2vec PCA Representation of Capitals and Countries

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5.14   Sample Sentence Tokenization with BERT

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5.15   Sentence Embeddings Correlations (Source: 05_VectorDatabases/30_Embedding/20_sentence_similarity. py)

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5.16   Principle of Cosine Similarity Calculation and Retrieval

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5.17   Maximum Margin Relevance Example

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5.18   Sample Output from Our Movie App

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5.19   Capstone Project: Streamlit App Rerun Options

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5.20   Capstone Project: Streamlit Slider for “Minimum IMDB Rating”

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5.21   Capstone Project: Streamlit Dropdown Box for Genre Filter

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 5.22   Capstone Project: Streamlit Chat Input Field

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 6.1   RAG General Pipeline

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 6.2   Simple RAG System Based on a Vector Database Backend

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 6.3   Retrieval Process

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 6.4   Pre-Retrieval Techniques

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 6.5   Hybrid RAG: Pipeline

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 6.6   Reciprocal Rank Fusion: Rank Calculation (Left) and Fusion (Right)

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 6.7   Contextual Retrieval (Source: Adapted from https://www.anthropic.com/news/contextual-retrieval )

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 6.8   Prompt Compression

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 6.9   Prompt Caching

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 6.10   Prompt Caching: First Chat Round with Cache Creation

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 6.11   Prompt Caching with Reading Cached Tokens

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 6.12   RAG Evaluation Metrics

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 6.13   RAG Evaluation Metric: Answer Relevance

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 7.1   Agentic System Workflow

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 7.2   Agent Flexibility/Reliability versus Autonomy

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 7.3   Agentic RAG Workflow

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 7.4   LangGraph: A Simple Graph

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 7.5   LangGraph: Our Simple Graph

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 7.6   LangGraph: Router Graph

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 7.7   LangGraph: Graph with Tool Use

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 7.8   Inability of LLMs to Count Letters

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 7.9   AG2 Human in the Loop (Source: Adapted from https://ag2ai.github.io/ag2/docs/tutorial/human-in-the-loop )

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 7.10   Hangman Gameplay Example

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 7.11   CrewAI Components

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 7.12   News Analysis Crew Setup

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 7.13   CrewAI Report on AI LLMs

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 7.14   News Analysis Crew: File Interactions

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 7.15   Snippet of News Analysis Crew Report

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 7.16   AI Escape and Safety Crew

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 7.17   Report on Escape and Defense Plan of a Rogue AI System

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 7.18   AgentOps: Session Drilldown

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 7.19   AgentOps: Session Replay

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 7.20   Logfire: New Project

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 7.21   Logfire: Project Logging (Source: https://logfire.pydantic.dev/bertgollnick/person-details )

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 8.1   Interaction between Server and User

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 8.2   Deployment Options

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 8.3   HTTP Methods Used by REST APIs

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 8.4   Postman: Interaction with API Endpoint “predict”

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 8.5   Streamlit App: Frontend


_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 8.6   Heroku: Create New App

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 8.7   Heroku Deployed App

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 8.8   Heroku App State and Estimated Cost

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 8.9   Heroku App State Stopped

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 8.10   GitHub Repository for Deployment to Streamlit

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 8.11   Streamlit: Source of Your App

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 8.12   Streamlit: Deploy an App

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 8.13   Streamlit: Advanced Settings

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 8.14   Render: Select a Service

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 8.15   Render: Connect to a GitHub Repository

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 8.16   Render: Select an Instance Type

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 8.17   Render: Environmental Variables

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 9.1   Bias Introduction into LLM Training

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 9.2   Biases Based on Political Agenda

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 9.3   Interpretability versus Complexity/Performance

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 9.4   Jailbreaking LLMs with MathPrompt

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 9.5   Jailbreaking Based on ArtPrompt

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 9.6   AI Capabilities over Time

_[OceanofPDF.com](https://oceanofpdf.com/)_


### Figure 9.7   Our AI Hype Cycle Prediction

_[OceanofPDF.com](https://oceanofpdf.com/)_


_[OceanofPDF.com](https://oceanofpdf.com/)_


# Footnotes


[ 1 ] If your default branch is called `master`, you need to change it to

`main` . This change is performed in the terminal. For that, make sure
that the terminal is visible. You can activate it via the menu: **View •**
**Terminal**, and then run the command `git checkout -b main` .


_[OceanofPDF.com](https://oceanofpdf.com/)_


