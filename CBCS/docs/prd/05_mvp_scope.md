# **5\. MVP Scope**

## **5.1 Strategic Scope Definition: The Cybernetic Engine**

The primary strategic objective of this Minimum Viable Product (MVP) is to validate the **"Identity Engineering"** hypothesis. We are testing whether a system designed around **Self-Perception Cybernetics**—specifically, the injection of high-fidelity behavioral "Training Data" via a Voice-First interface—can successfully resolve **Cognitive Dissonance** and shift the identity of the 50-65 demographic.

To achieve this validation, the MVP cannot be a "lite" version of a habit tracker or a simple chatbot wrapper. It must be a complete, vertically integrated **Agent-Orchestrated System**. We must deliver the full **Feedback Loop**: Assessment (Noise Detection) $\\rightarrow$ Research (Relevance) $\\rightarrow$ Assembly (Neuro-Persuasion) $\\rightarrow$ Priming (Vision Implant) $\\rightarrow$ Action (Evidence Generation) $\\rightarrow$ Reflection (Identity Shift).

While we are aggressively removing the client-side visual interface to eliminate "Compliance Fatigue," the backend logic and coach-facing tools must be robust enough to support a paid commercial launch immediately. The system must operate as a **"Psychological Operating System,"** capable of managing the complex state transitions of human emotion without breaking the "Illusion of Presence."

The MVP consists of seven distinct components defined below, engineered to ensure high fidelity, low latency, and economic viability via a $5.00/user margin model.

---

## **5.2 Core Technology Stack (The Non-Negotiables)**

The following technology choices are locked constraints for the MVP. This stack has been specifically selected to support the unique requirements of an **Event-Driven**, **High-Intimacy**, and **Psychologically Safe** system. We are moving away from a generic CRUD architecture to a specialized **Agentic Engineering** infrastructure.

### **A. The Interface Layer**

* **Client Interface (B2C): Telegram Bot API.** This replaces the PWA entirely. We utilize Telegram's cloud-native architecture for unlimited message history, secure file transfer, and rich media handling. By leveraging the platform where the user already resides ("The Digital Living Room"), we reduce the friction of adoption to near zero.  
* **Coach Interface (B2B): Next.js (React).** Hosted on **Vercel**. This provides the desktop-first "Master Composer" command center for the professional coach, utilizing **Tailwind CSS** for rapid UI development and **D3.js** for visualizing complex psychological data (Word Clouds, Context Premise Graphs).

### **B. The Intelligence & Logic Layer**

* **Orchestration Engine: LangGraph.** This handles the state management of the system. Since our interaction model requires complex temporal logic (e.g., "Wait for silence," "Pause for human intervention," "Transition from Sleep to Morning Prime"), we utilize **LangGraph** to maintain a persistent state machine for every user. It manages the cyclic workflows that stateless serverless functions cannot handle alone.  
* **Reasoning Engine: Pydantic AI.** This is the primary framework for defining our AI agents. Unlike raw API calls which return unstructured text, **Pydantic AI** enforces strict type safety on LLM outputs. It acts as the "Pre-Frontal Cortex," ensuring that the **Strategist Agent** selects a valid **Cognitive Bias** and **Story Formula** before the script is generated.  
* **The "Brain" (LLM): MiniMax-M2.** We utilize the **MiniMax-M2** model via its direct API endpoints to leverage its "Interleaved Thinking" (Chain of Thought) capabilities. This model offers the highest reasoning-to-cost ratio for empathetic tasks and is specifically tuned to handle the nuance of our **Context Premise** mapping.  
* **Backend Framework: FastAPI.** We use Python-based **FastAPI** for the core server logic. It is specifically chosen for its native support for asynchronous **BackgroundTasks**, allowing us to immediately acknowledge Telegram webhooks (preventing timeout loops) while processing heavy AI logic in detached worker threads.

### **C. The Memory & Data Layer (Hybrid Architecture)**

* **Relational Database: Supabase (PostgreSQL).** Acts as the primary system of record for Auth, User Profiles, Billing Status, and Ritual Logs. Crucially, we utilize **pgvector** within Supabase to store the semantic embeddings of the Coach’s content for the **RAG (Retrieval Augmented Generation)** pipeline.  
* **Graph Database: Neo4j.** To enable "God Mode" insights and deep personalization, we map the non-linear relationships between a client’s identity and their behaviors. **Neo4j** stores the "Psychological Graph" (e.g., Client $\\rightarrow$ BLOCKED\_BY $\\rightarrow$ Fear: Poverty). This graph structure enables the **Neuro-Persuasion Engine** to query complex emotional patterns that SQL cannot handle efficiently.

### **D. The Generative Media Layer (The Senses)**

