# send.py (explore-mailer)
# Send a digest of messages over email
import argparse
import configparser
import json
import logging
import os

import mail


def read_digest_file(digest_file):
    with open(digest_file) as f:
        return json.load(f)


def send(digest_file, config_file='config.ini'):
    for f in (digest_file, config_file):
        if not os.path.isfile(f):
            raise FileNotFoundError(f)

    log_file = os.path.join('logs', digest_file + '.log')
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - [%(created)d] - %(levelname)s - %(message)s')

    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    user = config_parser['user']

    user_email = user['email']
    user_key = user['key']

    digest_data = read_digest_file(digest_file)
    with mail.login(user_email, user_key) as connection:
        print(f'Successfully logged in to {user_email}')
        for idx, item in enumerate(digest_data):
            print(f'Sending email {idx+1}/{len(digest_data)}', end='...')
            recipient_email = item['params']['email']

            email = mail.Email(connection,
                               sender=user_email, receiver=recipient_email,
                               subject=item['subject'],
                               body=item['body'])

            level, response = email.send()

            print('success' if level == 0 else 'failed')
            if level == 0:
                logging.info(response)
            elif level == 1:
                logging.warning(response)
            elif level == 2:
                logging.error(response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send a digest of messages over email')
    parser.add_argument('-c', '--config', type=str, default='config.ini', help='Configuration INI file')
    parser.add_argument('digest_file', type=str, help='Digest JSON file')
    args = parser.parse_args()
    send(args.digest_file, args.config)
