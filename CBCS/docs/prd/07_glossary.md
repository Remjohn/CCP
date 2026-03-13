# **7\. Core Concepts Glossary**

To ensure the Engineering Team and the Coaching Team speak the same language, we define the following **Ubiquitous Language** (Domain-Driven Design).

## **7.1 The Identity Architecture**

* **Identity Pillar:** One of the 7 archetypes that define a user's core motivation (e.g., The Rebel, The Maker, The Vessel). This determines the *vocabulary* the AI uses.  
* **Context Premise:** The 12-dimensional map of a user's current psychological reality (e.g., "I am fighting [Enemy] because I fear [Fear]"). This determines the *content* the AI generates.  
* **Soul Data:** The unstructured, high-fidelity information captured via Voice Journaling (tone, hesitation, emotion) that is lost in text-based apps.  
* **Capacity Score:** A dynamic 0-100 score representing the user's available energy. Used to throttle the intensity of assigned rituals.

## **7.2 The Persuasion Architecture**

* **Neuro-Persuasion Engine:** The logic layer (The Assembler) that selects the optimal influence strategy.  
* **TTT (Temperament, Temperature, Tone):** The "Physics" of the AI's voice. A matrix from 10°F (Cold/Analytical) to 100°F (Hot/Emotional) that dictates prosody and syntax.  
* **Vision Implant:** The morning audio message designed to trigger the **Availability Heuristic** by forcing the user to visualize the action before doing it.  
* **Mirroring Effect:** The psychological phenomenon where a user mimics the modality and tone of the speaker. We use high-fidelity audio to force high-fidelity audio replies.

## **7.3 The System Architecture**

* **Invisible App:** A design philosophy where the interface is removed entirely, replaced by a conversational thread in an existing platform (Telegram).  
* **Agentic Mesh:** The network of specialized AI agents (Emilio, Aria, Atlas) that collaborate to manage the user, as opposed to a single monolithic LLM.  
* **Hybrid Memory:** The dual-database architecture using **Supabase** for linear logs and **Neo4j** for non-linear psychological relationships.  
* **Pantry:** The Coach's library of "Atomic Units of Transformation" (Rituals), tagged with 4-Dimensional attributes.

---

## **7.4 The Agentic Workforce (The Team)**

We do not refer to "The AI." We refer to the specific Agent responsible for the task.

* **Emilio (The Orchestrator):** The Manager. Handles state, timing, and safety.  
* **Aria (The Synthesizer):** The Listener. Handles transcription and entity extraction.  
* **Atlas (The Program Architect):** The Builder. Handles schedule construction.  
* **The Assembler (The Strategist):** The Thinker. Handles persuasion logic and component selection.  
* **The Artisan (The Copywriter):** The Writer. Handles script generation and TTT syntax application.  
* **The Voice (The Speaker):** The Mouth. Handles IndexTTS-2 synthesis.  
* **Maeva (Social Researcher):** The Scout. Handles trend analysis.  
* **Lionel (Deep Researcher):** The Librarian. Handles fact-checking.  
* **Liliane (The Empathy Agent):** The Nurse. Handles failure management and crisis de-escalation.  
* **Kimya (Business Analyst):** The Consultant. Handles Coach onboarding.  
* **Valeriane (Client Soul Extractor):** The Biographer. Handles Coach voice cloning.  
* **Dilaya (Tribe Soul Extractor):** The Anthropologist. Handles audience analysis.

---

## **7.5 The Technology Stack**

### **1\. The Core Nervous System**

* **FastAPI (Python):** The high-performance web framework handling the Telegram webhooks. It manages the asynchronous background tasks that allow the system to "think" without timing out the chat interface.  
* **LangGraph:** The state orchestration engine. It replaces linear "chains" with cyclic graphs, allowing the system to maintain persistent user states (e.g., "Waiting for Evidence") and handle complex loops like the "Compassionate Retrieval" process.

### **2\. The Brain (Inference)**

* **MiniMax-M2:** The primary Large Language Model (LLM). Selected for its superior "Chain of Thought" reasoning and high context window, allowing it to hold the user's entire 30-day history in active memory.  
* **Brain (Pydantic AI):** The structured reasoning layer that validates all outputs against schema definitions before generation. It ensures the AI selects the correct **Cognitive Bias** and **Story Formula** before generating text.  
* **Nervous System (LangGraph):** The state machine that manages the user's position in the journey. It handles the "Listening Window" and "Silencer" logic.

### **3\. Hybrid Memory Architecture**

* **Relational (Supabase):** Stores hard logs (Ritual completion, Subscription status, User Profile) and utilizes pgvector for RAG retrieval of the Coach's manuals.  
* **Graph (Neo4j):** Stores the **Context Premise** and **Identity Map**. It allows the system to traverse relationships (e.g., "Find all users where *Fear* is 'Poverty' and *Identity* is 'Maker'").

### **4\. The "Glass Wall" Protocol (Privacy)**

A rigorous security architecture ensuring that while the AI "knows" the user, it cannot leak their data.

* **Encryption:** All Voice Notes are encrypted at rest.  
* **Ephemeral Processing:** Audio files sent to **Groq** for transcription are processed in memory and purged immediately.  
* **Redaction:** Before data enters the **Neo4j** graph, **Aria** runs a redaction pass to strip names and PII, ensuring the graph tracks patterns, not identities.

### **5\. The Economic Engine (Stripe Connect)**

The financial infrastructure that makes the high-touch model viable.

* **Split Payments:** Automatically routes the $5.00 Service Fee to the platform per transaction.  
* **Cost Circuit Breaker:** Uses **Langfuse** to track token usage per user, throttling generation if costs exceed the unit economic margin ($4.00), ensuring sustainability.
