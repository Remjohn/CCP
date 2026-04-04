# Launch Manual — Unit Registry (Master)

> **Total: 97 units across 12 chapters**
> Status: All Chapter Syllabi generated with Science Sources + Schedule-Based Architecture + Harness Command Outputs
> **CCP Command Files Produced: 7** (`ccp-health-check`, `ccp-onboard`, `ccp-voice-track`, `ccp-onboard-client`, `ccp-deploy`, `ccp-schedule` + Pipeline DAG from Ch3.17)

---

## Registry Summary

| Chapter | Title | Units | Status | Schedule-Based? |
|---------|-------|-------|--------|----------------|
| Ch 01 | Systems Architecture | 6 units (1.1-1.6) | ✅ SYLLABUS DONE (v2 — with docs + schedule fix) | ✅ Corrected |
| Ch 02 | AWS Foundations + Nvidia NIM | 15 units (2.1-2.15) | ✅ SYLLABUS DONE (v3 — batch cost model fixed) | ✅ Corrected |
| Ch 03 | The Agentic Harness | **17 units** (3.1-3.17) | ✅ SYLLABUS DONE (v3 — +2 harness application units + `commands/` reference) | N/A (theory → practice) |
| Ch 04 | The CLI Operator | **11 units** (4.1-4.11) | ✅ SYLLABUS DONE (v3 — +3 command authoring units, produces `ccp-*` commands) | N/A (CLI skills → harness building) |
| Ch 05 | Hypergraph Memory | 8 units (5.1-5.8) | ✅ SYLLABUS DONE (needs doc source column update) | N/A (theory) |
| Ch 06 | The Agentic Core | 7 units (6.1-6.7) | ✅ SYLLABUS DONE (needs doc source + schedule fix for Telegram) | ⚠️ Needs Telegram schedule fix |
| Ch 07 | The CMF Pipeline | 10 units (7.1-7.10) | ✅ SYLLABUS DONE (needs doc source column update) | N/A (pipeline) |
| Ch 08 | The Video Editor | 9 units (8.1-8.9) | ✅ SYLLABUS DONE (v2 — with docs) | ✅ Correct (always-on dashboard) |
| Ch 09 | Coach Dashboard (AFFiNE) | 4 units (9.1-9.4) | ✅ SYLLABUS DONE (v2 — with docs) | ✅ Correct (always-on dashboard) |
| Ch 10 | Platform (Telegram + Stripe) | 4 units (10.1-10.4) | ✅ SYLLABUS DONE (v2 — with docs + schedule fix) | ✅ Corrected |
| Ch 11 | Persistence Layer | 5 units (11.1-11.5) | ✅ SYLLABUS DONE (v2 — with docs) | ✅ N/A (always-on DB) |
| Ch 12 | Launch & Hardening | 6 units (12.1-12.6) | ✅ SYLLABUS DONE (v2 — with docs + schedule design) | ✅ Corrected (CRON + GPU lifecycle) |

---

## Full Unit Index

### Chapter 01: Systems Architecture (6 units)
| Unit | Title | Status |
|------|-------|--------|
| 1.1 | Systems Thinking & Feedback Loops | `[ ]` pending |
| 1.2 | First Principles — The 4 Primitives | `[ ]` pending |
| 1.3 | The CCP Architecture Deep-Dive | `[ ]` pending |
| 1.4 | The CMF Architecture Deep-Dive | `[ ]` pending |
| 1.5 | The Infrastructure Map | `[x]` completed |
| 1.6 | Gap Analysis — What's Missing | `[ ]` pending |

### Chapter 02: AWS Foundations + Nvidia NIM (15 units)
| Unit | Title | Status |
|------|-------|--------|
| 2.1 | Cloud Computing First Principles | `[ ]` pending |
| 2.2 | IAM & Least-Privilege Security | `[ ]` pending |
| 2.3 | S3 Object Storage — CMF Asset Layer | `[ ]` pending |
| 2.4 | VPC & Networking | `[ ]` pending |
| 2.5 | EC2 Compute — Raw GPU Machines | `[ ]` pending |
| 2.6 | ECS Container Orchestration | `[x]` completed |
| 2.7 | AWS CLI Mastery | `[x]` completed |
| 2.8 | What is Nvidia NIM | `[ ]` pending |
| 2.9 | GPU Compute Physics | `[ ]` pending |
| 2.10 | AWS GPU Tier Map | `[ ]` pending |
| 2.11 | Cold Start Physics & Keep-Warm | `[ ]` pending |
| 2.12 | NIM for TTS — Deploying Voice | `[ ]` pending |
| 2.13 | NIM for ComfyUI — Visual Factory | `[ ]` pending |
| 2.14 | Migrating from RunningHub | `[ ]` pending |
| 2.15 | Cost Engineering & Budget Ceilings | `[ ]` pending |

