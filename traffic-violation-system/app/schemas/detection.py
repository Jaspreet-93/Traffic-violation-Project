from pydantic import BaseModel, Field

class DetectionStatusResponse(BaseModel):
    running: bool = Field(..., description="Flag indicating if real-time vehicle detection is enabled")

class DetectionStartResponse(BaseModel):
    message: str = Field(..., description="Success confirmation message")
    status: str = Field(..., description="Active stream processing state")

class DetectionStopResponse(BaseModel):
    message: str = Field(..., description="Success confirmation message")
    status: str = Field(..., description="Active stream processing state")
