import random
import string
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.models_email_verification import EmailVerificationCode
from app.models.user import User
from app.integrations.sendgrid_client import send_email_verification

# ============================================================
# CONFIGURACIÓN
# ============================================================
MAX_ATTEMPTS = 5
CODE_EXPIRATION_MINUTES = 10
RESEND_COOLDOWN_SECONDS = 60  # evita spam de reenvío


# ============================================================
# GENERADOR DE CÓDIGO
# ============================================================
def generate_code() -> str:
    """Genera un código alfanumérico de 6 caracteres."""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=6))


# ============================================================
# INVALIDAR CÓDIGOS ANTERIORES
# ============================================================
def invalidate_previous_codes(db: Session, user_id: int):
    """Marca como usados todos los códigos anteriores de ese usuario."""
    db.query(EmailVerificationCode).filter(
        EmailVerificationCode.user_id == user_id,
        EmailVerificationCode.used == False
    ).update({EmailVerificationCode.used: True})

    db.commit()


# ============================================================
# CREAR UN NUEVO CÓDIGO
# ============================================================
def create_code_record(db: Session, user_id: int) -> EmailVerificationCode:
    """Genera un nuevo código descartando todos los anteriores."""
    invalidate_previous_codes(db, user_id)

    code = generate_code()
    expires = datetime.utcnow() + timedelta(minutes=CODE_EXPIRATION_MINUTES)

    record = EmailVerificationCode(
        user_id=user_id,
        code=code,
        expires_at=expires,
        used=False
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    return record


# ============================================================
# ENVÍO DE EMAIL
# ============================================================
def send_verification_email(db: Session, user: User) -> dict:
    """
    Genera un código, lo guarda y envía email usando SendGrid.
    """

    # Protección anti-spam de reenvío
    last_code = db.query(EmailVerificationCode).filter(
        EmailVerificationCode.user_id == user.id
    ).order_by(EmailVerificationCode.id.desc()).first()

    if last_code:
        time_since_last = (datetime.utcnow() - last_code.created_at).total_seconds()
        if time_since_last < RESEND_COOLDOWN_SECONDS:
            return {
                "status": "cooldown",
                "message": f"Debes esperar {int(RESEND_COOLDOWN_SECONDS - time_since_last)} segundos para reenviar otro código."
            }

    # Generar el nuevo código
    code_record = create_code_record(db, user.id)

    # Enviar email HTML bonito
    success = send_email_verification(
        to_email=user.email,
        code=code_record.code
    )

    if not success:
        return {
            "status": "error",
            "message": "No se pudo enviar el email. Intenta nuevamente más tarde."
        }

    return {
        "status": "ok",
        "message": "Código enviado correctamente",
        "expires_in": CODE_EXPIRATION_MINUTES * 60,
    }


# ============================================================
# VERIFICACIÓN DEL CÓDIGO
# ============================================================
def verify_code(db: Session, user: User, code: str) -> bool:
    """
    Valida que el código exista, no esté usado y no esté expirado.
    """

    # Demasiados intentos → bloqueo temporal
    if user.verification_attempts >= MAX_ATTEMPTS:
        return False

    record = db.query(EmailVerificationCode).filter(
        and_(
            EmailVerificationCode.user_id == user.id,
            EmailVerificationCode.code == code,
            EmailVerificationCode.used == False
        )
    ).order_by(EmailVerificationCode.id.desc()).first()

    # Código incorrecto
    if not record:
        user.verification_attempts += 1
        db.commit()
        return False

    # Código expirado
    if record.expires_at < datetime.utcnow():
        return False

    # Marcar como usado y verificar usuario
    record.used = True
    user.verified = True
    user.verification_attempts = 0
    db.commit()

    return True


# ============================================================
# LIMPIEZA AUTOMÁTICA
# ============================================================
def cleanup_expired_codes(db: Session):
    """Elimina códigos expirados para no llenar la BD."""
    now = datetime.utcnow()
    db.query(EmailVerificationCode).filter(
        EmailVerificationCode.expires_at < now
    ).delete()
    db.commit()


# ============================================================
# MARCAR UN CÓDIGO COMO USADO (opcional)
# ============================================================
def mark_as_used(db: Session, record: EmailVerificationCode):
    record.used = True
    db.commit()
