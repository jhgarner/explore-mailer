# mail.py (explore-mailer)

import os
import base64
import smtplib
import ssl
from email.mime.text import MIMEText
from typing import Optional

from googleapiclient.discovery import build
from googleapiclient.discovery import Resource
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# PORT = 587
PORT = 465
SMTP_URL = 'smtp.gmail.com'

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class Email:
    """ Simple MIME Email class """
    __slots__ = ['connection', 'sender', 'receiver', 'subject', 'body', 'params']

    def __init__(self, connection: Resource,
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
        message = MIMEText(self.body.format(**self.params))
        message['From'] = self.sender
        message['To'] = self.receiver
        message['Subject'] = self.subject.format(**self.params)
        # message.attach(MIMEText(self.body.format(**self.params), 'plain'))
        return {'raw': base64.urlsafe_b64encode(str.encode(message.as_string()))}

    @property
    def _valid(self):
        """ Check whether or not Email is valid (ready to send) """
        return all(map(lambda v: v is not None,
                       (self.connection, self.sender, self.receiver, self.subject, self.body)))

    def send(self):
        """ Send Email over the established connection """
        if self._valid:
            try:
                self.connection.users().messages().send(userId=self.sender, body=self.formatted_message).execute()#(self.sender, self.receiver, self.formatted_message)
                return 0, f'Successfully sent email {self.sender} -> {self.receiver}'
            except Exception as e:
                print(e)
                return 2, str(e)
        else:
            return 1, 'Invalid email formatting, message not sent'


def login(username: str, password: str) -> Resource:
    """ Comes from official Google documentation at
    https://developers.google.com/gmail/api/quickstart/python """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)
