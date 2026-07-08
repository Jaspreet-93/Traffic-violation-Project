from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    full_name: str
    email_address: str
    phone_number: str
    password: str
    confirm_password: str

class UserLogin(BaseModel):
    email_address: str
    password: str
    remember_me: Optional[bool] = False

class UserUpdate(BaseModel):
    full_name: str
    phone_number: str

class PasswordChange(BaseModel):
    old_password: str
    new_password: str
    confirm_new_password: str

class ForgotPassword(BaseModel):
    email_address: str

class UserResponse(BaseModel):
    id: str
    full_name: str
    email_address: str
    phone_number: str
    created_at: str
    updated_at: str
