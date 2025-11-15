from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr
    plan: str

    class Config:
        from_attributes = True


class UserOut(UserBase):
    pass
