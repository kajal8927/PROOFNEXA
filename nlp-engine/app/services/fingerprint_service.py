import hashlib


def generate_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def generate_fingerprints(ngrams: list) -> set:
    return set(generate_hash(gram) for gram in ngrams)
