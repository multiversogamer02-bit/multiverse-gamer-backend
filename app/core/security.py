# app/core/security.py
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
import os

# ==========================
# CONFIGURACIÓN JWT
# ==========================

SECRET_KEY = os.getenv("JWT_SECRET", "ULTRA_SECRET_QUE_DEBES_CAMBIAR")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24hs

# ==========================
# HASHING SEGURO
# ==========================
# Compatibilidad completa:
# - bcrypt (hashes antiguos)
# - bcrypt_sha256 (nuevo y recomendado)
pwd_context = CryptContext(
    schemes=["bcrypt_sha256", "bcrypt"],   # Orden: primero el más seguro
    deprecated="auto"
)

def hash_password(password: str) -> str:
    """Genera un hash seguro con bcrypt_sha256 por defecto."""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """Verifica una contraseña con soporte para bcrypt y bcrypt_sha256."""
    try:
        return pwd_context.verify(plain, hashed)
    except Exception:
        return False

# ==========================
# TOKENS JWT
# ==========================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Genera un token JWT."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_access_token(token: str):
    """Verifica y decodifica un token JWT."""
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except JWTError:
        return None
