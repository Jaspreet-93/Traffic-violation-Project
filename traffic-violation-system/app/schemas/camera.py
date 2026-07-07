from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class CameraBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Unique name of the camera")
    location: str = Field(..., min_length=1, max_length=255, description="Physical location of the camera")
    rtsp_url: str = Field(..., min_length=1, description="RTSP video stream URL")
    is_active: bool = Field(True, description="Camera active status")

class CameraCreate(CameraBase):
    pass

class CameraResponse(CameraBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