### Chapter 03: The Agentic Harness (15 units)
| Unit | Title | Status |
|------|-------|--------|
| 3.1 | The Wrapper Trap vs The Harness | `[ ]` pending |
| 3.2 | The 5 Techniques of Agentic Engineers | `[ ]` pending |
| 3.3 | Swarm Mechanics — Entomology of Agents | `[ ]` pending |
| 3.4 | Skills Systems & MCP Protocol | `[ ]` pending |
| 3.5 | Contrastive Debate — Generator vs Adversary | `[ ]` pending |
| 3.6 | Deterministic Handoffs & A2A Protocol | `[ ]` pending |
| 3.7 | Hierarchical Context & Pheromone Trails | `[ ]` pending |
| 3.8 | Token Economics & Query Engine Design | `[ ]` pending |
| 3.9 | Hook Pipelines — Pre/Post/Stop | `[ ]` pending |
| 3.10 | CBAR — The Harness's Immune System | `[ ]` pending |
| 3.11 | Dynamic Persona Shifting | `[ ]` pending |
| 3.12 | Prompt Caching Physics | `[ ]` pending |
| 3.13 | Permission ACLs & Risk Classification | `[ ]` pending |
| 3.14 | The Human as Arbiter Node | `[ ]` pending |
| 3.15 | CBAR in the CCP Pipeline — Integration | `[ ]` pending |
| 3.16 | **The CCF Harness — Anatomy of 41 Commands** | `[ ]` pending |
| 3.17 | **Externalized State Theory — Why Harnesses Survive Context Death** | `[ ]` pending |

### Chapter 04: The CLI Operator (11 units)
| Unit | Title | Status |
|------|-------|--------|
| 4.1 | Terminal-Native Architecture | `[x]` completed |
| 4.2 | The Extended ReAct Loop | `[x]` completed |
| 4.3 | Context Engineering — AGENTS.md & Skills | `[x]` completed |
| 4.4 | Subagent Spawning & Delegation | `[x]` completed |
| 4.5 | Checkpointing & Tree History | `[x]` completed |
| 4.6 | Model Routing & Cascade | `[x]` completed |
| 4.7 | Tool Permission & Auto-Run | `[ ]` pending |
| 4.8 | Packaging Harness Extensions | `[ ]` pending |
| 4.9 | **Command File Anatomy — The Harness File Format** | `[ ]` pending |
| 4.10 | **Authoring `ccp-health-check` — First CCP Command** | `[ ]` pending | → produces `commands/ccp-health-check.md`
| 4.11 | **Authoring `ccp-onboard` — Coach Onboarding Command** | `[ ]` pending | → produces `commands/ccp-onboard.md`

### Chapter 05: Hypergraph Memory (8 units)
| Unit | Title | Status |
|------|-------|--------|
| 5.1 | The Vector Illusion vs Causality | `[x]` completed |
| 5.2 | Hypergraph Architecture — N-Ary Edges | `[x]` completed |
| 5.3 | The Hippocampal Extraction Engine | `[ ]` pending |
| 5.4 | Multi-Hop Graph Traversal | `[ ]` pending |
| 5.5 | Temporal Logic — Chronological Edges | `[x]` completed |
| 5.6 | Entity Resolution & Identity Merging | `[x]` completed |
| 5.7 | Graph Pruning — Physics of Forgetting | `[ ]` pending |
| 5.8 | Graph Injection — Working Context | `[ ]` pending |

### Chapter 06: The Agentic Core (7 units)
| Unit | Title | Status |
|------|-------|--------|
| 6.1 | The ReAct Loop — Reason → Act → Observe | `[ ]` pending |
| 6.2 | State Machine Theory — LangGraph | `[ ]` pending |
| 6.3 | Schema Enforcement with Pydantic AI | `[ ]` pending |
| 6.4 | The 4-Agent Pipeline Deep-Dive | `[ ]` pending |
| 6.5 | Context Engineering — 12D Premise | `[ ]` pending |
| 6.6 | TTT Enforcement — Voice as Psychology | `[ ]` pending |
| 6.7 | Wiring the Scheduled Voice Tracking Loop | `[ ]` pending |

### Chapter 07: The CMF Pipeline (10 units)
| Unit | Title | Status |
|------|-------|--------|
| 7.1 | The Pipeline Commander — 16 States | `[ ]` pending |
| 7.2 | Audio Physics — Whisper + Demucs | `[ ]` pending |
| 7.3 | Diffusion Model Theory | `[ ]` pending |
| 7.4 | I2V Physics — Motion & VRAM | `[ ]` pending |
| 7.5 | ComfyUI Architecture — Workflow JSON | `[ ]` pending |
| 7.6 | LoRA Training Science | `[ ]` pending |
| 7.7 | Fingerprinting & Surgical Regen | `[ ]` pending |
| 7.8 | Remotion — Declarative Video Manifests | `[ ]` pending |
| 7.9 | Caption Typography — Karaoke Sync | `[ ]` pending |
| 7.10 | The Constraint Gate Network | `[ ]` pending |

