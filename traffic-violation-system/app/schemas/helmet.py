from pydantic import BaseModel, Field
from typing import List

class HelmetStatusResponse(BaseModel):
    running: bool = Field(..., description="Flag indicating if real-time helmet detection is enabled")

class HelmetStartResponse(BaseModel):
    message: str = Field(..., description="API success confirmation message")
    status: str = Field(..., description="Status flag indicating current state")

class HelmetStopResponse(BaseModel):
    message: str = Field(..., description="API success confirmation message")
    status: str = Field(..., description="Status flag indicating current state")

class HelmetDetectionResponse(BaseModel):
    object_id: int = Field(..., description="Unique tracking ID placeholder")
    helmet_status: str = Field(..., description="Rider classification: 'helmet' or 'no helmet'")
    confidence: float = Field(..., description="Confidence score")
    bbox: List[int] = Field(..., description="Bounding box coordinates [x1, y1, x2, y2]")
