# **2\. Requirements**

This section defines the functional and non-functional specifications for the **Conscious Behavioral Change System**. The system is architected not as a linear application, but as a **"Cognitive Bias Navigation Engine"** designed to guide the user through the psychological stages of **Programmable Identity Shift**.

To visualize the engineering challenge, we utilize the analogy of **LoRA (Low-Rank Adaptation)** from Generative AI. We treat the user's current identity as a "Base Model" full of "Noise" (Cognitive Dissonance, Limiting Beliefs). The system functions as a fine-tuning engine, injecting high-fidelity "Training Data" (Behavioral Rituals) wrapped in specific "Prompts" (Persuasive Scripts) to denoise the user's self-perception and align it with their desired goal.

The architecture is composed of specific **Intelligence Engines**, each managed by a specialized **Agentic Workforce**. These agents do not operate in isolation; they are orchestrated by **LangGraph** to ensure data flows seamlessly from assessment to persuasion to action.

## **2.1 Functional Requirements: The Intelligence Library (The Logic Kernel)**

Before any dynamic generation occurs, the system must possess a static, immutable understanding of the Coach's psychology. We do not hard-code logic into Python; we load it from a version-controlled **Intelligence Library**.

FR 1.1: The Intelligence Repository Structure

The system must implement a file-based repository (/backend/intelligence\_library/) containing YAML and JSON configuration files. These files serve as the "Ground Truth" for the AI agents.

* **Identity Pillars (identity\_pillars.yaml):** Defines the 7 Archetypes (Rebel, Maker, Vessel, etc.), their specific vocabulary, shadow traits, and motivational triggers.  
* **TTT Matrix (ttt\_matrix.yaml):** Defines the physics of the 9 Voice Levels (10°F \- 100°F). It must specify syntax rules (e.g., "TTT-08 requires short, staccato sentences," "TTT-02 requires breathy, long-form empathy").  
* **Persuasion Layers (persuasion\_layers.yaml):** Defines the logic structures for the 9 Layers of Persuasion (e.g., "The Challenger," "Black & White Philosophy").  
* **Context Premise Map (context\_premise\_map.json):** The taxonomy of the 12 dimensions (Frustrations, Fears, Enemies, etc.) used for entity extraction.

FR 1.2: Runtime Injection via Pydantic AI

When any agent is instantiated, Pydantic AI must inject these configuration files into the agent's dependency context. The system is strictly forbidden from allowing the LLM to "improvise" a psychological framework. It must constrain generation to the definitions provided in the Library.

---

## **2.2 Functional Requirements: The Noise Detector (Assessment Engine)**

The Assessment Engine provides the "Signal" that allows us to filter out the "Noise" of daily life. It is the input terminal for the **Context Premise (Soul Data)**.

FR 2.1: The Setup Agents (Coach Onboarding)

Before the system can serve users, it must "download" the Coach's consciousness.

* **Kimya (Business Analyst):** The system must deploy an agent to interview the Coach via a web interface. Kimya must extract the "Unique Mechanism," "Economic Engine," and "Promise." She configures the initial logic of the Pantry.  
* **Valeriane (Client Soul Extractor):** The system must ingest the Coach's historical content (videos, emails) and use Valeriane to build the client\_soul.json. She must map the Coach's specific metaphors (e.g., "Life is a garden" vs. "Life is a battlefield") and their **TTT Baseline** to ensure the voice clone is accurate.  
* **Dilaya (Tribe Soul Extractor):** The system must scrape the target audience's digital footprint (forums, reviews) and use Dilaya to build the tribe\_soul.json. She must identify the specific slang, cultural heroes, and shared enemies of the user base.

FR 2.2: The User Assessment (Soul Data Mapping)

The system must provide a responsive web application for user intake.

