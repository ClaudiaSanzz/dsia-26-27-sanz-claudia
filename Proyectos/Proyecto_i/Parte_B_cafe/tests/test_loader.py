import pandas as pd
import pytest

from cafeterias.loader import DataLoadError, load


def test_load_correcto(tmp_path):
    """Comprueba que se carga correctamente un CSV válido."""

    archivo = tmp_path / "cafeterias.csv"

    datos = pd.DataFrame([
        {
            "reviewId": 1,
            "userId": "U001",
            "itemId": 100,
            "titulo_review": "Cafe genial",
            "texto_review": "Muy buen cafe",
            "fecha_review": "2023-05-10",
            "rating_review": 50,
            "language": "es",
            "images": "[]",
            "url_review": "https://review.com",
            "name": "Cafe Prueba",
            "city": "Madrid",
            "priceInterval": "$",
            "url_cafeteria": "https://cafe.com",
            "rating_cafeteria": 40,
            "categorias": "Cafe",
        }
    ])

    datos.to_csv(archivo, index=False)

    df = load(archivo)

    assert len(df) == 1
    assert list(df.columns) == [
        "reviewId",
        "userId",
        "itemId",
        "titulo_review",
        "texto_review",
        "fecha_review",
        "rating_review",
        "language",
        "images",
        "url_review",
        "name",
        "city",
        "priceInterval",
        "url_cafeteria",
        "rating_cafeteria",
        "categorias",
    ]


def test_load_archivo_no_existe():
    """Comprueba que se lanza DataLoadError si el archivo no existe."""

    with pytest.raises(DataLoadError):
        load("data/no_existe.csv")