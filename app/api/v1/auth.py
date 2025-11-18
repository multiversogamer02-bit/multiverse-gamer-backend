# app/api/v1/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.session import get_db
from app.crud.crud_user import (
    create_user,
    authenticate_user,
    get_user_by_email
)
from app.core.security import create_access_token

router = APIRouter()


@router.post("/register")
def register_user(data: dict, db: Session = Depends(get_db)):
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not email or not username or not password:
        raise HTTPException(status_code=400, detail="Faltan campos obligatorios.")

    if len(password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400,
            detail="La contraseña excede el límite de 72 bytes (bcrypt)."
        )

    exists = get_user_by_email(db, email)
    if exists:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")

    user = create_user(db, email=email, username=username, password=password)

    return {"success": True, "user_id": user.id}


@router.post("/login")
def login_user(data: dict, db: Session = Depends(get_db)):
    email = data.get("email")
    password = data.get("password")

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
