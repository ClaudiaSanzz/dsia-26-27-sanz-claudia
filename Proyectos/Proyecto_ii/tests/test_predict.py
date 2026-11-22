import pytest
from starter.predict import SentimentPredictor


def test_predict():
    # Comprobamos que el modelo predice un sentimiento válido
    predictor = SentimentPredictor()

    result = predictor.predict("Me encantó el café")

    assert result in ["positivo", "negativo", "neutro"]


@pytest.mark.parametrize("text", [
    "El café estaba buenísimo",
    "El servicio fue horrible",
    "La experiencia fue normal"
])
def test_predict_multiple_texts(text):
    # Comprobamos diferentes textos
    predictor = SentimentPredictor()

    result = predictor.predict(text)

    assert result in ["positivo", "negativo", "neutro"]
