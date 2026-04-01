# Canva Clone Integration into CCP — CVE Canvas Assembly

## Goal

Clone the [Canva clone repo](https://github.com/Davronov-Alimardon/canva-clone) (Next.js 14 + Fabric.js) into the CCP project and wire it to the existing `canvas_composition_service.py` backend (FR-VIS-05). This gives the CVE pipeline a visual canvas editor where operators can review, edit, and approve generated compositions.

## User Review Required

> [!IMPORTANT]
> **The Canva clone has heavy external dependencies.** The original repo requires: Neon PostgreSQL, UploadThing, Replicate AI, Stripe, Google OAuth, and GitHub OAuth. Our integration plan **strips out** all SaaS/payment dependencies and keeps only the Fabric.js canvas editor core + Unsplash image search. The CCP backend replaces the Hono.js API layer entirely.

> [!WARNING]
> **This repo uses `bun` as its package manager.** If you don't have `bun` installed, we'll fall back to `npm`. The plan accounts for both.

## Proposed Changes

### Component 1: Clone & Install the Canva Clone

#### [NEW] `canva-app/` (root-level directory)

- Clone the repo into `d:\Work\The Conscious Coaching Factory\canva-app\`
- Run `npm install` (or `bun install`) to set up dependencies
- Configure `.env` with minimal required variables:
  - `NEXT_PUBLIC_APP_URL=http://localhost:3000`
  - `NEXT_PUBLIC_UNSPLASH_ACCESS_KEY` (already have `UNSPLASH_ACCESS_KEY` in root `.env`)
  - `NEXT_PUBLIC_CCP_API_URL=http://localhost:8000` (our FastAPI backend)
  - `AUTH_SECRET` (generate a random secret for local dev)
  - `DATABASE_URL` (Neon free tier or local PostgreSQL — needed for Drizzle schema)

---

### Component 2: CCP Backend — New Canvas API Router

#### [NEW] [canvas_api.py](file:///d:/Work/The%20Conscious%20Coaching%20Factory/src/ccp/api/canvas_api.py)

New FastAPI router exposing the `CanvasCompositionService` to the Canva frontend:

- `POST /api/canvas/compositions` — Create composition from VCB
- `GET /api/canvas/compositions/{id}` — Get composition details  
- `POST /api/canvas/compositions/{id}/assets` — Receive RunningHub asset for a slide
- `POST /api/canvas/compositions/{id}/export` — Export composition
- `POST /api/canvas/compositions/{id}/approve` — Approve & publish
- `POST /api/canvas/compositions/{id}/regenerate` — Request slide regeneration
- `GET /api/canvas/templates` — List available templates

#### [MODIFY] [main.py](file:///d:/Work/The%20Conscious%20Coaching%20Factory/src/ccp/api/main.py)

- Import and register the new `canvas_api` router
- Add `http://localhost:3000` to CORS origins (for Canva frontend → CCP backend communication)

---

### Component 3: Docker Compose Update

#### [MODIFY] [docker-compose.yml](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docker/docker-compose.yml)

- Add a `canva-app` service running the Next.js frontend on port 3000
- Wire it to the same network as the CCP backend

---

## Verification Plan

### Automated Tests

**Existing tests (must still pass):**
```powershell
python -m pytest tests/integration/test_vis05_canvas_composition.py -v
# Expected: 60 tests passing (the existing 6 AC tests + edge cases)
```

**New test — Canvas API router:**
```powershell
python -m pytest tests/integration/test_canvas_api.py -v
```
- A new integration test file that tests the FastAPI endpoints using `TestClient`
- Covers: composition CRUD, asset reception via API, approval flow, CORS headers, error responses

### Manual Verification

1. **Start the Docker stack** with `docker-compose up -d` → verify `canva-app` container starts on port 3000
2. **Open `http://localhost:3000`** → verify the Canva editor loads
3. **Hit `http://localhost:8000/api/canvas/templates`** → verify templates endpoint returns JSON
4. **Full regression:** `python -m pytest tests/ -v` → all 1,913+ tests still pass