* **Voice Synthesis: IndexTTS-2 (Self-Hosted).** We host **IndexTTS-2** on **Runpod** Serverless GPU instances. We require absolute control over the prosody, breathing patterns, and emotional warmth of the voice to maintain the **"Mirroring Effect."** Standard cloud APIs are too robotic. The voice must be able to switch between **TTT-02 (Compassionate)** and **TTT-08 (Raw Confrontation)** dynamically based on the instructions from the **Strategist Agent**.  
* **Transcription: Groq (Whisper Large v3).** We utilize **Groq** for all Speech-to-Text operations. We chose Groq to solve the "Long Audio" problem cost-effectively ($0.03/hour), enabling users to send 15-minute "therapeutic vents" without exploding inference costs.

### **E. The Economic & Security Layer**

* **Payments: Stripe Connect.** The engine for the business model. We utilize Destination Charges to split payments automatically ($95 to Coach, $5 to Platform).  
* **Observability: Langfuse.** We mandate full tracing of every agent interaction. **Langfuse** tracks latency, token usage, and cost per conversation at the user\_id level, allowing us to enforce the "Cost Circuit Breaker."

---

## **5.3 Component 1: The Intelligence Library (The Kernel)**

Before any agent can operate, the MVP must include the **Intelligence Library**. These are the static, version-controlled configuration files that serve as the "Textbooks" for the AI. They reside in /backend/intelligence\_library/ and are injected into every agent's runtime environment via **Pydantic AI** dependency injection.

**Scope of Library Assets:**

* **identity\_pillars.yaml**: Definitions of the 7 Identity Pillars (Rebel, Maker, Vessel, etc.), including their specific vocabulary, shadow traits, and motivational triggers.  
* **ttt\_matrix.yaml**: The physics of the 9 TTT levels (10°F \- 100°F). This defines the syntax rules (e.g., "No contractions for TTT-01," "Short staccato sentences for TTT-08") that **The Artisan** must follow.  
* **persuasion\_layers.yaml**: The logic structures for the 9 Layers of Persuasion (e.g., "The Challenger," "Black & White Philosophy").  
* **story\_formulas.yaml**: The 16 Story Insight Formulas (e.g., DHD \+ Dreams \+ Enemy) used to construct the narrative arc.  
* **context\_premise\_map.json**: The taxonomy of the 12 dimensions (Frustrations, Fears, Enemies, etc.) used by **Aria** for entity extraction.

---

## **5.4 Component 2: The Noise Detector (Assessment Engine)**

The Assessment Engine is the input terminal for the system. It establishes the "Ground Truth" required to program the Identity Shift. This component involves both a web interface for the user and a background agentic process for the Coach.

### **5.4.1 The Setup Agents (Coach Onboarding)**

Before the client ever sees the system, the Coach must be onboarded. We deploy specific agents to clone the Coach's genius.

* **Kimya (Business Analyst):** An agent that interviews the Coach to extract their business model and "Unique Mechanism." She configures the initial logic of the Pantry.  
* **Valeriane (Client Soul Extractor):** An agent that ingests the Coach's historical content (videos, emails) to build the client\_soul.json. She maps the Coach's metaphors and TTT baseline to ensure the voice clone is accurate.  
* **Dilaya (Tribe Soul Extractor):** An agent that analyzes the target audience's digital footprint to build the tribe\_soul.json. She identifies the slang and cultural totems of the user base.

### **5.4.2 The User Assessment (Web View)**

A responsive web application linked from the Telegram onboarding flow.

* **Context Premise Mapping:** The assessment includes specific probe questions designed to map the user's 12-dimensional **Soul Data**. Users describe their Frustrations, Dreams, Enemies, and Fears.  
* **Graph Construction:** This data is parsed and stored as nodes in **Neo4j**, linking the User to specific concepts.  
* **Capacity Scoring:** The system calculates a Capacity\_Score (0-100) based on energy levels and time availability.  
* **Identity Pillar Identification:** Based on the user's language patterns, the system assigns a primary **Identity Pillar**.

### **5.4.3 Atlas (The Program Architect)**

Once the assessment is complete, **Atlas** activates.

* **Function:** Atlas reads the user's assessment data and the Coach's **Pantry**.  
* **Output:** Atlas constructs the initial 30-day roadmap. He selects the specific sequence of rituals that matches the user's Capacity Score and Identity Pillar. If the user is low-capacity, he builds a "Recovery Ramp-Up." If high-capacity, he builds a "High-Performance Sprint." This schedule is stored in **Supabase**.

---

## **5.5 Component 3: The Neuro-Persuasion Engine (Intelligence Layer)**

This is the "Brain" that connects the Coach's Pantry to the Client's Needs. It runs asynchronously every night to prepare the "Training Data" for the next day.

