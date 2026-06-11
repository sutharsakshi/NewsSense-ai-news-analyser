import nltk
from nltk.corpus import reuters, stopwords
from nltk import word_tokenize
import random
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Download resources
nltk.download('reuters')
nltk.download('punkt')
nltk.download('stopwords')

# Clean text
stop_words = set(stopwords.words("english"))

def clean_text(words):
    return ' '.join([w.lower() for w in words if w.isalpha() and w.lower() not in stop_words])

# Use only documents with one label
texts = []
labels = []

for fileid in reuters.fileids():
    cats = reuters.categories(fileid)
    if len(cats) == 1:
        text = clean_text(reuters.words(fileid))
        texts.append(text)
        labels.append(cats[0])

# Create TF-IDF pipeline
classifier = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Train model
classifier.fit(texts, labels)

# Save to correct path
joblib.dump(classifier, "NLPproject/news_classifier.pkl")
print("Reuters model trained and saved as news_classifier.pkl")

