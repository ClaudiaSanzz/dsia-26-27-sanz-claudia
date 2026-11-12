
import json
import os
import pandas as pd

from openai import OpenAI
from dotenv import load_dotenv


# 1. Cargamos las variables del archivo .env
load_dotenv()


# 2. Función para analizar una reseña
def analizar_resena(texto, modo="mock"):

    # Modo de prueba: no llamamos a NVIDIA
    if modo == "mock":
        return "Análisis simulado de la reseña"

    # Comprobamos que el modo sea correcto
    if modo != "real":
        raise ValueError("El modo debe ser mock o real")

    # 3. Obtenemos la clave de NVIDIA
    clave = os.getenv("NVIDIA_API_KEY")

    if not clave:
        raise ValueError("Falta NVIDIA_API_KEY en el archivo .env")

    # 4. Conectamos con NVIDIA
    cliente = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=clave
    )

    # 5. Indicamos qué queremos analizar
    prompt = (
        "Analiza esta reseña de una cafetería. "
        "Identifica las opiniones sobre ruido, ambiente, "
        "bebidas, comida, precio, comodidad y atención. "
        "Para cada característica indica positivo, negativo, "
        "neutro o no_mencionado. "
        "Si no aparece información, indica no_mencionado. "
        "No inventes información. "
        "Responde únicamente en formato JSON, sin explicaciones. "
        "Utiliza exactamente estas claves: ruido, ambiente, bebidas, "
        "comida, precio, comodidad, atencion.\n\n"
        + str(texto)
    )

    # 6. Enviamos la reseña al modelo NVIDIA Nemotron
    respuesta = cliente.chat.completions.create(
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

    # 7. Recuperamos el análisis
    contenido = respuesta.choices[0].message.content

    if not contenido:
        raise ValueError("NVIDIA no ha devuelto contenido")

    contenido = contenido.strip()

    # Eliminamos las marcas de Markdown si aparecen
    if contenido.startswith("```"):
        contenido = contenido.replace("```json", "")
        contenido = contenido.replace("```", "").strip()

    # Convertimos el JSON en un diccionario
    analisis = json.loads(contenido)

    # 8. Comprobamos las etiquetas devueltas
    caracteristicas = [
        "ruido", "ambiente", "bebidas", "comida",
        "precio", "comodidad", "atencion"
    ]

    resultado = {}

    for caracteristica in caracteristicas:

        valor = analisis.get(caracteristica)

        if valor == "neutral":
            valor = "neutro"

        if valor not in [
            "positivo", "negativo", "neutro", "no_mencionado"
        ]:
            raise ValueError(
                "Valor no válido para " + caracteristica
            )

        resultado[caracteristica] = valor

    return json.dumps(resultado, ensure_ascii=False)


# 9. Probamos con una reseña de nuestro dataset
if __name__ == "__main__":

    df = pd.read_csv("cafeterias_limpias.csv")

    resena = df.dropna(subset=["texto_review"]).iloc[0]

    print("\nCAFETERÍA:", resena["name"])
    print("\nRESEÑA:", resena["texto_review"])

    respuesta = analizar_resena(
        resena["texto_review"],
        modo=os.getenv("MODO_IA", "mock")
    )

    print("\nANÁLISIS:")
    print(respuesta)
