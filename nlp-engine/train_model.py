"""
train_model.py
==============
Entry point — trains the TF-IDF model on the 10k dataset and runs
a full evaluation with train/test split.

Usage
-----
    cd nlp-engine
    python train_model.py

Outputs (all inside nlp-engine/):
    models/tfidf_vectorizer.pkl
    models/model_metadata.json
    data/processed/processed_pairs.csv
"""

import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

from nlp_core.trainer   import ModelTrainer
from nlp_core.evaluator import ModelEvaluator


def main():
    # ── 1. Train ──────────────────────────────────────────────────────────────
    trainer    = ModelTrainer(ngram_range=(1, 3), max_features=75_000)
    vectorizer = trainer.run()

    # ── 2. Load processed data for evaluation ─────────────────────────────────
    import csv
    from pathlib import Path
    proc_path = Path(__file__).parent / "data" / "processed" / "processed_pairs.csv"
    cleaned = []
    with open(proc_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cleaned.append({
                "clean_text1": row["clean_text1"],
                "clean_text2": row["clean_text2"],
                "label":       int(row["label"]),
            })

    # ── 3. Evaluate with train/test split ─────────────────────────────────────
    evaluator = ModelEvaluator(test_size=0.20)
    report    = evaluator.evaluate(vectorizer, cleaned)

    # Update metadata with full evaluation report
    import json
    meta_path = Path(__file__).parent / "models" / "model_metadata.json"
    with open(meta_path) as f:
        meta = json.load(f)
    meta["full_evaluation"] = report.to_dict()
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)

    print("\n" + report.pretty())
    print("\n  Model artifacts saved inside  nlp-engine/models/")
    print("  Processed data saved inside   nlp-engine/data/processed/")
    print("\n  Training complete.")


if __name__ == "__main__":
    main()
