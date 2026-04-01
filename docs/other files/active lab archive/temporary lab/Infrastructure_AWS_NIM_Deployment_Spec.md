# Infrastructure Technical Specification: AWS × NVIDIA NIM Enterprise Deployment

**Document ID:** SPEC-INFRA-001
**Title:** Cloud Implementation & NVIDIA NIM Enterprise Deployment Architecture
**Version:** 1.0.0
**Date:** 2026-03-30
**Environment:** Production Launch (AWS)
**Classification:** STRATEGIC INFRASTRUCTURE

---

## 1. Executive Summary

This document serves as the exhaustive architectural blueprint for deploying the **Conscious Coaching Platform (CCP)** and the **Conscious Media Factory (CMF)** into production. It formally details the migration from legacy third-party proxy APIs (like RunningHub) to a sovereign, enterprise-grade cloud architecture utilizing **Amazon Web Services (AWS)** and the **NVIDIA NIM (NVIDIA Inference Microservices)** Enterprise program.

By securing access to the NVIDIA Enterprise Partnership and AWS Startup Credits, CCP is now positioned to host its own high-performance ML models on bare-metal or dedicated EC2 instances (H100/A100 class) with full data governance, no third-party rate limits, and sub-second inference latency.

This architecture specifically addresses the transition from a **single-user local prototype** to a **multi-user, state-isolated agentic platform**. It incorporates advanced GPU partitioning (MIG), strict state isolation protocols (via Redis), PII buffering, and compound agentic engineering to prevent cost explosions and data leakage across the isolated coach environments.

---

## 2. The Architectural Imperative: Multi-User vs. Single-User Agents

The most critical realization driving this infrastructure design is the fundamental difference between single-user agents ("agent core") and multi-user agents ("agent harness"). 

In a local, single-developer environment, an agent prioritizes depth: it can loop indefinitely, utilize unlimited context windows, and monopolize GPU VRAM. In a production multi-tenant environment (representing dozens of coaches and thousands of clients), this depth-first approach is catastrophic. 

### The Three Multi-User Threats:

1. **State Collision Risk:** The CCP handles deeply personal psychological data (Voice DNA, CBCS coping trajectories, SPT depth gauges). If Coach A's agent accidentally retrieves Coach B's telemetry due to a shared memory space, it is a fatal data breach. 
2. **Cost Explosion Risk:** Unbounded agentic loops (e.g., an LLM hallucinating and retrying a rejected visual prompt 500 times) running on a $40/hour H100 instance can bankrupt a startup overnight. Without hard per-user execution quotas and token budgets, the infrastructure is financially vulnerable.
3. **Concurrency Bottlenecks:** When 15 coaches trigger their weekly CCF generation batch simultaneously, attempting to load 15 separate instances of FLUX 2 Dev or a 70B language model into VRAM sequentially will cause system timeouts. The models must be served concurrently via optimized inference servers.

This deployment specification resolves these threats through a custom **Agent Harness Architecture**, leveraging AWS for structural isolation and NVIDIA NIM for optimized, concurrent inference.

---

## 3. NVIDIA NIM Enterprise Integration

NVIDIA Inference Microservices (NIM) provides pre-built, optimized, and accelerated containers for deploying AI models. By utilizing the NVIDIA Enterprise Partnership, CCP bypasses raw Docker / CUDA configuration in favor of production-ready Triton Inference Servers wrapped in NIM containers.

### 3.1 Model Serving Architecture

Instead of loading weights dynamically in Python scripts, all core ML models are deployed as persistent stateless services running on dedicated AWS p4d/p5 instances.

**The NIM Server Farm:**
- **LLM NIM (Language):** Serving Llama 3 / Mistral variants for the JIT Skill Compiler (CCF), Voice DNA distillation, and CRAL research summarization. Optimized with TensorRT-LLM for massive KV caching and continuous batching.
- **Vision NIM (Generation):** Serving FLUX 2 Dev (MMDiT) as the base model for the Visual Control Layer.
- **Audio NIM (Transcription/Processing):** Serving Whisper (STT) and Demucs for the CMF Video Pipeline's Audio Engine.
- **Embedding NIM (Retrieval):** Serving Nomic-Embed-Text or similar models for Neo4j vector ingestion and CRAL semantic searches.

### 3.2 MIG (Multi-Instance GPU) Partitioning

