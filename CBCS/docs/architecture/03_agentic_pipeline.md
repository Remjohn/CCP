## **2.2 The Agentic Pipeline (Chain of Thought)**

We do not make a single API call to "Chat." We orchestrate a **Sequential Agentic Workflow** managed by **LangGraph**. Each step in the pipeline is a discrete state transition performed by a specialized "Prompt Persona." This allows us to maintain a **Chain of Thought** that is auditable, debuggable, and resilient.

### **Phase 1: The Synthesizer (Agent: "Aria")**

* **Role:** The Noise Detector.  
* **Input:** Raw Audio Transcript (processed by **Groq** Whisper Large v3).  
* **Reference:** context\_premise\_map.json.  
* **Task:** Aria does not reply to the user. Her sole function is **Entity Extraction**. She analyzes the unstructured text of the voice note to identify psychological entities.  
* **Logic:** She looks for semantic patterns matching the 12 dimensions. If the user says, "I'm terrified of losing my savings," she extracts "Losing Savings" as a Fear entity.  
* **Output Schema (Pydantic):**  
```python
class SoulData(BaseModel):  
    primary_emotion: str  
    identified_enemies: List[str]  # e.g., "The Corporate Grind", "My Boss"  
    active_fears: List[str]        # e.g., "Being Irrelevant"  
    hidden_beliefs: List[str]      # e.g., "I'm too old to start"  
    ttt_state_detected: str        # e.g., "TTT-02 (Defeated)"
```
* **Action:** This structured data is written immediately to the **Neo4j** graph, linking the User node to these specific Concept nodes.

### **Phase 2: The Strategist (Agent: "The Assembler")**

* **Role:** The Neuro-Persuasion Engine.  
* **Input:** SoulData (from Aria) \+ UserHistory (from Supabase) \+ PantryIndex (from **Atlas**).  
* **Reference:** persuasion\_layers.yaml \+ story\_formulas.yaml.  
* **Task:** The Assembler decides *how* to influence the user. It selects the **Lego Blocks**. It does not write the script; it designs the architectural plan for the script.  
* **Logic:**  
  * *IF* Capacity\_Score \< 30 (Burnout) *AND* Identity\_Pillar \= "Maker":  
  * *SELECT* Formula \#4 (Validation \+ Micro-Step).  
  * *SELECT* Ritual: "5-Minute Breathwork" (Low Threshold).  
  * *SELECT* TTT Target: "TTT-02 Compassionate".  
* **Output Schema (Pydantic):**  
```python
class InterventionStrategy(BaseModel):  
    selected_formula_id: str  
    target_ttt: str  
    persuasion_angle: str  
    ritual_id: str  
    rationale: str # Chain of Thought explanation for the Coach
```

### **Phase 3: The Artisan (Agent: "The Copywriter")**

* **Role:** The Script Writer.  
* **Input:** InterventionStrategy.  
* **Reference:** identity\_pillars.yaml \+ ttt\_matrix.yaml.  
* **Task:** The Artisan generates the actual text script using **MiniMax-M2**. It applies the syntax constraints of the target TTT (e.g., "Use short, punchy sentences for TTT-08," "Use soft, flowing syntax for TTT-02").  
* **Constraint:** It must fill the slots of the selected **Story Formula** with the specific nouns extracted by Aria from the Neo4j graph.  
  * *Example:* "I know **\[Enemy: The Corporate Grind\]** is heavy today..."  
* **Validation:** The output is passed through a Pydantic validator to ensure it does not contain banned phrases (e.g., "I am an AI") and adheres to the character limit.

### **Phase 4: The Speaker (Agent: "The Voice")**

* **Role:** The Renderer.  
* **Input:** Final Script Text \+ target\_ttt.  
* **Task:** Sends the text to the **IndexTTS-2** engine hosted on **Runpod**.  
* **Modulation:** It maps the target\_ttt to specific inference parameters.  
  * *TTT-02:* Speed: 0.85, Breathiness: 0.8, Pitch: \-2.  
  * *TTT-08:* Speed: 1.1, Breathiness: 0.1, Pitch: \+1.
