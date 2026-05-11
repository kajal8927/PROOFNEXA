"""
nlp_core/predictor.py
=====================
Inference module — loads the trained model and exposes check_similarity().

Public API
----------
check_similarity(text1, text2) -> dict
    Returns:
        {
            "similarity_score":      0.73,          # raw cosine (0.0 – 1.0)
            "similarity_percentage": 73.0,          # same × 100
            "plagiarism_label":      1,             # 1 = plagiarised, 0 = original
            "risk_level":            "High",        # Low / Medium / High / Critical
            "is_plagiarised":        True,
        }

SimilarityPredictor
    Singleton class (lazy-loaded). Thread-safe for concurrent API requests.
"""

import json
import logging
import threading
from pathlib import Path
from typing import Dict, Any

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nlp_core.preprocessor import TextPreprocessor

logger = logging.getLogger("proofnexa.predictor")

# ── Paths ──────────────────────────────────────────────────────────────────────
_BASE          = Path(__file__).parent.parent        # nlp-engine/
_VECTORIZER    = _BASE / "models" / "tfidf_vectorizer.pkl"
_METADATA      = _BASE / "models" / "model_metadata.json"

# Default threshold if metadata unavailable
_DEFAULT_THRESHOLD = 0.15


def _load_threshold() -> float:
    """Read the tuned threshold from model_metadata.json."""
    try:
        with open(_METADATA) as f:
            meta = json.load(f)
        t = float(meta.get("similarity_threshold", _DEFAULT_THRESHOLD))
        logger.debug("Loaded threshold from metadata: %.4f", t)
        return t
    except Exception:
        logger.debug("metadata.json unavailable — using default threshold %.4f", _DEFAULT_THRESHOLD)
        return _DEFAULT_THRESHOLD


def _determine_risk(score_pct: float) -> str:
    """
    Convert percentage score to risk label.
    0–30   → Low
    31–60  → Medium
    61–80  → High
    81–100 → Critical
    """
    if score_pct <= 30:
        return "Low"
    elif score_pct <= 60:
        return "Medium"
    elif score_pct <= 80:
        return "High"
    return "Critical"


class SimilarityPredictor:
    """
    Thread-safe singleton that loads the trained TF-IDF vectorizer once
    and exposes a predict() method for production use.

    Falls back gracefully to an on-the-fly vectorizer if the trained
    model file is missing (e.g. before first training run).
    """

    _instance: "SimilarityPredictor | None" = None
    _lock = threading.Lock()

    def __new__(cls) -> "SimilarityPredictor":
        with cls._lock:
            if cls._instance is None:
                obj = super().__new__(cls)
                obj._initialised = False
                cls._instance = obj
        return cls._instance

    def _init(self):
        if self._initialised:
            return
        self._preprocessor = TextPreprocessor()
        self._threshold     = _load_threshold()
        self._vectorizer    = self._load_vectorizer()
        self._initialised   = True

    # ── Model loading ─────────────────────────────────────────────────────────

    def _load_vectorizer(self) -> TfidfVectorizer | None:
        if _VECTORIZER.exists():
            try:
                vec = joblib.load(_VECTORIZER)
                logger.info(
                    "Trained vectorizer loaded from %s  (vocab: %d terms)",
                    _VECTORIZER, len(vec.vocabulary_),
                )
                return vec
            except Exception as exc:
                logger.warning("Could not load vectorizer: %s — fallback active", exc)
        else:
            logger.warning(
                "Trained vectorizer not found at %s. "
                "Run train_model.py to build it.", _VECTORIZER
            )
        return None

    # ── Core prediction ───────────────────────────────────────────────────────

    def _cosine(self, clean1: str, clean2: str) -> float:
        """Return cosine similarity in [0, 1]."""
        if self._vectorizer is not None:
            mat = self._vectorizer.transform([clean1, clean2])
        else:
            # Fallback: fit on-the-fly (slower, less accurate)
            from sklearn.feature_extraction.text import TfidfVectorizer as TF
            tmp = TF(ngram_range=(1, 3), sublinear_tf=True)
            mat = tmp.fit_transform([clean1, clean2])
        return float(cosine_similarity(mat[0:1], mat[1:2])[0][0])

    def predict(self, text1: str, text2: str) -> Dict[str, Any]:
        """
        Compare two texts and return a structured similarity report.

        Parameters
        ----------
        text1, text2 : raw (uncleaned) strings

        Returns
        -------
        dict with keys:
            similarity_score      float  0.0 – 1.0
            similarity_percentage float  0.0 – 100.0
            plagiarism_label      int    0 or 1
            risk_level            str    Low / Medium / High / Critical
            is_plagiarised        bool
        """
        self._init()

        if not text1 or not text1.strip() or not text2 or not text2.strip():
            return {
                "similarity_score":      0.0,
                "similarity_percentage": 0.0,
                "plagiarism_label":      0,
                "risk_level":            "Low",
                "is_plagiarised":        False,
            }

        clean1 = self._preprocessor.clean_for_tfidf(text1)
        clean2 = self._preprocessor.clean_for_tfidf(text2)

        # Edge case: both texts reduce to empty after cleaning
        if not clean1 or not clean2:
            score = 0.0
        else:
            score = self._cosine(clean1, clean2)

        pct         = round(score * 100, 2)
        is_plag     = score >= self._threshold
        label       = 1 if is_plag else 0
        risk        = _determine_risk(pct)

        return {
            "similarity_score":      round(score, 4),
            "similarity_percentage": pct,
            "plagiarism_label":      label,
            "risk_level":            risk,
            "is_plagiarised":        is_plag,
        }


# ── Module-level convenience function ─────────────────────────────────────────

def check_similarity(text1: str, text2: str) -> Dict[str, Any]:
    """
    High-level function for plagiarism detection.

    Parameters
    ----------
    text1 : str  — original / reference text
    text2 : str  — text to check for plagiarism

    Returns
    -------
    dict:
        similarity_score      (float, 0.0–1.0)
        similarity_percentage (float, 0.0–100.0)
        plagiarism_label      (int, 0 or 1)
        risk_level            (str, Low/Medium/High/Critical)
        is_plagiarised        (bool)

    Example
    -------
    >>> result = check_similarity(
    ...     "Machine learning is a subset of artificial intelligence.",
    ...     "Deep learning is a branch of machine learning and AI."
    ... )
    >>> result["similarity_percentage"]
    68.5
    >>> result["plagiarism_label"]
    1
    >>> result["risk_level"]
    'High'
    """
    return SimilarityPredictor().predict(text1, text2)
