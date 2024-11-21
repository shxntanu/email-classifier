import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from faker import Faker
import os 
from dotenv import load_dotenv
load_dotenv()

def send_random_email(smtp_server, smtp_port, sender_email, sender_password, recipient_email):
    faker = Faker()

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)

        for _ in range(3):
            msg = MIMEMultipart()

            subject = faker.sentence(nb_words=6)
            body = faker.paragraph(nb_sentences=5)

            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))
            server.send_message(msg)

send_random_email("smtp.gmail.com", 587, os.environ["GMAIL_EMAIL_ID"], os.environ["EMAIL_APP_PASSWORD"], os.environ["OUTLOOK_EMAIL_ID"])