# Technical Architecture & Implementation Design: Host-Level Provisioning & Authenticated Loopback Routing

**Document Version:** 1.0 (Era 3 - Phase 2 Design)  
**Status:** Approved for implementation blueprints  
**Related Specs:** `FR-COM-02` (Global Admin), `FR-CA11-16` (Studio Block), `FR-ERA3-06` (Primitive Registry)

---

## 1. Multi-Tenant Container Provisioning (Cloning Script Design)

To provision a new isolated client environment without violating single-tenant quarantine, the Host Control Plane runs a cloning manager daemon. When triggered via `POST /api/operator/provision`, it executes the following orchestrator shell script to clone a master base tenant image.

### Orchestrator Cloning Script Blueprint (`/usr/local/bin/clone-tenant.sh`)

```bash
#!/usr/bin/env bash
# clone-tenant.sh - Securely provisions an isolated single-tenant container environment.
# Usage: ./clone-tenant.sh <tenant_id> <subdomain> <port> <tier>

set -euo pipefail

TENANT_ID=$1
SUBDOMAIN=$2
PORT=$3
TIER=$4

echo "[INFO] Starting provisioning sequence for Tenant: ${TENANT_ID} (Subdomain: ${SUBDOMAIN}, Port: ${PORT}, Tier: ${TIER})"

# 1. Define Directories and Variables
TENANT_DATA_DIR="/var/lib/ccp/tenants/${TENANT_ID}"
MASTER_TEMPLATES_DIR="/var/lib/ccp/templates/master-tenant"
JWT_SECRET=$(openssl rand -hex 32)
OPERATOR_TOKEN=$(openssl rand -hex 32)
DB_PASSWORD=$(openssl rand -hex 16)

# 2. Create isolated storage volume on the host
echo "[INFO] Creating isolated host directories..."
mkdir -p "${TENANT_DATA_DIR}/db"
mkdir -p "${TENANT_DATA_DIR}/s3-mock"
mkdir -p "${TENANT_DATA_DIR}/config"

# 3. Seed config parameters and environment variables
echo "[INFO] Generating isolated environment configurations..."
cat <<EOF > "${TENANT_DATA_DIR}/config/.env"
DATABASE_URL=postgresql://ccp_user:${DB_PASSWORD}@db-${TENANT_ID}:5432/ccp_${TENANT_ID}
JWT_SECRET=${JWT_SECRET}
OPERATOR_TOKEN=${OPERATOR_TOKEN}
SFL_BRAND_TIER=${TIER}
TENANT_SUBDOMAIN=${SUBDOMAIN}
PORT=${PORT}
PRIMITIVES_DIR=/app/primitives
EOF

# 4. Initialize Isolated Docker Network Bridge
NET_NAME="ccp-net-${TENANT_ID}"
echo "[INFO] Initializing isolated network bridge: ${NET_NAME}"
docker network create --internal "${NET_NAME}" || true
# Allow network connection to Host Gateway bridge only
docker network connect ccp-gateway-bridge "db-${TENANT_ID}" || true

# 5. Spin up isolated PostgreSQL Database Container
echo "[INFO] Spawning isolated Supabase database replica container..."
docker run -d \
  --name "db-${TENANT_ID}" \
  --network "${NET_NAME}" \
  -v "${TENANT_DATA_DIR}/db:/var/lib/postgresql/data" \
  -e POSTGRES_DB="ccp_${TENANT_ID}" \
  -e POSTGRES_USER="ccp_user" \
  -e POSTGRES_PASSWORD="${DB_PASSWORD}" \
  postgres:15-alpine

# Wait for PostgreSQL container to start accepting connections
echo "[INFO] Waiting for database initialization..."
until docker exec "db-${TENANT_ID}" pg_isready -U "ccp_user" -d "ccp_${TENANT_ID}" >/dev/null 2>&1; do
  sleep 1
done

# Run initial schema migrations and default database seeds
echo "[INFO] Running baseline schema migrations and data seeding..."
docker run --rm \
  --network "${NET_NAME}" \
  -v "${MASTER_TEMPLATES_DIR}/migrations:/migrations" \
  postgres:15-alpine \
  psql -h "db-${TENANT_ID}" -U "ccp_user" -d "ccp_${TENANT_ID}" -f /migrations/init_schema.sql

# 6. Spin up isolated FastAPI Application Container
echo "[INFO] Spawning tenant FastAPI service container..."
docker run -d \
  --name "app-${TENANT_ID}" \
  --network "${NET_NAME}" \
  --env-file "${TENANT_DATA_DIR}/config/.env" \
  -v "${TENANT_DATA_DIR}/s3-mock:/app/storage" \
  -p "${PORT}:8000" \
  ccp-master-tenant:latest

# 7. Register tenant credentials in Host Control Plane Registry
echo "[INFO] Registering container mappings in host registry..."
REGISTRY_FILE="/etc/ccp/tenant-registry.json"
tmp=$(mktemp)
jq --arg id "${TENANT_ID}" \
   --arg sub "${SUBDOMAIN}" \
   --arg port "${PORT}" \
   --arg token "${OPERATOR_TOKEN}" \
   '.tenants += [{"id": $id, "subdomain": $sub, "port": $port, "operator_token": $token}]' \
   "${REGISTRY_FILE}" > "$tmp" && mv "$tmp" "${REGISTRY_FILE}"

echo "[INFO] Provisioning completed successfully for: ${TENANT_ID} on port ${PORT}."
```

