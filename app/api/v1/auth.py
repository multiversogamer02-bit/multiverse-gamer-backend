# app/api/v1/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.session import get_db
from app.crud.crud_user import (
    create_user,
    authenticate_user,
    get_user_by_email,
    get_user_by_id
)
from app.core.security import create_access_token
from app.api.v1.auth_deps import get_current_user

router = APIRouter()


# ==============================================================
# REGISTRO
# ==============================================================

@router.post("/register")
def register_user(data: dict, db: Session = Depends(get_db)):
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not email or not username or not password:
        raise HTTPException(status_code=400, detail="Faltan campos obligatorios.")

    exists = get_user_by_email(db, email)
    if exists:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")

    user = create_user(db, email=email, username=username, password=password)
    return {"success": True, "user_id": user.id}


# ==============================================================
# LOGIN
# ==============================================================

@router.post("/login")
def login_user(data: dict, db: Session = Depends(get_db)):
    email = data.get("email")
    password = data.get("password")
    device_id = data.get("device_id")  # opcional

    if not email or not password:
        raise HTTPException(status_code=400, detail="Credenciales inválidas.")

    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=400, detail="Credenciales inválidas.")

    access_token_expires = timedelta(hours=12)

    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email},
        expires_delta=access_token_expires
    )

    return {
        "success": True,
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "plan": user.plan
        }
    }


# ==============================================================
# PERFIL DEL USUARIO /auth/me  **(NUEVO – OBLIGATORIO)
# ==============================================================

@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    """
    Devuelve el usuario autenticado usando el token.
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "plan": current_user.plan
    }
