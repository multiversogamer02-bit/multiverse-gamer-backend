# app/core/auth_deps.py

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import verify_access_token
from app.db.session import get_db
from app.crud.crud_user import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Valida token, decodifica JWT y devuelve el usuario actual.
    """
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido (falta user_id)")

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user
