from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import verify_access_token
from app.crud.crud_user import get_user_by_id
from app.schemas.user import UserOut


router = APIRouter()

# Middleware estándar para Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Extrae el usuario actual desde un token JWT.
    """

    # Verificar token
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )

    # Obtener user_id
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido (sin user_id)"
        )

    # Obtener usuario desde la BD
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return user


@router.get("/profile", response_model=UserOut)
def get_profile(current_user=Depends(get_current_user)):
    """
    Devuelve los datos del usuario autenticado.
    """
    return current_user
