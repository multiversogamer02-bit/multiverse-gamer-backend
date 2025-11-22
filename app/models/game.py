from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

# IMPORT CORRECTO PARA TU ESTRUCTURA
from app.database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    path = Column(String, nullable=False)
    cover = Column(String, nullable=True)

    # Para sincronización
    checksum = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # RELACIÓN INVERSA (asegúrate que User tenga back_populates="games")
    user = relationship("User", back_populates="games")
