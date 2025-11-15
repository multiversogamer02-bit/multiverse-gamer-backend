from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.schemas.user import UserCreate, UserLogin, UserOut
from app.db.session import get_db
from app.crud.crud_user import (
    create_user,
    authenticate_user,
    get_user_by_email,
    create_reset_token,
    get_user_by_reset_token,
    reset_user_password
)
from app.core.security import create_access_token
from app.core.email_utils import send_reset_email
from app.core.config import settings

router = APIRouter()


# -------------------------
#      REGISTER
# -------------------------

@router.post("/register", response_model=UserOut)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está en uso"
        )

    user = create_user(
        db=db,
        username=data.username,
        email=data.email,
        password=data.password
    )

    return user


# -------------------------
#       LOGIN
# -------------------------

@router.post("/login")
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email o contraseña incorrectos"
        )

    token = create_access_token({
        "user_id": user.id,
        "plan": user.plan
    })

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "plan": user.plan,
        "access_token": token,
        "token_type": "bearer"
    }


# -------------------------
#   FORGOT PASSWORD
# -------------------------

@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email)

    # Para no revelar mails válidos
    if not user:
        return {"status": "ok"}

    # Crear token y link
    token = create_reset_token(db, user)
    link = f"{settings.FRONTEND_RESET_URL}?token={token}"

    # Enviar email SendGrid
    send_reset_email(user.email, link)

    return {"status": "ok", "message": "Si el email existe, se envió un link de recuperación."}


# -------------------------
#   RESET PASSWORD
# -------------------------

@router.post("/reset-password")
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    user = get_user_by_reset_token(db, token)

    if not user:
        raise HTTPException(400, "Token inválido")

    if not user.reset_token_expire or user.reset_token_expire < datetime.utcnow():
        raise HTTPException(400, "Token expirado")

    reset_user_password(db, user, new_password)

    return {"status": "ok", "message": "Contraseña cambiada correctamente"}
