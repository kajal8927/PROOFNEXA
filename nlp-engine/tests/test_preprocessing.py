from app.services.preprocessing_service import clean_text, tokenize_text, split_into_sentences

def test_clean_text():
    raw_text = "Hello,   World! This is a test... "
    cleaned = clean_text(raw_text)
    assert cleaned == "hello world this is a test"

def test_tokenize_text():
    raw_text = "The quick brown fox jumps over the lazy dog."
    tokens = tokenize_text(raw_text)
    assert len(tokens) > 0
    assert "quick" in tokens
    assert "the" not in tokens # Stopword removed

def test_split_into_sentences():
    raw_text = "This is sentence one. This is sentence two! And three?"
    sentences = split_into_sentences(raw_text)
    assert len(sentences) >= 2
    assert sentences[0] == "This is sentence one."
