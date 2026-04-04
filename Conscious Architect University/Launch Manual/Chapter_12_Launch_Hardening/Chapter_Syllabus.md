# Chapter 12: Launch & Hardening (Go-Live)

**Chapter Goal:** Compose all subsystems into a production Docker deployment with CRON schedulers, monitoring, and the final go-live checklist
**Mastery Track:** CCP System Architect (capstone)
**Launch Track:** THE PLATFORM IS LIVE. First coach onboarded. First batch runs. First client interaction processed.
**Prerequisites:** ALL previous chapters (1-11)
**Estimated Time:** 8-10 hours

---

## CCP/CMF Reality Anchor

Every previous chapter built a subsystem in isolation. This chapter WIRES them together into a production deployment. Docker Compose orchestrates 6+ services. CRON schedulers trigger batch processing on schedule. Monitoring catches failures before clients notice. Load testing verifies the system handles 100 coaches × 5 clients. This is the final engineering effort before revenue generation.

**CRITICAL:** The deployment is SCHEDULE-BASED. Docker Compose starts persistent services (dashboards, API, databases) and CRON-scheduled batch services (content generation, voice tracking, CMF pipeline). GPU instances are provisioned ON-DEMAND by the scheduler, not kept running.

---

## Codebase Map

| File | Location | Size | Status |
|------|----------|------|--------|
| `cmf-docker/` | `cmf/` | directory | ✅ EXISTS — Docker configs |
| `pipeline_commander.py` | `cmf/apps/cmf-assembler/` | 24KB | ✅ EXISTS |
| `scheduled_monitor.py` | `src/ccp/agents/` | 17KB | ✅ EXISTS |
| `scheduled_monitor_service.py` | `src/ccp/services/` | 22KB | ✅ EXISTS |
| `docker-compose.yml` | — | — | ⚠️ BUILD REQUIRED — production compose |
| `Dockerfile` (per service) | — | — | ⚠️ BUILD REQUIRED |
| **`commands/`** | workspace root | **41 files** | ✅ EXISTS — production harness (ccp-* by Ch12 = 7+ commands) |
| `ccf-batch.md` | `commands/` | 243 lines | ✅ EXISTS — batch orchestration template for `ccp-deploy` |

**Files referenced: 8** ✅

---

## Science Sources

| Source | Location | Type |
|--------|----------|------|
| `Infrastructure_AWS_NIM_Deployment_Spec.md` (35KB) | `docs/architecture/` | Deployment architecture |
| `Final_Architecture_Stress_Test_Documentation.md` (45KB) | `docs/architecture/` | Stress test results |
| `Final_Architecture_Stress_Test_Phase4_CA11.md` (11KB) | `docs/architecture/` | Phase 4 stress test |
| `Final_Architecture_Stress_Test_Visual_Commercial_Layer.md` (31KB) | `docs/architecture/` | Visual layer stress test |
| `FR49_Single_Tenant_Deployment_Tech_Spec.md` (12KB) | `docs/architecture/` | Single-tenant deployment |
| `NVIDIA NCA AIIO Course` | workspace root | GPU infrastructure certification |

---

## Unit Map

