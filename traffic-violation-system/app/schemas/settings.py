from pydantic import BaseModel, Field
from typing import Optional

class SettingsRequest(BaseModel):
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    ai_confidence_threshold: Optional[float] = None
    ai_detection_threshold: Optional[float] = None
    camera_reconnect_interval_sec: Optional[int] = None
    recording_retention_days: Optional[int] = None
    storage_location: Optional[str] = None
    theme: Optional[str] = None # "dark", "light"
    language: Optional[str] = None # "en", "es", "hi"
    timezone: Optional[str] = None

class SettingsResponse(BaseModel):
    smtp_host: str
    smtp_port: int
    smtp_user: str
    ai_confidence_threshold: float
    ai_detection_threshold: float
    camera_reconnect_interval_sec: int
    recording_retention_days: int
    storage_location: str
    theme: str
    language: str
    timezone: str
