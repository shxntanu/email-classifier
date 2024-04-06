import imaplib
import os
import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()

# def read_subject_and_raw_body(mail_id, password):
#     mail = imaplib.IMAP4_SSL('imap.gmail.com')
#     mail.login(mail_id, password)
#     mail.select('inbox')
#     result, data = mail.search(None, 'ALL')
#     email_ids = data[0].split()
#     print(*email_ids, sep="\n")

#     for email_id in email_ids:
#         result, data = mail.fetch(email_id, '(RFC822)')
#         raw_email = data[0][1]
#         msg = email.message_from_bytes(raw_email)
        
#         subject = msg['Subject']
#         print("Subject:", subject)

#         # Fetch the raw body
#         body = raw_email.decode('utf-8')
#         print("Raw Body:", body)

#     mail.close()
#     mail.logout()
#     return (subject, body)

def get_email_body(mail_id: str, password: str) -> None:
    """
    Get the body of the email
    """

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(mail_id, password)
    mail.select('inbox')
    result, data = mail.search(None, 'ALL')
    email_ids = data[0].split()

    for email_id in email_ids:
        result, data = mail.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]
        # print(raw_email)
        msg = email.message_from_bytes(raw_email)
        
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(part.get_content_charset())
                    print(body)
        else:
            body = msg.get_payload(decode=True).decode(msg.get_content_charset())
            print(body)

    mail.close()
    mail.logout()

def send_email(sender_email, sender_password, recipient_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, recipient_email, text)
    server.quit()

def read_emails(email, password, imap_server, imap_port):
    mail = imaplib.IMAP4_SSL(imap_server, imap_port)
    mail.login(email, password)
    mail.select('inbox')
    result, data = mail.search(None, 'ALL')
    email_ids = data[0].split()

    for email_id in email_ids:
        result, data = mail.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]
        print(raw_email.decode('utf-8'))

    mail.close()
    mail.logout()

def read_subject_and_body(mail_id, password):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(mail_id, password)
    mail.select('inbox')
    result, data = mail.search(None, 'ALL')
    email_ids = data[0].split()

    for email_id in email_ids:
        result, data = mail.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        subject = msg['Subject']
        print("Subject:", subject)

        body = get_raw_email_body(msg)
        print("Body:", body)

    mail.close()
    mail.logout()
    return (subject, body)

def fetch_latest_email(email, password, imap_server, imap_port):
    mail = imaplib.IMAP4_SSL(imap_server, imap_port)
    mail.login(email, password)
    mail.select('inbox')
    result, data = mail.search(None, 'ALL')
    email_ids = data[0].split()

    latest_email_id = email_ids[-1]  # Get the latest email ID
    result, data = mail.fetch(latest_email_id, '(RFC822)')
    raw_email = data[0][1]
    mail.close()
    mail.logout()

    return raw_email

def forward_email(mail_id, password, recipient, forwarded_subject, forwarded_body):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Fetch the latest email
    raw_email = fetch_latest_email(mail_id, password)

    # Parse the email
    msg = email.message_from_bytes(raw_email)

    # Create a forwarded email
    forwarded_msg = MIMEMultipart()
    forwarded_msg['From'] = email
    forwarded_msg['To'] = recipient
    forwarded_msg['Subject'] = forwarded_subject

    # Copy the original email's body
    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            forwarded_msg.attach(part)
        elif part.get_content_type() == 'multipart/alternative':
            forwarded_msg.attach(part)

    # Add a note to the forwarded email body
    forwarded_msg.attach(MIMEText(forwarded_body, 'plain'))

    # Send the forwarded email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(mail_id, password)
        server.send_message(forwarded_msg)

email_id = os.environ["EMAIL_ID"]
password = os.environ["EMAIL_APP_PASSWORD"]

# Test run
# get_email_body(email_id, password)
# send_email(email_id, password, "recipient_email", "Subject", "Body")
# read_emails(email_id, password)
# read_subject_and_body(email_id, password)

# forward_email(email_id, password, "shantanuwable2003@gmail.com", "Forwarded Subject", "Forwarded Body")
# email_message = fetch_latest_email("c2k21107041@ms.pict.edu", "1@M3ss3n1ial", "outlook.office365.com", 993)