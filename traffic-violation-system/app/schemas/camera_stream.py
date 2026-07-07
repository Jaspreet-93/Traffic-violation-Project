from pydantic import BaseModel, Field
from typing import Union, Optional

class CameraStartRequest(BaseModel):
    source: Union[int, str] = Field(..., description="Camera stream source: integer (webcam) or string (RTSP/HTTP link)")

class CameraStartResponse(BaseModel):
    message: str = Field(..., description="Response confirmation message")
    status: str = Field(..., description="Current camera status (running, stopped)")
    source: Union[int, str] = Field(..., description="Active camera stream source")

class CameraStopResponse(BaseModel):
    message: str = Field(..., description="Response confirmation message")

class CameraStatusResponse(BaseModel):
    running: bool = Field(..., description="Camera stream execution flag")
    source: Optional[Union[int, str]] = Field(None, description="Active camera stream source")
