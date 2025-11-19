from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, users, plans, sessions, webhooks, games

app = FastAPI(title="Multiverse Gamer Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "message": "Multiverse Gamer Backend online"}


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(plans.router, prefix="/plans", tags=["Plans"])
app.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
app.include_router(games.router, prefix="/games", tags=["Games"])
