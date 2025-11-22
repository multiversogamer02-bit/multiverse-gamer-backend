# app/core/email_sender.py
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("SENDGRID_FROM", "no-reply@multiversegamer.com")


def send_verification_email(to_email: str, username: str, code: str):
    """
    Envía un email con el código de verificación.
    """
    if not SENDGRID_API_KEY:
        raise RuntimeError("SENDGRID_API_KEY no está configurado.")

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject="Tu código de verificación - Multiverse Gamer",
        html_content=f"""
        <h2>Hola {username} 👋</h2>
        <p>Tu código de verificación es:</p>
        <h1 style="color:#6F3CFF; font-size:32px;">{code}</h1>
        <p>Este código expira en <b>10 minutos</b>.</p>
        <br>
        <p>Si no solicitaste este registro, ignora este mensaje.</p>
        """
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        return True
    except Exception as e:
        print(f"[SendGrid] Error enviando email: {e}")
        return False
