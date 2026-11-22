
import joblib
import pandas as pd
from pathlib import Path


class SentimentPredictor:

    def __init__(self):
        # Cargamos el modelo y el vectorizador
        model_path = Path("models/model.joblib")
        vectorizer_path = Path("models/vectorizer.joblib")

        if not model_path.exists():
            raise FileNotFoundError(f"No existe: {model_path}")

        if not vectorizer_path.exists():
            raise FileNotFoundError(f"No existe: {vectorizer_path}")

        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)

    def predict(self, text):
        # Predecimos el sentimiento de una reseña
        text_vector = self.vectorizer.transform([text])
        prediction = self.model.predict(text_vector)

        return prediction[0]

    def predict_reviews(self, reviews):
        # Predecimos varias reseñas a la vez
        vectors = self.vectorizer.transform(reviews["texto_review"])
        predictions = self.model.predict(vectors)

        result = reviews.copy()
        result["sentimiento_predicho"] = predictions

        return result
