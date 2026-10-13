import pandas as pd
import pytest

from cafeterias.metrics import (
    numero_reviews_por_cafeteria,
    rating_medio_por_cafeteria,
    cafeterias_por_precio,
    rating_cafeteria_por_precio,
    numero_reviews_por_idioma,
    numero_reviews_por_rating,
    numero_reviews_por_ano,
)


@pytest.fixture
def datos_prueba():
    """Crea un DataFrame pequeño para probar las métricas."""

    return pd.DataFrame([
        {
            "reviewId": 1,
            "userId": "U001",
            "itemId": 100,
            "titulo_review": "Muy bien",
            "texto_review": "Buen cafe",
            "fecha_review": pd.to_datetime("2023-01-10").date(),
            "rating_review": 50,
            "language": "es",
            "images": "[]",
            "url_review": "https://review1.com",
            "name": "Cafe Uno",
            "city": "Madrid",
            "priceInterval": "$",
            "url_cafeteria": "https://cafe1.com",
            "rating_cafeteria": 40,
            "categorias": "Cafe",
        },
        {
            "reviewId": 2,
            "userId": "U002",
            "itemId": 100,
            "titulo_review": "Normal",
            "texto_review": "Estuvo bien",
            "fecha_review": pd.to_datetime("2023-02-15").date(),
            "rating_review": 30,
            "language": "en",
            "images": "[]",
            "url_review": "https://review2.com",
            "name": "Cafe Uno",
            "city": "Madrid",
            "priceInterval": "$",
            "url_cafeteria": "https://cafe1.com",
            "rating_cafeteria": 40,
            "categorias": "Cafe",
        },
        {
            "reviewId": 3,
            "userId": "U003",
            "itemId": 200,
            "titulo_review": "Genial",
            "texto_review": "Me encanto",
            "fecha_review": pd.to_datetime("2022-06-20").date(),
            "rating_review": 40,
            "language": "es",
            "images": "[]",
            "url_review": "https://review3.com",
            "name": "Cafe Dos",
            "city": "Madrid",
            "priceInterval": "$$ - $$$",
            "url_cafeteria": "https://cafe2.com",
            "rating_cafeteria": 50,
            "categorias": "Coffee & Tea",
        },
    ])


def test_numero_reviews_por_cafeteria(datos_prueba):
    resultado = numero_reviews_por_cafeteria(datos_prueba)

    assert resultado["Cafe Uno"] == 2
    assert resultado["Cafe Dos"] == 1


def test_rating_medio_por_cafeteria(datos_prueba):
    resultado = rating_medio_por_cafeteria(datos_prueba)

    assert resultado["Cafe Uno"] == 40
    assert resultado["Cafe Dos"] == 40


def test_cafeterias_por_precio(datos_prueba):
    resultado = cafeterias_por_precio(datos_prueba)

    assert resultado["$"] == 1
    assert resultado["$$ - $$$"] == 1


def test_rating_cafeteria_por_precio(datos_prueba):
    resultado = rating_cafeteria_por_precio(datos_prueba)

    assert resultado["$"] == 40
    assert resultado["$$ - $$$"] == 50


def test_numero_reviews_por_idioma(datos_prueba):
    resultado = numero_reviews_por_idioma(datos_prueba)

    assert resultado["es"] == 2
    assert resultado["en"] == 1


def test_numero_reviews_por_rating(datos_prueba):
    resultado = numero_reviews_por_rating(datos_prueba)

    assert resultado[50] == 1
    assert resultado[40] == 1
    assert resultado[30] == 1


def test_numero_reviews_por_ano(datos_prueba):
    resultado = numero_reviews_por_ano(datos_prueba)

    assert resultado[2023] == 2
    assert resultado[2022] == 1