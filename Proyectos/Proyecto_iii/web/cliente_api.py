
"""Cliente HTTP para comunicarse con la API de COFI."""

import os

import requests


class ClienteAPI:
    """Gestiona las peticiones del dashboard a Flask."""

    def __init__(self):
        self.url = os.getenv(
            "API_URL",
            "http://127.0.0.1:8000"
        ).rstrip("/")

    def pedir(self, metodo, ruta, datos=None):
        """Realiza una petición y devuelve el JSON."""

        try:
            respuesta = requests.request(
                metodo,
                self.url + ruta,
                json=datos,
                timeout=120 if ruta == "/recommend" else 30
            )

            respuesta.raise_for_status()
            return respuesta.json(), None

        except requests.exceptions.HTTPError:
            try:
                error = respuesta.json().get(
                    "error",
                    "Error al procesar la solicitud."
                )
            except ValueError:
                error = "Error al procesar la solicitud."

            return None, str(error)

        except requests.exceptions.Timeout:
            return None, "La API ha tardado demasiado en responder."

        except requests.exceptions.ConnectionError:
            return None, "No se puede conectar con la API Flask."

        except requests.exceptions.RequestException:
            return None, "Ha ocurrido un error de comunicación."

        except ValueError:
            return None, "La respuesta de la API no es válida."

    def recomendar(self, modo, preferencias):
        """Solicita recomendaciones de cafeterías."""

        datos = {
            "mode": modo,
            "preferences": preferencias
        }

        return self.pedir(
            "POST",
            "/recommend",
            datos
        )

    def analizar(self, texto):
        """Analiza una reseña."""

        return self.pedir(
            "POST",
            "/analyze",
            {"text": texto}
        )

    def comprobar_estado(self):
        """Consulta el estado de Flask."""

        return self.pedir("GET", "/health")
