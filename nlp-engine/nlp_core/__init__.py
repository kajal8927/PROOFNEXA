# nlp_core — standalone NLP training and inference package
# All public symbols re-exported for convenience.

from nlp_core.preprocessor import TextPreprocessor
from nlp_core.trainer     import ModelTrainer
from nlp_core.evaluator   import ModelEvaluator
from nlp_core.predictor   import SimilarityPredictor, check_similarity

__all__ = [
    "TextPreprocessor",
    "ModelTrainer",
    "ModelEvaluator",
    "SimilarityPredictor",
    "check_similarity",
]
