## **2.3 Data Models (The Hybrid Memory)**

The system relies on a **Hybrid Persistence** strategy to manage the complexity of human behavior. We use **Supabase** for transactional integrity and "Hard Data," and **Neo4j** for psychological complexity and "Soft Data."

### **2.3.1 Relational Schema (Supabase PostgreSQL)**

Used for the "Hard Logs," business logic, and vector storage. (Extending 002\_agent\_tables.sql).

**Table: user\_profiles** (Augmented)

* id: UUID (PK) \- Linked to Auth.  
* identity\_pillar: Enum (Rebel, Maker, Vessel, etc.).  
* capacity\_score: Integer (0-100) \- Updated daily via Aria.  
* current\_program\_id: UUID \- Link to the active roadmap.  
* subscription\_status: Varchar (Stripe status).  
* timezone: Varchar \- Critical for 8:00 AM triggers.

**Table: daily\_logs** (The Journal)

* id: UUID (PK).  
* user\_id: UUID (FK).  
* date: Date.  
* audio\_url: Text (Encrypted Path to Supabase Storage).  
* transcript\_text: Text (Output from Groq).  
* ttt\_state\_detected: Varchar (e.g., "TTT-02").  
* ritual\_completion\_status: Boolean.

**Table: ritual\_library** (The Pantry)

* id: UUID (PK).  
* title: Text.  
* media\_url: Text.  
* level\_threshold: Integer (1-10).  
* identity\_fit\_tags: Array (Rebel, Maker...).  
* goal\_fit\_tags: Array (Sleep, Energy, Focus...).  
* embedding: Vector(1536) \- Generated via OpenAI text-embedding-3-small for RAG retrieval by the Research Agents.

### **2.3.2 Graph Schema (Neo4j Ontology)**

Used for the **Context Premise** and non-linear relationships. This enables the "God Mode" queries that allow the AI to "remember" connections a human coach would forget.

**Nodes:**

* User: The client entity.  
* Identity: The archetype definition (e.g., Rebel).  
* Concept: The extracted psychological entities (e.g., "The Corporate Grind", "My Father", "Bankruptcy", "Marathon").  
  * *Property:* type (Enemy, Dream, Fear, Insecurity, Success\_Marker).  
  * *Property:* last\_mentioned (Timestamp).  
* Ritual: The intervention unit from the Pantry.

**Edges (Relationships):**

* (User)-\[:HAS\_IDENTITY\]-\>(Identity)  
* (User)-\[:FIGHTS\_AGAINST\]-\>(Concept {type: 'Enemy'})  
  * *Property:* intensity (1-10) \- Updates daily based on Aria's sentiment analysis.  
* (User)-\[:CRAVES\]-\>(Concept {type: 'Dream'})  
* (User)-\[:BLOCKED\_BY\]-\>(Concept {type: 'Fear'})  
* (Ritual)-\[:RESOLVES\]-\>(Concept {type: 'Fear'})  
* (Concept)-\[:TRIGGERS\]-\>(Concept) \- (e.g., "Bankruptcy" *TRIGGERS* "Fear of Failure").

Query Example (The "Magic" Query):

To generate a script for a Rebel struggling with Fear, The Assembler executes:

```cypher
MATCH (u:User {id: $uid})-[:BLOCKED_BY]->(fear:Concept)  
MATCH (u)-[:FIGHTS_AGAINST]->(enemy:Concept)  
WHERE fear.intensity > 7 AND enemy.intensity > 7  
RETURN fear.name, enemy.name  
ORDER BY fear.last_mentioned DESC LIMIT 1
```

Result: Fear="Irrelevance", Enemy="Ageism".

Script Application: "The world tells you you're too old (Ageism). That creates a fear that you don't matter (Irrelevance). Prove them wrong."
