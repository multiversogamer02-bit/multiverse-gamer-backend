from pydantic import BaseModel
from typing import Optional


# -----------------------------
# BASE
# -----------------------------
class PlanBase(BaseModel):
    name: str
    price: int
    description: Optional[str] = None
    max_sessions: int
    max_games: Optional[int] = None


# -----------------------------
# CREAR PLAN (admin / seed)
# -----------------------------
class PlanCreate(PlanBase):
    pass


# -----------------------------
# UPDATE (por si lo necesitás)
# -----------------------------
class PlanUpdate(BaseModel):
    price: Optional[int] = None
    description: Optional[str] = None
    max_sessions: Optional[int] = None
    max_games: Optional[int] = None


# -----------------------------
# RESPUESTA GENERAL
# -----------------------------
class PlanOut(PlanBase):
    id: int

    model_config = {
        "from_attributes": True  # Pydantic v2 reemplaza orm_mode
    }


# -----------------------------
# INTERNO (BASE DE DATOS)
# -----------------------------
class PlanInDB(PlanOut):
    pass
