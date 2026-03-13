# **6\. Core Workflows and Logic Loops**

## **6.1 The Cyclic Nature of Identity Engineering**

In traditional software architecture, workflows are linear: User logs in $\\rightarrow$ User performs action $\\rightarrow$ System saves state. The **Conscious Behavioral Change System** operates on a fundamentally different paradigm. To engineer identity, we must replicate the cyclic nature of human psychology. Our workflows are recursive loops that feed into one another, creating a flywheel of **Self-Perception Cybernetics**.

These workflows are orchestrated by **LangGraph**, which manages the state transitions of the user (e.g., moving from "Dormant" to "Primed" to "Active"). Within each state, **Pydantic AI** governs the reasoning logic, ensuring that every agentic action is constrained by the **Intelligence Library** and grounded in the **Context Premise** stored in **Neo4j**.

We define four primary logic loops that drive the system: The **Genesis Loop** (Setup), The **Daily Cybernetic Loop** (Production), The **Relevance Loop** (Research), and The **Safety Loop** (Crisis Management).

## **6.2 The Genesis Loop: From Stranger to Soul**

This workflow executes once per user. It transforms a generic "Client" into a fully mapped "Psychological Entity." It is the prerequisite for all future automation.

### **6.2.1 Intake & Soul Extraction**

* **Trigger:** A payment\_intent.succeeded webhook from **Stripe**.  
* **Agent Activation:** **Emilio (The Orchestrator)** initializes the user profile in **Supabase** and triggers the assessment flow.  
* **Psychometric Profiling:** The user interacts with the web-based **Noise Detector**. As they input data, **Aria (The Synthesizer)** processes the raw text using **Pydantic AI**. She does not just save string values; she performs **Entity Extraction** to populate the **Neo4j** graph.  
  * *Input:* "I hate feeling like a fraud at work."  
  * *Graph Action:* Create Insecurity Node ("Imposter Syndrome"); Link User to Insecurity with intensity: 0.9.  
* **Voice Cloning Calibration:** **Valeriane (Client Soul Extractor)** analyzes the Coach's uploaded content to establish the **TTT Baseline**. This ensures that when the system speaks to this specific user, it uses the Coach's specific metaphors and cadence.

### **6.2.2 Program Architecture (Atlas)**

Once the "Soul Data" is mapped, **Atlas (The Program Architect)** takes over.

* **Logic:** Atlas executes a deterministic algorithm to build the 30-day roadmap. He reads the Capacity\_Score (e.g., 35/100) and the Identity\_Pillar (e.g., "The Vessel").  
* **Query:** Atlas queries the **Ritual Pantry** in Supabase: SELECT \* FROM rituals WHERE level\_threshold \<= 3 AND identity\_fit \= 'Vessel'.  
* **Output:** A scheduled sequence of ritual\_id assignments is written to the user\_program table. This effectively "compiles" the coaching curriculum for the month, tailored to the user's current biological reality.

## **6.3 The Daily Cybernetic Loop: The Engine of Change**

This is the heartbeat of the system. It runs every 24 hours for every active user. It is an asynchronous state machine that moves the user from **Passive Observation** to **Active Evidence**.

### **6.3.1 State 1: Synthesis & Strategy (The Night Before)**

At 02:00 AM local time, a cron job triggers **Emilio**.

* **Context Retrieval:** **Emilio** pulls the user's history from **Supabase** and their psychological state from **Neo4j**.  
* **Strategy Selection:** **The Assembler (Strategist)** analyzes the data. It sees that yesterday the user failed their ritual due to "Time Constraints."  
* **Logic:** The Assembler consults the persuasion\_layers.yaml file. It selects **"The Challenger"** layer to provoke a reaction, paired with **Story Formula \#5** (Pain Amplification).  
* **Script Generation:** **The Artisan (Copywriter)** generates the script. It references the identity\_pillars.yaml to ensure the language targets the "Rebel" archetype. It inserts the specific "Enemy" node ("The Corporate Grind") extracted by **Aria**.  
* **Synthesis:** **The Voice** sends the script to **IndexTTS-2** on **Runpod**, applying **TTT-08** modulation (Fast, Direct, Raw). The audio file is encrypted and cached.

