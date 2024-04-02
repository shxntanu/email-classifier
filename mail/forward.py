import imaplib
import smtplib
from email.message import EmailMessage
from email import policy
from email.parser import BytesParser
import os
from email import message_from_bytes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import decode_header
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
SMTP_EMAIL = os.environ["EMAIL_ID"]
SMTP_PASSWORD = os.environ["EMAIL_APP_PASSWORD"]

# Email forwarding settings
FORWARD_TO = 'shantanuwable2003@gmail.com'

def fetch_latest_email():
    # Log in to the IMAP server
    imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    imap.login(EMAIL, PASSWORD)
    imap.select('INBOX')

    # Search for latest email
    typ, data = imap.search(None, 'ALL')
    latest_email_id = data[0].split()[-1]

    # Fetch the latest email
    typ, data = imap.fetch(latest_email_id, '(RFC822)')
    raw_email = data[0][1]
    email_message = message_from_bytes(raw_email)
    
    imap.close()
    imap.logout()
    
    return email_message

def decode_subject(subject):
    decoded = decode_header(subject)
    decoded_subject = []
    for part, encoding in decoded:
        if isinstance(part, bytes):
            decoded_subject.append(part.decode(encoding or 'utf-8'))
        else:
            decoded_subject.append(part)
    return ''.join(decoded_subject)

def forward_email(email_message):
    # Create a new email message
    forwarded_email = MIMEMultipart()
    forwarded_email['From'] = SMTP_EMAIL
    forwarded_email['To'] = FORWARD_TO
    forwarded_email['Subject'] = f"Fwd from EC: {decode_subject(email_message['Subject'])}" # EC = Email Classifier

    # Get the HTML part of the email (if available)
    html_part = None
    for part in email_message.walk():
        if part.get_content_type() == 'text/html':
            html_part = part.get_payload(decode=True).decode(part.get_content_charset())
            break

    if html_part:
        # Attach the HTML content
        forwarded_email.attach(MIMEText(html_part, 'html'))
    else:
        # If HTML part not found, use plain text
        text_part = email_message.get_payload(decode=True).decode(email_message.get_content_charset())
        forwarded_email.attach(MIMEText(text_part, 'plain'))

    # Add a custom string to the email
    custom_string = "\n\n-- This email was forwarded using the Email Classifier Service --"
    forwarded_email.attach(MIMEText(custom_string, 'plain'))

    # Connect to SMTP server and send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
        smtp.send_message(forwarded_email)

if __name__ == "__main__":
    latest_email = fetch_latest_email()
    forward_email(latest_email)
    print("Email forwarded successfully.")
