import streamlit as st
import imaplib
import os
import time
import email
from dotenv import load_dotenv
load_dotenv()

from lib.info import get_email_body
from lib.attachments import extract_attachments
from llm import return_ans

st.set_page_config(
    page_title="Email Classifier",
    page_icon="👋",
)

st.write("# Welcome to Email Classifier! 👋")

email_id = st.text_input("Enter your Email ID (Gmail) which you want to monitor", placeholder="johndoe@example.com")
app_password = st.text_input("Enter your App Password (Gmail) to access the emails through IMAP", placeholder="yourpassword")

monitor = st.button("Monitor")

if monitor and email_id and app_password:

    imap = imaplib.IMAP4_SSL(os.environ["GMAIL_IMAP_SERVER"], os.environ["GMAIL_IMAP_PORT"])
    imap.login(email_id, app_password)

    while True:
        
        imap.select('INBOX')
        typ, data = imap.search(None, '(UNSEEN)')

        if typ == 'OK':
            if len(data[0].split()) == 0:
                st.info("No new unseen message(s).", icon="ℹ️")
            
            else:
                st.success("Done!")
        
            for num in data[0].split():
                typ, msg_data = imap.fetch(num, '(RFC822)')
                if typ == 'OK':
                    raw_email = msg_data[0][1]
                    email_message = email.message_from_bytes(raw_email)
                    subject = email_message['Subject']
                    sender = email_message['From']
                    body = get_email_body(email_message)
                    
                    with st.expander(subject):
                    
                        st.subheader("From:")
                        st.write(sender)

                        st.subheader("Subject:")
                        st.write(subject)

                        st.subheader("Body:")
                        st.write(body)
                        
                        st.markdown(f'''## Team to which this mail should be forwarded to:\n
```
{return_ans(f"From: {sender}\n\nSubject: {subject}\n\nBody: {body}")['team']}
```''')
            
            
        with st.spinner('Checking for mail...'):
            time.sleep(10)