from fastapi import HTTPException
from app.services.database_service import get_previous_submissions
from app.services.similarity_service import (
    get_text_fingerprints,
    calculate_jaccard_similarity,
    find_matching_sentences
)


def analyze_text_controller(input_text: str):
    try:
        input_fingerprints = get_text_fingerprints(input_text)

        if not input_fingerprints:
            raise HTTPException(
                status_code=400,
                detail="Text is too short for analysis"
            )

        previous_submissions = get_previous_submissions()

        overall_similarity = 0
        all_matches = []

        for submission in previous_submissions:
            source_text = submission.get("originalText", "")
            source_file = submission.get("fileName", "Unknown File")
            
            # Optimization: Use precomputed fingerprints if available in DB
            source_fingerprints_list = submission.get("fingerprints")
            if source_fingerprints_list:
                source_fingerprints = set(source_fingerprints_list)
            else:
                source_fingerprints = get_text_fingerprints(source_text)

            score = calculate_jaccard_similarity(
                input_fingerprints,
                source_fingerprints
            )

            if score > overall_similarity:
                overall_similarity = score

            sentence_matches = find_matching_sentences(input_text, source_text)

            for match in sentence_matches:
                all_matches.append({
                    "sourceFile": source_file,
                    "matchedText": match["matchedText"],
                    "sourceText": match["sourceText"],
                    "similarity": match["similarity"]
                })

        all_matches = sorted(
            all_matches,
            key=lambda item: item["similarity"],
            reverse=True
        )[:10]

        return {
            "success": True,
            "similarity": overall_similarity,
            "matches": all_matches
        }

    except HTTPException:
        raise

    except Exception as error:
        print(f"Error in analyze_text_controller: {str(error)}")
        raise HTTPException(
            status_code=500,
            detail="Internal NLP engine error"
        )
