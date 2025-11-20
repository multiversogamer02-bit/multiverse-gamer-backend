from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GameBase(BaseModel):
    name: str
    platform: str
    path: str
    cover: Optional[str] = None

class GameCreate(GameBase):
    checksum: Optional[str] = None

class GameResponse(GameBase):
    id: int
    user_id: int
    checksum: Optional[str] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
