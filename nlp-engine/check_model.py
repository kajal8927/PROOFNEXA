import joblib

model = joblib.load("nlp-engine/models/tfidf_vectorizer.pkl")

print("Model type:", type(model))
print("Total words:", len(model.vocabulary_))
print("Top words:", list(model.vocabulary_.keys())[:20])