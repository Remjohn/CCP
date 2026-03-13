## **2.4 Core Technology Stack (Finalized)**

Based on the requirements for an **Agentic Engineering** approach, this is the locked technology stack.

| Component | Technology | Rationale |
| :---- | :---- | :---- |
| **Orchestration** | **LangGraph** | Essential for the cyclic state management of the 4-Agent Pipeline. It allows us to maintain the "User State" (Sleep \-\> Priming \-\> Action) and handle the "Human-in-the-Loop" interrupt for crisis management seamlessly. |
| **Agent Logic** | **Pydantic AI** | Enforces strict schema validation on all agent outputs. It acts as the "Pre-Frontal Cortex," preventing the AI from outputting invalid JSON or hallucinating advice that violates the capacity\_score. |
| **LLM (Reasoning)** | **MiniMax-M2** | Selected for its high "Chain of Thought" capability and superior cost-performance ratio, which is critical for the heavy processing load of the "Aria" synthesis phase. |
| **Database (Relational)** | **Supabase** | Provides Authentication, Vector Store (pgvector for RAG), and Real-time subscriptions (Supabase Realtime) to power the live "Cohort Vibe" visualization on the Coach Dashboard. |
| **Database (Graph)** | **Neo4j** | The only viable solution for mapping the 12-dimensional Context Premise efficiently. It allows for semantic queries that relational databases cannot execute performantly. |
| **Audio Input** | **Groq (Whisper)** | Required for near-zero latency transcription of long user rants. Its cost structure ($0.03/hr) is the economic enabler of the "Voice Journaling" feature. |
| **Audio Output** | **IndexTTS-2** | Self-hosted on **Runpod**. Essential for the TTT prosody control (breath, pausing, speed) that standard APIs (OpenAI/ElevenLabs) cannot provide. This maintains the "Mirroring Effect." |
| **Backend** | **FastAPI** | Async Python framework required to handle the high-concurrency Telegram webhooks without blocking the heavy inference threads. It supports the BackgroundTasks necessary for our event-driven architecture. |
| **Observability** | **Langfuse** | Tracks cost-per-user and agent latency. The "Circuit Breaker" logic relies on this to automatically downgrade users to text-mode if they exceed the $4.00/month margin cap. |

# **3\. Technology Stack Specification**

## **3.1 The Architectural Thesis: From Stack to Organism**

The technical infrastructure of the **Conscious Behavioral Change System** represents a radical departure from the traditional Model-View-Controller (MVC) paradigm that dominates modern web development. Standard SaaS applications are architected as "Systems of Record"—passive entities designed to store state and retrieve it upon request. They are technically reactive.

To achieve **Identity Engineering**, we must build a "System of Engagement" that is technically proactive. We are not building a software stack; we are engineering a digital organism capable of perception, reasoning, memory, and expression. This requires a "Hub-and-Spoke Agentic Mesh" where the central controller is not a user interface, but an intelligent orchestration layer that manages asynchronous state transitions across time.

This specification defines the technologies that power the four engines of the system: **The Noise Detector**, **The Neuro-Persuasion Engine**, **The Rapport Interface**, and **The Master Composer**. We prioritize **Psychological Fidelity** (accuracy of the persona), **Latency Management** (speed of presence), and **Unit Economics** (viability of scale) over simple CRUD throughput.

## **3.2 The Cognitive Core: Reasoning & Orchestration**

The "Brain" of the system consists of two distinct layers: the Reasoning Layer (Thought) and the Orchestration Layer (Flow). We reject the "Black Box" approach of sending raw prompts to an LLM. Instead, we utilize structured, deterministic frameworks to constrain the generative power of AI within the boundaries of our psychological methodology.

### **3.2.1 Reasoning Engine: Pydantic AI**

We utilize **Pydantic AI** as the structural interface between our business logic and the **MiniMax-M2** Large Language Model (LLM). In our architecture, Pydantic AI functions as the "Pre-Frontal Cortex" of the agentic workforce.

