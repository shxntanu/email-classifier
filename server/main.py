import imaplib
import email
import os
import time
import requests
import json
from cryptography.fernet import Fernet
from dotenv import load_dotenv
load_dotenv()

from lib.info import get_email_body
from lib.forward import forward_email
# from tasks import forward_email
from lib.attachments import extract_attachments

def encrypt_text(key, text):
    cipher_suite = Fernet(key)
    encrypted_text = cipher_suite.encrypt(text.encode())
    return encrypted_text

heirarchy = json.loads(open("server/src/heirarchy.json").read())

imap_server = os.environ["OUTLOOK_IMAP_SERVER"]
imap_port = os.environ["OUTLOOK_IMAP_PORT"]
smtp_server = os.environ["OUTLOOK_SMTP_SERVER"]
smpt_port = os.environ["OUTLOOK_SMTP_PORT"]
email_id = os.environ["OUTLOOK_EMAIL_ID"]
email_password = os.environ["OUTLOOK_EMAIL_PASSWORD"]

# imap_server = os.environ["GMAIL_IMAP_SERVER"]
# imap_port = os.environ["GMAIL_IMAP_PORT"]
# smtp_server = os.environ["GMAIL_SMTP_SERVER"]
# smpt_port = os.environ["GMAIL_SMTP_PORT"]
# email_id = os.environ["GMAIL_EMAIL_ID"]
# email_password = os.environ["GMAIL_APP_PASSWORD"]

LLM_URL = "http://192.168.45.165:5000/classify"


imap = imaplib.IMAP4_SSL(imap_server, imap_port)
imap.login(email_id, email_password)

while True:

    # try:
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
                sender = email_message['From']
                body = get_email_body(email_message)
                
                print("Sender:", sender)
                print("Subject:", subject)
                print("Body:", body)

                attachments = extract_attachments(email_message)

                enc_text = encrypt_text(os.environ["ENCRYPTION_KEY"], f"Subject: {subject}\n\nBody: {body}\n\nDocuments: {attachments}")

                req_data = {
                    "content": enc_text.decode()
                }

                response = requests.post(LLM_URL, json=req_data)
                res_data = response.json()

                """
                response.json() will be like:
                {
                    "industry": ...,
                    "sentiment": ...,
                    "status": ...,
                }
                """

                industry = res_data["industry"]
                sentiment = res_data["sentiment"]

                print("Industry:", industry)
                print("Sentiment:", sentiment)

                fwd_email = ""
                cc= []
                bcc=[]

                if sentiment.lower() == "neutral":
                    for dept in heirarchy:
                        if dept["department_name"] == industry.lower():
                            fwd_email = dept["department_mail"]
                            cc = []
                            bcc = []
                            break
                else:
                    for dept in heirarchy:
                        if dept["department_name"] == industry.lower():
                            cc.append(dept["department_mail"])
                            for subDept in dept["subDepartments"]:
                                if subDept["sentiment_name"] == sentiment.lower():
                                    fwd_email = subDept["subDepartment_mail"]
                                    bcc = []
                                    break

                cc.append("shantanuwable2003@gmail.com")
                print("Forwarding to:", fwd_email)
                print("CC:", *cc, sep=", ")
                print("BCC:", *bcc, sep=", ")

                # TODO: Search in DB for the department name received by LLM

                # forward_email.delay(email_message.as_string(), smtp_server, smpt_port, email_id, email_password, fwd_email, cc, bcc, sentiment) 
                # forward_email.delay(email_message.as_string(), smtp_server, smpt_port, email_id, email_password, fwd_email, cc.append("yarndev.barclays@gmail.com"), bcc, sentiment) 
                forward_email(email_message, smtp_server, smpt_port, email_id, email_password, fwd_email, cc, bcc, sentiment) 


                print("Email forwarded successfully!")
                
    print("Waiting for new emails...")
    time.sleep(10)

    # except Exception as e:
    #     print("Error:", e)
    #     print("Waiting for new emails...")
    #     time.sleep(10)