* **Psychometric Probing:** The intake must go beyond demographics. It must capture the 12 dimensions of the **Context Premise**: Frustrations, Dreams, Fears, Suspicions, Insecurities, Envy, Enemies, Coping Mechanisms, Hidden Beliefs, and Success Markers.  
* **Graph Construction:** This data must be parsed and stored as nodes in **Neo4j**, linking the User node to specific Concept nodes. This allows the **Neuro-Persuasion Engine** to reference these specific nouns later (e.g., "I know 'The Corporate Grind' \[Enemy\] is heavy today").

FR 2.3: Atlas (The Program Architect)

The system must deploy Atlas, a Program Builder Agent.

* **Input:** Atlas reads the user's Capacity\_Score (calculated from energy/time inputs), Identity\_Pillar (derived from language patterns), and the Coach's **Component Pantry**.  
* **Logic:** Atlas must dynamically assemble a 30-day sequence of rituals.  
  * *If* Capacity \< 40: Build a "Recovery Ramp-Up" (Week 1: Sleep focus).  
  * *If* Capacity \> 80: Build a "High Performance Sprint" (Week 1: Deep Work focus).  
* **Output:** A scheduled roadmap stored in **Supabase**, ready for daily execution.

---

## **2.3 Functional Requirements: The Neuro-Persuasion Engine (Dynamic Assembler)**

This is the "Brain" that connects the Coach's Pantry to the Client's Needs. It replaces linear logic with a probabilistic **"Persuasion Matrix"** managed by **Emilio (The Orchestrator)**.

FR 3.1: The Assembler (Strategist Agent)

The system must deploy The Assembler to determine the strategy for each daily interaction. The Assembler does not write text; it outputs a structured InterventionStrategy object.

* **Context Retrieval:** It must query **Neo4j** for the user's active nodes (e.g., "Fear: Poverty," "Enemy: My Boss").  
* **Lego Block Selection:** It must query the **Pantry** for the matching ritual (e.g., "5-Minute Breathwork").  
* **Logic:** It must select the optimal **Persuasion Layer** and **Story Formula** based on the user's state.

FR 3.2: The "4-Dimensional" Component Logic

Every component (Ritual) selected by The Assembler must be processed into a 4-Dimensional Object by Pydantic AI:

1. **Level Threshold (Capacity):** Matches the user's Capacity\_Score. If low, force "Micro-Habit" variant.  
2. **Identity Fit (Voice):** Wraps the task in the language of the user’s **Identity Pillar**. For a *Rebel*, the task is "Defiance"; for a *Maker*, it is "Optimization."  
3. **Goal Fit (Payoff):** Aligns the "Why" with the user's specific Pain Point (Hyperbolic Discounting).  
4. **Implementation (Action):** The specific media asset (Video/Audio).

FR 3.3: The 9 Layers of the Persuasion Cycle

The system must implement the 9-Layer Persuasion logic defined in the Intelligence Library. The Assembler must select one of the following layers to frame the message:

1. **Black and White Philosophy:** Reducing cognitive load via binary choice.  
2. **The Challenger (Reverse Psychology):** This is a critical requirement for high-resistance users. The system must **NOT** simply use direct confrontation ("I bet you can't"). It must utilize **Reverse Psychology** to bait the user's emotional triggers regarding their Enemies.  
   * *Logic:* "Maybe you are actually comfortable letting \[Enemy\] win. If you weren't, you would have done the work by now."  
   * *Mechanism:* This triggers **TTT-08: Raw Confrontation**.  
3. **Favorable Evidence:** Using the user's own past data to prove capability.  
4. **Pain Amplification:** Agitating the problem to create urgency.  
5. **Encourage Their Dreams:** Linking the micro-habit to the macro-vision.  
6. **Justify Past Failures:** Removing shame to allow action.  
7. **Allay Their Fears:** Reducing performance anxiety via compassion.  
8. **Throw Rocks at Their Enemies:** Validating their struggle against external forces.  
9. **Confirming Suspicions:** Validating their intuition ("You were right to feel stuck").

