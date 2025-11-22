# app/core/email_utils.py
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")


def send_verification_code(email: str, code: str) -> bool:
    """
    Envía un email con el código de verificación al usuario.
    """

    if not SENDGRID_API_KEY:
        print("ERROR: Environment variable SENDGRID_API_KEY not set")
        return False

    message = Mail(
        from_email="no-reply@multiversegamer.com",
        to_emails=email,
        subject="Tu código de verificación – Multiverse Gamer",
        html_content=f"""
        <h2 style="color:#6F3CFF">Código de verificación</h2>
        <p>Tu código es:</p>
        <h1 style="font-size:32px;letter-spacing:4px;color:#6F3CFF">{code}</h1>
        <p>Expira en <b>10 minutos</b>.</p>
        <p>Si no solicitaste esto, ignora este mensaje.</p>
        """
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        return True
    except Exception as e:
        print("SendGrid error:", e)
        return False


def send_welcome_email(email: str, username: str):
    """
    Se envía una vez verificado el email.
    """

    if not SENDGRID_API_KEY:
        print("ERROR: Environment variable SENDGRID_API_KEY not set")
        return False

    message = Mail(
        from_email="no-reply@multiversegamer.com",
        to_emails=email,
        subject="Bienvenido a Multiverse Gamer",
        html_content=f"""
        <h2 style="color:#6F3CFF">¡Bienvenido {username}!</h2>
        <p>Tu cuenta ha sido verificada con éxito.</p>
        <p>Ya podés iniciar sesión en el launcher.</p>
        """
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        return True
    except Exception as e:
        print("SendGrid error:", e)
        return False
