from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserLogin, UserOut
from app.core.security import hash_password, verify_password
from app.crud.crud_user import (
    create_user,
    get_user_by_email,
)
from app.db.session import get_db

router = APIRouter()


@router.post("/register", response_model=UserOut)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=400, detail="El email ya está registrado.")

    # HASH CORRECTO
    hashed = hash_password(data.password)

    # CREATE USER CORRECTAMENTE
    user = create_user(
        db=db,
        username=data.username,
        email=data.email,
        hashed_password=hashed,
        plan="BASIC"
    )

    return user


@router.post("/login", response_model=UserOut)
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=400, detail="Email o contraseña incorrectos.")

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Email o contraseña incorrectos.")

    return user
