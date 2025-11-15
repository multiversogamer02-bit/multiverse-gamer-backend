import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_key_12345")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 120

    # Render (PostgreSQL)
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Mercado Pago
    MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")

settings = Settings()
