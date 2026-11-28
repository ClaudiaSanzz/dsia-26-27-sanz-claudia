
"""Cliente HTTP para la API de recomendaciones de COFI."""

import os

import requests


class ClienteAPI:
    """Envía las preferencias del usuario a nuestra API."""

    def __init__(self):
        self.url = os.getenv(
            "API_URL",
            "http://127.0.0.1:8000"
        ).rstrip("/")

    def recomendar(self, modo, preferencias=None, texto=""):
        """Obtiene recomendaciones de cafeterías."""

        if texto.strip():
            datos = {
                "mode": "libre",
                "text": texto.strip()
            }
        else:
            datos = {
                "mode": modo,
                "preferences": preferencias or []
            }

        try:
            respuesta = requests.post(
                f"{self.url}/recommend",
                json=datos,
                timeout=60
            )

            resultado = respuesta.json()

            if not respuesta.ok:
                return {
                    "error": resultado.get(
                        "error",
                        "No se pudieron obtener recomendaciones."
                    )
                }

            return resultado

        except requests.RequestException:
            return {
                "error": (
                    "No se puede conectar con la API. "
                    "Comprueba que Flask está encendido."
                )
            }

        except ValueError:
            return {
                "error": "La API no ha devuelto un JSON válido."
            }
