import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from email_validator import EmailNotValidError, validate_email

logger = logging.getLogger(__name__)


class EmailServiceError(Exception):
    """邮件服务基础异常"""

    pass


class InvalidRecipientError(EmailServiceError):
    """无效收件人异常"""

    pass


class EmailSender:
    def __init__(
            self, smtp_server: str, smtp_port: int, sender_email: str, sender_password: str
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def _validate_recipients(self, emails: List[str]) -> List[str]:
        validated = []
        for email in emails:
            try:
                validated.append(
                    str(validate_email(email, check_deliverability=False).email)
                )
            except EmailNotValidError as e:
                logger.warning(
                    "无效邮箱地址被过滤", extra={"email": email, "error": str(e)}
                )
                continue
        if not validated:
            raise InvalidRecipientError("没有有效的收件人地址")
        return validated

    def _create_smtp_connection(self):
        try:
            if self.smtp_port == 465:
                return smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, timeout=30)
            else:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30)
                server.starttls()
                return server
        except Exception as e:
            raise EmailServiceError(f"SMTP连接失败: {str(e)}") from e

    def send_email(
            self, recipient_emails: List[str], subject: str, body: str, html: bool = False
    ):
        # 验证收件人
        valid_recipients = self._validate_recipients(recipient_emails)

        # 创建邮件内容
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = ", ".join(valid_recipients)
        msg["Subject"] = subject
        content_type = "html" if html else "plain"
        msg.attach(MIMEText(body, content_type))

        # 发送邮件
        try:
            with self._create_smtp_connection() as server:
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, valid_recipients, msg.as_string())
            logger.info(
                "邮件发送成功",
                extra={"recipients": valid_recipients, "subject": subject},
            )
        except Exception as e:
            logger.error(
                "邮件发送失败",
                exc_info=True,
                extra={"recipients": valid_recipients, "error": str(e)},
            )
            raise EmailServiceError(f"邮件发送失败: {str(e)}") from e
