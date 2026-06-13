<<<<<<< HEAD
from sklearn.feature_extraction import text

from flask import Flask, request, render_template
import nltk
import spacy
import textblob
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import joblib

# Load spaCy model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

# Load trained NLTK classifier
import os
model_path = os.path.join(os.path.dirname(__file__), "news_classifier.pkl")
print("Looking for model at:", model_path)
model = joblib.load(model_path)

# Function to clean and classify news text using NLTK model
def classify_news(text):
    stop_words = set(stopwords.words("english"))
    words = [w.lower() for w in word_tokenize(text) if w.isalpha() and w.lower() not in stop_words]
    features = {word: True for word in words}
    return model.predict(["text"])

# Function to preprocess text
def preprocess_text(text):
    tokens = nltk.word_tokenize(text)
    stop_words = set(nltk.corpus.stopwords.words("english"))
    tokens = [word.lower() for word in tokens if word.isalpha() and word not in stop_words]
    return " ".join(tokens)

# Function to summarize text
def summarize_text(text):
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers.lsa import LsaSummarizer

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 3)
    return " ".join([str(sentence) for sentence in summary])

# Function to perform sentiment analysis
def analyze_sentiment(text):
    blob = textblob.TextBlob(text)
    return blob.sentiment.polarity

# Function for Named Entity Recognition (NER)
def extract_named_entities(text):
    doc = nlp(text)
    return {ent.text: ent.label_ for ent in doc.ents}

# Function to scrape text from URL
def scrape_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")
    return " ".join([p.get_text() for p in paragraphs])

# Flask routes
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        input_type = request.form["input_type"]
        text = ""

        if input_type == "manual":
            text = request.form["manual_text"]
        elif input_type == "file":
            file = request.files["file"]
            text = file.read().decode("utf-8")
        elif input_type == "url":
            text = scrape_text_from_url(request.form["url"])

        preprocessed_text = preprocess_text(text)
        summary = summarize_text(text)
        sentiment = analyze_sentiment(text)
        category = classify_news(preprocessed_text)
        named_entities = extract_named_entities(text)

        return render_template("result.html", summary=summary, sentiment=sentiment, category=category, named_entities=named_entities)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

print(type(model))
print(text[:500])
=======
from sklearn.feature_extraction import text

from flask import Flask, request, render_template
import nltk
import spacy
import textblob
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import joblib

# Load spaCy model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

# Load trained NLTK classifier
import os
model_path = os.path.join(os.path.dirname(__file__), "news_classifier.pkl")
print("Looking for model at:", model_path)
model = joblib.load(model_path)

# Function to clean and classify news text using NLTK model
def classify_news(text):
    stop_words = set(stopwords.words("english"))
    words = [w.lower() for w in word_tokenize(text) if w.isalpha() and w.lower() not in stop_words]
    features = {word: True for word in words}
    return model.predict(["text"])

# Function to preprocess text
def preprocess_text(text):
    tokens = nltk.word_tokenize(text)
    stop_words = set(nltk.corpus.stopwords.words("english"))
    tokens = [word.lower() for word in tokens if word.isalpha() and word not in stop_words]
    return " ".join(tokens)

# Function to summarize text
def summarize_text(text):
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers.lsa import LsaSummarizer

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 3)
    return " ".join([str(sentence) for sentence in summary])

# Function to perform sentiment analysis
def analyze_sentiment(text):
    blob = textblob.TextBlob(text)
    return blob.sentiment.polarity

# Function for Named Entity Recognition (NER)
def extract_named_entities(text):
    doc = nlp(text)
    return {ent.text: ent.label_ for ent in doc.ents}

# Function to scrape text from URL
def scrape_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")
    return " ".join([p.get_text() for p in paragraphs])

# Flask routes
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        input_type = request.form["input_type"]
        text = ""

        if input_type == "manual":
            text = request.form["manual_text"]
        elif input_type == "file":
            file = request.files["file"]
            text = file.read().decode("utf-8")
        elif input_type == "url":
            text = scrape_text_from_url(request.form["url"])

        preprocessed_text = preprocess_text(text)
        summary = summarize_text(text)
        sentiment = analyze_sentiment(text)
        category = classify_news(preprocessed_text)
        named_entities = extract_named_entities(text)

        return render_template("result.html", summary=summary, sentiment=sentiment, category=category, named_entities=named_entities)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

print(type(model))
print(text[:500])
>>>>>>> 8218dd6ae85b971dc0f7e11ffd8c86eebbb7b983
#https://www.currentaffairs.org/news/why-do-we-love-birds-but-slaughter-chickens