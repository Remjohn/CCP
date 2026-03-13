# **2\. Technical Stack & Data Models**

## **2.1 The "Intelligence Library" Architecture**

The defining architectural decision of the **Conscious Behavioral Change System (CBCS)** is the strict decoupling of **Execution Logic** (Python Code) from **Psychological Logic** (Intelligence Library). We fundamentally reject the "Magic AI" approach where business logic is buried in opaque system prompts. Instead, we treat the coaching methodology as a configuration layer—a "Source Code for the Soul"—that the AI must reference but cannot alter.

This architecture ensures that the system remains deterministic in its reasoning even while being generative in its output. It allows the Coaching Team to update the definition of a "Rebel" or the syntax of a "Truth Bomb" without requiring a redeployment of the core backend infrastructure.

### **2.1.1 The Psychological Kernel (File Structure)**

The application will not initialize without first loading the **Intelligence Library** into memory. This library resides in /backend/intelligence\_library/ and consists of static, version-controlled YAML and JSON files that serve as the **Ground Truth** for the Agentic Team.

* **Archetypal Definitions (identity\_pillars.yaml):** This file defines the 7 Identity Pillars (e.g., The Rebel, The Maker, The Vessel). For each archetype, it defines the Voice Style (e.g., "Direct, Challenging"), the Keywords (e.g., "Freedom, Autonomy"), and the Shadow Traits (e.g., "Sabotage, Defiance").  
* **Voice Physics (ttt\_matrix.yaml):** This file quantifies the **TTT (Temperament, Temperature, Tone)** system. It defines the physics for the 9 levels of voice intensity (10°F to 100°F). It includes specific syntax rules (e.g., "TTT-08 requires short sentences under 8 words") and prosody settings for **IndexTTS-2** (Speed, Breathiness, Pitch).  
* **The Strategy Engine (persuasion\_layers.yaml):** This file defines the logic structures for the 9 Layers of Persuasion. It explicitly outlines the rhetorical steps for strategies like **"The Challenger"** (e.g., Step 1: Validate the capacity; Step 2: Use Reverse Psychology to bait the pride; Step 3: Issue the challenge).  
* **Narrative Structures (story\_formulas.yaml):** This file contains the 16 Story Insight Formulas (e.g., DHD \+ Dreams \+ Enemy \+ Fear). It acts as a template engine for **The Artisan**, ensuring that every script follows a proven narrative arc rather than rambling.  
* **The Taxonomy (context\_premise\_map.json):** This file defines the 12-dimensional map used by **Aria** for entity extraction. It standardizes the ontology of "Fears," "Enemies," "Dreams," and "Success Markers," ensuring consistent data entry into the Graph Database.

### **2.1.2 Runtime Injection (Pydantic AI)**

When an Agent is instantiated via the agent.py module, these configuration files are injected into the AgentDeps (Dependency) object.

* **Mechanism:** The System Prompt for agents like **The Assembler** does not contain the full logic of every persuasion angle. Instead, it contains instructions to *consult the library*.  
* **Execution Flow:** When **Emilio (The Orchestrator)** calls **The Assembler**, he passes the user's state. The Assembler reads the persuasion\_layers.yaml from its dependencies, retrieves the logic for the required angle (e.g., "Throw Rocks at Enemies"), and uses that specific definition to construct the strategy. This prevents "Prompt Drift" and ensures that every user receiving a "Challenger" script gets the exact same psychological treatment, tailored to their specific context.
