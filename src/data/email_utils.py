import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

SMTP_HOST = 'sandbox.smtp.mailtrap.io'
SMTP_PORT = 587
SMTP_USER = 'b36aa7814b3690'
SMTP_PASS = '76ee5f754e14d9'
FROM_EMAIL = 'noreply@isam.com'


def send_confirmation_email(to_email, username, token):
    subject = 'Confirma tu registro en ISAM'
    confirm_text = f"Tu código de confirmación es: <b>{token}</b><br>\nIngresa este código en la pantalla de confirmación para activar tu cuenta.\nEste código expira en 24 horas."
    body = f"""
    <html>
        <body>
            <p>Hola {username},</p>
            <p>{confirm_text}</p>
        </body>
    </html>
    """
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(FROM_EMAIL, to_email, msg.as_string())
