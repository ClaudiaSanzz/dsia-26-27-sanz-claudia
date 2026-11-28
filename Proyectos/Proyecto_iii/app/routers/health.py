
"""Endpoint para comprobar el estado de COFI."""

from pathlib import Path

from flask import Blueprint, jsonify


def create_health_blueprint(api):
    """Crea el router de salud."""

    health_bp = Blueprint("health", __name__)

    @health_bp.get("/health")
    def health():
        checks = {
            "api": True,
            "data": (
                Path("data/cafeterias_limpias.csv").exists()
                or Path("data/cafeterias_muestra.csv").exists()
            ),
            "model": Path("models/model.joblib").exists(),
            "vectorizer": Path("models/vectorizer.joblib").exists()
        }

        status = "ok" if all(checks.values()) else "degraded"
        code = 200 if status == "ok" else 503

        return jsonify({
            "status": status,
            "checks": checks
        }), code

    return health_bp
