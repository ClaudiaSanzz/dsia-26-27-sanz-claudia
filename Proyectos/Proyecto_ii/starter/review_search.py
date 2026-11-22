import joblib
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity
from starter.predict import SentimentPredictor


class ReviewSearch:

    def __init__(self, reviews):
        # Cargamos el vectorizador entrenado
        self.reviews = reviews.copy()
        self.vectorizer = joblib.load("models/vectorizer.joblib")

        # Convertimos las reseñas en vectores
        texts = self.reviews["texto_review"].fillna("")
        self.vectors = self.vectorizer.transform(texts)

    def search(self, query, top_n=10):
        # Transformamos la búsqueda del usuario
        query_vector = self.vectorizer.transform([query])

        # Calculamos la similitud con las reseñas
        similarities = cosine_similarity(
            query_vector, self.vectors
        ).flatten()

        # Ordenamos las reseñas
        results = self.reviews.copy()
        results["similarity"] = similarities

        results = results.sort_values(
            "similarity", ascending=False
        )

        return results.head(top_n)

    def search_cafes(self, query, top_n=10):
        # Buscamos reseñas relacionadas
        results = self.search(query, top_n=100)

        # Conservamos una reseña por cafetería
        results = results.drop_duplicates(subset=["itemId"])

        return results.head(top_n)

    def search_positive_cafes(self, query, top_n=10):
        # Buscamos reseñas relacionadas
        results = self.search(query, top_n=200)

        # Comprobamos si hay coincidencias
        results = results[results["similarity"] > 0]

        if results.empty:
            return results

        # Predecimos el sentimiento
        predictor = SentimentPredictor()
        results = predictor.predict_reviews(results)

        # Conservamos las reseñas positivas
        results = results[
            results["sentimiento_predicho"] == "positivo"
        ]

        # Una reseña por cafetería
        results = results.drop_duplicates(subset=["itemId"])

        return results.head(top_n)

    def rank_cafes(self, query, top_n=10):
        # Buscamos en todas las reseñas
        results = self.search(query, top_n=len(self.reviews))

        # Conservamos las reseñas relacionadas
        results = results[results["similarity"] > 0]

        # Evitamos predecir con un DataFrame vacío
        if results.empty:
            return pd.DataFrame()

        # Predecimos el sentimiento
        predictor = SentimentPredictor()
        results = predictor.predict_reviews(results)

        # Conservamos las reseñas positivas
        results = results[
            results["sentimiento_predicho"] == "positivo"
        ].copy()

        if results.empty:
            return pd.DataFrame()

        # Contamos las reseñas totales por cafetería
        total_reviews = self.reviews.groupby("itemId").size()

        # Seleccionamos las 3 mejores reseñas de cada cafetería
        results = results.sort_values(
            "similarity", ascending=False
        )
        results = results.groupby("itemId").head(3)

        # Agrupamos por cafetería
        ranking = results.groupby("itemId").agg(
            name=("name", "first"),
            relevant_reviews=("reviewId", "count"),
            average_similarity=("similarity", "mean"),
            best_similarity=("similarity", "max"),
            example_review=("texto_review", "first"),
            example_review_id=("reviewId", "first"),
            example_review_url=("url_review", "first")
        ).reset_index()


        # Añadimos las reseñas totales
        ranking["total_reviews"] = ranking["itemId"].map(
            total_reviews
        )

        # Exigimos un mínimo de 5 reseñas totales
        ranking = ranking[
            ranking["total_reviews"] >= 5
        ].copy()

        if ranking.empty:
            return ranking

        # Suavizamos la puntuación cuando hay pocas evidencias
        global_mean = results["similarity"].mean()
        k = 3

        ranking["score"] = (
            ranking["relevant_reviews"] * ranking["average_similarity"]
            + k * global_mean
        ) / (ranking["relevant_reviews"] + k)

        # Ordenamos las cafeterías
        ranking = ranking.sort_values(
            "score", ascending=False
        )

        return ranking.head(top_n)