### Chapter 08: The Video Editor (9 units)
| Unit | Title | Status |
|------|-------|--------|
| 8.1 | Manifest = Project File | `[ ]` pending |
| 8.2 | @remotion/player — Zero-Cost Preview | `[ ]` pending |
| 8.3 | Timeline Architecture — Tracks & Frames | `[ ]` pending |
| 8.4 | Beat-Level Review — Quality Gate Pattern | `[ ]` pending |
| 8.5 | The AI Copilot Pattern — NL → Edit | `[ ]` pending |
| 8.6 | Export Engineering — Codec & Bitrate | `[ ]` pending |
| 8.7 | Inspector + Gate M — Pre-Edit Validation | `[ ]` pending |
| 8.8 | The Dashboard — Project Management | `[ ]` pending |
| 8.9 | FastAPI Backend Bridge | `[ ]` pending |

### Chapter 09: Coach Dashboard / AFFiNE (4 units)
| Unit | Title | Status |
|------|-------|--------|
| 9.1 | AFFiNE Architecture — CRDT & BlockSuite | `[ ]` pending |
| 9.2 | Workspace Provisioning — Coach Isolation | `[ ]` pending |
| 9.3 | Client Workspace — Content Delivery | `[ ]` pending |
| 9.4 | Sync Engine — Headless CRDT Writes | `[ ]` pending |

### Chapter 10: Platform — Telegram + Stripe (4 units)
| Unit | Title | Status |
|------|-------|--------|
| 10.1 | Telegram Scheduled Voice Tracking | `[ ]` pending |
| 10.2 | Social Penetration Theory — SPT Stages | `[ ]` pending |
| 10.3 | Stripe Credits — Pay-Per-Use Economics | `[ ]` pending |
| 10.4 | The Onboarding Flow — User → Client | `[ ]` pending |

### Chapter 11: Persistence Layer (5 units)
| Unit | Title | Status |
|------|-------|--------|
| 11.1 | Dual-Database Architecture — Why Both | `[ ]` pending |
| 11.2 | Schema Design & Migrations | `[ ]` pending |
| 11.3 | Neo4j Production — Aura & Cypher | `[ ]` pending |
| 11.4 | Receipt Chain — Provenance Tracking | `[ ]` pending |
| 11.5 | Backup & Disaster Recovery | `[ ]` pending |

### Chapter 12: Launch & Hardening (6 units)
| Unit | Title | Status |
|------|-------|--------|
| 12.1 | Docker Compose — Service Orchestration | `[ ]` pending |
| 12.2 | CRON Scheduling — The Batch Clock | `[ ]` pending |
| 12.3 | GPU Lifecycle Manager — Spin Up/Down | `[ ]` pending |
| 12.4 | Monitoring & Alerting | `[ ]` pending |
| 12.5 | Load Testing — 100×5 Target | `[ ]` pending |
| 12.6 | Go-Live Checklist — Launch Day | `[ ]` pending |

---

## Critical Corrections Applied

### 1. Schedule-Based Architecture ✅
Chapters 1, 2, 6, 10, 12 updated to reflect:
- Agents activate on SCHEDULES, not continuously
- GPU instances spin up for batches then terminate
- Telegram is voice tracking (3-5 msgs/session), NOT chatbot
- Only dashboards (Video Editor + AFFiNE) + API + DB are always-on

### 2. Documentation Library ✅
All chapters map to our 290+ source documents:
- 148 tech specs (`docs/architecture/`)
- 43+ academic papers (`lab/`)
- 12+ root reference docs (AWS, NVIDIA, NLAH, etc.)
- 4 PRDs (`docs/prd/`)
- 75 skill files

### 3. Science Sources Column ✅
Unit map tables now include `📄 Science Sources` column (8 columns total)

### 4. Harness Command Output Gate (NEW) ✅
Build chapters now produce `ccp-*` command files as tangible outputs:

| Command | Produced In | Template | Purpose |
|---------|------------|----------|--------|
| `ccp-health-check.md` | Ch 4.10 | `ccf-validate.md` | Validate all CCP services operational |
| `ccp-onboard.md` | Ch 4.11 | `ccf-init.md` | Coach onboarding pipeline |
| `ccp-voice-track.md` | Ch 6.7 | `ccf-weekly.md` | Scheduled voice accountability session |
| `ccp-onboard-client.md` | Ch 10.4 | `ccf-init.md` | Client onboarding (coach counterpart) |
| `ccp-deploy.md` | Ch 12.1 | `ccf-batch.md` | Docker Compose production deployment |
| `ccp-schedule.md` | Ch 12.2 | `ccf-batch.md` | CRON scheduler configuration |
| CCP Pipeline DAG | Ch 3.17 | — | Dependency graph for all `ccp-*` commands |

### 5. Pi as Target Runtime ✅
Claude Code + Gemini CLI are studied as RESEARCH SUBJECTS (harness science extraction).
Pi Coding Agent is the TARGET RUNTIME where intelligence layers are built.
`commands/` format (markdown + YAML frontmatter) is Pi-compatible by design.
