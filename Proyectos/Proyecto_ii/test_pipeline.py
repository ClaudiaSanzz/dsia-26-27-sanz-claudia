
import pandas as pd

from predecir import predecir_sentimiento
from cliente_ia import analizar_resena
import pipeline


# 1. Comprobamos que el Random Forest predice un sentimiento válido
def test_predecir_sentimiento():

    resultado = predecir_sentimiento(
        "El café estaba buenísimo y el personal era muy amable"
    )

    assert resultado in ["positivo", "negativo", "neutro"]


# 2. Comprobamos que el modo mock funciona sin utilizar Gemini
def test_gemini_mock():

    resultado = analizar_resena(
        "El ambiente era agradable",
        modo="mock"
    )

    assert resultado == "Análisis simulado de la reseña"


# 3. Comprobamos que el pipeline genera resultados
def test_pipeline(monkeypatch, tmp_path):

    # Creamos un pequeño dataset de prueba
    datos = pd.DataFrame({
        "itemId": [1, 1, 2],
        "reviewId": [101, 102, 103],
        "name": ["Cafetería A", "Cafetería A", "Cafetería B"],
        "texto_review": [
            "El café estaba muy bueno",
            "El personal era amable",
            "El ambiente era agradable"
        ]
    })

    # Trabajamos en una carpeta temporal
    monkeypatch.chdir(tmp_path)

    # Guardamos las reseñas de prueba
    datos.to_csv("cafeterias_limpias.csv", index=False)

    # Forzamos el modo mock
    monkeypatch.setenv("MODO_IA", "mock")

    # Sustituimos temporalmente la predicción real
    # para probar el pipeline de forma independiente
    monkeypatch.setattr(
        pipeline,
        "predecir_sentimiento",
        lambda texto: "positivo"
    )

    # Ejecutamos el pipeline
    resultado = pipeline.ejecutar_pipeline()

    # Comprobamos que devuelve una reseña por cafetería
    assert len(resultado) == 2

    # Comprobamos que ha creado el archivo
    assert (tmp_path / "resultados_pipeline_mock.csv").exists()

    # Comprobamos que las predicciones se han guardado
    assert resultado["sentimiento"].tolist() == [
        "positivo", "positivo"
    ]
