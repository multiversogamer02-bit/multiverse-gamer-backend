from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
import os

# ============================================================
# CONFIG JWT – ACCESS + REFRESH
# ============================================================

SECRET_KEY = os.getenv("JWT_SECRET", "ULTRA_SECRET_QUE_DEBES_CAMBIAR")
REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET", "ULTRA_REFRESH_SECRET_CAMBIAR")

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24            # 24hs
REFRESH_TOKEN_EXPIRE_DAYS = 7                    # 7 días válidos

# ============================================================
# PASSWORD HASHING (bcrypt_sha256 + bcrypt)
# ============================================================

pwd_context = CryptContext(
    schemes=["bcrypt_sha256", "bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(plain, hashed)
    except Exception:
        return False

# ============================================================
# ACCESS TOKEN
# ============================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crea un access token JWT."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str):
    """Decodifica/valida un JWT de acceso."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None

# ============================================================
# REFRESH TOKEN
# ============================================================

def create_refresh_token(data: dict):
    """Crea un refresh token válido por más días."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

def verify_refresh_token(token: str):
    """Verifica y decodifica un refresh token."""
    try:
        return jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
