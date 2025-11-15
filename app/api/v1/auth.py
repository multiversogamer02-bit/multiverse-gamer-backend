from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserLogin, UserOut
from app.db.session import get_db
from app.crud.crud_user import (
    create_user,
    authenticate_user,
    get_user_by_email
)
from app.core.security import create_access_token

router = APIRouter()


@router.post("/register", response_model=UserOut)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    # Verifica email duplicado
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


@router.post("/login")
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email o contraseña incorrectos"
        )

    # Crear token
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
