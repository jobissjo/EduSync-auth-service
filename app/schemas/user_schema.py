from pydantic import BaseModel, Field, field_validator

from app.models.enums import UserRole
from typing import Optional


class LoginEmailSchema(BaseModel):
    email: str
    password: str


class RegisterSchema(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    otp: str
    role: UserRole


class VerifyUserSchema(BaseModel):
    email: str
    otp: str


class EmailVerifySchema(BaseModel):
    first_name: str
    email: str


class EmailVerifyOtpSchema(BaseModel):
    otp: str
    email: str


class BaseUserResponse(BaseModel):
    first_name: str
    last_name: Optional[str]
    email: str
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True
