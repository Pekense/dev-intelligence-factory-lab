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
