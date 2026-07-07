from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class EmailLogBase(BaseModel):
    violation_id: int = Field(..., description="ID of the violation associated with this log")
    recipient_email: str = Field(..., description="Recipient email address")
    subject: str = Field(..., min_length=1, max_length=200, description="Subject of the email")
    body: str = Field(..., min_length=1, description="Body content of the email")
    status: str = Field("PENDING", description="Delivery status of the email (PENDING, SENT, FAILED)")
    sent_at: Optional[datetime] = Field(None, description="Timestamp showing when the email was sent")
    error_message: Optional[str] = Field(None, description="Error message if email transmission failed")

class EmailLogCreate(EmailLogBase):
    pass

class EmailLogResponse(EmailLogBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
