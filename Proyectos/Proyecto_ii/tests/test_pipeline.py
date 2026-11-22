import pandas as pd

from starter.predict import SentimentPredictor
from starter.ia_client import AIClient
from starter.pipeline import CafePipeline


def test_predict_sentiment():
    # Comprobamos que el modelo real funciona
    predictor = SentimentPredictor()

    result = predictor.predict(
        "El café estaba buenísimo y el personal era muy amable"
    )

    assert result in ["positivo", "negativo", "neutro"]


def test_ai_mock():
    # Comprobamos el análisis simulado
    ai = AIClient("mock")

    result = ai.analyze_review(
        "El ambiente era agradable"
    )

    assert result["ambiente"] == "no_mencionado"


def test_pipeline(monkeypatch, tmp_path):
    # Creamos un dataset pequeño
    reviews = pd.DataFrame({
        "itemId": [1, 1, 2],
        "reviewId": [101, 102, 103],
        "name": ["Cafetería A", "Cafetería A", "Cafetería B"],
        "texto_review": [
            "El café estaba muy bueno",
            "El personal era amable",
            "El ambiente era agradable"
        ],
        "rating_review": [50, 50, 40]
    })

    # Creamos la carpeta de datos temporal
    data_folder = tmp_path / "data"
    data_folder.mkdir()

    reviews.to_csv(
        data_folder / "cafeterias_limpias.csv",
        index=False
    )

    # Simulamos el predictor solo para este test
    class FakePredictor:
        def predict(self, text):
            return "positivo"

    monkeypatch.setattr(
        "starter.pipeline.SentimentPredictor",
        FakePredictor
    )

    # Ejecutamos el pipeline en una carpeta temporal
    monkeypatch.chdir(tmp_path)

    pipeline = CafePipeline("mock")
    results = pipeline.run()

    # Comprobamos que procesa una reseña por cafetería
    assert len(results) == 2

    # Comprobamos que guarda el archivo
    assert (
        tmp_path / "outputs" / "resultados_pipeline_mock.csv"
    ).exists()

    # Comprobamos las predicciones
    assert results["sentimiento"].tolist() == [
        "positivo", "positivo"
    ]

    # Comprobamos las características simuladas
    assert (
        results["ambiente"] == "no_mencionado"
    ).all()
