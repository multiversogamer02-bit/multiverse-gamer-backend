from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


# ============================================================
# ESQUEMA – SOLICITAR ENVÍO DE CÓDIGO
# ============================================================

class EmailVerificationRequest(BaseModel):
    email: EmailStr = Field(..., description="Email al que se enviará el código")


# ============================================================
# ESQUEMA – RESPUESTA TRAS ENVIAR CÓDIGO
# ============================================================

class EmailVerificationSendResponse(BaseModel):
    message: str = "Verification code sent successfully"
    expires_at: datetime
    attempt_limit: int = 5
    code_length: int = 6


# ============================================================
# ESQUEMA – VERIFICAR CÓDIGO
# ============================================================

class EmailVerificationCheck(BaseModel):
    email: EmailStr
    code: str = Field(..., min_length=6, max_length=6, description="6-digit alphanumeric code")


# ============================================================
# ESQUEMA – RESPUESTA AL VERIFICAR CÓDIGO
# ============================================================

class EmailVerificationCheckResponse(BaseModel):
    valid: bool
    message: str
    remaining_attempts: int


# ============================================================
# ESQUEMA – OBJETO ALMACENADO EN DB / REDIS
# ============================================================

class EmailVerificationData(BaseModel):
    email: EmailStr
    code: str
    created_at: datetime
    expires_at: datetime
    attempts_left: int = 5
