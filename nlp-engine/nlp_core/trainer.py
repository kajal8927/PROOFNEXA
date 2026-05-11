"""
nlp_core/trainer.py
===================
Trains the TF-IDF vectorizer on the 10k plagiarism dataset.

Steps
-----
1. Load raw CSV (text1, text2, label, similarity_score)
2. Preprocess every text (lowercase, remove noise, stopwords)
3. Fit TF-IDF (1-3 gram) on the full corpus
4. Save vectorizer to  models/tfidf_vectorizer.pkl
5. Save metadata to    models/model_metadata.json

Run directly:
    python -m nlp_core.trainer
or via the top-level train_model.py
"""

import csv
import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nlp_core.preprocessor import TextPreprocessor

logger = logging.getLogger("proofnexa.trainer")

# ── Paths (relative to nlp-engine root) ───────────────────────────────────────
_BASE         = Path(__file__).parent.parent          # nlp-engine/
_DATA_RAW     = _BASE / "data" / "raw"
_DATA_PROC    = _BASE / "data" / "processed"
_MODEL_DIR    = _BASE / "models"

PRIMARY_DATASET   = _DATA_RAW / "plagiarism_10k_dataset.csv"
SECONDARY_DATASET = _DATA_RAW / "plagiarism_dataset.csv"
PROCESSED_CSV     = _DATA_PROC / "processed_pairs.csv"
VECTORIZER_PKL    = _MODEL_DIR / "tfidf_vectorizer.pkl"
METADATA_JSON     = _MODEL_DIR / "model_metadata.json"

# ── Threshold used to convert cosine score → binary label ─────────────────────
SIMILARITY_THRESHOLD = 0.15   # tuned from similarity_score distribution


