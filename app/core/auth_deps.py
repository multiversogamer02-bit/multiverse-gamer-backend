# app/api/v1/auth_deps.py

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.db.session import get_db
from app.crud.crud_user import get_user_by_id
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Token inválido o expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception

    return user
