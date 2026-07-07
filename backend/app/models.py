from sqlalchemy import Column, DateTime, Integer, Numeric, String

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
