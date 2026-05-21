from starlette.testclient import TestClient
from src.ccp.api.main import app

client = TestClient(app)
try:
    response = client.get("/api/phase0/operator/queue?workspace_id=test-ws-empty")
    print("STATUS CODE:", response.status_code)
    print("RESPONSE JSON:", response.json())
except Exception as e:
    import traceback
    traceback.print_exc()
