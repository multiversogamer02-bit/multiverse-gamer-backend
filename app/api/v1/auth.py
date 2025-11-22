# app/api/v1/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database.session import get_db
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token
)
from app.core.config import settings

from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, TokenResponse
from app.schemas_email_verification import EmailVerificationRequest, EmailCodeVerify
from app.crud.crud_user import user_crud
from app.crud.crud_email_verification import (
    send_verification_email,
    verify_code as verify_email_code,
    cleanup_expired_codes
)

router = APIRouter(prefix="/auth", tags=["Auth"])


# ---------------------------------------------------------
# REGISTER NEW USER
# ---------------------------------------------------------
@router.post("/register")
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = user_crud.get_by_email(db, payload.email)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Crear usuario (verified=False por defecto)
    user = user_crud.create_user(db, payload)

    # Enviar email de verificación profesional
    result = send_verification_email(db, user)

    if result.get("status") == "error":
        raise HTTPException(
            status_code=500,
            detail="User created but email could not be sent"
        )

    return {
        "message": "User registered successfully. Verification code sent.",
        "cooldown": 60
    }


# ---------------------------------------------------------
# SEND / RESEND VERIFICATION CODE
# ---------------------------------------------------------
@router.post("/send-code")
def send_verification_code(payload: EmailVerificationRequest, db: Session = Depends(get_db)):
    user = user_crud.get_by_email(db, payload.email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.verified:
        return {"message": "User already verified"}

    result = send_verification_email(db, user)

    if result["status"] == "cooldown":
        raise HTTPException(
            status_code=429,
            detail=result["message"]
        )

    if result["status"] == "error":
        raise HTTPException(
            status_code=500,
            detail="Failed to send verification email"
        )

    return {
        "message": "Verification code sent",
        "cooldown": 60
    }


# ---------------------------------------------------------
# VERIFY CODE
# ---------------------------------------------------------
@router.post("/verify-code")
def verify_code(payload: EmailCodeVerify, db: Session = Depends(get_db)):
    user = user_crud.get_by_email(db, payload.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Demasiados intentos → bloqueo temporal
    if user.verification_attempts >= settings.MAX_VERIFICATION_ATTEMPTS:
        raise HTTPException(
            status_code=403,
            detail="Account locked due to too many failed attempts"
        )

    # Verificar código
    valid = verify_email_code(db, user=user, code=payload.code)

    if not valid:
        raise HTTPException(status_code=400, detail="Invalid or expired code")

    return {"message": "Email verified successfully"}


# ---------------------------------------------------------
# LOGIN → Only if email verified
# ---------------------------------------------------------
@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = user_crud.get_by_email(db, payload.email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verificación obligatoria antes del login
    if not user.verified:
        raise HTTPException(
            status_code=403,
            detail="Email not verified"
        )

    # Validar contraseña
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    # Crear tokens JWT
    access = create_access_token({"sub": str(user.id)})
    refresh = create_refresh_token({"sub": str(user.id)})

    return TokenResponse(
        access_token=access,
        refresh_token=refresh,
        token_type="bearer"
    )


# ---------------------------------------------------------
# REFRESH TOKEN
# ---------------------------------------------------------
@router.post("/refresh")
def refresh(token: str):
    new_token = create_access_token({"sub": token})
    return {"access_token": new_token}


# ---------------------------------------------------------
# STATUS ENDPOINT (OPTIONAL)
# ---------------------------------------------------------
@router.get("/status")
def auth_status():
    return {"status": "auth module OK"}
