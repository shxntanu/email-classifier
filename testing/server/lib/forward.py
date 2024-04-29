import smtplib
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import message_from_string
from email.header import decode_header
from email.message import EmailMessage

def decode_subject(subject):
    """
    Decodes the subject header of an email message.

    Args:
        subject (str): The subject header of the email.

    Returns:
        str: Decoded subject.
    """
    decoded = decode_header(subject)
    decoded_subject = []
    for part, encoding in decoded:
        if isinstance(part, bytes):
            decoded_subject.append(part.decode(encoding or 'utf-8'))
        else:
            decoded_subject.append(part)
    return ''.join(decoded_subject)

def forward_email(email_message, smtp_server: str, smtp_port: int, smtp_email: str, smtp_password: str, forward_to: str, cc_to: list = [], bcc_to: list = []) -> None:
    """
    Forwards an email message to the specified recipient using SMTP while maintaining the formatting of the original message.

    Args:
        email_message (email.message.EmailMessage): The email message to forward.
        smtp_server (str): SMTP server hostname.
        smtp_port (int): SMTP server port number.
        smtp_email (str): Sender's email address.
        smtp_password (str): Sender's email password.
        forward_to (str): Recipient's email address.
    """
    email_message = message_from_string(email_message)
    # New email message
    forwarded_email = MIMEMultipart()
    forwarded_email['From'] = smtp_email
    forwarded_email['To'] = forward_to
    if cc_to:
        forwarded_email['CC'] = ', '.join(cc_to)
    forwarded_email['Subject'] = f"Fwd from EC: {decode_subject(email_message['Subject'])}" # EC = Email Classifier

    html_part = None
    for part in email_message.walk():
        if part.get_content_type() == 'text/html':
            html_part = part.get_payload(decode=True).decode(part.get_content_charset())
        elif part.get_content_disposition() == 'attachment':
            # Attachment
            new_part = MIMEBase(part.get_content_type().split('/')[0], part.get_content_type().split('/')[1])
            new_part.set_payload(part.get_payload(decode=True))
            encoders.encode_base64(new_part)
            new_part.add_header('Content-Disposition', 'attachment', filename=part.get_filename())
            forwarded_email.attach(new_part)
        else:
            continue

    if html_part:
        forwarded_email.attach(MIMEText(html_part, 'html'))
    else:
        # If HTML part not found, use plain text
        text_part = email_message.get_payload(decode=True).decode(email_message.get_content_charset())
        forwarded_email.attach(MIMEText(text_part, 'plain'))

    # TODO: Add custom HTML Content for denoting mails forwarded by our service

    # Add a custom string to the email
    custom_string = "\n\n-- This email was forwarded using the Email Classifier Service --"
    forwarded_email.attach(MIMEText(custom_string, 'plain'))

    # Connect to SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(smtp_email, smtp_password)
        smtp.send_message(forwarded_email, to_addrs=[forward_to] + (cc_to or []) + (bcc_to or []))