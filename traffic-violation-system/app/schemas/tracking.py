from pydantic import BaseModel, Field
from typing import List

class TrackingStatusResponse(BaseModel):
    running: bool = Field(..., description="Flag indicating if real-time tracking is enabled")

class TrackingStartResponse(BaseModel):
    message: str = Field(..., description="API success confirmation message")
    status: str = Field(..., description="Status flag indicating current state")

class TrackingStopResponse(BaseModel):
    message: str = Field(..., description="API success confirmation message")
    status: str = Field(..., description="Status flag indicating current state")

class TrackedVehicleResponse(BaseModel):
    vehicle_id: int = Field(..., description="Unique tracking ID assigned to vehicle")
    class_name: str = Field(..., description="Detected vehicle category name")
    confidence: float = Field(..., description="Confidence score")
    bbox: List[int] = Field(..., description="Bounding box coordinates [x1, y1, x2, y2]")
