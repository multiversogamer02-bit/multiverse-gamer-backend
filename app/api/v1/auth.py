# app/api/v1/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.crud_user import (
    create_user,
    authenticate_user,
    get_user_by_email
)

router = APIRouter()

@router.post("/register")
def register_user(data: dict, db: Session = Depends(get_db)):
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not email or not username or not password:
        raise HTTPException(status_code=400, detail="Faltan campos obligatorios.")

    if len(password) > 72:
        raise HTTPException(status_code=400, detail="La contraseña no puede superar los 72 caracteres.")

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

    return {"success": True, "user_id": user.id, "email": user.email}
