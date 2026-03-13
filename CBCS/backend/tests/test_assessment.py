import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.config import get_settings
from unittest.mock import MagicMock, patch

settings = get_settings()
client = TestClient(app)

# Mock Supabase Client to avoid hitting real DB in unit tests
# However, for integration verification, we might want to hit the real DB if configured.
# Given the user just ran the migration, let's try a real integration test if credentials are present.
# But usually, we mock external services in CI. Let's do a mocked test first for safety/speed.

@pytest.fixture
def mock_supabase():
    with patch("backend.api.assessment.supabase") as mock:
        yield mock

def test_submit_assessment_success(mock_supabase):
    # Setup Mock
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [] # No existing profile
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [{"id": "test-uuid"}] # Insert return

    payload = {
        "telegram_chat_id": 123456789,
        "first_name": "Test",
        "last_name": "User",
        "answers": {
            "dimension_1": 5,
            "dimension_2": "High"
        }
    }

    response = client.post("/api/v1/assessment/submit", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert "capacity_score" in data
    assert "identity_pillar" in data
    assert data["identity_pillar"] == "The Builder" # Default mock logic

    # Verify Supabase calls
    # 1. Check profile existence
    # 2. Insert profile
    # 3. Insert assessment
    assert mock_supabase.table.call_count >= 3
