from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Dependencias correctas
from app.api.v1.auth_deps import get_db

# Seguridad real
from app.core.security import verify_password, create_access_token

# CRUD
from app.crud import crud_user
from app.crud import crud_email_verification

# Schemas correctos
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserInDB,
    TokenResponse,
)

from app.schemas.schemas_email_verification import (
    EmailVerificationRequest,
    EmailCodeVerify,
)

router = APIRouter()


# ============================================================
# REGISTER
# ============================================================
@router.post("/register", response_model=UserInDB)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # 1. Check if email exists
    existing_user = crud_user.get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado.",
        )

    # 2. Create user
    new_user = crud_user.create_user(db, user_in)

    # 3. Generate email verification code
    crud_email_verification.create_code(db, new_user.id, new_user.email)

    return new_user


# ============================================================
# RESEND CODE
# ============================================================
@router.post("/send_verification_code")
def send_verification_code(data: EmailVerificationRequest, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, data.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado.",
        )

    crud_email_verification.resend_code(db, user.id, user.email)

    return {"message": "Código reenviado correctamente."}


# ============================================================
# VERIFY CODE
# ============================================================
@router.post("/verify_code")
def verify_code(data: EmailCodeVerify, db: Session = Depends(get_db)):
    valid = crud_email_verification.verify_code(
        db=db,
        email=data.email,
        code=data.code,
    )

    if not valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código inválido o expirado.",
        )

    crud_user.mark_email_verified(db, data.email)

    return {"message": "Email verificado correctamente."}


# ============================================================
# LOGIN
# ============================================================
@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, data.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas.",
        )

    # Check email verified
    if not user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Debes verificar tu email antes de iniciar sesión.",
        )

    # Password check
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas.",
        )

    # Generate token
    access_token = create_access_token({"sub": str(user.id)})

    return TokenResponse(access_token=access_token, token_type="bearer")
