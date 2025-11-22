from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# =========================================================
# REQUEST: solicitar código de verificación
# =========================================================
class EmailVerificationRequest(BaseModel):
    email: EmailStr = Field(..., description="Email donde se enviará el código.")


# =========================================================
# REQUEST: el usuario ingresa el código recibido
# =========================================================
class EmailCodeVerify(BaseModel):
    email: EmailStr = Field(..., description="El email del usuario.")
    code: str = Field(..., min_length=4, max_length=8, description="Código enviado al correo.")


# =========================================================
# RESPONSE: respuesta estándar del backend
# =========================================================
class EmailVerificationResponse(BaseModel):
    success: bool
    message: str
    verified: bool | None = None
    email: EmailStr | None = None
    created_at: datetime | None = None