FR 3.4: The Artisan (Copywriter Agent)

The system must deploy The Artisan to generate the final text script using MiniMax-M2.

* **Input:** The Strategy Object from The Assembler.  
* **Constraint:** The Artisan must apply the specific syntax rules of the selected **TTT** voice (e.g., "Use short sentences and zero hedging for TTT-08"). It must fill the slots of the selected **Story Insight Formula** (e.g., DHD \+ Dreams \+ Enemies \+ Fears) with the nouns extracted from Neo4j.

---

## **2.4 Functional Requirements: The Research & Relevance Engine (The Zeitgeist)**

To ensure the Voice Notes are not just psychologically accurate but culturally relevant, the system must deploy a **Weekly Research Loop**.

FR 4.1: Maeva (Social Researcher)

The system must deploy Maeva to scan social media and forums relevant to the Soul Tribe.

* **Function:** Identify shifts in collective sentiment. What is the tribe angry about this week? What are they celebrating?  
* **Output:** A "Sentiment Report" injected into The Assembler's context.

FR 4.2: Lionel (Deep Researcher)

The system must deploy Lionel to conduct deep research on the "Theme of the Week" using Google Search API and Tavily. Lionel must populate the system with data across 7 Planning Dimensions:

1. **Historical Evolution & Temporal Contrast:** "Just like in 2008, everyone is panicking..."  
2. **Contrarian Analysis & Hidden Truths:** "The news says X, but the data shows Y."  
3. **Emotional Landscape & Human Stories:** Integrating viral human interest stories relevant to the tribe.  
4. **Data-Driven Reality Check:** Using fresh statistics to validate or challenge beliefs.  
5. **Cultural Zeitgeist & Trend Analysis:** Referencing current memes or cultural moments to signal "Insider Status."  
6. **Cross-Disciplinary Frameworks & Metaphors:** Importing mental models from other fields.  
7. **Viral Potential Assessment:** Ensuring the angle has "shareability."

FR 4.3: Relevance Injection

The Assembler must prioritize these research inputs. If a major news event impacts the tribe (e.g., interest rate hike for real estate investors), the system must override the standard curriculum to address the immediate anxiety using the Relevance dimension.

---

## **2.5 Functional Requirements: The Rapport Interface (Client OS)**

The Client Interface is hosted entirely within **Telegram**. Its primary directive is **"Rapport-First."**

FR 5.1: The "Adaptive Primer" (Morning Intent Loop)

The Morning Hook is the "Prompt" that fine-tunes the user's daily identity model.

* **Trigger:** 08:00 AM (User Local Time).  
* **The Voice (Speaker Agent):** The system must utilize **IndexTTS-2** hosted on **Runpod** to generate high-fidelity audio. It must modulate the prosody (Speed, Breathiness) based on the TTT state selected by The Assembler.  
* **The "Vision Implant":** The audio must explicitly guide the user to *visualize* the action ("Close your eyes. See yourself doing it"). This leverages the **Availability Heuristic**.  
* **The Instruction Block:** Exactly 3 seconds after the audio (managed by **Redis** delay queue), the system must send the Text Block containing the link. This "Psychological Gap" ensures the user consumes the emotion before the logic.

FR 5.2: The "Evidence" Capture (Voice Journaling)

The system must rely on the Mirroring Effect. Because we send audio, the user replies with audio.

* **Transcription:** The system must stream the audio to **Groq** (Whisper Large v3) for instant transcription.  
* **Aria (The Synthesizer):** The system must deploy Aria to analyze the transcript. She performs **Entity Extraction** to update the **Context Premise** in Neo4j (e.g., creating a new "Fear" node).  
* **Signal Extraction:** Aria must identify "Identity Signals" (e.g., "I felt powerful today"). These are stored as **Favorable Evidence** to be echoed back to the user in future scripts.

