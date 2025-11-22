from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from app.database.base import Base

class EmailVerificationCode(Base):
    __tablename__ = "email_verification_codes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)

    code = Column(String(10), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    attempts = Column(Integer, default=0)
    max_attempts = Column(Integer, default=5)

    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
