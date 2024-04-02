import imaplib
import smtplib
from email.message import EmailMessage
from email import policy
from email.parser import BytesParser
import os
from dotenv import load_dotenv
load_dotenv()

# IMAP settings
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993
EMAIL = os.environ["EMAIL_ID"]
PASSWORD = os.environ["EMAIL_APP_PASSWORD"]

# SMTP settings
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# Email forwarding settings
FORWARD_TO = 'shantanuwable2003@example.com'

def fetch_latest_email():
    # Connect to IMAP server
    imap_conn = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    imap_conn.login(EMAIL, PASSWORD)
    imap_conn.select('INBOX')

    # Search for latest email
    _, data = imap_conn.search(None, 'ALL')
    latest_email_id = data[0].split()[-1]

    # Fetch latest email
    _, message_data = imap_conn.fetch(latest_email_id, '(RFC822)')
    raw_email = message_data[0][1]
    msg = BytesParser(policy=policy.default).parsebytes(raw_email)

    imap_conn.close()
    imap_conn.logout()

    return msg

def forward_email(msg):
    # Connect to SMTP server
    smtp_conn = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp_conn.starttls()
    smtp_conn.login(EMAIL, PASSWORD)

    # Create new email message
    forwarded_msg = EmailMessage()
    forwarded_msg['Subject'] = 'Fwd: ' + msg['Subject']
    forwarded_msg['From'] = EMAIL
    forwarded_msg['To'] = FORWARD_TO

    for part in msg.walk():
        content_type = part.get_content_type()
        content_disposition = str(part.get('Content-Disposition'))

        # Skip any non-multipart content
        if content_type == 'text/plain' and 'attachment' not in content_disposition:
            forwarded_msg.set_content(part.get_payload(decode=True), subtype='plain')
            forwarded_msg.set_charset(part.get_content_charset())
        elif content_type == 'text/html' and 'attachment' not in content_disposition:
            forwarded_msg.add_alternative(part.get_payload(decode=True), subtype='html')
            forwarded_msg.set_charset(part.get_content_charset())

    # Forward the email
    smtp_conn.send_message(forwarded_msg)

    smtp_conn.quit()

if __name__ == '__main__':
    latest_email = fetch_latest_email()
    forward_email(latest_email)
