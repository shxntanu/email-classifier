from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import os
from lib.listen import listen_for_emails
from threading import Thread
from pydantic import BaseModel
from joblib import load
import nltk
import string
import re
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

#pre-processing
stop_words = set(nltk.corpus.stopwords.words("english"))
spetial_chars = set(string.printable) - set(string.ascii_letters) - set(" ")
escaped_chars = [re.escape(c) for c in spetial_chars]
regex = re.compile(f"({'|'.join(escaped_chars)})")
stemmer = nltk.stem.porter.PorterStemmer()
url_regex = re.compile("(?P<url>https?://[^\s]+)")

class EmailInput(BaseModel):
    email_text: str

#loading the model
model_path = "lib/spam_detection_model.joblib"
spam_model = load(model_path)

def preprocess_text(text):
    # capitalization
    text = text.lower()

    # remove urls
    text = re.sub(url_regex," ",text)
    
    # tokenization
    text = nltk.word_tokenize(text, language='english')
        
    # stop words removal
    text = [word for word in text if word not in stop_words]
    
    # noise removal
    text = [word for word in text if word.isalpha()]
    
    # stemming
    text = [stemmer.stem(word) for word in text]
    
    return ' '.join(text)

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
    try:
        data = request.json
        email_input = EmailInput(**data)
        email_text = preprocess_text(email_input.email_text)
        prediction = spam_model.predict([email_text])
        is_spam = bool(prediction[0])

        return {"is_spam": is_spam}
    except:
        return Response("Invalid input", status=400)

if __name__ == "__main__":
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
    
    app.run(debug=True)
