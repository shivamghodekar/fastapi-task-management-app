from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List



conf = ConnectionConfig(
    MAIL_USERNAME = "shivamghodekar6@gmail.com",
    MAIL_PASSWORD = "nrsb lids jyfx xtqy",
    MAIL_FROM = "shivamghodekar6@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Task Management App",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)



async def send_email(emails: List[str]):
    html = """<p>Hi thanks for registration, Our team will connect you soon !</p> """

    message = MessageSchema(
        subject="Registration Confirmation",
        recipients=emails,
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    print({"message": "email has been sent"})







