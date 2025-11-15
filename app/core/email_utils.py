import smtplib
from email.mime.text import MIMEText


def send_email(to_email: str, subject: str, body: str):
    """
    Utilidad básica para enviar correos.
    Se puede integrar en /auth/forgot en el futuro.
    """

    sender = "no-reply@multiversegamer.com"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = ""   # tu email
    smtp_pass = ""   # tu contraseña o app password

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(sender, [to_email], msg.as_string())
        server.quit()
        return True

    except Exception as e:
        print("Error enviando email:", e)
        return False
