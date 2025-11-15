from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    plan = Column(String(20), default="BASIC")
    last_device = Column(String(255), nullable=True)

    # Recuperación de contraseña (SendGrid)
    reset_token = Column(String(255), nullable=True)
    reset_token_expire = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
