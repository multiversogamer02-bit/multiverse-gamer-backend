from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, users, plans, sessions, webhooks
from app.db.base import Base
from app.db.session import engine

app = FastAPI(
    title="Multiverse Gamer Backend",
    version="2.0",
    description="Backend oficial para Multiverse Gamer Launcher"
)

# Crear tablas automáticamente (si no existen)
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(plans.router, prefix="/plans", tags=["plans"])
app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])

@app.get("/")
def root():
    return {"status": "ok", "service": "Multiverse Gamer Backend"}

# --------------------------------------------------------------
# 🔥 NUEVO: ENDPOINT health (necesario para el launcher)
# --------------------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}
