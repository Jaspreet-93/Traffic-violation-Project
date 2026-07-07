from pydantic import BaseModel, Field
from typing import List

class PlateStatusResponse(BaseModel):
    running: bool = Field(..., description="Flag indicating if real-time plate detection is enabled")

class PlateStartResponse(BaseModel):
    message: str = Field(..., description="API success confirmation message")
    status: str = Field(..., description="Status flag indicating current state")

class PlateStopResponse(BaseModel):
    message: str = Field(..., description="API success confirmation message")
    status: str = Field(..., description="Status flag indicating current state")

class PlateDetectionResponse(BaseModel):
    vehicle_id: int = Field(..., description="Associated vehicle tracking ID")
    plate_bbox: List[int] = Field(..., description="Bounding box coordinates [x1, y1, x2, y2]")
    confidence: float = Field(..., description="Confidence score")
