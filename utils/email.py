import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from fastapi import HTTPException
from pydantic import BaseModel


class EmailRequest(BaseModel):
    recipient_emails: List[str]
    subject: str
    body: str


class EmailSender:
    def __init__(
        self, smtp_server: str, smtp_port: int, sender_email: str, sender_password: str
    ):
        """
        初始化邮件发送工具类
        :param smtp_server: SMTP 服务器地址
        :param smtp_port: SMTP 端口
        :param sender_email: 发件人邮箱地址
        :param sender_password: 发件人邮箱密码（或应用专用密码）
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, recipient_emails: List[str], subject: str, body: str):
        """
        发送电子邮件
        :param recipient_emails: 收件人邮箱列表
        :param subject: 邮件主题
        :param body: 邮件内容
        """
        if not recipient_emails or not all(
            isinstance(email, str) for email in recipient_emails
        ):
            raise HTTPException(
                status_code=400,
                detail="Recipient emails must be a non-empty list of strings.",
            )

        try:
            # 创建邮件内容
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = ", ".join(recipient_emails)
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            # 连接 SMTP 服务器并发送邮件
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # 启用 TLS 加密
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_emails, msg.as_string())

            print(f"Email sent to: {', '.join(recipient_emails)}")
        except smtplib.SMTPException as e:
            raise HTTPException(
                status_code=500, detail=f"SMTP error occurred: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to send email: {str(e)}"
            )
