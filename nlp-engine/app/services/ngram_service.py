def generate_ngrams(tokens: list, n: int = 3) -> list:
    """Generates word n-grams from a list of tokens."""
    if not tokens or len(tokens) < n:
        return []

    ngrams = []
    for i in range(len(tokens) - n + 1):
        gram = " ".join(tokens[i:i + n])
        ngrams.append(gram)

    return ngrams

def generate_sentence_ngrams(sentences: list, n: int = 2) -> list:
    """Generates sentence n-grams (phrases of sentences) for broader matching."""
    if not sentences or len(sentences) < n:
        return []
        
    ngrams = []
    for i in range(len(sentences) - n + 1):
        gram = " ".join(sentences[i:i + n])
        ngrams.append(gram)
        
    return ngrams
