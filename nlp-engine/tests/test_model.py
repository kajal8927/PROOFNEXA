"""
tests/test_model.py
===================
Full test suite for the trained NLP model.

Run:  python tests/test_model.py
"""

import sys, json, joblib, csv
from pathlib import Path

BASE = Path(__file__).parent.parent
sys.path.insert(0, str(BASE))

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

GREEN = "\033[92m"; RED = "\033[91m"; RESET = "\033[0m"; BOLD = "\033[1m"
_p = _f = 0

def check(desc, cond):
    global _p, _f
    print(f"  [{''+GREEN+'PASS'+RESET if cond else RED+'FAIL'+RESET}] {desc}")
    if cond: _p += 1
    else: _f += 1


def test_files():
    print(f"\n{BOLD}1. Artefact files{RESET}")
    check("tfidf_vectorizer.pkl exists",    (BASE/"models"/"tfidf_vectorizer.pkl").exists())
    check("model_metadata.json exists",     (BASE/"models"/"model_metadata.json").exists())
    check("10k dataset exists",             (BASE/"data"/"raw"/"plagiarism_10k_dataset.csv").exists())
    check("processed_pairs.csv exists",     (BASE/"data"/"processed"/"processed_pairs.csv").exists())


def test_vectorizer():
    print(f"\n{BOLD}2. Vectorizer{RESET}")
    vec = joblib.load(BASE/"models"/"tfidf_vectorizer.pkl")
    check("Loads without error",    vec is not None)
    check("Vocab >= 5000 terms",    len(vec.vocabulary_) >= 5000)
    check("ngram_range == (1,3)",   vec.ngram_range == (1, 3))
    check("sublinear_tf == True",   vec.sublinear_tf)
    return vec


def test_metadata():
    print(f"\n{BOLD}3. Metadata{RESET}")
    with open(BASE/"models"/"model_metadata.json") as f:
        m = json.load(f)
    check("Has trained_at",           "trained_at" in m)
    check("Has vocabulary_size",      m.get("vocabulary_size", 0) >= 5000)
    check("Has similarity_threshold", "similarity_threshold" in m)
    acc = m.get("evaluation", {}).get("accuracy", 0)
    check(f"Training accuracy >= 90% (got {acc*100:.1f}%)", acc >= 0.90)


def test_similarity_pairs(vec):
    print(f"\n{BOLD}4. Positive pairs (should be similar){RESET}")
    from nlp_core.preprocessor import TextPreprocessor
    pre = TextPreprocessor()
    pairs = [
        ("Albert Einstein developed the theory of relativity.",
         "The theory of relativity was formulated by Albert Einstein."),
        ("The human genome contains approximately 3 billion base pairs.",
         "About 3 billion base pairs make up the complete human genome."),
        ("Machine learning enables computers to learn from data.",
         "Computers can learn from data using machine learning techniques."),
    ]
    for t1, t2 in pairs:
        c1, c2 = pre.clean_for_tfidf(t1), pre.clean_for_tfidf(t2)
        mat = vec.transform([c1, c2])
        sim = float(cosine_similarity(mat[0:1], mat[1:2])[0][0]) * 100
        check(f"Paraphrase sim >= 30%  [{sim:.1f}%]  {t1[:50]}...", sim >= 30)

    print(f"\n{BOLD}5. Negative pairs (should be unrelated){RESET}")
    neg_pairs = [
        ("DNA carries the genetic information of living organisms.",
         "The football team won the championship after a dramatic shootout."),
        ("Blockchain provides a decentralised ledger for transactions.",
         "Fresh pasta is made from flour and eggs kneaded into smooth dough."),
    ]
    for t1, t2 in neg_pairs:
        c1, c2 = pre.clean_for_tfidf(t1), pre.clean_for_tfidf(t2)
        mat = vec.transform([c1, c2])
        sim = float(cosine_similarity(mat[0:1], mat[1:2])[0][0]) * 100
        check(f"Unrelated sim < 5%  [{sim:.1f}%]  {t1[:50]}...", sim < 5)


def test_check_similarity():
    print(f"\n{BOLD}6. check_similarity() function{RESET}")
    from nlp_core.predictor import check_similarity
    r = check_similarity(
        "Machine learning is a subset of artificial intelligence.",
        "Deep learning is a branch of machine learning and AI."
    )
    check("Returns dict",                    isinstance(r, dict))
    check("Has similarity_score",            "similarity_score" in r)
    check("Has similarity_percentage",       "similarity_percentage" in r)
    check("Has plagiarism_label",            "plagiarism_label" in r)
    check("Has risk_level",                  "risk_level" in r)
    check("Has is_plagiarised",              "is_plagiarised" in r)
    check("score in [0,1]",                  0.0 <= r["similarity_score"] <= 1.0)
    check("percentage in [0,100]",           0.0 <= r["similarity_percentage"] <= 100.0)
    check("label is 0 or 1",                 r["plagiarism_label"] in (0, 1))
    check("risk_level is valid",             r["risk_level"] in ("Low","Medium","High","Critical"))
    print(f"     Result: {r}")

    r2 = check_similarity("The cat sat on the mat.", "Stock prices fell sharply today.")
    check("Unrelated texts NOT plagiarised", not r2["is_plagiarised"])


def test_service():
    print(f"\n{BOLD}7. similarity_service integration{RESET}")
    from app.services.similarity_service import (
        calculate_overall_similarity, calculate_cosine_similarity,
        calculate_jaccard_similarity, determine_risk_level,
        get_text_fingerprints, find_matching_sentences,
    )
    score = calculate_overall_similarity(
        "The solar system has eight planets orbiting the Sun.",
        "Eight planets travel around the Sun in our solar system."
    )
    check("calculate_overall_similarity returns float", isinstance(score, float))
    check(f"Overall similarity > 10 [{score}]", score > 10)
    check("Risk Low  for 20",      determine_risk_level(20)  == "Low")
    check("Risk Medium for 50",    determine_risk_level(50)  == "Medium")
    check("Risk High   for 70",    determine_risk_level(70)  == "High")
    check("Risk Critical for 90",  determine_risk_level(90)  == "Critical")
    fp = get_text_fingerprints("machine learning artificial intelligence")
    check("Fingerprints is a set", isinstance(fp, set))
    check("Fingerprints non-empty", len(fp) > 0)
    j = calculate_jaccard_similarity({1,2,3}, {2,3,4})
    check("Jaccard({1,2,3},{2,3,4}) == 50.0", j == 50.0)


def main():
    print(f"\n{BOLD}{'='*52}\n  PROOFNEXA NLP Engine — Test Suite\n{'='*52}{RESET}")
    test_files()
    vec = test_vectorizer()
    test_metadata()
    test_similarity_pairs(vec)
    test_check_similarity()
    test_service()
    total = _p + _f
    col   = GREEN if _f == 0 else RED
    print(f"\n{BOLD}{'='*52}")
    print(f"  {_p}/{total} passed  {col}{'ALL PASSED' if _f==0 else str(_f)+' FAILED'}{RESET}")
    print(f"{'='*52}{RESET}\n")
    return 0 if _f == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