### **5.5.1 Emilio (The Orchestrator)**

**Emilio** is the master controller. He manages the **LangGraph** state machine. He decides when to call the Researcher, the Strategist, or the Artisan. He ensures the workflow adheres to the defined state transitions (e.g., Sleep $\\rightarrow$ Priming $\\rightarrow$ Action $\\rightarrow$ Reflection).

### **5.5.2 The Assembler (The Strategist)**

**The Assembler** is the logic core. It does not write text; it designs the strategy.

* **Selection Logic:** Every morning, The Assembler queries the **Neo4j** graph for the User's current state (Identity \+ Capacity \+ Pain Point).  
* **Lego Block Selection:** It queries the **Pantry** for the matching ritual (e.g., "Deep Work Video").  
* **Persuasion Layer Selection:** It consults persuasion\_layers.yaml. Based on the user's Trust Score and recent history, it selects the optimal persuasion angle.  
  * *Example:* If the user is a "Rebel" and is "Stuck," it selects **The Challenger**.  
* **Story Formula Selection:** It selects the narrative structure (e.g., DHD \+ Dreams \+ Enemy) that will frame the ritual.

### **5.5.3 The Artisan (The Copywriter)**

**The Artisan** takes the strategy object from The Assembler and generates the final script using **MiniMax-M2**.

* **TTT Application:** It references ttt\_matrix.yaml to apply the specific syntax rules of the selected voice (e.g., "TTT-08 Raw Confrontation").  
* **Formula Filling:** It fills the slots of the Story Formula with the specific nouns extracted from the user's Context Premise (e.g., replacing \[Enemy\] with "The Corporate Grind").  
* **The Challenger Logic:** When executing the Challenger layer, The Artisan must use **Reverse Psychology** as bait. It must *not* say "I bet you can't." It must say: *"Maybe you are actually comfortable letting \[Enemy\] win. If you weren't, you would have done the work by now."*

---

## **5.6 Component 4: The Rapport Interface (Client Telegram Interface)**

The "Invisible App" that delivers the intervention and captures the evidence. It is hosted entirely within Telegram.

### **5.6.1 The "Vision Implant" (Morning Loop)**

* **Trigger:** 08:00 AM (User Local Time).  
* **The Voice (Speaker Agent):** Sends the script to **IndexTTS-2** on Runpod. It modulates the audio properties (Speed, Breathiness) to match the TTT state.  
* **Delivery:** The audio is sent to the user.  
* **The "Mental Model" Prompt:** The audio explicitly guides the user to *visualize* the action ("Close your eyes. See yourself doing it"). This leverages the **Availability Heuristic**.  
* **Instruction Block:** 3 seconds later, the Text Block arrives with the link to the ritual content. This "Psychological Gap" ensures the user consumes the emotion before the logic.

### **5.6.2 The "Evidence Printing" (Evening Loop)**

* **Trigger:** 07:00 PM.  
* **Compassionate Retrieval:** If the ritual is pending, **Liliane (The Empathy Agent)** activates. She uses the "Allay Fears" or "Justify Past Failures" persuasion angles to extract the RFF (Reason for Failure) without shame.  
* **Evidence Locking:** If the ritual is complete, the Agent uses "Confirmation Bias" to validate the identity shift ("You proved you are an athlete today").  
* **Visual Reward:** The system generates a simple "Streak Flame" or "Evidence Card" image to reinforce the success.

### **5.6.3 Aria (The Synthesizer)**

The input processor for Voice Journaling.

* **Transcription:** Streams audio to **Groq** (Whisper Large v3) for instant text conversion.  
* **Entity Extraction:** Aria parses the transcript to extract **Soul Data**. She identifies new "Fears," "Enemies," or "Success Markers" and updates the **Neo4j** graph.  
* **Signal Extraction:** She identifies "Identity Signals" (e.g., "I felt powerful") to be used as **Favorable Evidence** in future scripts.

---

## **5.7 Component 5: The Master Composer (Coach Dashboard)**

The Coach Dashboard is the control center. It replaces the complex "Course Builder" with a streamlined "Component Pantry."

### **5.7.1 The Component Pantry (Ingredient Manager)**

The Coach acts as the Master Composer. They do not build linear schedules. They upload atomic units of transformation.

* **Asset Upload:** Support for Video (YouTube/Vimeo links), Audio (MP3), and PDF worksheets.  
* **4-Dimensional Tagging:** The Coach tags these components to define their fit:  
  * **Identity Fit:** "Good for Rebels," "Good for Makers."  
  * **Goal Fit:** "Fixes Sleep," "Fixes Anxiety."  
  * **Level:** "Beginner (Low Capacity)," "Advanced (High Capacity)."  
