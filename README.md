# CCP — Conscious Coaching Platform

The **Conscious Coaching Platform (CCP)** is a multi-agent, single-tenant, cloud-native Trigger-First Operating System that automates premium content creation, client relationship intelligence, and conversion systems for professional coaches.

---

## Quick-Start for Operators

To launch this project you do **not** need to complete the Conscious Architect University (CAU) first.

The CAU is an advanced educational curriculum designed to deepen technical mastery of specific platform roles (AWS infrastructure, agentic orchestration, video pipeline, etc.). Completing it is **optional enrichment**, not a prerequisite gate for going live.

**What you actually need before launching:**

1. Docker + Python 3.11
2. `.env` populated with the 16 required API keys (see Section 3 of the Getting Started Guide)
3. Supabase project + 4 V5 migrations applied
4. Telegram bot token + Notion integration configured
5. Neo4j password changed from the default

Start here: [`docs/other files/active lab archive/CCP_Operator_Getting_Started_Guide.md`](docs/other%20files/active%20lab%20archive/CCP_Operator_Getting_Started_Guide.md)

---

## Conscious Architect University (CAU)

The CAU lives in the [`Conscious Architect University/`](Conscious%20Architect%20University/) directory and provides 11 courses across 6 deep-technical tracks:

| Track | Courses | Target Role |
|-------|---------|-------------|
| 1 — Infrastructure & Sovereign Defense | Courses 1–2 | AWS Cloud Practitioner / Nvidia AI Infra Operator |
| 2 — Autonomous Agentic Orchestration | Courses 3–4 | Agentic Harness Engineer |
| 3 — The Autonomous Studio (CMF) | Courses 5–8 | Creative Pipeline Architect |
| 4 — Ecosystem Acquisition & Architecture | Course 9 | CCP Hub Architect |
| 5 — Native Operations | Course 10 | Gemini-CLI Operator |
| 6 — Behavioral Systems Architecture | Course 11 | Behavioral Systems Architect |

**Course 10: The Gemini-CLI Operator Certification** is the course most directly relevant to daily CCP operations. It covers terminal-native agentic development, ReAct loop tuning, MCP tool integration, and Pi CLI orchestration. Taking it is **recommended but not required** to launch.
