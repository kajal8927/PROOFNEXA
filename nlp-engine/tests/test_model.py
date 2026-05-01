"""
tests/test_model.py
===================
Tests for the trained NLP model and similarity detection pipeline.

Run:  python tests/test_model.py
      pytest tests/test_model.py -v
"""

import sys
import os
import re
import json
import string
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

MODEL_DIR       = BASE_DIR / "models"
VECTORIZER_PATH = MODEL_DIR / "tfidf_vectorizer.pkl"
METADATA_PATH   = MODEL_DIR / "model_metadata.json"
DATASET_PATH    = BASE_DIR / "data" / "raw" / "plagiarism_dataset.csv"
PROCESSED_PATH  = BASE_DIR / "data" / "processed" / "processed_pairs.csv"

GREEN = "\033[92m"
RED   = "\033[91m"
RESET = "\033[0m"
BOLD  = "\033[1m"

_pass = 0
_fail = 0


def check(description, condition):
    global _pass, _fail
    status = GREEN + "PASS" + RESET if condition else RED + "FAIL" + RESET
    print("  [" + status + "] " + description)
    if condition:
        _pass += 1
    else:
        _fail += 1


STOPWORDS = {
    "a","an","the","and","or","but","in","on","at","to","for","of","with",
    "by","from","is","are","was","were","be","been","being","have","has",
}


def preprocess(t):
    t = t.lower()
    t = t.translate(str.maketrans("", "", string.punctuation))
    return " ".join(w for w in t.split() if w not in STOPWORDS and len(w) > 1)


def test_files_exist():
    print("\n" + BOLD + "Test 1: Artefacts exist" + RESET)
    check("tfidf_vectorizer.pkl exists",   VECTORIZER_PATH.exists())
    check("model_metadata.json exists",    METADATA_PATH.exists())
    check("Raw dataset CSV exists",        DATASET_PATH.exists())
    check("Processed dataset CSV exists",  PROCESSED_PATH.exists())


def test_vectorizer_loads():
    print("\n" + BOLD + "Test 2: Vectorizer loads" + RESET)
    try:
        vec = joblib.load(VECTORIZER_PATH)
        check("Object loaded",           vec is not None)
        check("Has vocabulary",          len(vec.vocabulary_) > 0)
        check("Vocab >= 500 terms",      len(vec.vocabulary_) >= 500)
        check("ngram_range == (1,3)",    vec.ngram_range == (1, 3))
        return vec
    except Exception as exc:
        check("Loads without error: " + str(exc), False)
        return None


def test_metadata():
    print("\n" + BOLD + "Test 3: Metadata sanity" + RESET)
    try:
        with open(METADATA_PATH) as f:
            meta = json.load(f)
        check("Has trained_at",       "trained_at" in meta)
        check("Has dataset_size",     "dataset_size" in meta)
        check("Has vocab_size",       "vocab_size" in meta)
        check("Dataset >= 100 pairs", meta.get("dataset_size", 0) >= 100)
        acc = meta.get("validation", {}).get("accuracy", 0)
        check("Validation accuracy >= 80% (got " + str(round(acc*100,1)) + "%)", acc >= 0.80)
    except Exception as exc:
        check("Metadata readable: " + str(exc), False)


def test_positive_pairs(vec):
    print("\n" + BOLD + "Test 4: High similarity – paraphrase pairs" + RESET)
    if vec is None:
        check("Skipped (no vectorizer)", False)
        return

    pairs = [
        ("The quick brown fox jumps over the lazy dog",
         "A fast brown fox leaps over the idle dog"),
        ("Albert Einstein developed the theory of relativity",
         "The theory of relativity was formulated by Albert Einstein"),
        ("The human genome contains approximately 3 billion base pairs",
         "About 3 billion base pairs make up the complete human genome"),
        ("Machine learning is a subset of artificial intelligence",
         "Deep learning is a branch of machine learning and AI"),
    ]

    scores = []
    for t1, t2 in pairs:
        tfidf = vec.transform([preprocess(t1), preprocess(t2)])
        sim   = float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]) * 100
        scores.append(sim)
        label = t1[:45] + "..."
        check("Paraphrase sim >= 15% [" + str(round(sim,1)) + "%] " + label, sim >= 15.0)

    avg = np.mean(scores)
    check("Average paraphrase similarity >= 20% [avg " + str(round(avg,1)) + "%]", avg >= 20.0)


