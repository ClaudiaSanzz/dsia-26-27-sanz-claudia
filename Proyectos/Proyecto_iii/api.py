
"""API Flask de COFI."""

import logging

from flask import Flask

from starter.analysis_service import AnalysisService
from starter.recommendation_service import RecommendationService

from app.routers.health import create_health_blueprint
from app.routers.analyze import create_analyze_blueprint
from app.routers.recommend import create_recommend_blueprint


logging.basicConfig(level=logging.INFO)


class CafeMatchAPI:
    """Gestiona los servicios y endpoints de COFI."""

    def __init__(self, service=None):
        self.app = Flask(__name__)

        # Servicios de la aplicación
        self.service = service
        self.recommendation_service = None

        self.register_routes()

    def get_service(self):
        """Carga el servicio de análisis cuando se necesita."""

        if self.service is None:
            self.service = AnalysisService()

        return self.service

    def get_recommendation_service(self):
        """Carga el recomendador cuando se necesita."""

        if self.recommendation_service is None:
            self.recommendation_service = RecommendationService()

        return self.recommendation_service

    def register_routes(self):
        """Registra los tres routers de Flask."""

        self.app.register_blueprint(
            create_health_blueprint(self)
        )

        self.app.register_blueprint(
            create_analyze_blueprint(self)
        )

        self.app.register_blueprint(
            create_recommend_blueprint(self)
        )

    # Métodos compatibles con el código anterior
    def health(self):
        return self.app.view_functions["health.health"]()

    def analyze(self):
        return self.app.view_functions["analyze.analyze"]()

    def recommend(self):
        return self.app.view_functions["recommend.recommend"]()


# Aplicación Flask
cafe_api = CafeMatchAPI()
app = cafe_api.app


def main():
    app.run(
        host="127.0.0.1",
        port=8000,
        debug=False
    )


if __name__ == "__main__":
    main()
