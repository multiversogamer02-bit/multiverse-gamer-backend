from fastapi import Depends, HTTPException, status
from jose import JWTError
from app.core.security import decode_access_token
from app.database.session import get_db  # 🔥 IMPORT CORREGIDO
from sqlalchemy.orm import Session
from app.crud.crud_user import get_user_by_id


# ============================================================
# Dependencia: Obtener usuario autenticado desde el Token
# ============================================================
def get_current_user(
    token: str,
    db: Session = Depends(get_db)
):
    try:
        payload = decode_access_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )

    user_id: int | None = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: no contiene ID de usuario",
        )

    user = get_user_by_id(db, user_id=user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    return user
