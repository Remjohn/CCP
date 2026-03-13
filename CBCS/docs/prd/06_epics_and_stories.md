# **6\. Epic & Story Structure**

The development roadmap for the **Conscious Behavioral Change System** is structured around eight sequential Epics. These Epics represent the biological evolution of the digital organism we are building. We do not build "features" in isolation; we build "systems" that layer upon one another.

The build sequence follows the **Biological Imperative**:

1. **Nervous System:** Connectivity and State Management (Epic 1).  
2. **Senses & Memory:** Perception and Storage (Epic 2).  
3. **Soul & Logic:** The Static Intelligence Library (Epic 3).  
4. **Brain:** Reasoning and Strategy (Epic 4).  
5. **Voice:** Expression and Delivery (Epic 5).  
6. **Awareness:** External Context and Research (Epic 6).  
7. **Control:** The Coach's Interface (Epic 7).  
8. **Survival:** Economics and Safety (Epic 8).

This structure ensures that at every stage of development, the system is functional, testing the critical integration points between **LangGraph**, **Pydantic AI**, and the **Neo4j** graph database.

---

## **Epic 1: The Core Ingress & Cognitive Pipeline (The Nervous System)**

**Goal:** To establish the fundamental ability of the system to "Hear," "Transcribe," and "Think" within the constraints of a real-time chat interface. This Epic focuses on the **FastAPI** webhook architecture, the **Redis** "Listening Window," and the structured reasoning engine.

### **Story 1.1: The High-Concurrency Telegram Webhook**

As a System,

I want to receive high-volume messages from Telegram via a webhook endpoint that immediately acknowledges receipt,

So that I do not trigger Telegram's retry logic while processing heavy AI workloads.

* **Technical Context:** **FastAPI** running on serverless containers.  
* **Acceptance Criteria:**  
  * The endpoint must cryptographically verify the X-Telegram-Bot-Api-Secret-Token signature.  
  * Upon receipt of a payload, the system must return a 200 OK status code within 200ms, regardless of the processing load.  
  * The actual message processing logic (parsing, routing) must be spawned as a **FastAPI BackgroundTask**, completely decoupled from the response thread.  
  * The system must accurately classify incoming payloads into Audio, Text, Photo, or Command and route them to the appropriate handler.  
* **Failure Mode:** If the background task fails, the error must be logged to **Langfuse**, but the Telegram API must *not* receive an error code (to prevent infinite retry loops).

### **Story 1.2: The "Listening Window" Buffer (Redis)**

As a Client,

I want to be able to send five rapid-fire messages (a "stream of consciousness") without the bot interrupting me after the first sentence,

So that I feel heard rather than managed.

* **Technical Context:** **Redis** for ephemeral buffering; **LangGraph** for state management.  
* **Acceptance Criteria:**  
  * When the first message arrives, **Emilio (The Orchestrator)** must initiate a Listening\_Window state and start a configurable 5-minute timer.  
  * Subsequent messages must be appended to a **Redis List** keyed by the user\_id.  
  * The generative pipeline must *only* trigger when one of two conditions is met: (A) The 5-minute hard timer expires, OR (B) A "Soft Silence" interval of 90 seconds is detected.  
  * During the buffering phase, the system must send a "Typing..." or "Recording audio..." status action to Telegram every 4 seconds to signal presence.

### **Story 1.3: Long-Audio Transcription via Groq**

As a Client,

I want to send a 15-minute voice note venting about my day,

So that I can process my emotions without hitting file size limits or waiting minutes for a reply.

* **Technical Context:** **Groq** API (Whisper Large v3).  
* **Acceptance Criteria:**  
  * The system must accept .ogg and .opus audio files directly from the Telegram API URL.  
  * The file binary stream must be piped directly to **Groq** for transcription without intermediate transcoding (saving compute latency).  
  * Transcription must complete in under 5 seconds for a 10-minute audio file.  
  * The raw transcript must be stored in the **Supabase** daily\_logs table.  
  * **Privacy Requirement:** The raw audio file must be purged from the inference server memory immediately after processing.

---

## **Epic 2: The Noise Detector & Graph Memory (The Senses)**

**Goal:** To build the "Memory" of the system. This Epic focuses on the Assessment Engine and the **Neo4j** integration that maps the **Context Premise**.

### **Story 2.1: The Baseline Assessment Web App**

As a User,

I want to complete a deep psychological intake via a frictionless web interface,

So that the system understands my specific context and constraints.

