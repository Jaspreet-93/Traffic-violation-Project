from pydantic import BaseModel, Field
from typing import List

class DriverBehaviorStatusResponse(BaseModel):
    running: bool = Field(..., description="Flag indicating if real-time driver behavior detection is enabled")

class DriverBehaviorStartResponse(BaseModel):
    message: str = Field(..., description="API success confirmation message")
    status: str = Field(..., description="Status flag indicating current state")

class DriverBehaviorStopResponse(BaseModel):
    message: str = Field(..., description="API success confirmation message")
    status: str = Field(..., description="Status flag indicating current state")

class DriverBehaviorDetectionResponse(BaseModel):
    vehicle_id: int = Field(..., description="Associated vehicle tracking ID")
    behavior: str = Field(..., description="Classification category: 'cigarette', 'phone', or 'seatbelt'")
    confidence: float = Field(..., description="Confidence score")
    bbox: List[int] = Field(..., description="Bounding box coordinates [x1, y1, x2, y2]")
