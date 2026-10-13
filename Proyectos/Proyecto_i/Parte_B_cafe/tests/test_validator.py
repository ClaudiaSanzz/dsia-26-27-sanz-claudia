import pandas as pd
import pytest

from cafeterias.validator import validar_dataset


def crear_fila_valida():
    """Devuelve una fila válida de ejemplo."""

    return {
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


def test_fila_valida():
    """Comprueba que una fila correcta se considera válida."""

    df = pd.DataFrame([
        crear_fila_valida()
    ])

    validas, invalidas = validar_dataset(df)

    assert len(validas) == 1
    assert len(invalidas) == 0


@pytest.mark.parametrize(
    "campo, valor_invalido",
    [
        ("rating_review", 60),
        ("rating_cafeteria", -10),
        ("priceInterval", None),
        ("texto_review", None),
    ],
)
def test_filas_invalidas(campo, valor_invalido):
    """Comprueba diferentes casos de datos inválidos."""

    fila = crear_fila_valida()

    fila[campo] = valor_invalido

    df = pd.DataFrame([
        fila
    ])

    validas, invalidas = validar_dataset(df)

    assert len(validas) == 0
    assert len(invalidas) == 1


def test_review_duplicada():
    """Comprueba que un reviewId repetido se considera duplicado."""

    fila1 = crear_fila_valida()

    fila2 = crear_fila_valida()
    fila2["userId"] = "U002"

    df = pd.DataFrame([
        fila1,
        fila2,
    ])

    validas, invalidas = validar_dataset(df)

    assert len(validas) == 1
    assert len(invalidas) == 1