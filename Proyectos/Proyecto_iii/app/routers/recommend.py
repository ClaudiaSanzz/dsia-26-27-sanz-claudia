
"""Endpoint para recomendar cafeterías."""

import logging
import time
import uuid

from flask import Blueprint, jsonify, request

from starter.recommender import CafeRecommender


logger = logging.getLogger("cafe_match")


def create_recommend_blueprint(api):
    """Crea el router de recomendaciones."""

    recommend_bp = Blueprint("recommend", __name__)

    @recommend_bp.post("/recommend")
    def recommend():
        request_id = str(uuid.uuid4())

        payload = request.get_json(silent=True)

        if not isinstance(payload, dict):
            return jsonify({
                "error": "Se requiere un JSON válido",
                "request_id": request_id
            }), 400

        mode = payload.get("mode", "libre")
        text = payload.get("text", "")
        preferences = payload.get("preferences", [])

        # Validamos el modo y las preferencias
        if mode == "libre":
            if not isinstance(text, str) or not text.strip():
                return jsonify({
                    "error": "Debes indicar qué cafetería buscas",
                    "request_id": request_id
                }), 400

        else:
            options = CafeRecommender().options

            if (
                mode not in options
                or not isinstance(preferences, list)
                or not preferences
                or any(
                    preference not in options[mode]
                    for preference in preferences
                )
            ):
                return jsonify({
                    "error": "Modo o preferencias no válidas",
                    "request_id": request_id
                }), 400

        start = time.perf_counter()

        try:
            service = api.get_recommendation_service()

            if mode == "libre":
                result = service.recommend_from_text(text)
            else:
                recommendations = service.recommend(
                    mode, preferences
                )

                result = {
                    "recommendations": recommendations,
                    "preferences": preferences
                }

        except (RuntimeError, ConnectionError, TimeoutError, OSError):
            logger.exception(
                "recommend_dependency_error request_id=%s",
                request_id
            )

            return jsonify({
                "error": "Servicio de recomendaciones no disponible",
                "request_id": request_id
            }), 503

        except Exception:
            logger.exception(
                "recommend_error request_id=%s",
                request_id
            )

            return jsonify({
                "error": "Error interno del servidor",
                "request_id": request_id
            }), 500

        latency_ms = round(
            (time.perf_counter() - start) * 1000, 2
        )

        logger.info(
            "recommend_ok request_id=%s latency_ms=%s",
            request_id,
            latency_ms
        )

        return jsonify({
            **result,
            "provider": service.ai.mode,
            "request_id": request_id,
            "latency_ms": latency_ms
        }), 200

    return recommend_bp
