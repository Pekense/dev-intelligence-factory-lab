from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models import AIChangeRequest

client = TestClient(app)


def test_get_ai_change_requests_returns_list():
    response = client.get("/ai/change-requests")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_ai_change_request_returns_new_request():
    created_request_id = None

    payload = {
        "title": "Test AI change request",
        "requester": "CIO",
        "request_type": "FUNCTIONAL",
        "priority": "MEDIUM",
        "description": "Test request created from automated backend test.",
        "constraints": "DEV only. No secrets.",
    }

    try:
        response = client.post("/ai/change-requests", json=payload)

        assert response.status_code == 200

        data = response.json()
        created_request_id = data["id"]

        assert data["title"] == payload["title"]
        assert data["requester"] == "CIO"
        assert data["request_type"] == "FUNCTIONAL"
        assert data["priority"] == "MEDIUM"
        assert data["status"] == "NEW"
        assert "id" in data
        assert "created_at" in data

    finally:
        if created_request_id is not None:
            db = SessionLocal()
            try:
                db.query(AIChangeRequest).filter(
                    AIChangeRequest.id == created_request_id
                ).delete()
                db.commit()
            finally:
                db.close()
