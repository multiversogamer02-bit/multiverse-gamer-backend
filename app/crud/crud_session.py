from sqlalchemy.orm import Session
from app.models.session import Session as SessionModel
from app.models.user import User
from app.models.plan import Plan
from datetime import datetime


def get_active_sessions(db: Session, user_id: int):
    return db.query(SessionModel).filter(
        SessionModel.user_id == user_id,
        SessionModel.active == True
    ).all()


def create_session(db: Session, user_id: int, device_id: str):
    session = SessionModel(
        user_id=user_id,
        device_id=device_id,
        active=True
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def close_session(db: Session, session_id: int):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        return False

    session.active = False
    session.ended_at = datetime.utcnow()
    db.commit()
    return True


def enforce_session_limit(db: Session, user: User, plan: Plan, device_id: str):
    """
    Controla cuántas sesiones tiene el usuario y aplica el límite del plan.
    """

    active = get_active_sessions(db, user.id)

    # Si ya existe sesión con ese device_id → permitir
    for s in active:
        if s.device_id == device_id:
            return s  # sesión válida existente

    # Si hay lugar → crear una sesión nueva
    if len(active) < plan.max_sessions:
        return create_session(db, user.id, device_id)

    # Si NO hay lugar → cerrar la más antigua
    oldest = sorted(active, key=lambda x: x.started_at)[0]
    close_session(db, oldest.id)

    # Crear sesión nueva
    return create_session(db, user.id, device_id)


def close_all_sessions(db: Session, user_id: int):
    sessions = get_active_sessions(db, user_id)
    for s in sessions:
        s.active = False
        s.ended_at = datetime.utcnow()
    db.commit()
