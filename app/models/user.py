from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    plan = Column(String, default="basic")
    last_device = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)
    reset_token_expire = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # 🔥 nueva relación con juegos
    games = relationship("Game", back_populates="user", cascade="all, delete-orphan")