* **Technical Context:** **Next.js** Web Form linked to **Supabase** (Relational) and **Neo4j** (Graph).  
* **Acceptance Criteria:**  
  * A responsive web form accessible via a unique tokenized link sent in Telegram.  
  * The form must capture the 12 dimensions of the **Context Premise** (Frustrations, Wants, Dreams, Fears, Suspicions, Insecurities, Envy, Enemies, Coping Mechanisms, Hidden Beliefs, Emotional Triggers, Success Markers).  
  * Upon submission, the system must calculate the Capacity\_Score (0-100) based on energy/time inputs.  
  * The system must identify the dominant **Identity Pillar** based on linguistic patterns in the user's responses.

### **Story 2.2: Context Premise Graph Construction**

As a System,

I want to parse assessment data into a graph structure,

So that the Agent can query specific relationships between the user and their psychological blockers.

* **Technical Context:** **Pydantic AI** Entity Extractor \+ **Neo4j**.  
* **Acceptance Criteria:**  
  * The extraction agent (**Aria**) must parse text inputs into nodes and edges.  
  * **Example:** Input: "I hate my boss." $\\rightarrow$ Create Node (Enemy: "Boss") $\\rightarrow$ Create Edge (User)-\[:FIGHTS\]-\>(Enemy).  
  * **Example:** Input: "I want to retire on a beach." $\\rightarrow$ Create Node (Dream: "Beach Retirement") $\\rightarrow$ Create Edge (User)-\[:CRAVES\]-\>(Dream).  
  * The graph schema must support all 12 Context Premise dimensions.

### **Story 2.3: The Voice Journaling Extraction Pipeline**

As a System,

I want to extract structured data from unstructured daily voice journals,

So that the psychological map evolves over time as the user changes.

* **Technical Context:** **Aria (The Synthesizer)** using **Pydantic AI**.  
* **Acceptance Criteria:**  
  * When a user sends a daily journal, the transcript is passed to Aria.  
  * Aria must identify new entities: "I felt strong today" $\\rightarrow$ Create Identity\_Signal node with positive polarity.  
  * Aria must identify **Context Shifts**: "I'm not scared of my boss anymore" $\\rightarrow$ Decrease intensity of the (User)-\[:FEARS\]-\>(Enemy: Boss) relationship.  
  * This updated graph data must be available for **The Assembler** immediately for the next day's generation.

---

## **Epic 3: The Intelligence Library & Logic Kernel (The Soul)**

**Goal:** To define the static psychological laws that govern the system. This prevents the AI from hallucinating its own coaching methodology.

### **Story 3.1: The Library File System**

As a Developer,

I want a centralized repository of YAML configuration files,

So that I can update the coaching methodology without deploying new code.

* **Technical Context:** Git-versioned YAML files in /backend/intelligence\_library/.  
* **Acceptance Criteria:**  
  * Create identity\_pillars.yaml: Definitions of the 7 Archetypes.  
  * Create ttt\_matrix.yaml: Syntax rules for the 9 Voice Levels.  
  * Create persuasion\_layers.yaml: Logic for the 9 Persuasion Strategies.  
  * Create story\_formulas.yaml: The 16 Narrative Structures.  
  * Create context\_premise\_map.json: The taxonomy of the 12 dimensions.

### **Story 3.2: Runtime Injection via Pydantic AI**

As a System,

I want to inject these configuration files into the Agent's dependency context at runtime,

So that the LLM is constrained by the specific definitions of the Intelligence Library.

* **Technical Context:** **Pydantic AI** AgentDeps.  
* **Acceptance Criteria:**  
  * When **The Assembler** is initialized, it must load the persuasion\_layers.yaml into its context.  
  * The System Prompt must explicitly reference these files: "You are The Assembler. Consult the persuasion\_layers provided in your context..."  
  * The Agent must fail to start if these files are missing or malformed (Fail Fast).

---

## **Epic 4: The Neuro-Persuasion Engine (The Brain)**

**Goal:** To build the "Brain" that decides *how* to speak to the user. This Epic focuses on **The Assembler** (Strategist) and **The Artisan** (Copywriter).

### **Story 4.1: The Dynamic Assembler (Lego Block Selection)**

As a System,

I want to select the correct "Ritual Variant" based on the user's real-time state,

So that I never assign a task that is too hard (Burnout) or too easy (Boredom).

* **Technical Context:** **The Assembler** Agent querying **Supabase** and **Neo4j**.  
* **Acceptance Criteria:**  
  * **Hue 1 (Capacity):** The system must compare the user's Capacity\_Score against the Level\_Threshold of the ritual. If Capacity \< 30, force select the "Micro-Habit" variant.  
  * **Hue 2 (Identity):** The system must match the Identity\_Pillar tag of the user to the Voice\_Wrapper of the ritual.  
  * **Hue 3 (Goal):** The system must match the user's Primary\_Pain to the Goal\_Fit tag of the ritual.  
  * **Output:** The query must return a single, specific media\_url and script\_template.

