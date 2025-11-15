from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, nullable=False)

    # Límites de sesiones simultáneas
    max_sessions = Column(Integer, nullable=False)

    # Límite de juegos detectados (Basic)
    max_games = Column(Integer, nullable=False)

    # Objeto descriptivo opcional
    description = Column(String(255), nullable=True)
