from sqlalchemy import Column, Integer, String

from backend.app.db.base import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    max_sessions = Column(Integer, nullable=False)
    max_games = Column(Integer, nullable=False)
    description = Column(String(255))
