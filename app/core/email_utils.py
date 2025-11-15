import sendgrid
from sendgrid.helpers.mail import Mail
from app.core.config import settings


def send_reset_email(to_email: str, reset_link: str):
    """
    Envía email de recuperación usando SendGrid.
    """

    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

    message = Mail(
        from_email="no-reply@multiversegamer.com",
        to_emails=to_email,
        subject="Recupera tu contraseña - Multiverse Gamer",
        html_content=f"""
        <h2>Restablecer contraseña</h2>
        <p>Haz clic en el siguiente enlace para cambiar tu contraseña:</p>
        <p><a href="{reset_link}">{reset_link}</a></p>
        <br>
        <p>Este enlace es válido por 15 minutos.</p>
        """
    )

    try:
        sg.send(message)
        return True
    except Exception as e:
        print("SendGrid error:", e)
        return False