* **The Starter Pack:** The MVP ships with the **12 Core Ritual Categories** pre-loaded and pre-tagged.

### **5.7.2 The "Cohort Vibe" Visualization**

To provide leverage, the dashboard synthesizes individual data into aggregate insights.

* **Word Cloud Engine:** **Pydantic AI** analyzes the last 24 hours of client journals to extract high-frequency emotional keywords. These are visualized as a Word Cloud.  
* **Red Flag Feed:** A filtered list of clients who are "Stuck" (high dissonance, missed rituals), flagged by **Liliane**. The Coach can click "Intercept" to send a Telegram voice note directly.

---

## **5.8 Component 6: The Research Engine (The Zeitgeist)**

To ensure the system feels "alive" and culturally relevant, we include a weekly research loop.

### **5.8.1 The Research Team**

* **Maeva (Social Researcher):** Scans social media and forums for Tribe-specific sentiment shifts.  
* **Lionel (Deep Researcher):** Conducts deep research on the "Theme of the Week" using the **7 Planning Dimensions**:  
  1. **Historical Evolution & Temporal Contrast.**  
  2. **Contrarian Analysis & Hidden Truths.**  
  3. **Emotional Landscape & Human Stories.**  
  4. **Data-Driven Reality Check.**  
  5. **Cultural Zeitgeist & Trend Analysis.**  
  6. **Cross-Disciplinary Frameworks & Metaphors.**  
  7. **Viral Potential Assessment.**  
* **The News Agent:** Connects to **Tavily** to fetch trending news relevant to the Soul Tribe.

### **5.8.2 Relevance Injection**

This data is fed into **The Assembler** (Strategist). This allows the system to generate scripts that reference current events (Recency) and cultural moments (Zeitgeist), preventing the content from feeling "canned."

---

## **5.9 Component 7: The Economic & Security Infrastructure**

The infrastructure that makes the business model viable and safe.

### **5.9.1 Stripe Connect Integration**

* **Split Payments:** The system utilizes **Stripe Connect** (Destination Charges).  
* **Logic:** Upon a successful $100 program purchase, the system routes $95 to the Coach and $5 to the Platform.  
* **Gating:** The Telegram onboarding link is only generated *after* the payment webhook is verified.

### **5.9.2 Cost Circuit Breaker (Langfuse)**

* **Monitoring:** **Langfuse** tracks the cumulative cost of LLM tokens and GPU seconds for each user\_id.  
* **The Threshold:** If a user's cost exceeds $4.00 in a billing cycle, **LangGraph** transitions them to "Economy Mode."  
* **Economy Mode:** The Agent switches to Text-Only replies (saving voice generation costs) and reduces the frequency of proactive check-ins.

### **5.9.3 The "Glass Wall" Protocol**

* **Privacy:** All Voice Notes are encrypted at rest. Audio processed by **Groq** is held in ephemeral memory only.  
* **Redaction:** Before data enters the **Neo4j** graph, a local NLP layer redacts names and PII, ensuring the psychological map tracks patterns, not identities.

---

## **5.10 Out of Scope for MVP**

To ensure we can deliver this complex, high-fidelity system within the timeline, the following are explicitly excluded:

* **Client PWA / Native App:** Retired entirely. There is no client-facing website or app store download.  
* **Real-Time Voice Streaming:** We are using asynchronous Voice Notes (files), not LiveKit/WebRTC telephony. The "Live Call" feature is reserved for a future update.  
* **Direct B2C Signups:** Clients must be added via a Coach invite or a specific Funnel entry point.  
* **Group Chats:** The system supports 1-on-1 coaching only. Community happens via Zoom/Facebook, not inside the Telegram bot.  
* **Video Hosting:** We rely on Unlisted YouTube links. We are not building a video streaming backend.  
* **Funnel Builder UI:** We are not building a drag-and-drop website builder. Marketing pages are handled externally; the system only manages the Checkout/Entry link.  
* **Complex Visual Logic Editors:** The "Ritual Builder" is a form-based tagging system, not a visual node editor.

---

## **5.11 Summary of MVP Architecture**

This scope defines a system that is:

* **Scientifically Grounded:** Built on Self-Perception Theory and Cognitive Dissonance.  
* **Psychologically Intelligent:** Using Context Premises, 9-Layer Persuasion, and 7 Cognitive Biases defined in the Intelligence Library.  
* **Technically Advanced:** Leveraging Agent Orchestration (Emilio, Aria, Atlas), Graph Databases (Neo4j), and Generative Voice (IndexTTS-2).  
* **Economically Sustainable:** Protected by split payments and cost circuit breakers.

It is a machine designed to turn "Noise" into "Signal," and "Goals" into "Identity."
