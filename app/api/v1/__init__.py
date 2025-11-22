from fastapi import APIRouter

from app.api.v1 import auth
from app.api.v1 import users
from app.api.v1 import plans
from app.api.v1 import sessions
from app.api.v1 import games
from app.api.v1 import webhooks

# NUEVO → import del router de verificación de email
from app.api.v1 import routes_email_verification

api_router = APIRouter()

# Rutas ya existentes
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(plans.router, prefix="/plans", tags=["Plans"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])
api_router.include_router(games.router, prefix="/games", tags=["Games"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])

# NUEVO → rutas de verificación de email
api_router.include_router(
    routes_email_verification.router,
    prefix="/auth",
    tags=["Email Verification"]
)
