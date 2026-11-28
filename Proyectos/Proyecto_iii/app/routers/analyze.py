
"""Endpoint para analizar reseñas."""

import logging
import time
import uuid

from flask import Blueprint, jsonify, request


logger = logging.getLogger("cafe_match")


def create_analyze_blueprint(api):
    """Crea el router de análisis."""

    analyze_bp = Blueprint("analyze", __name__)

    @analyze_bp.post("/analyze")
    def analyze():
        request_id = str(uuid.uuid4())

        # Validamos el JSON recibido
        payload = request.get_json(silent=True)
        text = payload.get("text") if isinstance(payload, dict) else None

        if not isinstance(text, str) or not text.strip():
            logger.warning(
                "invalid_input request_id=%s",
                request_id
            )

            return jsonify({
                "error": "El campo 'text' es obligatorio y no puede estar vacío",
                "request_id": request_id
            }), 400

        start = time.perf_counter()

        try:
            # Utilizamos el servicio existente
            result = api.get_service().analyze(text.strip())

        except (RuntimeError, ValueError, ConnectionError, TimeoutError):
            logger.exception(
                "dependency_error request_id=%s",
                request_id
            )

            return jsonify({
                "error": "El servicio de análisis no está disponible",
                "request_id": request_id
            }), 503

        except Exception:
            logger.exception(
                "internal_error request_id=%s",
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
            "analyze_ok request_id=%s latency_ms=%s provider=%s",
            request_id,
            latency_ms,
            result["provider"]
        )

        return jsonify({
            **result,
            "request_id": request_id,
            "latency_ms": latency_ms
        }), 200

    return analyze_bp
