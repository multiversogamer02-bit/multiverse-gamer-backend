from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.crud import crud_user
from app.crud import crud_email_verification

from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse,
)

from app.schemas.schemas_email_verification import (
    EmailVerificationRequest,
    EmailVerificationSendResponse,
    EmailVerificationCheck,
    EmailVerificationCheckResponse,
)

from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
)

router = APIRouter()


# --------------------------------------------------------------------------------------
#   REGISTER (Crea usuario y envía código de verificación)
# --------------------------------------------------------------------------------------
@router.post("/register", response_model=EmailVerificationSendResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Existe?
    existing = crud_user.get_user_by_email(db, user_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este email ya está registrado.",
        )

    # Crear usuario
    user = crud_user.create_user(db, user_data)

    # Generar código + guardar
    code = crud_email_verification.generate_code()
    crud_email_verification.store_code(db, user.id, code)

    # Enviar email
    crud_email_verification.send_email(user.email, code)

    return EmailVerificationSendResponse(
        message="Usuario creado. Código enviado al correo.",
        email=user.email,
    )


# --------------------------------------------------------------------------------------
#   REENVIAR CÓDIGO
# --------------------------------------------------------------------------------------
@router.post("/resend-code", response_model=EmailVerificationSendResponse)
def resend_code(payload: EmailVerificationRequest, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, payload.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado.",
        )

    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya está verificado.",
        )

    # Nuevo código
    code = crud_email_verification.generate_code()
    crud_email_verification.store_code(db, user.id, code)
    crud_email_verification.send_email(user.email, code)

    return EmailVerificationSendResponse(
        message="Código reenviado.",
        email=user.email,
    )


# --------------------------------------------------------------------------------------
#   VERIFICAR CÓDIGO
# --------------------------------------------------------------------------------------
@router.post("/verify-code", response_model=EmailVerificationCheckResponse)
def verify_code(payload: EmailVerificationCheck, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, payload.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado.",
        )

    ok = crud_email_verification.verify_code(db, user.id, payload.code)

    if not ok:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código inválido o expirado.",
        )

    crud_user.mark_verified(db, user.id)

    return EmailVerificationCheckResponse(
        message="Cuenta verificada correctamente.",
        email=user.email,
        verified=True,
    )


# --------------------------------------------------------------------------------------
#   LOGIN
# --------------------------------------------------------------------------------------
@router.post("/login", response_model=TokenResponse)
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Credenciales inválidas.",
        )

    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas.",
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tu cuenta aún no fue verificada.",
        )

    # Tokens
    access = create_access_token({"sub": str(user.id)})
    refresh = create_refresh_token({"sub": str(user.id)})

    return TokenResponse(
        access_token=access,
        refresh_token=refresh,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            email=user.email,
            plan=user.plan,
            is_verified=user.is_verified,
            created_at=user.created_at,
        ),
    )
