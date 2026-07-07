from fastapi import FastAPI

from app.config import ENVIRONMENT, DASHBOARD_REFRESH_INTERVAL_SECONDS

app = FastAPI(
    title="DEV Intelligence Factory API",
    version="0.1.0"
)

shipments = [
    {
        "id": 1,
        "client": "ACME Pharma",
        "destination": "Madrid",
        "location": "Zaragoza Hub",
        "status": "IN_TRANSIT",
        "transport_service": "Cold Chain Express",
        "eta": "2026-07-08T18:00:00"
    },
    {
        "id": 2,
        "client": "Global Retail",
        "destination": "Barcelona",
        "location": "Valencia Port",
        "status": "PENDING",
        "transport_service": "Maritime Standard",
        "eta": "2026-07-09T09:30:00"
    }
]


@app.get("/health")
def health():
    return {
        "status": "ok",
        "environment": ENVIRONMENT
    }


@app.get("/config")
def get_config():
    return {
        "dashboard_refresh_interval_seconds": DASHBOARD_REFRESH_INTERVAL_SECONDS
    }


@app.get("/shipments")
def get_shipments():
    return shipments
