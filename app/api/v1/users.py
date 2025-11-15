from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import decode_token
from app.crud.crud_user import get_user_by_id
from app.schemas.user import UserOut

router = APIRouter()


def get_current_user(db: Session = Depends(get_db), token: str = None):
    """
    Obtiene el usuario actual desde el JWT enviado por
    el launcher en Authorization: Bearer <token>
    """

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado"
        )

    payload = decode_token(token)
    user_id = payload.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no existe"
        )

    return user


@router.get("/profile", response_model=UserOut)
def get_profile(
    db: Session = Depends(get_db),
    token: str = Depends(get_current_user)
):
    return token