class ModelTrainer:
    """
    End-to-end training pipeline for the TF-IDF plagiarism detection model.

    Usage
    -----
    >>> trainer = ModelTrainer()
    >>> vectorizer = trainer.run()
    """

    def __init__(
        self,
        ngram_range:  Tuple[int, int] = (1, 3),
        max_features: int              = 75_000,
        threshold:    float            = SIMILARITY_THRESHOLD,
    ):
        self.ngram_range  = ngram_range
        self.max_features = max_features
        self.threshold    = threshold
        self.preprocessor = TextPreprocessor(remove_stopwords=True)

        # Ensure output directories exist
        _DATA_PROC.mkdir(parents=True, exist_ok=True)
        _MODEL_DIR.mkdir(parents=True, exist_ok=True)

    # ── Step 1: Load ───────────────────────────────────────────────────────────

    def load_dataset(self) -> list:
        """Load raw CSV. Prefers 10k dataset; falls back to small dataset."""
        path = PRIMARY_DATASET if PRIMARY_DATASET.exists() else SECONDARY_DATASET
        if not path.exists():
            raise FileNotFoundError(
                f"No dataset found. Expected:\n  {PRIMARY_DATASET}\n  {SECONDARY_DATASET}"
            )
        logger.info("Loading dataset: %s", path)

        rows = []
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                rows.append(row)

        logger.info("Loaded %d rows", len(rows))
        return rows

    # ── Step 2: Preprocess ─────────────────────────────────────────────────────

    def preprocess_dataset(self, rows: list) -> list:
        """Clean all texts and return enriched row dicts."""
        logger.info("Preprocessing %d rows …", len(rows))
        cleaned = []
        skipped = 0
        for row in rows:
            t1 = self.preprocessor.clean_for_tfidf(str(row.get("text1", "")))
            t2 = self.preprocessor.clean_for_tfidf(str(row.get("text2", "")))
            if not t1 or not t2:
                skipped += 1
                continue
            cleaned.append({
                "text1":            str(row.get("text1", "")).strip().strip('"'),
                "text2":            str(row.get("text2", "")).strip().strip('"'),
                "clean_text1":      t1,
                "clean_text2":      t2,
                "label":            int(row.get("label", 0)),
                "similarity_score": float(row.get("similarity_score", 0.0)),
            })
        logger.info("Preprocessed: %d valid, %d skipped", len(cleaned), skipped)
        return cleaned

    def save_processed(self, cleaned: list):
        """Persist processed dataset for inspection / re-use."""
        with open(PROCESSED_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["text1","text2","clean_text1","clean_text2",
                               "label","similarity_score"]
            )
            writer.writeheader()
            writer.writerows(cleaned)
        logger.info("Processed dataset saved → %s", PROCESSED_CSV)

    # ── Step 3: Fit TF-IDF ────────────────────────────────────────────────────

    def fit_vectorizer(self, cleaned: list) -> TfidfVectorizer:
        """Fit a TF-IDF vectorizer on the combined corpus of all texts."""
        logger.info("Fitting TF-IDF vectorizer (ngram=%s, max_features=%d) …",
                    self.ngram_range, self.max_features)

        corpus = []
        for row in cleaned:
            corpus.append(row["clean_text1"])
            corpus.append(row["clean_text2"])

        vectorizer = TfidfVectorizer(
            analyzer      = "word",
            ngram_range   = self.ngram_range,
            max_features  = self.max_features,
            sublinear_tf  = True,        # apply log normalisation to TF
            min_df        = 1,           # keep rare terms (important for plagiarism)
            max_df        = 0.95,        # drop near-universal terms
            strip_accents = "unicode",
        )
        vectorizer.fit(corpus)
        logger.info("Vectorizer fitted. Vocabulary size: %d", len(vectorizer.vocabulary_))
        return vectorizer

    # ── Step 4: Evaluate ──────────────────────────────────────────────────────

    def evaluate(self, vectorizer: TfidfVectorizer, cleaned: list) -> dict:
        """
        Compute accuracy using the cosine similarity threshold.
        Also uses similarity_score from the dataset to tune the threshold.
        """
        logger.info("Evaluating model on %d pairs …", len(cleaned))

        # Tune threshold using similarity_score column
        ref_scores = [r["similarity_score"] for r in cleaned if r["label"] == 1]
        if ref_scores:
            tuned_threshold = float(np.percentile(ref_scores, 20))
            tuned_threshold = max(0.10, min(tuned_threshold, 0.30))
        else:
            tuned_threshold = self.threshold
        logger.info("Tuned similarity threshold from dataset: %.4f", tuned_threshold)

        correct = 0
        cosine_scores = []
        for row in cleaned:
            tfidf = vectorizer.transform([row["clean_text1"], row["clean_text2"]])
            sim   = float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0])
            cosine_scores.append(sim)
            predicted = 1 if sim >= tuned_threshold else 0
            if predicted == row["label"]:
                correct += 1

        accuracy = correct / len(cleaned)
        pos_scores = [s for s, r in zip(cosine_scores, cleaned) if r["label"] == 1]
        neg_scores = [s for s, r in zip(cosine_scores, cleaned) if r["label"] == 0]

        stats = {
            "accuracy":          round(accuracy, 4),
            "threshold_used":    round(tuned_threshold, 4),
            "avg_sim_positive":  round(float(np.mean(pos_scores)), 4) if pos_scores else 0,
            "avg_sim_negative":  round(float(np.mean(neg_scores)), 4) if neg_scores else 0,
            "total_pairs":       len(cleaned),
            "positive_pairs":    len(pos_scores),
            "negative_pairs":    len(neg_scores),
        }
        logger.info(
            "Accuracy: %.2f%%  |  avg_pos: %.4f  |  avg_neg: %.4f",
            accuracy * 100, stats["avg_sim_positive"], stats["avg_sim_negative"]
        )
        return stats

    # ── Step 5: Save ──────────────────────────────────────────────────────────

    def save_vectorizer(self, vectorizer: TfidfVectorizer):
        joblib.dump(vectorizer, VECTORIZER_PKL, compress=3)
        size_kb = round(VECTORIZER_PKL.stat().st_size / 1024, 1)
        logger.info("Vectorizer saved → %s  (%.1f KB)", VECTORIZER_PKL, size_kb)

    def save_metadata(self, vectorizer: TfidfVectorizer, stats: dict, elapsed: float):
        meta = {
            "model_name":         "TF-IDF Cosine Similarity — PROOFNEXA",
            "trained_at":         datetime.now(timezone.utc).isoformat(),
            "training_time_sec":  round(elapsed, 2),
            "vectorizer_path":    str(VECTORIZER_PKL),
            "ngram_range":        list(self.ngram_range),
            "max_features":       self.max_features,
            "vocabulary_size":    len(vectorizer.vocabulary_),
            "sublinear_tf":       True,
            "similarity_threshold": stats["threshold_used"],
            "evaluation":         stats,
            "dataset": {
                "file":           str(PRIMARY_DATASET.name),
                "total_pairs":    stats["total_pairs"],
                "positive_pairs": stats["positive_pairs"],
                "negative_pairs": stats["negative_pairs"],
            },
        }
        with open(METADATA_JSON, "w") as f:
            json.dump(meta, f, indent=2)
        logger.info("Metadata saved → %s", METADATA_JSON)

    # ── Main pipeline ─────────────────────────────────────────────────────────

    def run(self) -> TfidfVectorizer:
        """Execute the full training pipeline. Returns the trained vectorizer."""
        t0 = time.perf_counter()
        logger.info("=" * 55)
        logger.info("  PROOFNEXA — TF-IDF Model Training")
        logger.info("=" * 55)

        rows    = self.load_dataset()
        cleaned = self.preprocess_dataset(rows)

        self.save_processed(cleaned)

        vectorizer = self.fit_vectorizer(cleaned)
        stats      = self.evaluate(vectorizer, cleaned)

        self.save_vectorizer(vectorizer)
        self.save_metadata(vectorizer, stats, time.perf_counter() - t0)

        logger.info("Training complete in %.2f sec.", time.perf_counter() - t0)
        logger.info("=" * 55)
        return vectorizer


# ── CLI entry point ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    ModelTrainer().run()
