from email.message import EmailMessage
from dotenv import load_dotenv
import os
import smtplib


load_dotenv()


class NotificationManager:
    def __init__(self):
        self.sender = os.getenv("GOOGLE_SENDER")
        self.receiver = os.getenv("GOOGLE_RECEIVER")
        self.passwd = os.getenv("GOOGLE_SENDER_PASSWORD")

    def send_mail(self, content):
        message = EmailMessage()
        message.set_content(content)
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(self.sender, self.passwd)
        connection.send_message(
            from_addr=self.sender, to_addrs=self.receiver, msg=message
        )
        connection.quit()
