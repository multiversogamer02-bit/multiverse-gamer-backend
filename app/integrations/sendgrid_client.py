import os
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from fastapi import HTTPException

# ============================================================
# CONFIGURACIÓN DEL LOGGER
# ============================================================
logger = logging.getLogger("sendgrid")
logger.setLevel(logging.INFO)


# ============================================================
# CARGA DE API KEY DESDE VARIABLES DE ENTORNO
# ============================================================
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

if not SENDGRID_API_KEY:
    raise RuntimeError(
        "❌ ERROR: No se encontró la variable de entorno SENDGRID_API_KEY.\n"
        "Configúrala en Render / local antes de enviar emails."
    )


# ============================================================
# FUNCIÓN PRINCIPAL DE ENVÍO DE EMAIL
# ============================================================
def send_email_verification(to_email: str, code: str) -> bool:
    """
    Envía un email con el código de verificación.
    
    Devuelve:
        True  = Envío exitoso
        False = Fallo controlado
    """
    sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)

    subject = "🎮 Multiverse Gamer – Verificación de Email"
    html_content = f"""
    <html>
        <body style="font-family: Arial; background-color: #0e0e10; padding: 20px; color: #ffffff;">
            <div style="max-width: 500px; margin: auto; background: #1a1a1d; padding: 25px; border-radius: 10px;">
                <h2 style="color: #7A5CFA; text-align: center;">
                    Multiverse Gamer – Verifica tu Email
                </h2>
                <p style="font-size: 16px; text-align: center;">
                    Gracias por registrarte en <strong>Multiverse Gamer</strong>.<br>
                    Para completar tu cuenta, ingresa el siguiente código:
                </p>

                <div style="text-align: center; margin: 25px 0;">
                    <span style="display: inline-block; background-color: #7A5CFA; padding: 12px 25px; 
                                 border-radius: 8px; font-size: 24px; letter-spacing: 3px; 
                                 color: white; font-weight: bold;">
                        {code}
                    </span>
                </div>

                <p style="text-align: center; font-size: 14px; opacity: 0.8;">
                    El código expira en 10 minutos por razones de seguridad.
                </p>

                <p style="text-align: center; margin-top: 35px; color: #aaaaaa; font-size: 12px;">
                    © {2025} Multiverse Gamer – Todos los derechos reservados.
                </p>
            </div>
        </body>
    </html>
    """

    message = Mail(
        from_email=Email("no-reply@multiversegamer.com", "Multiverse Gamer"),
        to_emails=To(to_email),
        subject=subject,
        html_content=Content("text/html", html_content)
    )

    try:
        response = sg.send(message)
        logger.info(f"📧 Email enviado a {to_email} – Status {response.status_code}")

        if response.status_code in [200, 202]:
            return True

        logger.error(f"❌ SendGrid devolvió error: {response.status_code}")
        return False

    except Exception as e:
        logger.exception(f"❌ Error enviando email a {to_email}: {str(e)}")
        return False
