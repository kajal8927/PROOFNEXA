"""
app/services/similarity_service.py
===================================
Bridge between the FastAPI controllers and the nlp_core inference layer.

All heavy NLP logic lives in nlp_core/.
This file only adapts the nlp_core API to the shapes the controllers expect.
"""

import re
import logging
from pathlib import Path

from nlp_core.predictor   import check_similarity, SimilarityPredictor, _determine_risk
from nlp_core.preprocessor import TextPreprocessor
from app.services.ngram_service        import generate_ngrams
from app.services.fingerprint_service  import generate_fingerprints

logger      = logging.getLogger("proofnexa.similarity_service")
_pre        = TextPreprocessor()
_predictor  = SimilarityPredictor()


# ── Public helpers used by controllers ────────────────────────────────────────

def determine_risk_level(score: float) -> str:
    """score is 0-100 (percentage). Returns Low/Medium/High/Critical."""
    return _determine_risk(score)


def get_text_fingerprints(text: str, n: int = 3) -> set:
    tokens = _pre.tokenize(text)
    ngrams = generate_ngrams(tokens, n)
    return generate_fingerprints(ngrams)


def calculate_jaccard_similarity(set_a: set, set_b: set) -> float:
    """Returns 0-100."""
    if not set_a or not set_b:
        return 0.0
    return round(len(set_a & set_b) / len(set_a | set_b) * 100, 2)


def calculate_cosine_similarity(text1: str, text2: str) -> float:
    """Returns 0-100 using the trained TF-IDF model."""
    result = check_similarity(text1, text2)
    return result["similarity_percentage"]


def calculate_overall_similarity(text1: str, text2: str) -> float:
    """
    Ensemble score (0-100):
        Fingerprint Jaccard  x 0.40
        TF-IDF Cosine        x 0.60
    """
    fp1 = get_text_fingerprints(text1)
    fp2 = get_text_fingerprints(text2)
    jaccard = calculate_jaccard_similarity(fp1, fp2)
    cosine  = calculate_cosine_similarity(text1, text2)
    return round(jaccard * 0.40 + cosine * 0.60, 2)


def find_matching_sentences(
    input_text: str, source_text: str, threshold: float = 25.0
) -> list:
    """Sentence-level matching using fingerprint Jaccard."""
    try:
        input_sentences  = _pre.split_sentences(input_text)
        source_sentences = _pre.split_sentences(source_text)
    except Exception:
        input_sentences  = [s.strip() for s in re.split(r"(?<=[.!?])\s+", input_text)  if len(s.strip()) > 10]
        source_sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", source_text) if len(s.strip()) > 10]

    matches = []
    for inp in input_sentences:
        fp_inp = get_text_fingerprints(inp, n=2)
        for src in source_sentences:
            fp_src = get_text_fingerprints(src, n=2)
            score  = calculate_jaccard_similarity(fp_inp, fp_src)
            if score >= threshold:
                matches.append({
                    "matchedText": src,
                    "inputText":   inp,
                    "similarity":  score,
                    "matchType":   "ngram",
                })
    return matches
