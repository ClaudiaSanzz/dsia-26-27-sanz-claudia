import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class AIClient:

    def __init__(self, mode="mock"):
        # Configuramos el modo de IA
        if mode not in ["mock", "real"]:
            raise ValueError("El modo debe ser mock o real")

        self.mode = mode
        self.client = None

        if mode == "real":
            api_key = os.getenv("NVIDIA_API_KEY")

            if not api_key:
                raise ValueError("Falta NVIDIA_API_KEY")

            self.client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=api_key
            )

    def ask_nvidia(self, prompt):
        # Enviamos una petición a NVIDIA
        response = self.client.chat.completions.create(
            model=os.getenv(
                "NVIDIA_MODEL",
                "nvidia/nemotron-3.5-super-vl-120b-a12b"
            ),
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=1,
            top_p=0.95,
            max_tokens=1000,
            stream=False,
            extra_body={
                "chat_template_kwargs": {
                    "enable_thinking": False
                }
            }
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError("NVIDIA no ha devuelto contenido")

        # Limpiamos posibles marcas de Markdown
        content = content.strip()

        if content.startswith("```"):
            content = content.replace("```json", "")
            content = content.replace("```", "").strip()

        return json.loads(content)

    def analyze_review(self, text):
        # Características que queremos analizar
        features = [
            "ruido", "ambiente", "bebidas", "comida",
            "precio", "comodidad", "atencion"
        ]

        # Modo simulado
        if self.mode == "mock":
            return {
                feature: "no_mencionado"
                for feature in features
            }

        # Analizamos la reseña con NVIDIA
        prompt = f"""
        Analiza esta reseña de una cafetería.

        Para cada característica indica:
        positivo, negativo, neutro o no_mencionado.

        Características:
        ruido, ambiente, bebidas, comida,
        precio, comodidad, atencion.

        No inventes información.
        Devuelve únicamente un JSON con esas siete claves.

        Reseña:
        {text}
        """

        result = self.ask_nvidia(prompt)

        # Comprobamos la respuesta
        if not isinstance(result, dict):
            raise ValueError("NVIDIA debe devolver un diccionario")

        for feature in features:
            value = result.get(feature)

            if value == "neutral":
                value = "neutro"

            if value not in [
                "positivo", "negativo", "neutro", "no_mencionado"
            ]:
                raise ValueError(
                    f"Valor no válido para {feature}"
                )

            result[feature] = value

        return {feature: result[feature] for feature in features}

    def interpret_preferences(self, text):
        # Preferencias iniciales de Café Match
        preferences = [
            "quiet", "work", "wifi", "matcha", "brunch"
        ]

        # Modo simulado con palabras clave
        if self.mode == "mock":
            text = text.lower()

            return {
                "quiet": any(word in text for word in [
                    "tranquil", "silencio", "ruido"
                ]),
                "work": any(word in text for word in [
                    "estudi", "trabaj", "portátil",
                    "portatil", "ordenador"
                ]),
                "wifi": "wifi" in text or "wi-fi" in text,
                "matcha": "matcha" in text,
                "brunch": "brunch" in text
            }

        # NVIDIA interpreta la petición del usuario
        prompt = f"""
        Identifica qué busca el usuario en una cafetería.

        Devuelve únicamente un JSON con estas claves:
        quiet, work, wifi, matcha, brunch.

        Significado:
        quiet: busca tranquilidad.
        work: quiere estudiar o trabajar.
        wifi: necesita conexión wifi.
        matcha: quiere tomar matcha.
        brunch: quiere hacer brunch.

        Cada valor debe ser true o false.

        Marca true solamente si el usuario expresa
        esa preferencia de forma afirmativa.
        No inventes preferencias.

        Petición:
        {text}
        """

        result = self.ask_nvidia(prompt)

        # Comprobamos que las preferencias sean válidas
        if not isinstance(result, dict):
            raise ValueError("NVIDIA debe devolver un diccionario")

        for preference in preferences:
            if type(result.get(preference)) is not bool:
                raise ValueError(
                    f"Preferencia no válida: {preference}"
                )

        return {
            preference: result[preference]
            for preference in preferences
        }


def main():
    # Prueba sencilla del cliente
    ai = AIClient(mode=os.getenv("MODO_IA", "mock"))

    text = "Quiero estudiar en un sitio tranquilo con wifi"

    result = ai.interpret_preferences(text)

    print("Petición:", text)
    print("Preferencias:", result)


if __name__ == "__main__":
    main()
