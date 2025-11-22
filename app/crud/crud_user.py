# app/crud/crud_user.py

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


class CRUDUser:

    # ============================================================
    # OBTENER USUARIO
    # ============================================================

    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    def get(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    # ============================================================
    # CREAR USUARIO (NUEVO SISTEMA)
    # ============================================================

    def create_user(self, db: Session, payload: UserCreate):
        """
        Crea un usuario usando el sistema moderno:
        - verified = False
        - verification_attempts = 0
        - password_hash = hash seguro
        - plan básico por defecto
        """

        db_user = User(
            username=payload.username,
            email=payload.email,
            password_hash=get_password_hash(payload.password),

            verified=False,
            verification_attempts=0,

            plan="BASIC"
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    # ============================================================
    # ACTUALIZAR CAMPOS
    # ============================================================

    def update(self, db: Session, user: User, new_values: dict):
        for field, value in new_values.items():
            setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user

    # ============================================================
    # MARCAR USUARIO COMO VERIFICADO
    # ============================================================

    def set_verified(self, db: Session, user: User):
        user.verified = True
        user.verification_attempts = 0
        db.commit()
        db.refresh(user)
        return user

    # ============================================================
    # AUMENTAR INTENTOS (solo usado si fuera necesario)
    # ============================================================

    def increment_attempts(self, db: Session, user: User):
        user.verification_attempts += 1
        db.commit()
        return user


user_crud = CRUDUser()
