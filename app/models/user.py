from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)

    # Password correcta
    password_hash = Column(String, nullable=False)

    # Verificación moderna
    verified = Column(Boolean, default=False)
    verification_attempts = Column(Integer, default=0)

    # Plan del usuario (nuevo sistema)
    plan = Column(String, default="BASIC")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
