from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# -----------------------------
# BASE
# -----------------------------
class UserBase(BaseModel):
    email: EmailStr
    username: str


# -----------------------------
# REGISTRO
# -----------------------------
class UserCreate(UserBase):
    password: str


# -----------------------------
# LOGIN
# -----------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# -----------------------------
# RESPUESTA GENERAL
# -----------------------------
class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    plan_id: Optional[int] = None
    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


# -----------------------------
# INTERNO (BASE DE DATOS)
# -----------------------------
class UserInDB(UserOut):
    hashed_password: str


# -----------------------------
# TOKEN RESPONSE (FALTABA)
# -----------------------------
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# -----------------------------
# REFRESH ENDPOINT RESPONSE
# -----------------------------
class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