### **Story 4.2: The Story Insight Formula Synthesis**

As a System,

I want to construct the "Vision Implant" script using proven persuasion architecture,

So that the message triggers "Hot Cognition."

* **Technical Context:** **The Assembler** utilizing **Neo4j** queries.  
* **Acceptance Criteria:**  
  * The system must dynamically select one of the **16 Story Insight Formulas** based on the retrieved **Context Premise**.  
  * **Example Logic:** If Context contains "Enemies" and "Fears," select **Formula \#6** (DHD \+ Dreams \+ Enemies \+ Fears).  
  * The system must inject the specific nouns from the Neo4j graph into the formula slots (e.g., replace \[Enemy\] with "The Corporate Grind").  
  * The generated script must follow the **"Rapport-First"** structure: Validation $\\rightarrow$ Bias Trigger $\\rightarrow$ Vision Implant.

### **Story 4.3: The "Challenger" Logic Implementation**

As a Coach,

I want the AI to use Reverse Psychology on rebellious users,

So that I can bypass their resistance to authority.

* **Technical Context:** **The Artisan** Agent Prompt Engineering.  
* **Acceptance Criteria:**  
  * When **The Assembler** selects the **"Challenger"** layer, **The Artisan** must generate a script that uses **Reverse Psychology**.  
  * **Constraint:** The script must NOT say "I bet you can't." It MUST say something akin to: "Maybe you are comfortable letting \[Enemy\] win. If you weren't, you would have acted by now."  
  * **TTT Enforcement:** This layer must trigger **TTT-08 (Raw Confrontation)** syntax: short sentences, direct address, zero hedging.

---

## **Epic 5: The Generative Media Layer (The Voice)**

**Goal:** To establish the "Mouth" of the system. This Epic focuses on high-fidelity voice synthesis and the **"Vision Implant"** delivery.

### **Story 5.1: IndexTTS-2 Host Configuration (Runpod)**

As a Coach,

I want the AI to speak with my exact prosody and breathiness,

So that the client suspends disbelief and feels they are talking to me.

* **Technical Context:** Self-hosted **IndexTTS-2** on **Runpod** GPU.  
* **Acceptance Criteria:**  
  * The system must successfully load the Coach’s cloned voice weights into GPU VRAM.  
  * The inference API must accept text and a **TTT Style Parameter**.  
  * **Style Mapping:**  
    * TTT-02 (Compassionate) $\\rightarrow$ Speed 0.85x, Breathiness High.  
    * TTT-08 (Challenger) $\\rightarrow$ Speed 1.1x, Breathiness Low, Pitch Dynamic.

### **Story 5.2: The "Keep-Warm" Scheduler**

As a User,

I want the voice note to arrive quickly after I see the "Recording..." status,

So that the interaction feels conversational.

* **Technical Context:** Cron Jobs hitting Runpod endpoints.  
* **Acceptance Criteria:**  
  * A scheduler must ping the GPU endpoint every 4 minutes during the "Peak Window" (07:00 AM \- 10:00 AM Client Time).  
  * This ping must force the container to stay "Warm," preventing the 15-second Cold Start latency.

### **Story 5.3: The Instruction Block Delay Queue**

As a Client,

I want to listen to the emotional support message before I see the logistical task,

So that I don't feel overwhelmed by a "To-Do" list immediately.

* **Technical Context:** Asynchronous sequencing via **Redis**.  
* **Acceptance Criteria:**  
  * The system must execute a strict outbound sequence:  
    1. Send Voice Note (Audio).  
    2. Wait **3000ms** (Sleep).  
    3. Send Instruction Block (Text \+ Link).  
  * **Logic:** This delay allows the **Availability Heuristic** to set in during the "Vision Implant" phase.

---

## **Epic 6: The Research & Relevance Engine (The Zeitgeist)**

**Goal:** To ensure the system feels "Alive" and culturally plugged-in.

### **Story 6.1: The Social Researcher (Maeva)**

As a System,

I want to know what my Soul Tribe is talking about this week,

So that I can reference it in my coaching.

* **Technical Context:** **Maeva** Agent using **Tavily** and social scraping.  
* **Acceptance Criteria:**  
  * Maeva must scan specific subreddits, forums, and news sources defined in tribe\_soul.json.  
  * She must output a "Sentiment Report" identifying the top 3 emotional themes of the week (e.g., "Anxiety about interest rates").  
  * This report must be injected into **The Assembler's** context for the week.

### **Story 6.2: The Deep Researcher (Lionel)**

As a Coach,

I want the AI to use deep facts and history to support its advice,

So that I sound like an expert, not a cheerleader.

