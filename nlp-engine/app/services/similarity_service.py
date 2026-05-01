"""
similarity_service.py
=====================
Plagiarism / text-similarity detection.

Strategy
--------
1. Fingerprint overlap (Jaccard on Winnowing hashes)      – exact phrase matching
2. Trained TF-IDF vectorizer (1-3 grams, cosine sim)      – robust vocabulary matching
3. Weighted ensemble:  fingerprint * 0.55 + tfidf * 0.45  – best of both
"""

import re
import string
import logging
from pathlib import Path

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sk_cosine

from app.services.preprocessing_service import tokenize_text, split_into_sentences
from app.services.ngram_service import generate_ngrams
from app.services.fingerprint_service import generate_fingerprints

logger = logging.getLogger("proofnexa.similarity")

# ── Model path ──────────────────────────────────────────────────────────────────
_MODEL_DIR       = Path(__file__).parent.parent.parent / "models"
_VECTORIZER_PATH = _MODEL_DIR / "tfidf_vectorizer.pkl"

# ── Lazy-loaded model singleton ─────────────────────────────────────────────────
_vectorizer: TfidfVectorizer | None = None


def _load_vectorizer() -> TfidfVectorizer | None:
    """Load the pre-trained TF-IDF vectorizer once and cache it."""
    global _vectorizer
    if _vectorizer is not None:
        return _vectorizer

    if _VECTORIZER_PATH.exists():
        try:
            _vectorizer = joblib.load(_VECTORIZER_PATH)
            logger.info(
                f"Loaded trained TF-IDF vectorizer from {_VECTORIZER_PATH} "
                f"(vocab: {len(_vectorizer.vocabulary_)} terms)"
            )
        except Exception as exc:
            logger.warning(
                f"Could not load trained vectorizer: {exc}. "
                "Falling back to on-the-fly vectorizer."
            )
            _vectorizer = None
    else:
        logger.warning(
            f"Trained vectorizer not found at {_VECTORIZER_PATH}. "
            "Run train_model.py to build it. Using on-the-fly vectorizer."
        )
    return _vectorizer


# ── Lightweight preprocessing (no NLTK dependency) ─────────────────────────────
_STOPWORDS = {
    "a","an","the","and","or","but","in","on","at","to","for","of","with",
    "by","from","is","are","was","were","be","been","being","have","has","had",
    "do","does","did","will","would","could","should","may","might","shall",
    "that","this","these","those","it","its","they","them","their","we","our",
    "i","me","my","you","your","he","him","his","she","her","as","if","so",
    "not","no","nor","yet","just","than","then","also","into","about","over",
    "up","out","which","who","what","when","where","how","all","each","any",
}


def _simple_preprocess(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = [t for t in text.split() if t not in _STOPWORDS and len(t) > 1]
    return " ".join(tokens)


# ── Core similarity functions ───────────────────────────────────────────────────

def calculate_jaccard_similarity(set_a: set, set_b: set) -> float:
    """Jaccard similarity between two fingerprint sets, returns 0-100."""
    if not set_a or not set_b:
        return 0.0
    intersection = set_a & set_b
    union         = set_a | set_b
    return round(len(intersection) / len(union) * 100, 2)


def calculate_cosine_similarity(text1: str, text2: str) -> float:
    """
    TF-IDF cosine similarity.
    Uses the pre-trained vectorizer when available; otherwise fits on-the-fly.
    Returns a value in [0, 100].
    """
    if not text1.strip() or not text2.strip():
        return 0.0
    try:
        clean1 = _simple_preprocess(text1)
        clean2 = _simple_preprocess(text2)

        vec = _load_vectorizer()

        if vec is not None:
            tfidf = vec.transform([clean1, clean2])
        else:
            # Fallback: fit a temporary vectorizer
            try:
                tmp = TfidfVectorizer(
                    tokenizer=tokenize_text, token_pattern=None,
                    lowercase=True, ngram_range=(1, 3), sublinear_tf=True
                )
                tfidf = tmp.fit_transform([text1, text2])
            except Exception:
                tmp = TfidfVectorizer(ngram_range=(1, 3), sublinear_tf=True)
                tfidf = tmp.fit_transform([clean1, clean2])

        sim = sk_cosine(tfidf[0:1], tfidf[1:2])
        return round(float(sim[0][0]) * 100, 2)

    except Exception as exc:
        logger.error(f"Error in calculate_cosine_similarity: {exc}")
        return 0.0


def get_text_fingerprints(text: str, n: int = 3) -> set:
    """Winnowing fingerprints for a text."""
    try:
        tokens = tokenize_text(text)
    except Exception:
        tokens = _simple_preprocess(text).split()
    ngrams = generate_ngrams(tokens, n)
    return generate_fingerprints(ngrams)


def determine_risk_level(score: float) -> str:
    """0-30 Low | 31-60 Medium | 61-80 High | 81-100 Critical"""
    if score <= 30:
        return "Low"
    elif score <= 60:
        return "Medium"
    elif score <= 80:
        return "High"
    return "Critical"


def calculate_overall_similarity(text1: str, text2: str) -> float:
    """
    Ensemble score:
        - Fingerprint Jaccard  x 0.55  (exact phrase overlap)
        - TF-IDF Cosine        x 0.45  (vocabulary/semantic similarity)
    Returns 0-100.
    """
    fp1 = get_text_fingerprints(text1)
    fp2 = get_text_fingerprints(text2)

    jaccard_score = calculate_jaccard_similarity(fp1, fp2)
    cosine_score  = calculate_cosine_similarity(text1, text2)

    final_score = (jaccard_score * 0.55) + (cosine_score * 0.45)
    return round(final_score, 2)


def find_matching_sentences(
    input_text: str, source_text: str, threshold: float = 25.0
) -> list:
    """
    Finds sentence-level matches between two documents.
    Uses fingerprint Jaccard for fast exact-match detection.
    """
    try:
        input_sentences  = split_into_sentences(input_text)
        source_sentences = split_into_sentences(source_text)
    except Exception:
        input_sentences  = [s.strip() for s in re.split(r"(?<=[.!?])\s+", input_text)  if len(s.strip()) > 10]
        source_sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", source_text) if len(s.strip()) > 10]

    matches = []
    for inp_sent in input_sentences:
        inp_fp = get_text_fingerprints(inp_sent, n=2)
        for src_sent in source_sentences:
            src_fp  = get_text_fingerprints(src_sent, n=2)
            j_score = calculate_jaccard_similarity(inp_fp, src_fp)
            if j_score >= threshold:
                matches.append({
                    "matchedText": src_sent,
                    "inputText":   inp_sent,
                    "similarity":  j_score,
                    "matchType":   "ngram",
                })

    return matches
