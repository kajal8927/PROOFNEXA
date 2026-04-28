from app.services.ngram_service import generate_ngrams, generate_sentence_ngrams

def test_generate_ngrams():
    tokens = ["quick", "brown", "fox", "jumps"]
    ngrams = generate_ngrams(tokens, n=3)
    assert len(ngrams) == 2
    assert ngrams[0] == "quick brown fox"
    assert ngrams[1] == "brown fox jumps"

def test_generate_ngrams_too_short():
    tokens = ["quick", "brown"]
    ngrams = generate_ngrams(tokens, n=3)
    assert len(ngrams) == 0

def test_generate_sentence_ngrams():
    sentences = ["Sentence one.", "Sentence two.", "Sentence three."]
    ngrams = generate_sentence_ngrams(sentences, n=2)
    assert len(ngrams) == 2
    assert ngrams[0] == "Sentence one. Sentence two."