* **Schema Enforcement over Prompt Engineering:** We do not rely on the LLM to "guess" the correct output format. Every agent interaction is governed by strict Python classes (Pydantic Models). When **The Assembler (Strategist Agent)** decides on a persuasion strategy, it must output an InterventionStrategy object containing specific fields: target\_formula\_id, cognitive\_bias\_selected, and rationale.  
* **Runtime Validation:** Before any thought is acted upon, Pydantic validators execute against the **Intelligence Library**. If the LLM selects a "High Intensity" ritual for a user whose Capacity\_Score is low (Burnout), the validator intercepts the response, throws a ValidationError, and forces the LLM to retry with a self-correction prompt. This guarantees that the system never hallucinates dangerous advice.  
* **Model Selection:** We utilize **MiniMax-M2** via direct API for its superior "Chain of Thought" reasoning capabilities and cost-effectiveness relative to GPT-4o, which is critical for the heavy processing load of the **Aria (Synthesizer)** agent.

### **3.2.2 State Orchestration: LangGraph**

While Pydantic AI handles individual thoughts, **LangGraph** handles the flow of consciousness. It serves as the "Nervous System," managing the persistent state of the user interaction over days, weeks, and months.

* **Cyclic State Management:** Unlike linear directed acyclic graphs (DAGs), our conversation flows are cyclic. **Emilio (The Orchestrator)** manages a state graph that supports loops (e.g., Priming $\\rightarrow$ Action $\\rightarrow$ Failure $\\rightarrow$ Compassionate Retrieval $\\rightarrow$ Action). LangGraph persists this state to **Supabase**, ensuring that if the server restarts, the agent "remembers" exactly where it was in the conversation.  
* **Human-in-the-Loop Interrupts:** LangGraph allows us to define "Breakpoints." If **Liliane (The Empathy Agent)** detects high-risk keywords or a collapse in user sentiment (e.g., TTT-02 Defeated), the graph transitions to a Human\_Override state. This effectively "pauses" the AI and routes control to the Coach via the Dashboard, a critical safety feature for high-ticket coaching.

## **3.3 The Intelligence Repository: Configuration as Code**

The most unique component of our stack is the **Intelligence Library**, located in /backend/intelligence\_library/. This is a repository of static YAML and JSON configuration files that decouple the "Psychology" from the "Code."

* **Purpose:** This allows the Coaching Team to update the methodology without requiring engineering deployment.  
* **Components:**  
  * **identity\_pillars.yaml:** Defines the 7 Archetypes (Rebel, Maker, etc.) and their linguistic markers.  
  * **ttt\_matrix.yaml:** Defines the 9 Voice Physics profiles (10°F \- 100°F), controlling syntax length, punctuation density, and vocabulary.  
  * **persuasion\_layers.yaml:** Defines the 9 logic structures for influence (e.g., "The Challenger," "Black & White Philosophy").  
  * **context\_premise\_map.json:** Defines the taxonomy of the 12 psychological dimensions used for entity extraction.  
* **Injection:** These files are loaded into memory at startup and injected into the AgentDeps context. This ensures that every agent instance operates from the exact same "Ground Truth."

## **3.4 Hybrid Memory Architecture: The Dual Brain**

To facilitate **Identity Engineering**, we must store two types of data: linear facts and non-linear meaning. We employ a **Hybrid Persistence Architecture**.

### **3.4.1 Relational & Vector Storage: Supabase (PostgreSQL)**

**Supabase** acts as the "Left Brain" of the system—logical, orderly, and transactional.

* **Logistical Data:** It stores the hard logs: user\_profiles, daily\_logs (transcripts), subscription\_status, and ritual\_library. We utilize **Row Level Security (RLS)** to strictly isolate tenant data.  
* **Semantic Memory (pgvector):** We utilize the pgvector extension to store embeddings of the Coach’s content manuals and past advice. When **Lionel (The Researcher)** needs to fact-check a statement, he performs a RAG (Retrieval Augmented Generation) search against this vector store. This ensures the AI stays within the "Glass Wall" of the Coach's specific methodology.

### **3.4.2 Psychological Graph: Neo4j**

**Neo4j** acts as the "Right Brain"—associative, emotional, and complex. It stores the **Context Premise**.

* **The Ontology:** We map the user's psyche into nodes and relationships.  
  * Nodes: User, IdentityPillar, Concept (with properties like type and intensity), Ritual.  
  * Relationships: (:User)-\[:FIGHTS\]-\>(:Concept {type: "Enemy"}), (:User)-\[:CRAVES\]-\>(:Concept {type: "Dream"}).  
