"""
nlp_core/evaluator.py
=====================
Train / test split + detailed evaluation metrics.

Provides:
    ModelEvaluator.evaluate(vectorizer, cleaned_rows) -> EvalReport
    EvalReport  — dataclass with all metrics + pretty-print
"""

import logging
import random
from dataclasses import dataclass, field, asdict
from typing import List, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger("proofnexa.evaluator")


@dataclass
class EvalReport:
    """All evaluation metrics in one place."""
    total_pairs:    int
    train_pairs:    int
    test_pairs:     int
    threshold:      float
    accuracy:       float
    precision:      float
    recall:         float
    f1:             float
    confusion:      List[List[int]]
    avg_sim_pos:    float
    avg_sim_neg:    float
    positive_pairs: int
    negative_pairs: int

    def to_dict(self) -> dict:
        return asdict(self)

    def pretty(self) -> str:
        sep = "=" * 48
        lines = [
            sep,
            "  PROOFNEXA — Model Evaluation Report",
            sep,
            f"  Dataset       : {self.total_pairs} pairs  "
            f"(train {self.train_pairs} / test {self.test_pairs})",
            f"  Threshold     : {self.threshold:.4f}",
            f"  Accuracy      : {self.accuracy*100:.2f}%",
            f"  Precision     : {self.precision*100:.2f}%",
            f"  Recall        : {self.recall*100:.2f}%",
            f"  F1 Score      : {self.f1*100:.2f}%",
            f"  Avg Sim (pos) : {self.avg_sim_pos:.4f}",
            f"  Avg Sim (neg) : {self.avg_sim_neg:.4f}",
            f"  Confusion     : TN={self.confusion[0][0]}  FP={self.confusion[0][1]}",
            f"                  FN={self.confusion[1][0]}  TP={self.confusion[1][1]}",
            sep,
        ]
        return "\n".join(lines)


class ModelEvaluator:
    """
    Splits the processed dataset into train/test and computes full metrics.

    Usage
    -----
    >>> ev = ModelEvaluator(test_size=0.2)
    >>> report = ev.evaluate(vectorizer, cleaned_rows)
    >>> print(report.pretty())
    """

    def __init__(self, test_size: float = 0.20, random_seed: int = 42):
        self.test_size   = test_size
        self.random_seed = random_seed

    # ── Helpers ────────────────────────────────────────────────────────────────

    @staticmethod
    def _cosine(vectorizer: TfidfVectorizer, t1: str, t2: str) -> float:
        mat = vectorizer.transform([t1, t2])
        return float(cosine_similarity(mat[0:1], mat[1:2])[0][0])

    @staticmethod
    def _tune_threshold(
        vectorizer: TfidfVectorizer,
        rows: list,
        candidates: Tuple[float, ...] = (0.10, 0.13, 0.15, 0.18, 0.20, 0.25),
    ) -> float:
        """Pick threshold that maximises F1 on the training set."""
        best_f1, best_t = -1.0, candidates[0]
        scores = [
            ModelEvaluator._cosine(vectorizer, r["clean_text1"], r["clean_text2"])
            for r in rows
        ]
        labels = [r["label"] for r in rows]
        for t in candidates:
            preds = [1 if s >= t else 0 for s in scores]
            f = f1_score(labels, preds, zero_division=0)
            if f > best_f1:
                best_f1, best_t = f, t
        logger.debug("Best threshold on train: %.4f  (F1=%.4f)", best_t, best_f1)
        return best_t

    # ── Main ──────────────────────────────────────────────────────────────────

    def evaluate(self, vectorizer: TfidfVectorizer, cleaned: list) -> EvalReport:
        """
        Parameters
        ----------
        vectorizer : fitted TfidfVectorizer
        cleaned    : list of dicts with keys clean_text1, clean_text2, label

        Returns
        -------
        EvalReport
        """
        # Stratified split — keep class ratio
        rng = random.Random(self.random_seed)
        pos = [r for r in cleaned if r["label"] == 1]
        neg = [r for r in cleaned if r["label"] == 0]
        rng.shuffle(pos); rng.shuffle(neg)

        def split(lst):
            n_test = max(1, int(len(lst) * self.test_size))
            return lst[n_test:], lst[:n_test]      # train, test

        train_pos, test_pos = split(pos)
        train_neg, test_neg = split(neg)
        train = train_pos + train_neg
        test  = test_pos  + test_neg
        rng.shuffle(train); rng.shuffle(test)

        logger.info(
            "Split — train: %d (pos=%d neg=%d)  test: %d (pos=%d neg=%d)",
            len(train), len(train_pos), len(train_neg),
            len(test),  len(test_pos),  len(test_neg),
        )

        # Tune threshold on training set
        threshold = self._tune_threshold(vectorizer, train[:500])   # sample for speed

        # Score test set
        y_true, y_pred, sim_list = [], [], []
        for row in test:
            sim = self._cosine(vectorizer, row["clean_text1"], row["clean_text2"])
            sim_list.append(sim)
            y_true.append(row["label"])
            y_pred.append(1 if sim >= threshold else 0)

        cm = confusion_matrix(y_true, y_pred, labels=[0, 1]).tolist()

        # Sim stats
        pos_sims = [s for s, l in zip(sim_list, y_true) if l == 1]
        neg_sims = [s for s, l in zip(sim_list, y_true) if l == 0]

        report = EvalReport(
            total_pairs    = len(cleaned),
            train_pairs    = len(train),
            test_pairs     = len(test),
            threshold      = round(threshold, 4),
            accuracy       = round(accuracy_score(y_true, y_pred), 4),
            precision      = round(precision_score(y_true, y_pred, zero_division=0), 4),
            recall         = round(recall_score(y_true, y_pred, zero_division=0), 4),
            f1             = round(f1_score(y_true, y_pred, zero_division=0), 4),
            confusion      = cm,
            avg_sim_pos    = round(float(np.mean(pos_sims)), 4) if pos_sims else 0.0,
            avg_sim_neg    = round(float(np.mean(neg_sims)), 4) if neg_sims else 0.0,
            positive_pairs = len(pos),
            negative_pairs = len(neg),
        )
        logger.info(report.pretty())
        return report
