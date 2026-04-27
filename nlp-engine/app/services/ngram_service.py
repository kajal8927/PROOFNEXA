def generate_ngrams(tokens: list, n: int = 3) -> list:
    if len(tokens) < n:
        return []

    ngrams = []

    for i in range(len(tokens) - n + 1):
        gram = " ".join(tokens[i:i + n])
        ngrams.append(gram)

    return ngrams
