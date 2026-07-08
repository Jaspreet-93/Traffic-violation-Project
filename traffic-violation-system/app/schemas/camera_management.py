from pydantic import BaseModel, Field
from typing import Optional, List

class CameraCreate(BaseModel):
    name: str = Field(..., description="Camera device name")
    url: str = Field(..., description="Stream connection URL/path")
    resolution: str = Field("1920x1080", description="Resolution dimensions")
    fps: int = Field(30, description="Frames per second value")
    recording_enabled: bool = Field(True, description="Whether storage recording is active")

class CameraUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    resolution: Optional[str] = None
    fps: Optional[int] = None
    enabled: Optional[bool] = None
    recording_enabled: Optional[bool] = None

class CameraResponse(BaseModel):
    id: int
    name: str
    url: str
    resolution: str
    fps: int
    enabled: bool
    recording_enabled: bool
    status: str
    health: str
    last_active: str

    model_config = {
        "from_attributes": True
    }

class CameraStatusResponse(BaseModel):
    total_cameras: int
    online_cameras: int
    offline_cameras: int
    recording_cameras: int

class CameraHealthResponse(BaseModel):
    camera_id: int
    health_score: int
    packet_loss_pct: float
    jitter_ms: float
    latency_ms: float
    status: str
