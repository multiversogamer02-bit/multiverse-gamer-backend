from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import decode_token
from app.crud.crud_user import get_user_by_id
from app.crud.crud_session import (
    enforce_session_limit,
    close_session,
    get_active_sessions
)
from app.crud.crud_plan import get_plan_by_name


router = APIRouter()


def _get_user_from_token(db: Session, token: str):
    """
    Obtiene usuario desde token JWT.
    """

    if not token:
        raise HTTPException(status_code=401, detail="Token requerido")

    payload = decode_token(token)
    user_id = payload.get("user_id")

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user


@router.post("/start")
def start_session(
    device_id: str,
    db: Session = Depends(get_db),
    Authorization: str = None
):
    """
    Inicia una sesión remota según las reglas del plan del usuario.
    """

    if Authorization is None:
        raise HTTPException(status_code=401, detail="Token requerido")

    token = Authorization.replace("Bearer ", "")
    user = _get_user_from_token(db, token)

    plan = get_plan_by_name(db, user.plan)
    if not plan:
        raise HTTPException(status_code=400, detail="Plan inválido")

    # Lógica principal del sistema de sesiones
    session = enforce_session_limit(db, user, plan, device_id)

    return {
        "status": "ok",
        "session_id": session.id,
        "active_sessions": len(get_active_sessions(db, user.id)),
        "max_sessions": plan.max_sessions
    }


@router.post("/close")
def close_user_session(
    session_id: int,
    db: Session = Depends(get_db),
    Authorization: str = None
):
    """
    Cierra una sesión específica.
    """
    if Authorization is None:
        raise HTTPException(status_code=401, detail="Token requerido")

    ok = close_session(db, session_id)

    if not ok:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    return {"status": "ok", "closed_session": session_id}
