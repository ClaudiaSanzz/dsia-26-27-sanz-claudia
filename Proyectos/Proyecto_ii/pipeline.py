
import json
import logging
import os

import pandas as pd

from dotenv import load_dotenv
from predecir import predecir_sentimiento
from cliente_ia import analizar_resena


# 1. Cargamos la configuración del archivo .env
load_dotenv()


# 2. Configuramos los logs
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)


# 3. Función principal del pipeline
def ejecutar_pipeline():

    # Consultamos si queremos utilizar Gemini o el modo de prueba
    modo = os.getenv("MODO_IA", "mock").lower()

    if modo not in ["mock", "real"]:
        raise ValueError("MODO_IA debe ser mock o real")

    logging.info("Iniciando pipeline de Café Match")
    logging.info("Modo de IA: %s", modo)

    # 4. Cargamos las reseñas
    df = pd.read_csv("cafeterias_limpias.csv")

    logging.info("Reseñas disponibles: %s", len(df))

    # Eliminamos reseñas sin texto
    df = df.dropna(subset=["texto_review"])

    # Elegimos una reseña por cafetería para probar
    # la integración de todos los componentes
    df = df.drop_duplicates(subset=["itemId"])

    # En modo real limitamos las llamadas a Gemini
    # para no consumir demasiada cuota gratuita
    if modo == "real":
        df = df.head(5)

    logging.info("Cafeterías que vamos a procesar: %s", len(df))

    # 5. Analizamos las reseñas
    resultados = []

    for _, fila in df.iterrows():

        texto = str(fila["texto_review"])

        # Predecimos el sentimiento con Random Forest
        sentimiento = predecir_sentimiento(texto)

        # Analizamos las características con Gemini
        respuesta = analizar_resena(
            texto,
            modo=modo
        )

        # Convertimos la respuesta de Gemini en un diccionario
        if modo == "real":

            aspectos = json.loads(respuesta)

            # Unificamos las etiquetas
            for clave in aspectos:
                if aspectos[clave] == "neutral":
                    aspectos[clave] = "neutro"

        else:
            # En mock no inventamos opiniones de Gemini
            aspectos = {}

        # Guardamos los resultados de cada reseña
        resultado = {
            "itemId": fila["itemId"],
            "reviewId": fila["reviewId"],
            "name": fila["name"],
            "sentimiento": sentimiento
        }

        resultado.update(aspectos)

        resultados.append(resultado)

        # Informamos del avance cada 50 reseñas
        if len(resultados) % 50 == 0:
            logging.info(
                "Reseñas procesadas: %s",
                len(resultados)
            )

    # 6. Convertimos los resultados en una tabla
    df_resultados = pd.DataFrame(resultados)

    # Guardamos mock y real por separado
    # para no sobrescribir los análisis reales
    archivo = "resultados_pipeline_" + modo + ".csv"

    df_resultados.to_csv(archivo, index=False)

    # 7. Mostramos el resumen final
    logging.info("Pipeline terminado correctamente")
    logging.info("Reseñas procesadas: %s", len(df_resultados))
    logging.info("Resultados guardados en %s", archivo)

    return df_resultados


# 8. Ejecutamos el pipeline
if __name__ == "__main__":
    ejecutar_pipeline()
