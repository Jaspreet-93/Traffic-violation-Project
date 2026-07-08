from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class EmailSettingsUpdate(BaseModel):
    station_name: str = Field(..., description="Name of the monitoring station")
    station_email: str = Field(..., description="Default destination/station email address")
    smtp_email: str = Field(..., description="SMTP Server Username/Email")
    smtp_password: str = Field(..., description="SMTP Server App Password")
    enabled: bool = Field(True, description="Enable email alerts flag")

class EmailSettingsResponse(BaseModel):
    station_name: str
    station_email: str
    smtp_email: str
    smtp_password: str
    enabled: bool

class SendTestEmailRequest(BaseModel):
    recipient_email: str = Field(..., description="Target test email recipient")

class EmailLogResponse(BaseModel):
    id: int
    violation_id: int
    recipient_email: str
    subject: str
    body: str
    status: str
    sent_at: Optional[datetime] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True
