from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.core.security import decode_access_token
from app.crud.crud_user import get_user_by_id
from app.db.session import get_db   # ← CORREGIDO

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Obtiene el usuario actual a partir del token JWT.
    """

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token faltante",
        )

    # Decodificar JWT
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: falta sub",
        )

    # Buscar usuario real
    user = get_user_by_id(db, int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no existe",
        )

    # Bloqueo temporal
    if user.locked_until is not None:
        now = datetime.now(timezone.utc)
        if user.locked_until > now:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Usuario bloqueado hasta {user.locked_until}",
            )

    return user


async def get_current_active_user(
    user=Depends(get_current_user)
):
    """
    Valida que el usuario esté verificado y activo.
    """

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Debes verificar tu email antes de usar tu cuenta",
        )

    return user
