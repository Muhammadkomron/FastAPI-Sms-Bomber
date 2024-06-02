from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import func

from app.choices import LogStatus


class Base(BaseModel):
    created_at: date = Field(default=func.now())
    updated_at: date = Field(default=func.now())


class UserBase(Base):
    username: str
    email: EmailStr = Field(default='')
    full_name: Optional[str] = Field(default='')


class UserCreateUpdate(UserBase):
    is_staff: bool = Field(default=False)
    is_superuser: bool = Field(default=False)
    password: str


class User(UserBase):
    id: int
    is_staff: bool
    is_superuser: bool
    is_blocked: bool

    class Config:
        from_attributes = True


class StudentBase(Base):
    phone_number: str
    username: Optional[str] = Field(default=None)


class StudentCreateUpdate(StudentBase):
    full_name: Optional[str] = Field(default=None)
    birth_date: Optional[date] = Field(default=None)


class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True


class LogBase(Base):
    notification_id: int
    student_id: int
    status: Optional[Enum] = Field(default=LogStatus.PENDING)
