"""
PROOFNEXA NLP Engine - Model Training Script
=============================================
Trains and saves a TF-IDF based plagiarism detection model.
Run this script once to build the model artifacts:
    python train_model.py

Outputs:
    models/tfidf_vectorizer.pkl   - Trained TF-IDF vectorizer
    models/model_metadata.json    - Training stats and metadata
    data/processed/processed_pairs.csv - Cleaned dataset
"""

import os
import re
import sys
import json
import string
import logging
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("train_model")

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent
DATA_RAW   = BASE_DIR / "data" / "raw" / "plagiarism_dataset.csv"
DATA_PROC  = BASE_DIR / "data" / "processed" / "processed_pairs.csv"
MODEL_DIR  = BASE_DIR / "models"
VECTORIZER = MODEL_DIR / "tfidf_vectorizer.pkl"
METADATA   = MODEL_DIR / "model_metadata.json"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
(BASE_DIR / "data" / "processed").mkdir(parents=True, exist_ok=True)


# ── Preprocessing ──────────────────────────────────────────────────────────────
# Common English stopwords (no NLTK dependency)
STOPWORDS = {
    "a","an","the","and","or","but","in","on","at","to","for","of","with",
    "by","from","is","are","was","were","be","been","being","have","has","had",
    "do","does","did","will","would","could","should","may","might","shall",
    "that","this","these","those","it","its","they","them","their","we","our",
    "i","me","my","you","your","he","him","his","she","her","as","if","so",
    "not","no","nor","yet","just","than","then","also","into","about","over",
    "up","out","which","who","what","when","where","how","all","each","any",
    "both","few","more","most","other","some","such","only","own","same",
    "too","very","can","us","after","before","through","between","during",
}


def preprocess(text: str) -> str:
    """Lowercase, remove punctuation, strip stopwords."""
    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = [t for t in text.split() if t not in STOPWORDS and len(t) > 1]
    return " ".join(tokens)


def load_and_clean_dataset(path: Path) -> pd.DataFrame:
    logger.info(f"Loading dataset from {path}")
    df = pd.read_csv(path)

    # Strip stray quotes from text columns
    for col in ["text1", "text2"]:
        df[col] = df[col].astype(str).str.strip('"').str.strip("'")

    df["clean_text1"] = df["text1"].apply(preprocess)
    df["clean_text2"] = df["text2"].apply(preprocess)

    # Drop empty rows after cleaning
    df = df[
        (df["clean_text1"].str.strip() != "") &
        (df["clean_text2"].str.strip() != "")
    ].reset_index(drop=True)

    logger.info(f"Dataset loaded: {len(df)} pairs "
                f"({df['label'].sum()} positive, {(df['label']==0).sum()} negative)")
    return df


def train_and_save_vectorizer(df: pd.DataFrame) -> TfidfVectorizer:
    """Fit TF-IDF on ALL text in the corpus (both columns)."""
    logger.info("Training TF-IDF vectorizer …")

    corpus = pd.concat([df["clean_text1"], df["clean_text2"]]).tolist()

    vectorizer = TfidfVectorizer(
        analyzer="word",
        ngram_range=(1, 3),         # unigrams + bigrams + trigrams
        min_df=1,
        max_df=0.95,
        sublinear_tf=True,          # log-normalise term frequencies
        max_features=50_000,
    )
    vectorizer.fit(corpus)

    joblib.dump(vectorizer, VECTORIZER)
    logger.info(f"Vectorizer saved → {VECTORIZER}  "
                f"(vocab size: {len(vectorizer.vocabulary_)})")
    return vectorizer


def validate_model(vectorizer: TfidfVectorizer, df: pd.DataFrame) -> dict:
    """Quick accuracy check on labelled pairs."""
    logger.info("Validating model on dataset …")

    correct = 0
    scores  = []
    for _, row in df.iterrows():
        vec = vectorizer.transform([row["clean_text1"], row["clean_text2"]])
        sim = float(cosine_similarity(vec[0:1], vec[1:2])[0][0])
        scores.append(sim)

        predicted = 1 if sim >= 0.15 else 0
        if predicted == int(row["label"]):
            correct += 1

    accuracy = correct / len(df)
    avg_pos  = float(np.mean([s for s, l in zip(scores, df["label"]) if l == 1]))
    avg_neg  = float(np.mean([s for s, l in zip(scores, df["label"]) if l == 0]))

    logger.info(f"Accuracy: {accuracy:.2%}  |  "
                f"avg sim (positive): {avg_pos:.4f}  |  "
                f"avg sim (negative): {avg_neg:.4f}")
    return {"accuracy": round(accuracy, 4), "avg_pos_sim": round(avg_pos, 4),
            "avg_neg_sim": round(avg_neg, 4)}


def save_metadata(stats: dict, vectorizer: TfidfVectorizer, df: pd.DataFrame):
    meta = {
        "trained_at":      datetime.utcnow().isoformat() + "Z",
        "dataset_size":    len(df),
        "positive_pairs":  int(df["label"].sum()),
        "negative_pairs":  int((df["label"] == 0).sum()),
        "vocab_size":      len(vectorizer.vocabulary_),
        "ngram_range":     [1, 3],
        "max_features":    50000,
        "vectorizer_path": str(VECTORIZER),
        "validation":      stats,
    }
    with open(METADATA, "w") as f:
        json.dump(meta, f, indent=2)
    logger.info(f"Metadata saved → {METADATA}")


def main():
    if not DATA_RAW.exists():
        logger.error(f"Dataset not found: {DATA_RAW}")
        sys.exit(1)

    # 1. Load & clean
    df = load_and_clean_dataset(DATA_RAW)

    # 2. Save processed data
    df.to_csv(DATA_PROC, index=False)
    logger.info(f"Processed dataset saved → {DATA_PROC}")

    # 3. Train
    vectorizer = train_and_save_vectorizer(df)

    # 4. Validate
    stats = validate_model(vectorizer, df)

    # 5. Metadata
    save_metadata(stats, vectorizer, df)

    logger.info("✅  Training complete.")
    return vectorizer


if __name__ == "__main__":
    main()