* **Technical Context:** **Lionel** Agent using **Google Search API**.  
* **Acceptance Criteria:**  
  * Lionel must execute the **7 Planning Dimensions** search (Historical, Contrarian, Scientific, etc.).  
  * He must produce a "Fact Bank" for the current coaching theme.  
  * **The Artisan** must effectively use these facts to create "Data-Driven Reality Checks" in the scripts.

---

## **Epic 7: The Master Composer (Coach Dashboard)**

**Goal:** To provide the Coach with the "Pantry" to store ingredients and the "Lens" to view the cohort.

### **Story 7.1: The Component Pantry UI**

As a Coach,

I want to upload and tag ritual content easily,

So that the AI knows when to use it for specific user types.

* **Technical Context:** **Next.js** Dashboard \+ **Supabase Storage**.  
* **Acceptance Criteria:**  
  * A "Drag and Drop" interface for Video/Audio files.  
  * A **Tagging Interface** that forces the coach to define the **4-Dimensional Attributes**:  
    * **Level Threshold:** Slider (Micro $\\rightarrow$ Standard $\\rightarrow$ Heroic).  
    * **Identity Fit:** Multi-select (Rebel, Maker, Seeker, etc.).  
    * **Goal Fit:** Dropdown (Sleep, Energy, Focus, Anxiety).  
  * The system must visually indicate "Gaps" in the pantry (e.g., "Warning: You have no rituals for 'High Anxiety Rebels'").

### **Story 7.2: The "Cohort Vibe" Word Cloud**

As a Coach,

I want to see the aggregate mood of my clients,

So that I can intuitively understand the group's energy without reading 500 transcripts.

* **Technical Context:** Aggregated NLP Analysis via **Pydantic AI** \+ **D3.js**.  
* **Acceptance Criteria:**  
  * The system must analyze the last 24 hours of client journals from the Neo4j graph.  
  * It must extract high-frequency emotional adjectives (e.g., "Tired," "Proud," "Stuck").  
  * It must render a **Word Cloud** on the dashboard home screen where font size correlates to frequency.  
  * **Interactivity:** Clicking a word (e.g., "Tired") must filter the client list to show the specific users who expressed that emotion.

### **Story 7.3: Atlas (The Program Architect)**

As a System,

I want to automatically build a 30-day schedule for a new user,

So that the Coach doesn't have to manually assign 30 videos.

* **Technical Context:** **Atlas** Agent logic.  
* **Acceptance Criteria:**  
  * Atlas must read the user's Capacity\_Score and Identity\_Pillar.  
  * It must traverse the Pantry and select a sequence of 30 rituals.  
  * **Logic:** If Capacity is Low, Week 1 must be 100% "Micro-Habits." If Capacity is High, Week 1 starts with "Standard" intensity.  
  * The schedule must be saved to the user\_program table in Supabase.

---

## **Epic 8: The Economic & Security Infrastructure**

**Goal:** To ensure the business model works and the data is safe.

### **Story 8.1: Stripe Connect Split Payments**

As a Platform,

I want to automatically take $5.00 from every client subscription,

So that I can pay for the GPU costs without invoicing the Coach manually.

* **Technical Context:** **Stripe Connect** Destination Charges.  
* **Acceptance Criteria:**  
  * When a user pays via the Funnel, the transaction must reference the Coach's stripe\_account\_id.  
  * The transaction metadata must define application\_fee\_amount: 500 (cents).  
  * The webhook payment\_intent.succeeded must trigger the provisioning of the Supabase user account and the generation of the Telegram onboarding link.

### **Story 8.2: Cost Circuit Breaker (Langfuse)**

As a Business,

I want to limit the AI usage of "Power Users" who chat excessively,

So that they don't erode the profit margin.

* **Technical Context:** **Langfuse** Token Tracking.  
* **Acceptance Criteria:**  
  * The system must track cumulative cost per user\_id per month (Tokens \+ GPU Seconds).  
  * If cost \> $4.00, **Emilio** must transition the user to Economy\_Mode.  
  * In Economy\_Mode, **The Voice** agent is bypassed, and the system sends text-only replies.

### **Story 8.3: The "Glass Wall" Privacy Protocol**

As a User,

I want to know my sensitive voice notes are secure,

So that I feel safe sharing vulnerable truths.

* **Technical Context:** **Supabase** RLS & Encryption.  
* **Acceptance Criteria:**  
  * All audio files in Storage buckets must be encrypted at rest.  
  * **Row Level Security (RLS)** policies must strictly enforce that Coach A cannot query the data of Coach B.  
  * The **Groq** transcription worker must demonstrate "Ephemeral Processing"—proving that audio buffers are wiped from memory immediately after text extraction.  
  * **Aria** must redact PII (Names, Addresses) before writing nodes to **Neo4j**.