To maximize the ROI of high-cost A100/H100 instances, the CCP infrastructure utilizes NVIDIA's **MIG (Multi-Instance GPU)** technology. MIG allows a single physical GPU to be securely partitioned into up to seven fully isolated GPU instances, each with its own high-bandwidth memory, cache, and compute cores.

**Partitioning Strategy for an A100 (80GB):**
- **Partition A (40GB):** Dedicated strictly to the Vision NIM (FLUX 2 Dev + ComfyUI). Image generation requires massive contiguous VRAM for batch processing 1080p generation with ControlNet and Adapters.
- **Partition B (20GB):** Dedicated to the LLM NIM. Handles all JIT Skill Compiler requests.
- **Partition C (10GB):** Dedicated to the Audio NIM (Whisper + Demucs) which only spikes during video pipeline initialization.
- **Partition D (10GB):** Dedicated to the Embedding NIM and utility models (e.g., CLIP scoring for the T2I Quality Gate).

**Why MIG solves the multi-user bottleneck:** Without MIG, if the Vision NIM is generating a 20-image batch, the Audio NIM might be starved of compute, causing the Whisper transcription to hang. MIG guarantees strict hardware isolation — a heavy load on Partition A has zero impact on the latency of Partition B.

---

## 4. AWS Cloud Infrastructure Footprint

The CCP backend migrates from a local `docker-compose` stack to a highly available, scalable AWS footprint.

### 4.1 Compute Layer (ECS/EKS & EC2)

- **Agent Orchestration (CPU):** The Python FastApi backend, the CMF Pipeline Commander, the JIT Skill Compiler orchestrator, and the 84+ agents run on **AWS ECS (Elastic Container Service) on AWS Fargate**. These are stateless, CPU-bound processes. Running them on Fargate means we only pay for exact compute time, and they scale horizontally as more coaches trigger pipelines.
- **Inference (GPU):** The NIM containers and custom ComfyUI backends run on **Amazon EC2 p4d.24xlarge (A100) or p5.48xlarge (H100)** instances depending on scaling demands. These instances are reserved utilizing the startup cloud credits. They run inside an Auto Scaling Group (ASG) based on queue depth metrics.

### 4.2 Storage & Database Layer

- **Supabase / PostgreSQL (RDS):** The relational database (users, billing, `learning_path_registry`, `social_performance`) is hosted on **Amazon RDS for PostgreSQL**. 
- **Neo4j Graph Database (EC2/Aura):** The Context Premise hypergraph and user memory maps.
- **AWS ElastiCache (Redis):** Crucial for the Multi-User Agent Harness. Used for:
  - **State Isolation:** Agent "scratchpads" and working memory are stored in Redis under strict `coach_id:session_id` keys to guarantee separation.
  - **Queueing:** CMF Pipeline batch queues and Social Scheduler queues (Celery/RQ).
  - **Receipt Chain Caching:** Ensuring rapid cryptographic hashing for the Receipt Chain Guard.
- **AWS S3 (Simple Storage Service):** The definitive blob storage replacing local disk. 
  - `ccp-raw-audio`: Unprocessed coach voice notes.
  - `ccp-generated-assets`: T2I keyframes, ComfyUI videos, rendered Remotion MP4s. (Segmented by `coach_id`).
  - `ccp-system-backups`: Nightly AFFiNE database backups and Neo4j dumps.

### 4.3 PII Buffering & Security Pipeline

Coaching involves extremely raw, private data (trauma, financial realities, relationship issues). The architecture implements a **PII Buffer Layer** before data ever reaches the LLM NIM.

1. **Ingestion:** A Telegram voice note arrives. It is sent to the local Whisper NIM (no data leaves the VPC).
2. **Buffering:** A lightweight Named Entity Recognition (NER) model (e.g., Presidio) runs locally to scrub proper nouns, phone numbers, and exact locations, replacing them with generic tokens (e.g., `[CLIENT_NAME]`, `[CITY]`).
3. **Processing:** The anonymized transcript is processed by the agent. 
4. **Rehydration:** The output is rehydrated with the real entities just before delivery to the coach's AFFiNE workspace.

Because the NVIDIA NIM containers run inside our own AWS Virtual Private Cloud (VPC), **zero data is transmitted to OpenAI, Anthropic, or external providers for the core confidential workloads.** This provides total data sovereignty.

---

## 5. Cost Containment & The "Kill Switch" Architecture

