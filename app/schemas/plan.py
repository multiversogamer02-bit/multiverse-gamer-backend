from pydantic import BaseModel
from typing import Optional


class PlanBase(BaseModel):
    name: str
    price: int
    description: Optional[str] = None
    max_sessions: int
    max_games: Optional[int] = None


class PlanCreate(PlanBase):
    pass


class PlanResponse(PlanBase):
    id: int

    class Config:
        orm_mode = True
