from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class ViolationBase(BaseModel):
    camera_id: int = Field(..., description="ID of the camera that captured the violation")
    vehicle_number: Optional[str] = Field(None, max_length=50, description="Detected vehicle license plate number")
    vehicle_type: str = Field(..., min_length=1, max_length=50, description="Type of vehicle e.g. CAR, BIKE")
    violation_type: str = Field(..., min_length=1, max_length=100, description="Violation classification e.g. SPEEDING")
    timestamp: Optional[datetime] = Field(None, description="Time of violation occurrence")
    snapshot_path: Optional[str] = Field(None, description="Local path to infraction snapshot image")
    is_processed: bool = Field(False, description="Status showing if violation is processed")

class ViolationCreate(ViolationBase):
    pass

class ViolationResponse(ViolationBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
