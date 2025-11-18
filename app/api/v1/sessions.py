from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.auth_deps import get_current_user
from app.crud.crud_session import (
    enforce_session_limit,
    close_session,
    get_active_sessions
)
from app.crud.crud_plan import get_plan_by_name


router = APIRouter()


@router.post("/start")
def start_session(
    device_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Inicia una sesión remota según las reglas del plan del usuario.
    """

    plan = get_plan_by_name(db, current_user.plan)
    if not plan:
        raise HTTPException(status_code=400, detail="Plan inválido")

    session = enforce_session_limit(db, current_user, plan, device_id)

    return {
        "status": "ok",
        "session_id": session.id,
        "active_sessions": len(get_active_sessions(db, current_user.id)),
        "max_sessions": plan.max_sessions
    }


@router.post("/close")
def close_user_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Cierra una sesión específica.
    """

    ok = close_session(db, session_id)

    if not ok:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    return {"status": "ok", "closed_session": session_id}
