from flask import Flask, jsonify, request, Response
import imaplib
import email
import requests
import os
import time
from lib.info import get_email_body
from dotenv import load_dotenv
from threading import Thread

load_dotenv()

app = Flask(__name__)

def listen_for_emails(imap_server, imap_port, email_address, password):
    """
    Listens for incoming emails on the specified email account and prints the subject and contents of new emails.

    Args:
        imap_server (str): IMAP server hostname.
        imap_port (int): IMAP server port number.
        email_address (str): Email address.
        password (str): Email password.
    """
    imap = imaplib.IMAP4_SSL(imap_server, imap_port)
    imap.login(email_address, password)

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

                    # Hit an endpoint with the latest email data
                    url = 'http://localhost:5000/email_data'
                    data = {'subject': subject, 'body': body}
                    response = requests.post(url, json=data)
                    print("Response:", response.text)

        print("Waiting for new emails...")
        time.sleep(10)

@app.route('/email_data', methods=['POST'])
def receive_email_data():
    """
    Endpoint to receive email data.
    """

    data = request.json
    print("Received email data:", data)
    return jsonify({"message": "Email data received successfully"})

if __name__ == "__main__":
    # Start email listening in a background thread
    email_thread = Thread(target=listen_for_emails, args=('imap.gmail.com', 993, os.environ["EMAIL_ID"], os.environ["EMAIL_APP_PASSWORD"]))
    email_thread.start()

    # Run the Flask app
    app.run(debug=True)
