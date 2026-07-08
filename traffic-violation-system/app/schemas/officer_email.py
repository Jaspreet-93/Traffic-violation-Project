from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class OfficerEmailCreate(BaseModel):
    email_address: str
    active: Optional[bool] = True
    primary: Optional[bool] = False

class OfficerEmailUpdate(BaseModel):
    email_address: Optional[str] = None
    active: Optional[bool] = None
    primary: Optional[bool] = None

class OfficerEmailResponse(BaseModel):
    id: str
    email_address: str
    active: bool
    primary: bool
    created_at: str
    updated_at: str
