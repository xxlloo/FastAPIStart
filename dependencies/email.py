from config.config import settings
from utils.email import EmailSender


def get_email_sender() -> EmailSender:
    return EmailSender(
        smtp_server=settings.SMTP_SERVER,
        smtp_port=settings.SMTP_PORT,
        sender_email=settings.SENDER_EMAIL,
        sender_password=settings.SENDER_PASSWORD,
    )
