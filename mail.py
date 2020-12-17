# mail.py (explore-mailer)

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

PORT = 465
SMTP_URL = 'smtp.gmail.com'


class Email:
    """ Simple MIME Email class """
    __slots__ = ['connection', 'sender', 'receiver', 'subject', 'body', 'params']

    def __init__(self, connection: smtplib.SMTP_SSL,
                 sender: Optional[str] = None,
                 receiver: Optional[str] = None,
                 subject: Optional[str] = None,
                 body: Optional[str] = None,
                 params: Optional[dict] = None):
        self.connection = connection
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.body = body
        self.params = params if params else dict()

    @property
    def formatted_message(self):
        """ Get the formatted MIMEMultipart message string """
        message = MIMEMultipart()
        message['From'] = self.sender
        message['To'] = self.receiver
        message['Subject'] = self.subject.format(**self.params)
        message.attach(MIMEText(self.body.format(**self.params), 'plain'))
        return message.as_string()

    @property
    def _valid(self):
        """ Check whether or not Email is valid (ready to send) """
        return all(map(lambda v: v is not None,
                       (self.connection, self.sender, self.receiver, self.subject, self.body)))

    def send(self):
        """ Send Email over the established connection """
        if self._valid:
            self.connection.sendmail(self.sender, self.receiver, self.formatted_message)
        else:
            print('Error: Invalid Email. Message not sent.')


def login(username: str, password: str) -> smtplib.SMTP_SSL:
    """ Log in (establish SSL connection to SMTP server) """
    context = ssl.create_default_context()
    smtp_connection = smtplib.SMTP_SSL(SMTP_URL, port=PORT, context=context)
    smtp_connection.login(username, password)
    return smtp_connection
