from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import DASHBOARD_REFRESH_INTERVAL_SECONDS, ENVIRONMENT
from app.database import get_db
from app.models import Shipment
from app.schemas import ShipmentResponse

app = FastAPI(
    title="DEV Intelligence Factory API",
    description="Backend DEV para seguimiento de mercancías dentro del laboratorio DEV Intelligence Factory.",
    version="0.3.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
        "environment": ENVIRONMENT,
        "dashboard_refresh_interval_seconds": DASHBOARD_REFRESH_INTERVAL_SECONDS
    }


@app.get("/shipments", response_model=list[ShipmentResponse])
def get_shipments(db: Session = Depends(get_db)):
    return db.query(Shipment).all()
