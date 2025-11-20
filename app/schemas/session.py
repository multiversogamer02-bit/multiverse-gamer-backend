from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SessionBase(BaseModel):
    device_id: str
    ip_address: Optional[str] = None


class SessionCreate(SessionBase):
    user_agent: Optional[str] = None


class SessionResponse(SessionBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    class Config:
        orm_mode = True
