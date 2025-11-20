# app/api/v1/auth_deps.py

from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import SECRET_KEY, ALGORITHM
from app.crud.crud_user import get_user_by_id


def get_current_user(token: str = Depends(...), db: Session = Depends(get_db)):
    """
    Extrae usuario desde el token JWT.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user
