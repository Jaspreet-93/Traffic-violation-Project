from pydantic import BaseModel, Field
from typing import List

class SeatBeltStatusResponse(BaseModel):
    running: bool = Field(..., description="Flag indicating if real-time seat belt detection is enabled")

class SeatBeltStartResponse(BaseModel):
    message: str = Field(..., description="API success confirmation message")
    status: str = Field(..., description="Status flag indicating current state")

class SeatBeltStopResponse(BaseModel):
    message: str = Field(..., description="API success confirmation message")
    status: str = Field(..., description="Status flag indicating current state")

class SeatBeltDetectionResponse(BaseModel):
    vehicle_id: int = Field(..., description="Associated vehicle tracking ID")
    seat_belt_status: str = Field(..., description="Classification category: 'seat belt' or 'no seat belt'")
    confidence: float = Field(..., description="Confidence score")
    bbox: List[int] = Field(..., description="Bounding box coordinates [x1, y1, x2, y2]")
