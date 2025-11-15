from pydantic import BaseModel


class PlanOut(BaseModel):
    name: str
    max_sessions: int
    max_games: int
    description: str | None = None

    class Config:
        from_attributes = True
