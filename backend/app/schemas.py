from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ShipmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client: str
    destination: str
    location: str
    status: str
    transport_service: str
    eta: datetime
    temperature_current: Decimal | None = None
    alert_status: str | None = None
    last_logistic_event: str | None = None


class AIChangeRequestCreate(BaseModel):
    title: str
    requester: str
    request_type: str
    priority: str = "MEDIUM"
    description: str
    constraints: str | None = None


class AIChangeRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    requester: str
    request_type: str
    priority: str
    description: str
    constraints: str | None = None
    status: str
    created_at: datetime


class AIChangeProposalCreate(BaseModel):
    change_request_id: int
    model_name: str
    proposal_markdown: str
    confidence_level: str | None = None


class AIChangeProposalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    change_request_id: int
    model_name: str
    proposal_markdown: str
    confidence_level: str | None = None
    review_status: str
    created_at: datetime
