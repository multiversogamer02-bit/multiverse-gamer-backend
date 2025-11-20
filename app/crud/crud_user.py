# app/crud/crud_user.py

from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password, pwd_context

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    """Devuelve un usuario por ID."""
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, email: str, username: str, password: str):
    hashed = hash_password(password)

    user = User(
        email=email,
        username=username,
        hashed_password=hashed,
        plan="basic",
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    """
    Autentica usuarios con compatibilidad total:
    - bcrypt (viejo)
    - bcrypt_sha256 (nuevo)
    Y migra automáticamente los hashes viejos al nuevo formato.
    """
    user = get_user_by_email(db, email)
    if not user:
        return None

    # 1️⃣ Validar contraseña
    valid = verify_password(password, user.hashed_password)
    if not valid:
        return None

    # 2️⃣ Identificar el esquema actual del hash
    current_scheme = pwd_context.identify(user.hashed_password)

    # 3️⃣ Migración automática si el hash es viejo
    if current_scheme != "bcrypt_sha256":
        new_hash = hash_password(password)
        user.hashed_password = new_hash
        db.commit()
        db.refresh(user)

    return user

def update_user_plan(db: Session, user_id: int, new_plan: str):
    """Actualiza el plan del usuario."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    user.plan = new_plan
    db.commit()
    db.refresh(user)
    return user
