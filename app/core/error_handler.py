# app/core/error_handler.py

from fastapi import Request
from fastapi.responses import JSONResponse
from passlib.exc import PasswordValueError

async def bcrypt_error_handler(request: Request, exc: PasswordValueError):
    """
    Intercepta el error cuando la contraseña supera los 72 bytes.
    """
    return JSONResponse(
        status_code=400,
        content={
            "detail": "La contraseña ingresada es demasiado larga. Máximo permitido: 72 caracteres."
        }
    )
