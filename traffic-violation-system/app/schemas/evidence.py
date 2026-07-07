from pydantic import BaseModel, Field
from typing import Optional

class EvidenceResponse(BaseModel):
    vehicle_id: Optional[int] = Field(None, description="ID of the tracked vehicle")
    violation: str = Field(..., description="Violation classification label")
    image_path: str = Field(..., description="Relative path to captured snapshot image proof")
    timestamp: str = Field(..., description="Standard UTC format timestamp")

    model_config = {
        "from_attributes": True
    }

class EvidenceDetail(BaseModel):
    evidence_id: int
    violation_id: int
    vehicle_id: Optional[int] = None
    plate_number: Optional[str] = None
    violation: str
    image_path: Optional[str] = None
    video_path: Optional[str] = None
    timestamp: str

    model_config = {
        "from_attributes": True
    }
