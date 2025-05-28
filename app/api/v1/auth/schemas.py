from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: UUID
    is_active: bool = True # Assuming default true
    email_notifications: bool = True
    push_notifications: bool = True
    marketing_emails: bool = False
    two_factor_auth_enabled: bool = False
    bio: Optional[str] = None
    language: str
    theme: str

    class Config:
        from_attributes = True # Pydantic v2: orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None