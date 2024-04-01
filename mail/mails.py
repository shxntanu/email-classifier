import imaplib
import os
import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()

def get_email_body(mail_id, password):
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


email_id = os.environ["EMAIL_ID"]
password = os.environ["EMAIL_APP_PASSWORD"]
get_email_body(email_id, password)