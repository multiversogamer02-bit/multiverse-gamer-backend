from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from backend.app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)

    plan = Column(String(20), default="BASIC")

    last_device = Column(String(255))
    reset_token = Column(String(255))
    reset_token_expire = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
