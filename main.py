import imaplib
import email
import requests
import os
import time
from dotenv import load_dotenv
load_dotenv()
from server.lib.info import get_email_body
from server.lib.spam_filter import preprocess_text, spam_model, EmailInput
# from server.lib.forward import forward_email
from celery_tasks import forward_email

imap_server = "imap.gmail.com"
imap_port = 993
smtp_server = "smtp.gmail.com"
smpt_port = 587
email_id = os.environ["EMAIL_ID"]
email_password = os.environ["EMAIL_APP_PASSWORD"]
fw_mail_id = os.environ["FWD_EMAIL_ID"]

imap = imaplib.IMAP4_SSL(imap_server, imap_port)
imap.login(email_id, email_password)

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
                
                sub_body = f'Subject: {subject}\n{body}'
                email_text = preprocess_text(sub_body)
                prediction = spam_model.predict([email_text])
                is_spam = bool(prediction[0])

                if(is_spam):
                    print("Spam detected!")

                    # TODO: Handle Spam Detection (flagging) 
                    
                else:
                    print("Not spam!")

                    # TODO: Send email contents to LLM and get receiver list

                    # TODO: Search in DB for the department name received by LLM

                    raw_email = email_message.as_string()
                    # forward_email(raw_email, smtp_server, smpt_port, email_id, email_password, fw_mail_id) 
                    forward_email.delay(raw_email, smtp_server, smpt_port, email_id, email_password, fw_mail_id)                
                
    print("Waiting for new emails...")
    time.sleep(10)
