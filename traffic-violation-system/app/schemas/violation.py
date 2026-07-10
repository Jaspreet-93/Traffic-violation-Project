from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

# Legacy schemas (kept for backward compatibility)
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

class LegacyViolationResponse(ViolationBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

# New schemas (for Stage 15 decision engine)
class ViolationResponse(BaseModel):
    id: Optional[int] = None
    vehicle_id: int = Field(..., description="ID of the tracked vehicle")
    plate_number: str = Field(..., description="Extracted plate registration number")
    violation: str = Field(..., description="Detected traffic violation type")
    confidence: float = Field(..., description="Model confidence score")
    vehicle_type: Optional[str] = "car"
    timestamp: Optional[str] = None
    camera_id: Optional[str] = "Camera-01"
    evidence_id: Optional[int] = None
    original_image_path: Optional[str] = None
    annotated_image_path: Optional[str] = None
    status: Optional[str] = "processed"

    model_config = {
        "from_attributes": True
    }

class ViolationDetail(BaseModel):
    camera_id: int
    vehicle_id: Optional[int] = None
    plate_number: Optional[str] = None
    vehicle_type: str
    violation_type: str
    confidence: Optional[float] = None
    evidence_path: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
