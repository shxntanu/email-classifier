from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import os
from lib.listen import listen_for_emails
from dotenv import load_dotenv
from threading import Thread

load_dotenv()

app = Flask(__name__)
CORS(app)

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
    email_thread = Thread(target=listen_for_emails, args=('imap.gmail.com', 993, os.environ["EMAIL_ID"], os.environ["EMAIL_APP_PASSWORD"], "http://localhost:5000/email_data"))
    email_thread.start()

    # Run the Flask app
    app.run(debug=True)
