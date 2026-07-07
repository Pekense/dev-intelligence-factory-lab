from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.config import DASHBOARD_REFRESH_INTERVAL_SECONDS, ENVIRONMENT
from app.database import get_db
from app.models import Shipment
from app.schemas import ShipmentResponse

app = FastAPI(
    title="DEV Intelligence Factory API",
    version="0.2.0"
)


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


@app.get("/shipments", response_model=list[ShipmentResponse])
def get_shipments(db: Session = Depends(get_db)):
    return db.query(Shipment).all()
