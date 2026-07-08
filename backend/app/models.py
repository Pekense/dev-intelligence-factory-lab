from sqlalchemy import Column, DateTime, Integer, Numeric, String, func

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
