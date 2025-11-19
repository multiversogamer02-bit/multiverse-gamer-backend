from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    name = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    path = Column(String, nullable=False)
    cover = Column(String, nullable=True)

    user = relationship("User", back_populates="games")