def test_negative_pairs(vec):
    print("\n" + BOLD + "Test 5: Low similarity – unrelated pairs" + RESET)
    if vec is None:
        check("Skipped (no vectorizer)", False)
        return

    pairs = [
        ("The quick brown fox jumps over the lazy dog",
         "Stock prices rose sharply after the central bank announcement"),
        ("Machine learning algorithms process large datasets efficiently",
         "The recipe requires flour eggs and butter for the cake"),
        ("Climate change threatens marine ecosystems globally",
         "The latest smartphone has a powerful new processor chip"),
    ]

    for t1, t2 in pairs:
        tfidf = vec.transform([preprocess(t1), preprocess(t2)])
        sim   = float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]) * 100
        label = t1[:45] + "..."
        check("Unrelated sim < 15% [" + str(round(sim,1)) + "%] " + label, sim < 15.0)


def test_service_integration():
    print("\n" + BOLD + "Test 6: Service layer integration" + RESET)
    try:
        from app.services.similarity_service import (
            calculate_overall_similarity,
            calculate_cosine_similarity,
            calculate_jaccard_similarity,
            determine_risk_level,
            get_text_fingerprints,
            find_matching_sentences,
        )

        t1 = "The solar system consists of the Sun and eight planets."
        t2 = "Eight planets along with the Sun make up our solar system."
        score = calculate_overall_similarity(t1, t2)
        check("calculate_overall_similarity returns float", isinstance(score, float))
        check("Paraphrase overall similarity > 5 [" + str(score) + "]", score > 5)

        check("Risk 'Low'      for 20",  determine_risk_level(20)  == "Low")
        check("Risk 'Medium'   for 50",  determine_risk_level(50)  == "Medium")
        check("Risk 'High'     for 70",  determine_risk_level(70)  == "High")
        check("Risk 'Critical' for 90",  determine_risk_level(90)  == "Critical")

        fp = get_text_fingerprints("Machine learning is great for data science")
        check("get_text_fingerprints returns set", isinstance(fp, set))
        check("Fingerprint set non-empty",         len(fp) > 0)

        j = calculate_jaccard_similarity({1, 2, 3}, {2, 3, 4})
        check("Jaccard({1,2,3},{2,3,4}) == 50.0 [" + str(j) + "]", j == 50.0)

        doc1 = "The mitochondria is the powerhouse of the cell. It produces ATP energy."
        doc2 = "Mitochondria serve as energy-producing organelles. They generate ATP."
        matches = find_matching_sentences(doc1, doc2, threshold=10.0)
        check("find_matching_sentences returns list", isinstance(matches, list))

    except ImportError as exc:
        check("Service imports OK: " + str(exc), False)
    except Exception as exc:
        check("Service runs without error: " + str(exc), False)


def main():
    print("\n" + BOLD + "=" * 58)
    print("  PROOFNEXA NLP Engine - Model Test Suite")
    print("=" * 58 + RESET)

    test_files_exist()
    vec = test_vectorizer_loads()
    test_metadata()
    test_positive_pairs(vec)
    test_negative_pairs(vec)
    test_service_integration()

    total = _pass + _fail
    print("\n" + BOLD + "=" * 58)
    result = "ALL TESTS PASSED" if _fail == 0 else str(_fail) + " FAILED"
    color  = GREEN if _fail == 0 else RED
    print("  Results: " + str(_pass) + "/" + str(total) + "  " + color + result + RESET)
    print("=" * 58 + RESET + "\n")
    return 0 if _fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