* **The Magic Query:** This structure allows **The Assembler** to perform semantic queries that relational databases cannot handle. For example: *"Find the 'Enemy' node connected to this User that has the highest intensity score and is blocking a 'Dream' node."* This allows the system to generate scripts that feel deeply insightful because they reference the specific connections in the user's mind.

## **3.5 The Generative Media Pipeline: The Senses**

The system interacts with the world through Audio. We prioritize high-fidelity synthesis to maintain the **"Mirroring Effect."**

### **3.5.1 Voice Synthesis: IndexTTS-2 on Runpod**

We host a self-managed **IndexTTS-2** engine on **Runpod** Serverless GPU instances. We strictly avoid standard APIs (like OpenAI Voice or ElevenLabs) because they lack the granular control over prosody required for the **TTT (Temperament, Temperature, Tone)** system.

* **Granular Modulation:** **The Voice (Speaker Agent)** sends instructions to the inference engine to modulate Speed, Breathiness, and Pitch based on the TTT state. For "Compassionate" mode, we inject breath tokens; for "Challenger" mode, we increase the speed and remove pauses.  
* **Latency Optimization:** To mitigate the "Cold Start" latency (15-20s) of serverless GPUs, we implement a "Keep-Warm" scheduler. A Cron job pings the Runpod endpoint every 4 minutes during the "Peak Window" (07:00 AM \- 10:00 AM User Local Time) to keep the model loaded in VRAM, ensuring Time-To-First-Byte (TTFB) remains under 500ms.

### **3.5.2 Hearing & Transcription: Groq**

We utilize **Groq** running **Whisper Large v3** for all audio ingestion.

* **The Cost Arbitrage:** Groq processes audio at approximately $0.03/hour. This is the economic enabler of the "Voice Journaling" feature, allowing users to send long therapeutic vents without destroying our margins.  
* **Stream Processing:** We stream the OGG file directly from Telegram's servers to the Groq API without intermediate local storage, minimizing latency.

## **3.6 The Ingress & Application Layer**

### **3.6.1 Ingress Controller: FastAPI**

The entry point is a **FastAPI** application. It is designed to be stateless and high-throughput.

* **Event Bus:** It receives webhooks from Telegram and Stripe, validates signatures, and immediately offloads processing to **BackgroundTasks**. This ensures that the ingress layer never blocks, adhering to the strict 200ms response requirement of the Telegram API.  
* **The Listening Window (Redis):** To handle "bursty" user behavior (sending 5 short messages in a row), we implement a buffering layer using **Redis**. **Emilio** collects messages into a Redis List and only triggers the cognitive pipeline once a "Soft Silence" (90 seconds) is detected. This allows the AI to reply to the *whole* thought, not just the first sentence.

### **3.6.2 Frontend: Next.js & D3.js**

The Coach Command Center is built on **Next.js** (React).

* **Data Visualization:** We use **D3.js** to render the complex Neo4j graph data into interactive "Constellation Maps" and "Word Clouds."  
* **Real-Time Sync:** The dashboard uses **Supabase Realtime** subscriptions. When **Aria** updates the database with new analysis, the Coach's view updates instantly without a page refresh, reinforcing the "God Mode" feeling of omniscience.

## **3.7 Observability & Economics**

### **3.7.1 Cost Circuit Breaker: Langfuse**

We integrate **Langfuse** deeply into the LLM calls.

* **Tagging:** Every token consumed and every GPU second used is tagged with the user\_id and coach\_id.  
* **Logic:** **Emilio** checks the cumulative monthly cost for a user before generating a response. If the cost exceeds $4.00, the system automatically degrades to **"Economy Mode"** (Text-Only replies), ensuring positive unit economics.

### **3.7.2 Privacy Layer**

* **Redaction:** Before **Aria** writes any data to the Neo4j graph, she passes the text through a local NLP redaction layer to strip names, addresses, and phone numbers. The graph stores psychological patterns, not surveillance data.  
* **Encryption:** All raw audio files in Supabase Storage are encrypted at rest using AES-256.
