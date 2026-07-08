from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import DASHBOARD_REFRESH_INTERVAL_SECONDS, ENVIRONMENT
from app.database import get_db
from app.models import AIChangeRequest, Shipment
from app.schemas import (
    AIChangeRequestCreate,
    AIChangeRequestResponse,
    ShipmentResponse,
)

app = FastAPI(
    title="DEV Intelligence Factory API",
    description="Backend DEV para seguimiento de mercancías y solicitudes gobernadas de IA.",
    version="0.4.0"
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


@app.get("/ai/change-requests", response_model=list[AIChangeRequestResponse])
def get_ai_change_requests(db: Session = Depends(get_db)):
    return db.query(AIChangeRequest).order_by(AIChangeRequest.created_at.desc()).all()


@app.post("/ai/change-requests", response_model=AIChangeRequestResponse)
def create_ai_change_request(
    request: AIChangeRequestCreate,
    db: Session = Depends(get_db)
):
    change_request = AIChangeRequest(
        title=request.title,
        requester=request.requester,
        request_type=request.request_type,
        priority=request.priority,
        description=request.description,
        constraints=request.constraints,
        status="NEW",
    )

    db.add(change_request)
    db.commit()
    db.refresh(change_request)

    return change_request
