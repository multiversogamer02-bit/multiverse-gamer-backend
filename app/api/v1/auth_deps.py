from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.security import decode_access_token
from app.crud.crud_user import user_crud


# ============================================================
# OBTENER USUARIO ACTUAL DESDE EL TOKEN JWT
# ============================================================

def get_current_user(token: str, db: Session = Depends(get_db)):
    """
    Extrae el usuario desde el token JWT.
    Decodifica el token, obtiene user_id y busca en la BD.
    """

    payload = decode_access_token(token)

    if payload is None or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )

    user_id = int(payload["sub"])

    # 🔥 CAMBIO IMPORTANTE: usamos el método correcto
    user = user_crud.get(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return user


# ============================================================
# ALIAS más amigable para el resto del backend
# ============================================================

def get_db_user(current_user=Depends(get_current_user)):
    return current_user
