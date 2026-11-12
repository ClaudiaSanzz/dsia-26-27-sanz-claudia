
import os
from pathlib import Path

import joblib
from dotenv import load_dotenv
from huggingface_hub import hf_hub_download


# 1. Cargamos las variables de entorno
load_dotenv()


# 2. Carpeta donde están nuestros archivos
carpeta = Path(__file__).resolve().parent

# Identificador de nuestro modelo en Hugging Face
repositorio = os.getenv("HF_REPO")


# 3. Función para localizar los archivos del modelo
def buscar_archivo(nombre):

    # Primero buscamos el archivo en nuestro ordenador
    ruta = carpeta / nombre

    if ruta.exists():
        return ruta

    # Si no existe, lo descargamos de Hugging Face
    if not repositorio:
        raise ValueError("Falta HF_REPO en el archivo .env")

    print("Descargando", nombre, "desde Hugging Face...")

    return hf_hub_download(
        repo_id=repositorio,
        filename=nombre,
        token=os.getenv("HF_TOKEN")
    )


# 4. Cargamos el Random Forest y el vectorizador
modelo = joblib.load(
    buscar_archivo("modelo_sentimiento.joblib")
)

vectorizador = joblib.load(
    buscar_archivo("vectorizador.joblib")
)


# 5. Función para predecir el sentimiento
def predecir_sentimiento(texto):

    # Convertimos el texto en números
    texto_vectorizado = vectorizador.transform([texto])

    # Predecimos el sentimiento
    prediccion = modelo.predict(texto_vectorizado)

    return prediccion[0]


# 6. Prueba individual
if __name__ == "__main__":

    texto = "El café estaba buenísimo y el ambiente era agradable"

    resultado = predecir_sentimiento(texto)

    print("Sentimiento:", resultado)