| Unit | Title | 🧠 Science Topic | UNLEARN | 📂 Code Files | 📄 Science Sources | Build Target | Verify |
|------|-------|-------------------|---------|---------------|-------------------|-------------|--------|
| 12.1 | Docker Compose — Service Orchestration | Multi-service composition: persistent services (API, dashboards, databases) + CRON-triggered services (agent batches, CMF pipeline). Health checks, restart policies, shared networks, volume mounts. Why Compose beats manual Docker run | "Run each service manually." False — 6+ services with interdependencies, health checks, and restart policies require orchestration. Docker Compose makes the entire stack reproducible with `docker compose up` | `cmf-docker/`, existing Dockerfiles | `Infrastructure_AWS_NIM_Deployment_Spec.md` §Docker | 🤖 Build production `docker-compose.yml` + `commands/ccp-deploy.md` harness command: PRE-FLIGHT (all images built, .env populated) → COMPOSE-UP (start all services) → HEALTH-CHECK (run `ccp-health-check` from Ch4.10) → VERIFY (all services healthy) → CHECKPOINT (deployment log). Template: `ccf-batch.md` | Execute `ccp-deploy` → all services healthy, `docker compose ps` → no restarts |
| 12.2 | CRON Scheduling — The Batch Clock | How CRON drives the schedule-based architecture. **TWO separate schedules:** (1) **COACH content schedule** — weekly: `ccf-weekly` produces scripts + recording guides → coach records via Studio Block during the week → raw recordings upload to S3 → CMF pipeline processes. (2) **CLIENT accountability schedule** — PROGRAM-DEPENDENT: each program's `check_in_schedule` field (FR-COM-04) defines which days (daily, MWF, TuTh, etc.) via `PantryConfig`. Atlas's 4+1+2 template governs eligible days. Rest Days are sacred = zero messages. CMF pipeline trigger fires after content batch + after recording upload | "The system sends daily check-ins." False — TWO CRON clocks: (1) Weekly content batch (Sunday night: scripts generated → coach records during the week → CMF processes recordings), (2) Per-client accountability (2-3x/week per program, NOT daily unless `check_in_schedule` explicitly says so). Rest Days are physically blocked. Between schedules, GPU services are OFF | `scheduled_monitor.py`, `scheduled_monitor_service.py` | `FR15_Scheduled_Monitor_Agent_Tech_Spec.md`, `FR-COM-04_Program_Campaign_Manager_Tech_Spec.md` (check_in_schedule field), `FR28_Dynamic_Journaling_Tech_Spec.md` (PantryConfig + 4+1+2) | 🤖 Build `commands/ccp-schedule.md` harness command: PRE-FLIGHT (verify deployment healthy) → CONFIGURE-CONTENT-BATCH (Sunday 22:00 `ccf-weekly` trigger) → CONFIGURE-COACH-RECORDING (weekly recording window via Studio Block) → CONFIGURE-CLIENT-ACCOUNTABILITY (read each program's `check_in_schedule`, configure per-client CRON slots respecting 4+1+2 Rest Days) → CONFIGURE-CMF (trigger after content batch + after recording upload) → VERIFY (all CRON rules active) → CHECKPOINT | Execute `ccp-schedule` → `aws events list-rules` shows: weekly content batch + per-program accountability CRONs + CMF pipeline trigger |
| 12.3 | GPU Lifecycle Manager — Spin Up/Down | How spot instances are provisioned ON-DEMAND for GPU-intensive tasks (ComfyUI T2I, I2V, TTS). The lifecycle: CRON triggers → request spot instance → wait for capacity → run batch → terminate instance → log cost. Cold-start mitigation via pre-warm | "Keep GPUs running 24/7." False — $30/hr × 24h × 30 days = $21,600/month. On-demand spot: $2/hr × 3h/week = $24/month. Lifecycle management is the difference between bankruptcy and profitability | `pipeline_commander.py` — cost tracking | `Infrastructure_AWS_NIM_Deployment_Spec.md` §Cost Model, `NVIDIA NCA AIIO Course` §GPU Scheduling | 🤖 Build GPU lifecycle manager (request → provision → run → terminate) | Spot instance provisioned → batch processed → instance terminated → CloudWatch log shows cost |
| 12.4 | Monitoring & Alerting | CloudWatch dashboards for batch completion rates, GPU costs, database size, error rates. PagerDuty/SNS alerting for batch failures. The 4 golden signals: latency, traffic, errors, saturation | "We'll add monitoring later." False — monitoring is a LAUNCH REQUIREMENT, not a post-launch luxury. A failed batch that goes unnoticed means a coach's content week is missing. Alerting catches failures before clients do | — | `Final_Architecture_Stress_Test_Documentation.md` (45KB) | 🤖 Build CloudWatch dashboard + batch failure alarm | `aws cloudwatch describe-alarms` → alarm configured. Simulate batch failure → alert fires |
| 12.5 | Load Testing — 100×5 Target | The production target: 100 coaches × 5 clients × weekly batch. Simulating concurrent batch processing. Database connection pooling. S3 concurrent upload limits. Identifying the bottleneck (GPU, database, or API) | "It works for 1 coach so it works for 100." False — concurrent batch processing creates contention: database connections, S3 rate limits, GPU availability. Load testing reveals the FIRST bottleneck before paying clients find it | `pipeline_commander.py` | `Final_Architecture_Stress_Test_Documentation.md`, `Final_Architecture_Stress_Test_Phase4_CA11.md` | ⌨️ Run load test simulating 100 concurrent batch requests | Load test passes for 100 coaches. No database timeouts. All batches complete within 4 hours |
| 12.6 | Go-Live Checklist — Launch Day | The final verification: all services healthy, first coach onboarded, first batch triggered, first client interaction processed, backups verified, monitoring active, billing functional. The definition of DONE | "Launch when it feels ready." False — launch has a CHECKLIST of 15 binary pass/fail items. If any item fails, launch is blocked. Feelings are not an observable | All files across all chapters | All stress test documentation | ✅ Execute the 15-item go-live checklist | All 15 checklist items pass. First coach receives first batch. System is LIVE |

---

## Quality Gates

- [x] **Unit Count Gate:** 6 units ✅
- [x] **5-File Gate:** 8 codebase + 6 science sources ✅
- [x] **Schedule-Based Gate:** Units 12.2 and 12.3 ARE the schedule-based architecture ✅
- [x] **Harness Artifact Gate (NEW):** 2 new `ccp-*` commands produced (`ccp-deploy.md`, `ccp-schedule.md`) ✅
