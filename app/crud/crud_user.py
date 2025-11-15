from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets

from app.models.user import User
from app.core.security import hash_password, verify_password


# -------------------------
#   REGISTRO
# -------------------------

def create_user(db: Session, username: str, email: str, password: str):
    user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        plan="BASIC"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# -------------------------
#   USUARIOS
# -------------------------

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


# -------------------------
#   AUTENTICACIÓN
# -------------------------

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# -------------------------
#   RESET PASSWORD TOKEN
# -------------------------

def create_reset_token(db: Session, user: User):
    token = secrets.token_urlsafe(32)
    expire = datetime.utcnow() + timedelta(minutes=15)

    user.reset_token = token
    user.reset_token_expire = expire

    db.commit()
    db.refresh(user)
    return token


def get_user_by_reset_token(db: Session, token: str):
    return db.query(User).filter(User.reset_token == token).first()


def reset_user_password(db: Session, user: User, new_password: str):
    user.hashed_password = hash_password(new_password)
    user.reset_token = None
    user.reset_token_expire = None

    db.commit()
    db.refresh(user)
    return user


# -------------------------
#   ACTUALIZAR PLAN
# -------------------------

def update_user_plan(db: Session, user_id: int, new_plan: str):
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    user.plan = new_plan
    db.commit()
    db.refresh(user)

    return user