### **6.3.2 State 2: The "Vision Implant" (08:00 AM)**

* **Delivery:** **Emilio** pushes the cached audio to Telegram via **FastAPI**.  
* **The Psychological Gap:** The system enforces a 3-second delay managed by **Redis**.  
* **The Instruction:** The Text Block containing the ritual link is sent.  
* **Transition:** The user state moves to Waiting\_For\_Action.

### **6.3.3 State 3: The "Evidence" Capture (The Mirroring Effect)**

* **Stimulus:** The user listens to the audio (Vision Implant) and feels the social pressure of the **Mirroring Effect**.  
* **Response:** The user records a voice note: "I did the breathwork, but I felt stupid doing it."  
* **Ingestion:** The audio streams to **Groq**.  
* **Extraction:** **Aria** analyzes the transcript.  
  * *Signal:* "I did the breathwork" $\\rightarrow$ **Ritual Complete**.  
  * *Noise:* "I felt stupid" $\\rightarrow$ **New Insecurity Node** ("Fear of Judgment").  
* **Graph Update:** Aria updates the **Neo4j** graph, increasing the weight of the "Fear of Judgment" node. This ensures that tomorrow's script will address this specific insecurity using the **"Allay Fears"** persuasion angle.

### **6.3.4 State 4: The Evening Reflection (07:00 PM)**

* **Logic Check:** **Emilio** checks the ritual\_completion\_status.  
* **Branch A (Success):** If complete, **The Artisan** generates a **Confirmation Bias** message ("See? You are capable.").  
* **Branch B (Failure):** If incomplete, **Liliane (The Empathy Agent)** intercepts. She overrides the standard logic and deploys the **"Compassionate Retrieval"** protocol to prevent shame.

## **6.4 The Relevance Loop: The "Zeitgeist" Integration**

To prevent the AI from feeling "canned" or static, we run a parallel weekly loop that injects external context into the system.

* **Scanning:** **Maeva (Social Researcher)** scans the specific subreddits and forums identified in tribe\_soul.json. She looks for spikes in negative sentiment or new viral topics.  
* **Deep Dive:** **Lionel (Deep Researcher)** uses **Google Search API** to find "Contrarian Truths" or "Historical Parallels" related to these topics.  
* **Injection:** This data is compiled into a "Zeitgeist Context Object." When **The Assembler** runs the nightly strategy loop, it checks this object. If a topic reaches a relevance threshold, The Assembler overrides the standard curriculum to reference the current event (e.g., "I know the news about interest rates is scary right now..."). This makes the "Invisible App" feel alive and present in the real world.

## **6.5 The Safety Loop: The Crisis Circuit**

We are automating psychology, which carries inherent risk. The Safety Loop is a high-priority, interrupt-driven workflow designed to catch users falling through the cracks.

* **Sentiment Monitoring:** Every time **Aria** processes a user message, she assigns a Sentiment\_Score (-1.0 to \+1.0).  
* **The Trigger:** If the score drops below \-0.7, or if specific "Red Flag" keywords (e.g., "give up," "hopeless," "quit") are detected, the standard loop is **Halted**.  
* **The Interrupt:** **LangGraph** transitions the user state to Human\_Override.  
  1. The automated queue is paused.  
  2. A "Crisis Alert" is pushed to the Coach via the Dashboard.  
  3. The Coach enters **Operator Mode** to send a manual voice note.  
* **Resumption:** Only after the Coach manually clears the alert does the system resume the automated feedback loop, usually resetting the user to a "Recovery" track defined by **Atlas**.

## **6.6 Conclusion on Workflows**

These workflows represent the operational soul of the **Conscious Behavioral Change System**. By leveraging **Agentic Orchestration**, we move beyond simple "If This Then That" logic into complex, stateful, and context-aware behaviors.

We do not simply execute code; we simulate a relationship. **Emilio** manages the time, **Aria** manages the memory, **The Assembler** manages the strategy, and **The Voice** manages the emotion. Together, they form a cohesive digital organism dedicated to the user's transformation.