---

## 2. Host Gateway Loopback Routing (FastAPI Design)

The **Host Gateway** acts as the broker for all operator queries. To preview a client's content, the operator issues queries to the Host Gateway. The Gateway maps the domain, fetches the internal port, and executes an authenticated loopback query directly to the tenant's container using the operator secret token.

### Host Gateway Router Blueprint (`src/ccp/api/host_gateway.py`)

```python
import httpx
import json
from fastapi import APIRouter, Header, HTTPException, Request, Response
from typing import Dict, Any

router = APIRouter(prefix="/api/operator")
REGISTRY_PATH = "/etc/ccp/tenant-registry.json"

def get_tenant_routing_info(tenant_id: str) -> Dict[str, Any]:
    """Resolves tenant ID to internal container host, port, and operator token."""
    try:
        with open(REGISTRY_PATH, "r") as f:
            registry = json.load(f)
        for tenant in registry.get("tenants", []):
            if tenant["id"] == tenant_id:
                return tenant
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Host Tenant Registry not found.")
    raise HTTPException(status_code=404, detail="Tenant environment not found.")

@router.api_route("/tenant/{tenant_id}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def route_loopback_proxy(
    tenant_id: str, 
    path: str, 
    request: Request,
    authorization: str = Header(..., description="Operator Master Key")
):
    # 1. Authenticate Operator Gateway request
    if authorization != "Bearer MASTER_CONTROL_KEY_SECRET":
        raise HTTPException(status_code=401, detail="Unauthorized Operator Access")

    # 2. Resolve target container network details
    tenant_info = get_tenant_routing_info(tenant_id)
    target_url = f"http://app-{tenant_id}:8000/api/admin/{path}"
    
    # 3. Read body from the operator's incoming payload
    body = await request.body()
    headers = dict(request.headers)
    
    # 4. Inject the tenant-specific Operator Token for authentication bypass
    headers["X-Operator-Token"] = tenant_info["operator_token"]
    headers.pop("host", None)
    headers.pop("authorization", None)

    # 5. Dispatch async loopback request to target isolated container
    async with httpx.AsyncClient() as client:
        try:
            target_response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                params=dict(request.query_params),
                timeout=10.0
            )
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=f"Loopback API failure: {exc}")

    # 6. Propagate response back to the Global Admin console
    return Response(
        content=target_response.content,
        status_code=target_response.status_code,
        headers=dict(target_response.headers)
    )
```

