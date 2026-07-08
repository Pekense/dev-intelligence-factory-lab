from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text, func

from app.database import Base


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    client = Column(String)
    destination = Column(String)
    location = Column(String)
    status = Column(String)
    transport_service = Column(String)
    eta = Column(DateTime)
    temperature_current = Column(Numeric)
    alert_status = Column(String)
    last_logistic_event = Column(String)


class AIChangeRequest(Base):
    __tablename__ = "ai_change_requests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    requester = Column(String)
    request_type = Column(String)
    priority = Column(String)
    description = Column(String)
    constraints = Column(String)
    status = Column(String)
    created_at = Column(DateTime, server_default=func.now())


class AIChangeProposal(Base):
    __tablename__ = "ai_change_proposals"

    id = Column(Integer, primary_key=True, index=True)
    change_request_id = Column(Integer, ForeignKey("ai_change_requests.id"), nullable=False)
    model_name = Column(String)
    proposal_markdown = Column(Text)
    confidence_level = Column(String)
    review_status = Column(String, default="PENDING_REVIEW")
    created_at = Column(DateTime, server_default=func.now())
