# run.py (explore-mailer)
from typing import Tuple

import mail
import json


def read_config(filename='config.json') -> Tuple[str, str]:
    """ Helper to read 'username' and 'password' fields from JSON config """
    with open(filename) as f:
        config = json.load(f)
        return config['username'], config['password']


def test_send(username, password):
    """ Test function, send one email """
    receiver = input('RECIPIENT> ')
    subject = input('SUBJECT> ')
    body = input('MESSAGE> ')
    with mail.login(username, password) as connection:
        print('Logged in successfully.')
        test_email = mail.Email(connection, sender=username, receiver=receiver,
                                subject=subject, body=body,
                                params={'name': 'Kevin'})
        try:
            print('Sending email...')
            test_email.send()
            print('Email sent.')
        except Exception as e:
            print('Error: Email not sent.')
            print(e)


def main():
    # Read email, password
    username, password = read_config()

    # Run a test, TODO fill in real code here
    test_send(username, password)


if __name__ == '__main__':
    main()
