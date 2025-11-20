from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), unique=True, nullable=False)
    price = Column(Integer, nullable=False)  # 💰 PRECIO REAL
    max_sessions = Column(Integer, nullable=False)
    max_games = Column(Integer, nullable=False)
    description = Column(String(255), nullable=True)
