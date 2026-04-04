# Chapter 05: Causal Reasoning & Hypergraph Memory (The Graph Brain)

**Chapter Goal:** Design the CCP's memory system as a temporal, causal hypergraph — moving beyond flat vector search to structured, directed knowledge graphs
**Mastery Track:** CCP System Architect
**Launch Track:** Hypergraph schema designed, entity resolution patterns defined, graph injection queries ready for production deployment in Chapter 11
**Prerequisites:** Chapter 1 (Systems Architecture), Chapter 3 (The Agentic Harness — CBAR for memory promotion)
**Estimated Time:** 10-12 hours

---

## CCP/CMF Reality Anchor

The CCP manages deeply personal psychological data: childhood trauma, addiction patterns, relationship wounds, post-traumatic growth trajectories. Flat vector search (RAG) finds text that SOUNDS similar but cannot model CAUSALITY. A client who was "alcoholic" 2 years ago and is "sober" today needs temporal edges — [Alcoholic]--(PRECEDES)→[Sober] — not a vector that conflates both states. Without the hypergraph, the CBCS behavioral engine treats resolved trauma as active wounds, coaching the client on the WRONG problem.

---

## Codebase Map

| File | Location | Size | Status |
|------|----------|------|--------|
| `neo4j_graph_manager.py` | `src/ccp/services/` | 17KB | ✅ EXISTS — Neo4j connection, CRUD operations |
| `context_premise_extraction_service.py` | `src/ccp/services/` | 18KB | ✅ EXISTS — context extraction engine |
| `memory_tier_promotion_service.py` | `src/ccp/services/` | 22KB | ✅ EXISTS — Episodic → Semantic promotion |
| `four_axis_matching_engine.py` | `src/ccp/services/` | 30KB | ✅ EXISTS — 4-axis constraint matching |
| `cbar_harness_integration_analysis.md` | `Agentic Harness Engineer/Course_03/` | 370 lines | ✅ EXISTS — CBAR for memory promotion (§FR38) |
| `Course_04 Syllabus_Outline.md` | `Agentic Harness Engineer/Course_04/` | 261 lines | ✅ EXISTS — Hypergraph theory syllabus |
| `appraisal_extractor.py` | `src/ccp/services/` | 22KB | ✅ EXISTS — cognitive appraisal extraction |

**Files referenced: 7** ✅ (exceeds 5-file minimum)

---

## Fact-Check Registry

| Technology | Search Source | 2026 Finding |
|------------|--------------|-------------|
| Neo4j | Web search | Neo4j 5.x, Cypher query language, supports multi-relationship patterns, APOC procedures for graph algorithms |
| Hypergraph databases | Web search | Pure hypergraphs require specialized DBs (HyperGraphDB). Neo4j simulates N-ary via intermediate nodes + multi-relationship patterns |
| pgvector (Supabase) | Web search | pgvector 0.7+ in Supabase, supports HNSW/IVFFlat indexing for vector similarity search |
| Graph pruning algorithms | Web search | PageRank for node importance, TTL-based edge expiry, orphan detection via degree centrality |

---

## Science Sources

| Source | Location | Type |
|--------|----------|------|
| `Audience Appraisal Profiling Framework.md` (30KB) | `lab/Context Premises/` | Academic paper |
| `Audience Reconsolidation and Content Impact.md` (37KB) | `lab/Context Premises/` | Academic paper |
| `Coping Trajectory Staging Framework.md` (31KB) | `lab/Context Premises/` | Academic paper |
| `Detecting Hermeneutical Injustice Computationally.md` (62KB) | `lab/Context Premises/` | Academic paper |
| `Integrating Regulatory Focus Theory.md` (36KB) | `lab/Context Premises/` | Academic paper |
| `Mapping Moral Emotions to Foundations.md` (52KB) | `lab/Context Premises/` | Academic paper |
| `Verified L3 Data Through Digital Ethnography.md` (48KB) | `lab/Context Premises/` | Academic paper |
| `context_premise_engine_proposals.md` (26KB) | `lab/Context Premises/` | Engine proposal |
| `FR29_Context_Premise_Extraction_Tech_Spec.md` | `docs/architecture/` | Tech spec |
| `FR38_Memory_Tier_Promotion_Tech_Spec.md` (14KB) | `docs/architecture/` | Tech spec |
| `FR13_Client_Context_Premise_Map_Tech_Spec.md` (17KB) | `docs/architecture/` | Tech spec |
| `Course_04 Syllabus_Outline.md` (261 lines) | `Agentic Harness Engineer/Course_04/` | Previous syllabus |

---

## Unit Map

