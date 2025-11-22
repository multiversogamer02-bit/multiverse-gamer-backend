from sqlalchemy import Column, Integer, String, Boolean, Numeric, DateTime
from sqlalchemy.sql import func
from app.database.base import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)

    # Nombre del plan (Basic, Pro, Elite)
    name = Column(String(30), unique=True, nullable=False)

    # Nivel de plan (útil para comparar permisos)
    level = Column(Integer, nullable=False, default=1)

    # Precio con decimales
    price = Column(Numeric(10, 2), nullable=False)

    # Límites del plan
    max_sessions = Column(Integer, nullable=False, default=1)
    max_games = Column(Integer, nullable=False, default=200)

    # Descripción del plan
    description = Column(String(255), nullable=True)

    # Activado o no
    is_active = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