In an agentic system, a logical bug can consume thousands of dollars in an hour. To protect the AWS Startup Credits, the infrastructure implements hardware and software kill switches.

### 5.1 Per-User Quotas (Redis Token Bucket)

Every coach account is assigned a strictly enforced token budget for:
- LLM inference tokens (in/out)
- Image generation seconds
- Video rendering minutes

The API Gateway queries Redis using a Token Bucket algorithm before routing any request to the NIM servers. If a coach's agentic loop goes rogue, it will drain the bucket and the system will automatically halt further generation for that coach, firing a high-priority alert to the Platform Ops channel via AWS SNS.

### 5.2 Agent Execution Timeouts

The CMF Pipeline Commander orchestrates up to 30 tool calls per CMF video. All agent orchestrations run within AWS Step Functions or a persistent Celery worker tree. Every node in the workflow has a hard timeout:
- Transcription: Max 300s
- Image Generation: Max 45s per image
- Agent Reasoning: Max 60s per loop

If an agent gets stuck in a "thought loop", the worker terminates the process, refunds the partial token cost, and marks the job as `REGENERATING_REQUIRED` with a backoff.

### 5.3 Infrastructure Alarms

**AWS CloudWatch** billing alarms are configured at $50, $100, and $500 daily increments. If a rogue process bypasses the token bucket and spins up additional EC2 instances, a Lambda function is triggered directly by CloudWatch to immediately scale the GPU Auto Scaling Group down to 0, physically cutting the cost vector until an operator intervenes.

---

## 6. Integration: ComfyUI Migration on AWS

The previous PRD formalized the migration from RunningHub (third-party) to self-hosted ComfyUI. Under this AWS architecture, ComfyUI becomes a first-class citizen inside the VPC.

### 6.1 ComfyUI Server Setup

- Deployed as a Docker container on the same instances hosting the Vision NIM, utilizing direct access to Partition A of the A100.
- Workflows are statically defined as JSON in the Git repository (`comfyui-workflows/`).
- **Asset Mounting:** AWS Elastic File System (EFS) or S3 fuse (s3fs) is mounted directly to ComfyUI's `/models` directory to provide instant access to the **ConsciousPose Library** (DEP-VIS-010), **ConsciousSmile Adapter** (DEP-VIS-008), and the **Identity LoRAs** (DEP-VIS-011). 
- By sharing the EFS mount across multiple ComfyUI replicas, the system can autoscale horizontally. When a new GPU instance boots, it instantly has access to the full 300+ ControlNet map library without downloading gigabytes of data.

---

## 7. Operational Workflow: Deployment Pipeline

To deploy updates to this infrastructure without disrupting live coaches, the system uses a Blue/Green AWS CodePipeline.

1. **Agent Logic Updates:** Changes to `skills/**/*.md` or Python source code trigger a GitHub Action.
2. **Container Build:** A new Docker image is built for the ECS Fargate cluster.
3. **Approval Gate:** Automated tests (the 1,913 integration tests + 480 CMF tests) must pass.
4. **Zero-Downtime Rollout:** ECS provisions the new containers. Traffic is dynamically routed via the AWS Application Load Balancer (ALB). Once the new containers report healthy, the old containers are terminated.
5. **Model Weight Updates:** If a new Identity LoRA is trained, it is uploaded directly to the EFS/S3 model store. The ComfyUI instances do not need to restart; their REST API dynamic loading fetches the new weights instantly on the next request.

---

## 8. Summary of Architectural Achievements

By successfully bridging the CCP prototype to AWS and NVIDIA NIM:

1. **Data Sovereignty:** Achieved 100%. No client psychological data touches public API endpoints.
2. **Hardware Efficiency:** Achieved through NVIDIA MIG partitioning, maximizing the utility of every dollar spent on A100/H100 instances.
3. **Multi-User Safety:** Achieved via Redis state isolation, ensuring zero memory bleed between coach instances.
4. **Cost Certainty:** Achieved through the Token Bucket quota system and CloudWatch hardware kill switches.
5. **Visual Determinism:** Achieved by bringing ComfyUI in-house with direct volume mounts to the ConsciousPose and Identity LoRA libraries.

This infrastructure is not merely a hosting environment; it is the physical manifestation of the Conscious Coaching Platform's intelligence layer, built to scale to thousands of coaches without a linear increase in operational overhead.
