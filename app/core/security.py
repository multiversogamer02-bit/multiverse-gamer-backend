# app/core/security.py

from passlib.context import CryptContext
from passlib.exc import PasswordValueError

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)

def hash_password(password: str) -> str:
    """
    Hashea la contraseña. Passlib lanza PasswordValueError si supera los 72 bytes.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica contraseña.
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except PasswordValueError:
        return False
