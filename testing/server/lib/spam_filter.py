import nltk
import re
import string
from joblib import load
from pydantic import BaseModel

class EmailInput(BaseModel):
    email_text: str

#pre-processing
stop_words = set(nltk.corpus.stopwords.words("english"))
spetial_chars = set(string.printable) - set(string.ascii_letters) - set(" ")
escaped_chars = [re.escape(c) for c in spetial_chars]
regex = re.compile(f"({'|'.join(escaped_chars)})")
stemmer = nltk.stem.porter.PorterStemmer()
url_regex = re.compile("(?P<url>https?://[^\s]+)")

#loading the model
model_path = "server/lib/spam_detection_model.joblib"
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