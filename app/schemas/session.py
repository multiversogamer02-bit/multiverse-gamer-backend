from pydantic import BaseModel
from datetime import datetime


class SessionCreate(BaseModel):
    user_id: int
    device_id: str


class SessionOut(BaseModel):
    id: int
    user_id: int
    device_id: str
    active: bool
    started_at: datetime
    ended_at: datetime | None = None

    class Config:
        from_attributes = True
