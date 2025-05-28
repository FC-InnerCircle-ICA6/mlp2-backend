from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserResponse(UserBase):
    id: UUID
    bio: Optional[str] = None
    language: str
    theme: str
    email_notifications: bool
    push_notifications: bool
    marketing_emails: bool
    two_factor_auth_enabled: bool

    class Config:
        from_attributes = True

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    language: Optional[str] = None
    theme: Optional[str] = None

class UserNotificationUpdate(BaseModel):
    email_notifications: Optional[bool] = None
    push_notifications: Optional[bool] = None
    marketing_emails: Optional[bool] = None

class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

class MessageResponse(BaseModel):
    message: str

# class LoginHistoryResponse(BaseModel):
#     id: UUID
#     login_time: datetime
#     ip_address: Optional[str] = None
#     device_info: Optional[str] = None
#     location: Optional[str] = None
#     class Config:
#         from_attributes = True