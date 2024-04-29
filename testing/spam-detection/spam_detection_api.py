from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from joblib import load
import nltk
import string
import re

#launch server
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the origin of your frontend application
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
model_path = "spam_detection_model.joblib"
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


#rest api for spam detection
@app.post("/predict")
def detect_spam(email_input: EmailInput):
    email_text = preprocess_text(email_input.email_text)

    prediction = spam_model.predict([email_text])

    is_spam = bool(prediction[0])

    return {"is_spam": is_spam}
