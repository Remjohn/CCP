# Chapter 11: The Persistence Layer (Supabase + Neo4j Production)

**Chapter Goal:** Deploy the dual-database persistence layer (Supabase for relational/vector, Neo4j for graph) with production-grade schemas, migrations, backups, and security
**Mastery Track:** CCP System Architect
**Launch Track:** Supabase tables deployed, Neo4j Aura running, graph schemas applied, all CCP services connected to production databases
**Prerequisites:** Chapter 5 (Hypergraph Memory — the theory), Chapter 6 (Agentic Core — the consumers)
**Estimated Time:** 6-8 hours

---

## CCP/CMF Reality Anchor

The CCP's intelligence is stateless without the persistence layer. Client psychology profiles, coaching session history, Voice DNA extractions, Emotional DNA scores, accountability tracking data, and graph relationships — all stored across Supabase (relational + pgvector) and Neo4j (graph). Without production databases, every conversation is forgotten, every pattern detected is lost, and every coaching insight vanishes. This chapter deploys the MEMORY that makes the CCP a persistent intelligence, not a stateless tool.

---

## Codebase Map

| File | Location | Size | Status |
|------|----------|------|--------|
| `neo4j_graph_manager.py` | `src/ccp/services/` | 17KB | ✅ EXISTS |
| `memory_tier_promotion_service.py` | `src/ccp/services/` | 22KB | ✅ EXISTS |
| `fingerprint_archive_engine.py` | `src/ccp/services/` | 16KB | ✅ EXISTS |
| `receipt_chain_guard.py` | `src/ccp/services/` | 18KB | ✅ EXISTS |
| `neo4j config` in CCP `.env` | workspace root | — | ✅ EXISTS |
| `supabase schema` | — | — | ⚠️ BUILD REQUIRED — needs migrations |

**Files referenced: 5** ✅

---

## Science Sources

| Source | Location | Type |
|--------|----------|------|
| `FR38_Memory_Tier_Promotion_Tech_Spec.md` (14KB) | `docs/architecture/` | Memory promotion |
| `FR21_Receipt_Chain_Guard_Tech_Spec.md` (15KB) | `docs/architecture/` | Receipt chain |
| `FR23_Skill_Fingerprint_ID_Tech_Spec.md` (13KB) | `docs/architecture/` | Fingerprinting |
| `FR46_Universal_Asset_ID_Tech_Spec.md` (11KB) | `docs/architecture/` | Universal IDs |
| `FR47_Receipt_Chain_Guard_Tech_Spec.md` (13KB) | `docs/architecture/` | Receipt chain v2 |
| `FR48_Forensic_Audit_Protocol_Tech_Spec.md` (12KB) | `docs/architecture/` | Audit protocol |
| `Infrastructure_AWS_NIM_Deployment_Spec.md` (35KB) | `docs/architecture/` | DB deployment |

---

## Unit Map

| Unit | Title | 🧠 Science Topic | UNLEARN | 📂 Code Files | 📄 Science Sources | Build Target | Verify |
|------|-------|-------------------|---------|---------------|-------------------|-------------|--------|
| 11.1 | Dual-Database Architecture — Why Both | Relational (Supabase) for structured records + vector search. Graph (Neo4j) for causal relationships. Why ONE database doesn't serve both: storing causality in rows destroys traversal performance, storing tabular data in graphs wastes memory | "One database can do everything." False — relational databases model RECORDS (rows/columns). Graph databases model RELATIONSHIPS (nodes/edges). The CCP needs both: records for client profiles, relationships for causal chains | `neo4j_graph_manager.py`, `.env` config | `Infrastructure_AWS_NIM_Deployment_Spec.md` §Database Layer | — | Explain what goes in Supabase vs Neo4j. Give 3 examples for each |
| 11.2 | Schema Design & Migrations | RLS (Row Level Security) for multi-tenant isolation — each coach sees ONLY their clients. Migration patterns: forward-only, timestamped, reversible. pgvector columns for embedding search | "Just create tables manually." False — manual schema management is non-reproducible. Migrations are version-controlled schema evolution scripts. RLS enforces tenant isolation at the database level, not the application level | — | `FR46_Universal_Asset_ID_Tech_Spec.md`, `FR49_Single_Tenant_Deployment_Tech_Spec.md` | ⌨️ Build Supabase migrations with RLS policies | `supabase migration list` → shows applied migrations. RLS blocks cross-coach access |
| 11.3 | Neo4j Production — Aura & Cypher | Neo4j Aura (managed cloud) vs self-hosted. Production Cypher patterns for the CCP graph schema. Index creation for traversal performance | "Self-host Neo4j in Docker." Risky — Neo4j Aura provides automated backups, scaling, and monitoring. Self-hosting adds ops burden without benefit at our scale | `neo4j_graph_manager.py` — all Cypher queries | `FR38_Memory_Tier_Promotion_Tech_Spec.md` | ⌨️ Deploy Neo4j Aura, apply CCP graph schema | `neo4j_graph_manager.py` connects to Aura and performs a test write/read |
| 11.4 | Receipt Chain — Provenance Tracking | Every agent action, every pipeline execution, every data write generates a receipt. Receipts chain together (hash-linked) to create an audit trail. Forensic auditability: prove WHAT happened, WHEN, and WHY | "Logs are enough for auditing." False — logs are append-only text. Receipt chains are hash-linked, tamper-evident records that prove provenance. If a receipt is missing, the chain breaks — indicating tampering or system failure | `receipt_chain_guard.py` (18KB), `fingerprint_archive_engine.py` (16KB) | `FR21_Receipt_Chain_Guard_Tech_Spec.md`, `FR48_Forensic_Audit_Protocol_Tech_Spec.md` | — | Read receipt_chain_guard.py. Identify the hash-linking mechanism |
| 11.5 | Backup & Disaster Recovery | RTO (Recovery Time Objective) vs RPO (Recovery Point Objective). Automated daily backups for Supabase. Neo4j Aura built-in snapshots. S3 cross-region replication for CMF assets | "Backups are for later." False — losing ONE client's coaching data (psychology profile, session history) is unrecoverable. The FIRST production deployment must include automated backups | — | `Infrastructure_AWS_NIM_Deployment_Spec.md` §Backup | ⌨️ Configure automated backups for both databases | Supabase daily backup verified + Neo4j Aura snapshot verified |

---

## Quality Gates

- [x] **Unit Count Gate:** 5 units ✅
- [x] **5-File Gate:** 5 codebase + 7 science sources ✅
