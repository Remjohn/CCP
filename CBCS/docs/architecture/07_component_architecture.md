# **5\. Component Architecture & API Design**

## **5.1 The Agentic Mesh: Beyond Monoliths**

The **Conscious Behavioral Change System** is not architected as a monolithic web server but as a distributed **Agentic Mesh**. In a traditional Model-View-Controller (MVC) application, the controller dictates the logic. In our architecture, the "Controller" is dissolved into a swarm of autonomous agents, each possessing a specific cognitive domain, communicating through structured event streams.

This component architecture is designed to support **Asynchronous Cognitive Loads**. A single user interaction (e.g., a Voice Note) triggers a cascade of operations—transcription, entity extraction, graph querying, strategy selection, script generation, and audio synthesis—that cannot occur within a standard HTTP request/response cycle. Therefore, the system is built on an **Event-Driven Backbone** managed by **FastAPI** and **Redis**, with **LangGraph** serving as the state manager for the agentic workforce.

The architecture is divided into four primary component domains: **The Ingress & Buffering Layer**, **The Cognitive Core**, **The Perception & Expression Engines**, and **The API Surface**.

## **5.2 The Ingress & Buffering Layer**

This layer is the system's sensory receptor. It is responsible for high-concurrency I/O, cryptographic validation, and "Silence Detection."

### **5.2.1 The FastAPI Event Bus**

The entry point for the system is a lightweight **FastAPI** service. It does not contain business logic; it contains routing logic.

* **The Webhook Receiver:** The primary endpoint POST /webhooks/telegram accepts high-velocity traffic from the Telegram Bot API. It performs signature verification to ensure request integrity and immediately pushes the payload to a background worker using BackgroundTasks.  
* **The 200ms Mandate:** To prevent Telegram from treating our server as unresponsive and retrying messages (creating "Ghost Loops"), this layer guarantees a 200 OK response within 200 milliseconds, regardless of the downstream AI processing load.

### **5.2.2 The Redis "Listening Window"**

Humans do not speak in single API calls; they speak in bursts. A user might send three short text messages and one voice note in the span of 30 seconds. If the system replies to each one individually, it breaks the **"Illusion of Presence."** To solve this, we implement a **Burst Aggregation Component** backed by **Redis**.

* **The Buffer:** When **Emilio (The Orchestrator)** detects a new message stream, he initializes a Redis List for that user\_id. All incoming payloads are appended to this list.  
* **The Silence Sentinel:** A specialized background worker monitors the timestamp of the last message in the buffer. It enforces a "Soft Silence" threshold (90 seconds). Only when the user has stopped typing/recording for 90 seconds does the Sentinel package the buffer into a single ConversationContext object and dispatch it to the Cognitive Core. This ensures **Aria** analyzes the *complete* thought, not just the first sentence.

## **5.3 The Cognitive Core: LangGraph & Pydantic AI**

This is the "Brain" where state is managed and decisions are made. It is hosted within the FastAPI worker process but operates independently of the HTTP cycle.

### **5.3.1 LangGraph State Orchestration**

**Emilio** utilizes **LangGraph** to manage the user's lifecycle as a directed cyclic graph. Unlike linear workflows, human coaching requires loops, interrupts, and persistent memory.

* **State Nodes:** The graph defines specific states: Sleep, Priming, Listening, Analyzing, Strategizing, Speaking, and Crisis\_Override.  
* **State Persistence:** LangGraph creates checkpoints after every state transition, saving the entire stack to **Supabase**. If the server restarts, Emilio "wakes up" knowing exactly where every user is in their journey.  
* **Conditional Edges:** The graph utilizes logic gates driven by **Liliane (The Empathy Agent)**. If Liliane detects a Sentiment\_Score below a safety threshold during the Analyzing phase, she triggers a conditional edge that bypasses the standard Strategizing node and routes the user to the Human\_Handoff node, alerting the Coach via the Dashboard.

### **5.3.2 Pydantic AI Reasoning Engine**

We do not use "Prompt Engineering" in the traditional sense; we use **"Schema Engineering."** The agents do not output text; they output data. **Pydantic AI** wraps the **MiniMax-M2** model, forcing it to adhere to strict Python classes.

* **Dependency Injection:** When **The Assembler (Strategist)** is called, Pydantic AI injects the **Intelligence Library** (YAML configurations) into the runtime context. This ensures the LLM has read-only access to the persuasion\_layers.yaml and identity\_pillars.yaml files.  
* **Validator Interceptors:** Before any agent output is accepted, Pydantic validators run sanity checks. For example, if **Atlas (Program Architect)** attempts to assign a "Heroic" ritual to a user with a low Capacity\_Score, the validator catches the logic error and forces a regeneration. This acts as a "Cognitive Firewall" against hallucination.

