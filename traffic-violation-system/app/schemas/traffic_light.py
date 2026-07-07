from pydantic import BaseModel, Field
from typing import List

class TrafficLightStatusResponse(BaseModel):
    running: bool = Field(..., description="Flag indicating if real-time traffic light detection is enabled")

class TrafficLightStartResponse(BaseModel):
    message: str = Field(..., description="API success confirmation message")
    status: str = Field(..., description="Status flag indicating current state")

class TrafficLightStopResponse(BaseModel):
    message: str = Field(..., description="API success confirmation message")
    status: str = Field(..., description="Status flag indicating current state")

class TrafficLightDetectionResponse(BaseModel):
    signal: str = Field(..., description="Detected signal bulb state: 'red', 'yellow', or 'green'")
    confidence: float = Field(..., description="Confidence score")
    bbox: List[int] = Field(..., description="Bounding box coordinates [x1, y1, x2, y2]")