**FR 5.3: The Evening Reflection Loop**

* **Trigger:** 07:00 PM.  
* **Scenario A (Success):** If the ritual is complete, **The Artisan** generates a voice note using **Confirmation Bias** ("You proved you are an athlete"). The system generates a "Streak Flame" image.  
* **Scenario B (Friction):** If the ritual is pending, **Liliane (The Empathy Agent)** is activated. She uses the **Justify Past Failures** persuasion layer to extract the Reason for Failure (RFF) without shame.

---

## **2.6 Functional Requirements: The Master Composer (Coach Dashboard)**

The Coach Dashboard allows the expert to configure the "Ingredients," while the AI handles the "Recipe."

FR 6.1: The "Pantry" (Component Manager)

The system must provide a tagging interface for the Coach to upload "Atomic Units of Transformation" (Rituals).

* **Tagging:** The Coach must apply the 4-Dimensional tags (Identity Fit, Goal Fit, Level Threshold).  
* **Starter Pack:** The system must ship with the **12 Core Ritual Categories** pre-loaded and pre-tagged.

FR 6.2: The "Cohort Vibe" Visualization

The dashboard must synthesize individual data into aggregate insights.

* **Word Cloud:** **Pydantic AI** must analyze the last 24 hours of client journals to extract high-frequency emotional keywords. These must be visualized via **D3.js**.  
* **Red Flag Feed:** The system must highlight users who are "Stuck" (high dissonance, missed rituals).  
* **Operator Mode:** The Coach must be able to click "Intercept" to pause the AI loop and send a personal voice note via Telegram.

---

## **2.7 Functional Requirements: The Economic & Security Infrastructure**

FR 7.1: Stripe Connect Integration

The system must automate the business model.

* **Split Payments:** Upon a successful $100 transaction, **Stripe Connect** must automatically route $95 to the Coach and $5 to the Platform.  
* **Provisioning:** The Telegram onboarding link must only be generated *after* the payment webhook is verified.

FR 7.2: Cost Circuit Breaker (Langfuse)

The system must enforce unit economics.

* **Monitoring:** **Langfuse** must track the cumulative cost of tokens and GPU seconds per user\_id.  
* **Threshold:** If a user exceeds $4.00/month, **Emilio** must transition the user to **"Economy Mode."**  
* **Economy Mode:** The system must bypass **IndexTTS-2** and switch to text-only replies, and enforce a stricter "Listening Window" to reduce frequency.

FR 7.3: The "Glass Wall" Privacy Protocol

The system must treat data with HIPAA-adjacent rigor.

* **Encryption:** All Voice Notes must be encrypted at rest in **Supabase Storage**.  
* **Ephemeral Processing:** Audio processed by **Groq** must be held in ephemeral memory only.  
* **Redaction:** Before data is sent to **Neo4j**, **Aria** must run a redaction pass to strip names and PII, ensuring the graph tracks *patterns*, not *people*.

---

## **2.8 Non-Functional Requirements (NFR)**

**NFR 1: Latency & The "Thinking Gap"**

* **Constraint:** The Audio Reply must be generated and sent within 15 seconds of the trigger.  
* **Requirement:** The system must utilize **Runpod's** FlashBoot or a "Keep-Warm" scheduler during peak hours (07:00 AM \- 10:00 AM) to ensure GPU availability.  
* **UX:** During generation, the system must trigger the Telegram "Recording audio..." status to simulate human presence.

**NFR 2: Data Sovereignty & Isolation**

* **Constraint:** Coach A must never access the data or Pantry of Coach B.  
* **Requirement:** **Row Level Security (RLS)** must be strictly enforced in Supabase.

**NFR 3: Reliability & Failover**

* **Constraint:** If the GPU cluster fails, the system must not crash.  
* **Requirement:** The system must gracefully degrade to **Text Mode**, sending the script as a text message with a "Technical difficulties" prefix.
