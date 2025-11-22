from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from app.models.user import User
from app.schemas.user import UserCreate


# ---------------------------------------------------------
# Obtener usuario por ID (NECESARIO PARA auth_deps)
# ---------------------------------------------------------
def get_user_by_id(db: Session, user_id: int) -> User | None:
    """
    Obtiene un usuario por su ID primario.
    """
    return db.query(User).filter(User.id == user_id).first()


# ---------------------------------------------------------
# Buscar usuario por email
# ---------------------------------------------------------
def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Retorna un usuario por email.
    """
    return db.query(User).filter(User.email == email).first()


# ---------------------------------------------------------
# Crear usuario nuevo (registro)
# ---------------------------------------------------------
def create_user(db: Session, user: UserCreate, password_hash: str) -> User:
    """
    Crea un nuevo usuario con contraseña hasheada.
    """
    db_user = User(
        email=user.email,
        username=user.username,
        password_hash=password_hash,
        plan="basic",
        is_verified=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(db_user)

    try:
        db.commit()
        db.refresh(db_user)
    except SQLAlchemyError:
        db.rollback()
        raise

    return db_user


# ---------------------------------------------------------
# Actualizar plan del usuario
# ---------------------------------------------------------
def update_user_plan(db: Session, user_id: int, new_plan: str) -> User | None:
    """
    Actualiza el plan del usuario (basic, pro, elite).
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    user.plan = new_plan
    user.updated_at = datetime.utcnow()

    try:
        db.commit()
        db.refresh(user)
    except SQLAlchemyError:
        db.rollback()
        raise

    return user


# ---------------------------------------------------------
# Actualizar contraseña
# ---------------------------------------------------------
def update_password(db: Session, user_id: int, new_password_hash: str) -> User | None:
    """
    Cambia la contraseña del usuario.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    user.password_hash = new_password_hash
    user.updated_at = datetime.utcnow()

    try:
        db.commit()
        db.refresh(user)
    except SQLAlchemyError:
        db.rollback()
        raise

    return user


# ---------------------------------------------------------
# Marcar email como verificado
# ---------------------------------------------------------
def set_verified(db: Session, user_id: int) -> User | None:
    """
    Marca un usuario como verificado.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    user.is_verified = True
    user.updated_at = datetime.utcnow()

    try:
        db.commit()
        db.refresh(user)
    except SQLAlchemyError:
        db.rollback()
        raise

    return user
