import imaplib
from email import message_from_bytes
from email.message import EmailMessage

def get_email_body(msg: EmailMessage) -> str:
    """
    Extracts the body of an email message.
    Note: This function does NOT return the raw body, it return the parsed body in plain text form.
    """

    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                body += part.get_payload(decode=True).decode(part.get_content_charset())
    else:
        body = msg.get_payload(decode=True).decode(msg.get_content_charset())
    return body

def latest_email_message(imap_server, imap_port, email, password):
    """
    Fetches the latest email from the specified email account using IMAP.

    Args:
        `imap_server` (str): IMAP server hostname
        `imap_port` (int): IMAP server port number
        `email` (str): Email address
        `password` (str): Email password (App password for Gmail)

    Returns:
        email.message.EmailMessage: The latest email message.

    You can access the sender, subject, and body of the email using the following properties:
    ```
        sender = msg['From']
        subject = msg['Subject']
        body = get_email_body(msg)
    ```

    """
    # Log in to the IMAP server
    imap = imaplib.IMAP4_SSL(imap_server, imap_port)
    imap.login(email, password)
    imap.select('INBOX')

    # Search for the latest email
    _, data = imap.search(None, 'ALL')
    email_ids = data[0].split()
    if not email_ids:
        print("No emails found. Inbox is empty.")
        return None
    
    latest_email_id = email_ids[-1]
    typ, data = imap.fetch(latest_email_id, '(RFC822)')
    raw_email = data[0][1]
    email_message = message_from_bytes(raw_email)
    
    imap.close()
    imap.logout()
    
    return data, email_message

def get_ssb(mail: EmailMessage) -> tuple:
    """
    Fetch the sender, subject, and body of an email.

    return: Tuple of sender, subject, and body
    """

    sender = mail['From']
    subject = mail['Subject']
    body = get_email_body(mail)

    return sender, subject, body

def RAWEmail(mail: EmailMessage) -> str:
    """
    Fetch the raw email.

    return: Raw email
    """
    return mail.decode('utf-8')