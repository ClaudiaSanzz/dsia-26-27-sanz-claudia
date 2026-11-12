
import json
import os
import pandas as pd

from google import genai
from dotenv import load_dotenv


# 1. Cargamos la clave API desde el archivo .env
load_dotenv()


# 2. Función para analizar una reseña
def analizar_resena(texto, modo="mock"):

    # Modo de prueba: no utilizamos la API
    if modo == "mock":
        return "Análisis simulado de la reseña"

    # Modo real: utilizamos la API de Gemini
    elif modo == "real":

        # Conectamos con Gemini utilizando nuestra clave
        cliente = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        # Le indicamos a la IA qué queremos analizar
        prompt = (
            "Analiza esta reseña de una cafetería. "
            "Identifica las opiniones sobre ruido, ambiente, "
            "bebidas, comida, precio, comodidad y atención. "
            "Para cada característica indica positivo, negativo o neutro. "
            "Si no aparece información, indica no_mencionado. "
            "No inventes información. "
            "Responde únicamente en formato JSON, sin explicaciones. "
            "Utiliza estas claves: ruido, ambiente, bebidas, comida, "
            "precio, comodidad, atencion.\n\n"
            + texto
        )

        # Enviamos la reseña a Gemini
        respuesta = cliente.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
            contents=prompt
        )

        return respuesta.text

    else:
        raise ValueError("El modo debe ser mock o real")


# 3. Probamos con reseñas de varias cafeterías
if __name__ == "__main__":

    # Cargamos las reseñas
    df = pd.read_csv("cafeterias_limpias.csv")

    # Eliminamos las reseñas sin texto
    df = df.dropna(subset=["texto_review"])

    # Seleccionamos 5 cafeterías diferentes
    cafeterias = df["itemId"].drop_duplicates().head(2)

    # Nos quedamos con las reseñas de esas cafeterías
    df = df[df["itemId"].isin(cafeterias)]

    # Seleccionamos 5 reseñas por cafetería
    resenas = df.groupby("itemId").head(3)

    resultados = []

    # 4. Analizamos cada reseña
    for _, fila in resenas.iterrows():

        print("\nCAFETERÍA:", fila["name"])
        print("RESEÑA:", fila["texto_review"])

        # Pedimos el análisis a Gemini
        respuesta = analizar_resena(fila["texto_review"], modo="real")

        # Convertimos el JSON en un diccionario
        analisis = json.loads(respuesta)

        # Unificamos las etiquetas
        for clave in analisis:
            if analisis[clave] == "neutral":
                analisis[clave] = "neutro"

        # Añadimos los datos de la cafetería y la reseña
        analisis["itemId"] = fila["itemId"]
        analisis["reviewId"] = fila["reviewId"]
        analisis["name"] = fila["name"]

        # Guardamos el resultado
        resultados.append(analisis)

        print("\nANÁLISIS:")
        print(analisis)

    # 5. Guardamos todos los resultados
    df_resultados = pd.DataFrame(resultados)

    df_resultados.to_csv("analisis_resenas.csv", index=False)

    print("\nAnálisis guardados en analisis_resenas.csv")
    print("Reseñas analizadas:", len(df_resultados))
    print("Cafeterías analizadas:", df_resultados["itemId"].nunique())