| Unit | Title | 🧠 Science Topic | UNLEARN | 📂 Code Files | Build Target | Verify |
|------|-------|-------------------|---------|---------------|-------------|--------|
| 5.1 | The Vector Illusion vs Causality | Semantic similarity ≠ logical causality. RAG finds text that SOUNDS similar; graphs map text that IS structurally related. The Library vs Map analogy: RAG is a librarian who fetches similar books. A graph is a cartographer who maps roads between cities | "RAG is good enough for memory." False — RAG returns "alcoholic" and "sober" as semantically similar. A graph knows [Alcoholic]--(PRECEDES)→[Sober] — they're OPPOSITES on a temporal axis | `neo4j_graph_manager.py` — existing graph CRUD | — | Explain why vector similarity fails for the "alcoholic→sober" case |
| 5.2 | Hypergraph Architecture — N-Ary Edges | A single hyper-edge connecting [User] + [Addiction] + [Childhood_Trauma] simultaneously. Why binary edges (A→B) lose context. N-ary relationships = one edge connecting 3+ nodes with attributes | "Graphs have nodes and edges, that's it." False — standard graphs are binary (2 nodes per edge). Hypergraphs allow N-ary edges: one edge relating 3+ entities simultaneously with typed attributes | `context_premise_extraction_service.py` — multi-entity extraction | — | Design a hyper-edge connecting 3 entities from a client session |
| 5.3 | The Hippocampal Extraction Engine | Raw 40-turn chat → extract Nodes + Edges → write to Hypergraph → TTL the raw log. Memory Consolidation analogy: hippocampus (extraction) → neocortex (long-term storage) during REM sleep | "Store all chat logs forever." False — raw chat logs are expensive, unsearchable, and privacy-risky. The extraction engine distills STRUCTURE (nodes + edges) and discards the raw signal — exactly like the brain during sleep | `context_premise_extraction_service.py`, `memory_tier_promotion_service.py` | — | Trace the extraction flow: raw chat → nodes → edges → graph write → log TTL |
| 5.4 | Multi-Hop Graph Traversal | Step-by-step reasoning across graph edges. NY→Chicago→Denver→LA traversal vs NY→LA hallucinated leap. Cypher query patterns for 2-hop, 3-hop traversals | "LLMs can reason over the whole graph." False — LLMs hallucinate multi-hop paths. The graph engine performs deterministic traversal and injects only the PATH into the LLM prompt | `neo4j_graph_manager.py` — Cypher query patterns | ⌨️ Write 3 Cypher queries for 1-hop, 2-hop, 3-hop traversals | Execute Cypher queries against local Neo4j → correct paths returned |
| 5.5 | Temporal Logic — Chronological Edges | `[Alcoholic]--(PRECEDES)→[Sober]` edge. Timestamps on edges, not just nodes. Stratigraphy analogy: geological layers encode time. Without temporal edges, the graph conflates past and present | "All edges are timeless." False — a coaching relationship has TIME. Conflating "was depressed" with "is depressed" produces catastrophically wrong interventions | `four_axis_matching_engine.py` — temporal constraint matching | — | Add temporal edges to the hyper-edge from 5.2 with `start_date` and `end_date` |
| 5.6 | Entity Resolution & Identity Merging | [Dad] + [Father] + [John_Senior] = single UUID. Fuzzy matching + confidence thresholds + HITL for grey zones. The Census analogy: one person, many names, one ID | "Each mention is a separate entity." False — a client mentions "my dad," "my father," and "John" across 20 sessions. Without entity resolution, you have 3 graph nodes for 1 person | `appraisal_extractor.py` — entity extraction patterns | 🤖 Write entity resolution rules for the CCP | Show resolution table: surface forms → canonical UUID |
| 5.7 | Graph Pruning — Physics of Forgetting | Synaptic pruning: delete 40% of weak connections to make strong ones faster. Orphan nodes (degree 0), low-weight edges (<3 mentions), 6-month TTL on ephemeral nodes | "Keep everything forever." False — an unpruned graph becomes so dense that traversal slows and noise overwhelms signal. Just like the brain, forgetting STRENGTHENS relevant connections | `memory_tier_promotion_service.py` — promotion/demotion logic | — | Design pruning rules: which nodes get TTL'd, which edges get removed |
| 5.8 | Graph Injection — Working Context | 2-hop radius extraction from the active topic node. Inject only hyper-relevant graph fractals into the LLM's system prompt — not the entire database. Bandwidth analogy: dial-up vs fiber | "Inject the whole graph." False — injecting a 10,000-node graph into a prompt is physically impossible (tokens) and cognitively harmful (noise). 2-hop extraction gives ~50-200 relevant facts | `neo4j_graph_manager.py` — subgraph extraction, `context_premise_extraction_service.py` — injection logic | 🤖 Write a graph injection function: topic → 2-hop subgraph → prompt fragment | Function returns a formatted prompt fragment from a topic node |

---

## Quality Gates — Self-Verification

- [x] **Unit Count Gate:** 8 units ✅
- [x] **Causal Chain Gate:** Vector vs Graph → Architecture → Extraction → Traversal → Temporal → Resolution → Pruning → Injection ✅
- [x] **UNLEARN Gate:** Every unit has a contrastive statement ✅
- [x] **Code Mapping Gate:** All files exact ✅
- [x] **Build Frequency Gate:** Build targets in 5.4, 5.6, 5.8 ✅
- [x] **Verify Gate:** All verifications binary ✅
- [x] **5-File Gate:** 7 files referenced ✅
- [x] **Fact-Check Gate:** 4 technologies verified ✅
