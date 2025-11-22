# app/api/v1/routes_email_verification.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.auth_deps import get_current_user_optional

from app.schemas.schemas_email_verification import (
    SendVerificationCodeResponse,
    VerifyCodeRequest,
    VerifyCodeResponse
)

from app.services.services_email_verification import (
    email_verification_service
)

router = APIRouter(
    prefix="/auth",
    tags=["Email Verification"]
)

# ============================================================
#  POST /auth/send-code
# ============================================================

@router.post("/send-code", response_model=SendVerificationCodeResponse)
async def send_verification_code(
    db: Session = Depends(get_db),
    user=Depends(get_current_user_optional)
):
    """
    Enviar un código de verificación de 6 caracteres (alfa-numérico)
    usando SendGrid.

    Si el usuario está autenticado → usa su email.
    Si NO está autenticado → se debe pasar por query param o body
      → pero en esta versión lo simplificamos: requiere login previo.
    """

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Debes iniciar sesión para solicitar un código."
        )

    ok, message = await email_verification_service.generate_and_send_code(
        db=db,
        email=user.email
    )

    if not ok:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    return SendVerificationCodeResponse(
        message=message
    )


# ============================================================
#  POST /auth/verify-code
# ============================================================

@router.post("/verify-code", response_model=VerifyCodeResponse)
async def verify_code(
    payload: VerifyCodeRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_optional)
):
    """
    Verifica el código enviado al correo.
    Reglas:
      - 6 caracteres alfanuméricos
      - Expira a los 10 minutos
      - Máx 5 intentos
    """

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Debes iniciar sesión para verificar tu email."
        )

    ok, message = email_verification_service.verify_code(
        db=db,
        email=user.email,
        code=payload.code
    )

    if not ok:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    return VerifyCodeResponse(
        verified=True,
        message=message
    )
