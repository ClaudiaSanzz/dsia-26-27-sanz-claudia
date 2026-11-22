import logging
import os

import pandas as pd

from dotenv import load_dotenv

from starter.loader import CafeLoader
from starter.validator import CafeValidator
from starter.predict import SentimentPredictor
from starter.ia_client import AIClient


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)


class CafePipeline:

    def __init__(self, mode="mock"):
        # Configuramos los modelos
        self.mode = mode
        self.loader = CafeLoader()
        self.validator = CafeValidator()
        self.predictor = SentimentPredictor()
        self.ai = AIClient(mode)

    def load_reviews(self):
        # Cargamos y preparamos las reseñas
        reviews = self.loader.load_csv(
            "data/cafeterias_limpias.csv"
        )

        reviews = self.validator.validate_columns(reviews)
        reviews = self.validator.remove_empty_reviews(reviews)

        logging.info("Reseñas disponibles: %s", len(reviews))

        return reviews

    def select_reviews(self, reviews):
        # Seleccionamos una reseña por cafetería
        reviews = reviews.drop_duplicates(
            subset=["itemId"]
        )

        # Limitamos las llamadas reales a NVIDIA
        if self.mode == "real":
            reviews = reviews.head(5)

        return reviews

    def analyze_reviews(self, reviews):
        # Analizamos las reseñas seleccionadas
        results = []

        for _, review in reviews.iterrows():
            text = str(review["texto_review"])

            sentiment = self.predictor.predict(text)
            features = self.ai.analyze_review(text)

            result = {
                "itemId": review["itemId"],
                "reviewId": review["reviewId"],
                "name": review["name"],
                "sentimiento": sentiment
            }

            result.update(features)
            results.append(result)

            if len(results) % 50 == 0:
                logging.info(
                    "Reseñas procesadas: %s",
                    len(results)
                )

        return pd.DataFrame(results)

    def save_results(self, results):
        # Guardamos los resultados
        os.makedirs("outputs", exist_ok=True)

        path = f"outputs/resultados_pipeline_{self.mode}.csv"

        results.to_csv(path, index=False)

        logging.info("Resultados guardados en %s", path)

    def run(self):
        logging.info("Iniciando pipeline de Café Match")
        logging.info("Modo de IA: %s", self.mode)

        reviews = self.load_reviews()
        reviews = self.select_reviews(reviews)

        logging.info(
            "Cafeterías que vamos a procesar: %s",
            len(reviews)
        )

        results = self.analyze_reviews(reviews)
        self.save_results(results)

        logging.info("Pipeline terminado correctamente")
        logging.info("Reseñas procesadas: %s", len(results))

        return results


def main():
    mode = os.getenv("MODO_IA", "mock").lower()

    pipeline = CafePipeline(mode)
    pipeline.run()


if __name__ == "__main__":
    main()
