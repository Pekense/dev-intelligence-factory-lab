from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["environment"] == "DEV"


def test_config_endpoint_returns_refresh_interval():
    response = client.get("/config")

    assert response.status_code == 200
    assert response.json()["dashboard_refresh_interval_seconds"] == 60


def test_shipments_endpoint_returns_database_data():
    response = client.get("/shipments")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 2

    first = data[0]

    assert "client" in first
    assert "destination" in first
    assert "location" in first
    assert "status" in first
    assert "transport_service" in first
    assert "eta" in first
    assert "temperature_current" in first
    assert "alert_status" in first
    assert "last_logistic_event" in first
