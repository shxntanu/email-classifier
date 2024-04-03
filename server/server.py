from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import os
from threading import Thread
from dotenv import load_dotenv
load_dotenv()
from lib.listen import listen_for_emails
from lib.spam_filter import preprocess_text, spam_model, EmailInput

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

    # TODO: Implement sending data to Mixtral Model here

@app.post("/predict")
def detect_spam():
    """
    Function to process an email and determine if it is spam or not.

    `body` of the request must be of the format:
    ```json
    {
        "email_text": "your email contents"
    }
    ```
    """
    try:
        data = request.json
        email_input = EmailInput(**data)
        email_text = preprocess_text(email_input.email_text)
        prediction = spam_model.predict([email_text])
        is_spam = bool(prediction[0])

        return jsonify({"is_spam": is_spam})
    except:
        return Response("Invalid input", status=400)

def start():
    # Email listening in a background thread
    email_thread = Thread(
        target=listen_for_emails, 
        args=(
            'imap.gmail.com', 
            993, os.environ["EMAIL_ID"], 
            os.environ["EMAIL_APP_PASSWORD"], 
            "http://localhost:5000/email_data"
        )
    )
    email_thread.start()

    # Keeping `debug=True` spawns two threads which monitor the same email address
    app.run(debug=False)

start()