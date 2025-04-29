from celery_app import celery_app
from config.config import settings
from utils.email import EmailSender


@celery_app.task(
    name="tasks.send_email",
)
def send_email_task(email: str, subject: str, body: str):
    email_sender = EmailSender(
        smtp_server=settings.SMTP_SERVER,
        smtp_port=settings.SMTP_PORT,
        sender_email=settings.SENDER_EMAIL,
        sender_password=settings.SENDER_PASSWORD,
    )
    email_sender.send_email([email], subject, body)
