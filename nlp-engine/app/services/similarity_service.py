from app.services.preprocessing_service import tokenize_text, split_into_sentences
from app.services.ngram_service import generate_ngrams
from app.services.fingerprint_service import generate_fingerprints


def calculate_jaccard_similarity(set_a: set, set_b: set) -> float:
    if not set_a or not set_b:
        return 0.0

    intersection = set_a.intersection(set_b)
    union = set_a.union(set_b)

    return round((len(intersection) / len(union)) * 100, 2)


def calculate_levenshtein_distance(str1: str, str2: str) -> float:
    """
    Calculates the Levenshtein distance between two strings 
    and returns a similarity percentage.
    """
    if not str1 or not str2:
        return 0.0
    
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

    max_len = max(m, n)
    distance = dp[m][n]
    
    similarity = ((max_len - distance) / max_len) * 100
    return round(similarity, 2)


def get_text_fingerprints(text: str) -> set:
    tokens = tokenize_text(text)
    ngrams = generate_ngrams(tokens, 3)
    fingerprints = generate_fingerprints(ngrams)

    return fingerprints


def find_matching_sentences(input_text: str, source_text: str) -> list:
    input_sentences = split_into_sentences(input_text)
    source_sentences = split_into_sentences(source_text)

    matches = []

    for input_sentence in input_sentences:
        input_fp = get_text_fingerprints(input_sentence)

        for source_sentence in source_sentences:
            source_fp = get_text_fingerprints(source_sentence)

            # 1. Check Jaccard (Fast)
            jaccard_score = calculate_jaccard_similarity(input_fp, source_fp)

            # 2. Check Levenshtein (Accurate for paraphrasing)
            levenshtein_score = calculate_levenshtein_distance(
                input_sentence.lower(), 
                source_sentence.lower()
            )

            # Use maximum of both scores for final match
            final_score = max(jaccard_score, levenshtein_score)

            if final_score >= 40:  # Threshold reduced slightly for better recall
                matches.append({
                    "matchedText": input_sentence,
                    "sourceText": source_sentence,
                    "similarity": final_score
                })

    return matches
