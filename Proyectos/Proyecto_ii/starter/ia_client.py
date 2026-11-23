
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

    
    def ask_nvidia(self, prompt, json_response=True):
        # Enviamos la petición a NVIDIA
        try:
            response = self.client.chat.completions.create(
                model=os.getenv(
                    "NVIDIA_MODEL",
                    "nvidia/nemotron-3.5-super-vl-120b-a12b"
                ),
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                top_p=0.95,
                max_tokens=1000,
                stream=False,
                extra_body={
                    "chat_template_kwargs": {
                        "enable_thinking": False
                    }
                }
            )
        except Exception as error:
            raise RuntimeError(
                f"Error al conectar con NVIDIA: {error}"
            ) from error

        # Comprobamos que NVIDIA devuelve contenido
        if not response.choices:
            raise ValueError("NVIDIA no ha devuelto respuestas")

        content = response.choices[0].message.content

        if not content:
            raise ValueError("NVIDIA no ha devuelto contenido")

        content = content.strip()

        # Si queremos texto, lo devolvemos directamente
        if not json_response:
            return content

        # Limpiamos posibles marcas Markdown del JSON
        if content.startswith("```"):
            content = content.replace("```json", "")
            content = content.replace("```", "").strip()

        # Comprobamos que la respuesta sea un JSON válido
        try:
            return json.loads(content)
        except json.JSONDecodeError as error:
            raise ValueError(
                "NVIDIA ha devuelto un JSON no válido"
            ) from error

    def analyze_review(self, text):
        # Características de las reseñas
        features = [
            "ruido", "ambiente", "bebidas", "comida",
            "precio", "comodidad", "atencion"
        ]

        if self.mode == "mock":
            return {
                feature: "no_mencionado"
                for feature in features
            }

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

        # Validamos la respuesta
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

        return {
            feature: result[feature]
            for feature in features
        }

    def interpret_preferences(self, text):
        # Preferencias iniciales de Café Match
        preferences = [
            "quiet", "work", "wifi", "matcha", "brunch"
        ]

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

        # Validamos las preferencias
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

    def explain_recommendation(self, user_request, cafe_name, review):
        # Explicación simulada
        if self.mode == "mock":
            return (
                f"{cafe_name}: recomendación basada en una reseña "
                "relacionada con tu búsqueda."
            )

        # Explicamos la recomendación con una reseña real
        prompt = f"""
        Eres el asistente de Café Match.

        El usuario busca:
        {user_request}

        Cafetería:
        {cafe_name}

        Reseña real:
        {review}

        Explica brevemente por qué esta cafetería
        podría encajar con lo que busca el usuario.

        Reglas:
        - Utiliza únicamente la información de la reseña.
        - No inventes características.
        - Si la reseña no confirma alguna preferencia,
          indica que no tenemos información suficiente.
        - No afirmes que una característica está disponible
          solo porque el usuario la haya solicitado.
        - Responde en español, con 2 o 3 frases.
        """

        return self.ask_nvidia(prompt, json_response=False)


def main():
    # Probamos las funcionalidades sin llamar a NVIDIA
    ai = AIClient(mode="mock")

    text = "Quiero estudiar en un sitio tranquilo con wifi"

    preferences = ai.interpret_preferences(text)

    explanation = ai.explain_recommendation(
        text,
        "La Bicicleta Cafe",
        "Un excelente espacio para tomar un café y estudiar"
    )

    print("\nPETICIÓN:")
    print(text)

    print("\nPREFERENCIAS:")
    print(preferences)

    print("\nEXPLICACIÓN:")
    print(explanation)


if __name__ == "__main__":
    main()
