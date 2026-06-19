#https://www.currentaffairs.org/news/why-do-we-love-birds-but-slaughter-chickens

from flask import Flask, render_template, request
from textblob import TextBlob
import spacy
import joblib
import os
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from newspaper import Article

app = Flask(__name__)

# Load classification model
model_path = os.path.join("model", "news_classifier.pkl")

classifier = joblib.load(model_path)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


# -----------------------------
# SUMMARIZATION
# -----------------------------
def summarize_text(text, sentence_count=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()

    summary = summarizer(parser.document, sentence_count)

    return " ".join(str(sentence) for sentence in summary)


# -----------------------------
# SENTIMENT ANALYSIS
# -----------------------------
def analyze_sentiment(text):
    blob = TextBlob(text)

    polarity = blob.sentiment.polarity

    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return sentiment, polarity


# -----------------------------
# NAMED ENTITY RECOGNITION
# -----------------------------
def extract_entities(text):
    doc = nlp(text)

    entities = []

    for ent in doc.ents:
        entities.append((ent.text, ent.label_))

    return entities

# -----------------------------
# URL EXTRACTION
# -----------------------------
def extract_article_from_url(url):

    article = Article(url)

    article.download()

    article.parse()

    return article.text

# -----------------------------
# NEWS CATEGORY
# -----------------------------
def classify_news(text):

    prediction = classifier.predict([text])[0]

    print(prediction)

    return prediction

# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# ANALYZE ROUTE
# -----------------------------
@app.route("/analyze", methods=["POST"])
def analyze():

    text = request.form["news_text"]

    url = request.form["news_url"]

    #If url provided, extract article text
    if url.strip() != "":
        text = extract_article_from_url(url)

    # NLP Tasks
    summary = summarize_text(text)

    sentiment, polarity = analyze_sentiment(text)

    entities = extract_entities(text)

    category = classify_news(text)

    return render_template(
        "result.html",
        original_text=text,
        summary=summary,
        sentiment=sentiment,
        polarity=polarity,
        entities=entities,
        category=category
    )


if __name__ == "__main__":
    app.run(debug=True)