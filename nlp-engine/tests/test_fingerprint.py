from app.services.fingerprint_service import generate_hash, generate_fingerprints

def test_generate_hash():
    text = "test string"
    hashed = generate_hash(text)
    assert len(hashed) == 64 # SHA-256 hex length
    assert isinstance(hashed, str)

def test_generate_fingerprints():
    ngrams = ["quick brown fox", "brown fox jumps"]
    fingerprints = generate_fingerprints(ngrams)
    assert len(fingerprints) == 2
    assert isinstance(fingerprints, set)
