import imaplib
import email
import os
from info import get_email_body
import time
from dotenv import load_dotenv
load_dotenv()

def listen_for_emails(imap_server, imap_port, email_address, password):
    """
    Listens for incoming emails on the specified email account and prints the subject and contents of new emails.

    Args:
        imap_server (str): IMAP server hostname.
        imap_port (int): IMAP server port number.
        email_address (str): Email address.
        password (str): Email password.
    """
    imap = imaplib.IMAP4_SSL(imap_server, imap_port)
    imap.login(email_address, password)

    while True:
        print("Checking for new emails...")
        imap.select('INBOX')
        typ, data = imap.search(None, '(UNSEEN)')

        if typ == 'OK':
            for num in data[0].split():
                typ, msg_data = imap.fetch(num, '(RFC822)')
                if typ == 'OK':
                    raw_email = msg_data[0][1]
                    email_message = email.message_from_bytes(raw_email)
                    subject = email_message['Subject']
                    body = get_email_body(email_message)

                    print("Subject:", subject)
                    print("Body:", body)

        # TODO: Add logic here to hit an endpoint with the latest email data

        print("Waiting for new emails...")
        time.sleep(10)

# Example usage
listen_for_emails('imap.gmail.com', 993, os.environ["EMAIL_ID"], os.environ["EMAIL_APP_PASSWORD"])