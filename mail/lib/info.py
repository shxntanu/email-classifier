import imaplib
import email
from email import message_from_bytes
from email.message import EmailMessage

def get_email_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                body += part.get_payload(decode=True).decode(part.get_content_charset())
    else:
        body = msg.get_payload(decode=True).decode(msg.get_content_charset())
    return body

def LatestEmailMessage(imap_server, imap_port, email, password) -> EmailMessage:
    """
    Fetches the latest email from the specified email account using IMAP.

    Args:
        `imap_server` (str): IMAP server hostname
        `imap_port` (int): IMAP server port number
        `email` (str): Email address
        `password` (str): Email password (App password for Gmail)

    Returns:
        email.message.EmailMessage: The latest email message.
    """
    # Log in to the IMAP server
    imap = imaplib.IMAP4_SSL(imap_server, imap_port)
    imap.login(email, password)
    imap.select('INBOX')

    # Search for the latest email
    _, data = imap.search(None, 'ALL')
    latest_email_id = data[0].split()[-1]

    # Fetch the latest email
    typ, data = imap.fetch(latest_email_id, '(RFC822)')
    raw_email = data[0][1]
    email_message = message_from_bytes(raw_email)
    
    imap.close()
    imap.logout()
    
    return email_message

def LatestEmailInfo(email_id: str, password: str) -> tuple:
    """
    Fetch the latest email's sender, subject, and body.
    `email_id`: Email ID
    `password`: Email password (App password for Gmail)

    return: Tuple of sender, subject, and body
    """

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email_id, password)
    mail.select('inbox')
    _, data = mail.search(None, 'ALL')
    email_ids = data[0].split()

    if not email_ids:
        print("No emails found. Inbox is empty.")
        return None

    latest_email_id = email_ids[-1]  # Get the latest email ID
    _, data = mail.fetch(latest_email_id, '(RFC822)')
    raw_email = data[0][1]
    mail.close()
    mail.logout()

    msg = email.message_from_bytes(raw_email)

    sender = msg['From']
    subject = msg['Subject']
    body = get_email_body(msg)

    return sender, subject, body

def RAWEmail(email_id: str, password: str) -> str:
    """
    Fetch the raw email.

    `email_id`: Email ID
    `password`: Email password (App password for Gmail)

    return: Raw email
    """
    
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email_id, password)
    mail.select('inbox')
    _, data = mail.search(None, 'ALL')
    email_ids = data[0].split()

    if not email_ids:
        print("No emails found. Inbox is empty.")
        return None

    latest_email_id = email_ids[-1]  # Get the latest email ID
    _, data = mail.fetch(latest_email_id, '(RFC822)')
    raw_email = data[0][1]
    mail.close()
    mail.logout()

    return raw_email.decode('utf-8')