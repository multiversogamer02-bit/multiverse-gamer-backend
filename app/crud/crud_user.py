from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password


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


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def update_user_plan(db: Session, user_id: int, new_plan: str):
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    user.plan = new_plan
    db.commit()
    db.refresh(user)
    return user
