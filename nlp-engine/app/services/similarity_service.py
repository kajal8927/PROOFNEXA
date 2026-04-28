import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.services.preprocessing_service import tokenize_text, split_into_sentences
from app.services.ngram_service import generate_ngrams
from app.services.fingerprint_service import generate_fingerprints
from app.utils.logging import logger

def calculate_jaccard_similarity(set_a: set, set_b: set) -> float:
    """Calculates Jaccard similarity between two sets."""
    if not set_a or not set_b:
        return 0.0

    intersection = set_a.intersection(set_b)
    union = set_a.union(set_b)

    return round((len(intersection) / len(union)) * 100, 2)

def calculate_cosine_similarity(text1: str, text2: str) -> float:
    """Calculates TF-IDF Cosine Similarity between two texts."""
    try:
        if not text1.strip() or not text2.strip():
            return 0.0
            
        vectorizer = TfidfVectorizer(tokenizer=tokenize_text, token_pattern=None, lowercase=True)
        tfidf = vectorizer.fit_transform([text1, text2])
        
        sim = cosine_similarity(tfidf[0:1], tfidf[1:2])
        return round(float(sim[0][0]) * 100, 2)
    except Exception as e:
        logger.error(f"Error calculating cosine similarity: {str(e)}")
        return 0.0

def get_text_fingerprints(text: str, n: int = 3) -> set:
    """Generates fingerprints for a given text."""
    tokens = tokenize_text(text)
    ngrams = generate_ngrams(tokens, n)
    return generate_fingerprints(ngrams)

def determine_risk_level(score: float) -> str:
    """
    Determines risk level based on similarity score.
    0–30 Low, 31–60 Medium, 61–80 High, 81–100 Critical
    """
    if score <= 30:
        return "Low"
    elif score <= 60:
        return "Medium"
    elif score <= 80:
        return "High"
    else:
        return "Critical"

def calculate_overall_similarity(text1: str, text2: str) -> float:
    """Combines fingerprint overlap and Cosine similarity for a robust score."""
    fp1 = get_text_fingerprints(text1)
    fp2 = get_text_fingerprints(text2)
    
    jaccard_score = calculate_jaccard_similarity(fp1, fp2)
    cosine_score = calculate_cosine_similarity(text1, text2)
    
    # Weighted average: Fingerprints (60%), TF-IDF Cosine (40%)
    # This gives weight to exact phrase matches while capturing semantic similarity
    final_score = (jaccard_score * 0.6) + (cosine_score * 0.4)
    return round(final_score, 2)

def find_matching_sentences(input_text: str, source_text: str, threshold: float = 30.0) -> list:
    """Finds matching sentences between input and source text."""
    input_sentences = split_into_sentences(input_text)
    source_sentences = split_into_sentences(source_text)

    matches = []

    for input_sentence in input_sentences:
        input_fp = get_text_fingerprints(input_sentence, n=2) # Smaller n-gram for sentences
        
        for source_sentence in source_sentences:
            source_fp = get_text_fingerprints(source_sentence, n=2)
            
            jaccard_score = calculate_jaccard_similarity(input_fp, source_fp)
            
            if jaccard_score >= threshold:
                matches.append({
                    "matchedText": source_sentence,
                    "inputText": input_sentence,
                    "similarity": jaccard_score,
                    "matchType": "ngram"
                })
                
    return matches
