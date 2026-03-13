from fastapi.testclient import TestClient
from backend.main import app
from backend.config import get_settings
import pytest

client = TestClient(app)
settings = get_settings()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_telegram_webhook_missing_token():
    response = client.post("/webhooks/telegram", json={"test": "data"})
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid Secret Token"

def test_telegram_webhook_invalid_token():
    headers = {"X-Telegram-Bot-Api-Secret-Token": "wrong_token"}
    response = client.post("/webhooks/telegram", json={"test": "data"}, headers=headers)
    assert response.status_code == 403

def test_telegram_webhook_valid_token():
    # Mock settings to ensure we match the token
    settings.TELEGRAM_SECRET_TOKEN = "test_secret_token"
    
    headers = {"X-Telegram-Bot-Api-Secret-Token": "test_secret_token"}
    payload = {
        "update_id": 10000,
        "message": {
            "message_id": 1365,
            "from": {
                "id": 1111111,
                "is_bot": False,
                "first_name": "Test",
                "username": "TestUser"
            },
            "chat": {
                "id": 1111111,
                "first_name": "Test",
                "username": "TestUser",
                "type": "private"
            },
            "date": 1441645532,
            "text": "/start"
        }
    }
    
    response = client.post("/webhooks/telegram", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