### Tenant Local Security Bypass (FastAPI Middleware in Tenant Containers)

```python
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

async def check_operator_token_middleware(request: Request, call_next):
    """Bypasses normal Row-Level Security checks for operations authenticated by host gateway."""
    operator_token = request.headers.get("X-Operator-Token")
    expected_token = os.environ.get("OPERATOR_TOKEN")
    
    if request.url.path.startswith("/api/admin/"):
        if not operator_token or operator_token != expected_token:
            return JSONResponse(status_code=403, content={"detail": "Forbidden: Invalid Operator Token"})
        
        # Inject operator context flag for bypass logic inside DB helper
        request.state.is_operator = True
        
    return await call_next(request)
```

---

## 3. Studio Block WebRTC SFU Route Decommissioning (FR-CA11-16 Cleanup)

To remove all live broadcasting, WebRTC SFU relays, and multi-party guest join endpoints, the following steps must be taken to clean the codebase during construction:

### A. Endpoint Cleanup Map
1. **Remove Route:** `POST /api/studio/broadcast/signal` inside [studio_block_api.py](file:///d:/Work/The%20Conscious%20Coaching%20Factory/src/ccp/api/studio_block_api.py).
2. **Remove Route:** `POST /api/studio/guest-invite` inside [studio_block_api.py](file:///d:/Work/The%20Conscious%20Coaching%20Factory/src/ccp/api/studio_block_api.py).
3. **Remove Websocket Route:** `/ws/stream/{session_id}` inside [studio_block_api.py](file:///d:/Work/The%20Conscious%20Coaching%20Factory/src/ccp/api/studio_block_api.py).
4. **Remove Websocket Route:** `/signal/{session_id}` inside [studio_block_api.py](file:///d:/Work/The%20Conscious%20Coaching%20Factory/src/ccp/api/studio_block_api.py).

### B. Obsolete Code Elimination
* **Delete File:** `src/ccp/services/guest_join_service.py`
* **Delete File:** `src/ccp/services/studio_block_service.py`
* **Delete File:** `tests/integration/test_ca11_fr21_guest_join.py`

---

## 4. Kept CBCS Mini-Apps: Integration with SFL, SDA, and Primitives

The 6 kept CBCS mini-apps track psychological progression and intimacy scales. They are integrated with the **Primitive Registry Query Service (`FR-ERA3-06`)** and log status to the **Receipt Chain Guard (`FR47`)**.

### Mini-App Integration Pattern

```python
from ccp.services.primitive_query import PrimitiveRegistryQueryService
from ccp.core.receipt_chain import ReceiptChainGuard
from ccp.models.cbcs_models import DepthGaugeScore

class SocialPenetrationDepthGauge:
    def __init__(self, db_session):
        self.db = db_session
        self.primitives = PrimitiveRegistryQueryService()
        self.receipt_guard = ReceiptChainGuard(db_session)

    async def evaluate_disclosure_depth(self, client_id: str, message_text: str) -> DepthGaugeScore:
        # 1. Fetch rating constants from Primitive Registry (FR-ERA3-06)
        scale_constants = self.primitives.query("social_penetration/scales")
        intimacy_thresholds = scale_constants["thresholds"]
        
        # 2. Run NLP semantic lookup (SFL evaluation rules)
        depth_score = calculate_semantic_closeness(message_text, intimacy_thresholds)
        
        # 3. Save score to database
        db_record = DepthGaugeScore(client_id=client_id, score=depth_score)
        self.db.add(db_record)
        await self.db.commit()
        
        # 4. Log immutable validation trace via Receipt Chain Guard (FR47)
        await self.receipt_guard.write_receipt(
            action="evaluate_disclosure_depth",
            asset_id=client_id,
            metadata={"depth_score": depth_score}
        )
        
        return db_record
```
