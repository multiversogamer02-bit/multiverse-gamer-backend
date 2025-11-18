from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    """
    Devuelve un usuario por ID.
    Necesaria para endpoints que requieren autenticación.
    """
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, email: str, username: str, password: str):
    hashed = hash_password(password)

    user = User(
        email=email,
        username=username,
        hashed_password=hashed,
        plan="basic",  # plan por defecto
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    """
    Autentica un usuario comparando la contraseña ingresada
    con el hash almacenado en la base de datos.
    Retorna el usuario si es correcto, o None si falla.
    """
    user = get_user_by_email(db, email)
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def update_user_plan(db: Session, user_id: int, new_plan: str):
    """
    Actualiza el plan de un usuario y devuelve el usuario actualizado.
    Usado por:
      - /plans/apply
      - webhook de Mercado Pago
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    user.plan = new_plan
    db.commit()
    db.refresh(user)
    return user
