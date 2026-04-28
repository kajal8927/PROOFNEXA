from app.services.similarity_service import (
    calculate_jaccard_similarity,
    calculate_cosine_similarity,
    determine_risk_level,
    calculate_overall_similarity
)

def test_jaccard_similarity():
    set_a = {"a", "b", "c"}
    set_b = {"b", "c", "d"}
    score = calculate_jaccard_similarity(set_a, set_b)
    # Intersection: 2, Union: 4 -> 2/4 = 50%
    assert score == 50.0

def test_cosine_similarity():
    text1 = "The quick brown fox"
    text2 = "The fast brown fox"
    score = calculate_cosine_similarity(text1, text2)
    assert score > 0.0
    assert score <= 100.0

def test_determine_risk_level():
    assert determine_risk_level(10.0) == "Low"
    assert determine_risk_level(45.0) == "Medium"
    assert determine_risk_level(75.0) == "High"
    assert determine_risk_level(90.0) == "Critical"

def test_calculate_overall_similarity():
    text1 = "This is a test document for plagiarism detection."
    text2 = "This is a test document for plagiarism detection."
    score = calculate_overall_similarity(text1, text2)
    assert score == 100.0