## **5.4 The Perception & Expression Engines**

These components handle the transformation of raw media (Voice) into structured meaning (Graph Data) and back into media (Audio).

### **5.4.1 The Perception Engine (Groq \+ Aria)**

This component is responsible for "Hearing" and "Understanding."

* **Transcription Pipeline:** Raw .ogg audio is streamed from Telegram to **Groq** (Whisper Large v3). We utilize ephemeral memory buffers to ensure no raw audio is written to disk before encryption, adhering to the "Glass Wall" protocol.  
* **Entity Extraction Service:** **Aria** takes the text transcript and performs a Named Entity Recognition (NER) pass using the taxonomy defined in context\_premise\_map.json. She identifies "Enemies," "Fears," and "Dreams."  
* **Graph Write Service:** Aria translates these entities into **Cypher** queries to update the **Neo4j** database, creating or reinforcing relationships (e.g., increasing the weight of (User)-\[:FEARS\]-\>(Poverty)).

### **5.4.2 The Expression Engine (Artisan \+ IndexTTS-2)**

This component is responsible for "Writing" and "Speaking."

* **Script Generation Service:** **The Artisan** receives an InterventionStrategy object from The Assembler. It uses **Jinja2** templates to fuse the **Story Insight Formula** with the specific nouns extracted from Neo4j.  
* **Voice Synthesis Cluster:** We maintain a cluster of **Runpod** Serverless GPUs hosting the **IndexTTS-2** engine. This component exposes an internal gRPC or HTTP API that accepts text and **TTT (Temperament, Temperature, Tone)** parameters.  
* **The Keep-Warm Scheduler:** To meet the NFR of \<15s latency, a scheduler pings the IndexTTS-2 cluster during peak windows (07:00-10:00 AM) to prevent GPU cold starts.

## **5.5 API Design & Surface Area**

The system exposes three distinct API surfaces: The Public Webhook API (Ingress), the Internal Agent API (Inter-service), and the Dashboard API (Egress).

### **5.5.1 Public Webhook API (Ingress)**

This surface is exposed to the internet and secured via shared secrets and signature validation.

* POST /webhooks/telegram: Accepts Update objects from Telegram. Validates X-Telegram-Bot-Api-Secret-Token.  
* POST /webhooks/stripe: Accepts Event objects from Stripe. Handles checkout.session.completed (Provisioning) and customer.subscription.deleted (Deprovisioning).

### **5.5.2 The Coach Dashboard API (Egress)**

This API powers the **Next.js** frontend. It utilizes **Supabase** for authentication and data retrieval.

* GET /api/cohort/vibe: Returns the aggregated Word Cloud data generated by **Maeva**.  
* GET /api/client/{id}/graph: Returns the force-directed graph JSON of the user's **Context Premise** from **Neo4j**.  
* GET /api/client/{id}/spider: Returns the dataset for the "Evidence Printer" radar chart.  
* POST /api/intervention/send: The endpoint for **Operator Mode**. Accepts a text or audio payload from the Coach and injects it directly into the user's Telegram stream, bypassing the AI agent.

### **5.5.3 Realtime Subscriptions**

We utilize **Supabase Realtime** (WebSockets) to push state changes to the Dashboard without polling.

* channel: cohort\_feed: Pushes new **Insight Cards** to the "Psychological Feed" as Aria processes them.  
* channel: alerts: Pushes "Red Flag" events triggered by **Liliane**.

## **5.6 Data Flow & Sequence**

1. **Stimulus:** User sends Voice Note via Telegram.  
2. **Ingress:** FastAPI receives webhook $\\rightarrow$ Pushes to Redis $\\rightarrow$ Returns 200 OK.  
3. **Perception:** Redis Silence Timer fires $\\rightarrow$ Groq Transcribes $\\rightarrow$ **Aria** extracts Soul Data $\\rightarrow$ Neo4j Graph Updated.  
4. **Cognition:** **Emilio** triggers **The Assembler** $\\rightarrow$ Assembler reads Neo4j \+ Intelligence Library $\\rightarrow$ Outputs InterventionStrategy.  
5. **Expression:** **The Artisan** generates Script $\\rightarrow$ **The Voice** sends to Runpod $\\rightarrow$ IndexTTS-2 generates Audio.  
6. **Delivery:** Audio sent to Telegram $\\rightarrow$ 3s Delay $\\rightarrow$ Text Block sent.  
7. **Feedback:** **Langfuse** logs cost/latency $\\rightarrow$ **Maeva** updates Cohort Vibe stats.
