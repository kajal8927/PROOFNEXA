import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from nltk.stem import PorterStemmer

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")


STOP_WORDS = set(stopwords.words("english"))
stemmer = PorterStemmer()


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text.strip()


def tokenize_text(text: str) -> list:
    cleaned = clean_text(text)
    tokens = word_tokenize(cleaned)
    tokens = [
        stemmer.stem(token) for token in tokens
        if token not in STOP_WORDS and len(token) > 1
    ]
    return tokens


def split_into_sentences(text: str) -> list:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [sentence.strip() for sentence in sentences if len(sentence.strip()) > 10]
