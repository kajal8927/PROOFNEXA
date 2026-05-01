"""
nlp_core/preprocessor.py
========================
Handles all text cleaning and normalisation.

No heavy dependencies — works without NLTK installed.
If NLTK is present, it uses its stopword list; otherwise falls back
to a built-in list that covers all common English stopwords.
"""

import re
import string
import logging
from typing import List

logger = logging.getLogger("proofnexa.preprocessor")


# ── Stopword list (built-in fallback, no NLTK needed) ─────────────────────────
_BUILTIN_STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "that", "this", "these",
    "those", "it", "its", "they", "them", "their", "we", "our", "i", "me",
    "my", "you", "your", "he", "him", "his", "she", "her", "as", "if",
    "so", "not", "no", "nor", "yet", "just", "than", "then", "also",
    "into", "about", "over", "up", "out", "which", "who", "what", "when",
    "where", "how", "all", "each", "any", "both", "few", "more", "most",
    "other", "some", "such", "only", "own", "same", "too", "very", "can",
    "us", "after", "before", "through", "between", "during", "without",
    "again", "further", "once", "here", "there", "while", "because",
    "until", "against", "among", "throughout", "despite", "towards",
    "upon", "concerning", "of", "to", "in", "for", "on", "with", "at",
    "by", "from", "as", "into", "through", "during", "including", "until",
    "against", "nor", "not", "but", "or", "because", "as", "until",
    "while", "although", "though", "even", "since", "whether", "either",
}


def _load_stopwords() -> set:
    """Try NLTK first; fall back to built-in list."""
    try:
        from nltk.corpus import stopwords
        import nltk
        try:
            sw = set(stopwords.words("english"))
            logger.debug("Using NLTK stopwords (%d words)", len(sw))
            return sw
        except LookupError:
            nltk.download("stopwords", quiet=True)
            return set(stopwords.words("english"))
    except Exception:
        logger.debug("NLTK not available — using built-in stopwords")
        return _BUILTIN_STOPWORDS


class TextPreprocessor:
    """
    Stateless text cleaning pipeline.

    Usage
    -----
    >>> p = TextPreprocessor()
    >>> p.clean("The Quick Brown FOX!")
    'quick brown fox'
    >>> p.clean_for_tfidf("Machine learning is a field of AI.")
    'machine learning field ai'
    """

    def __init__(self, remove_stopwords: bool = True, min_token_len: int = 2):
        self.remove_stopwords = remove_stopwords
        self.min_token_len    = min_token_len
        self._stopwords       = _load_stopwords() if remove_stopwords else set()
        self._punct_table     = str.maketrans("", "", string.punctuation)

    # ── Public API ─────────────────────────────────────────────────────────────

    def clean(self, text: str) -> str:
        """
        Basic cleaning only:  lowercase + strip punctuation + collapse whitespace.
        Stopwords are NOT removed — used when we need original meaning preserved
        (e.g. sentence splitting, display purposes).
        """
        if not text or not isinstance(text, str):
            return ""
        text = text.lower()
        text = text.translate(self._punct_table)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def clean_for_tfidf(self, text: str) -> str:
        """
        Full cleaning pipeline for TF-IDF training/inference:
          1. Lowercase
          2. Remove punctuation
          3. Collapse whitespace
          4. Remove stopwords
          5. Filter short tokens
        Returns a single cleaned string.
        """
        text = self.clean(text)
        if not text:
            return ""
        tokens = [
            t for t in text.split()
            if t not in self._stopwords and len(t) >= self.min_token_len
        ]
        return " ".join(tokens)

    def tokenize(self, text: str) -> List[str]:
        """Return list of clean tokens (for fingerprinting / n-gram use)."""
        return self.clean_for_tfidf(text).split()

    def split_sentences(self, text: str) -> List[str]:
        """Split text into sentences, filtering very short fragments."""
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return [s.strip() for s in sentences if len(s.strip()) > 15]

    def batch_clean(self, texts: List[str]) -> List[str]:
        """Vectorised cleaning for a list of texts."""
        return [self.clean_for_tfidf(t) for t in texts]
