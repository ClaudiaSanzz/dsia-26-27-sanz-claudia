import pandas as pd
import pytest

from ventas.loader import load
from ventas.validator import validar_dataset


def test_fila_valida():
    """Comprueba que una fila correcta se considera válida."""

    df = pd.DataFrame([
        {
            "fecha": "2026-01-09",
            "region": "Sur",
            "producto": "Cable Kit",
            "unidades": 7,
            "precio_unitario": 12.5,
            "cliente_id": "C005",
        }
    ])

    validas, invalidas = validar_dataset(df)

    assert len(validas) == 1
    assert len(invalidas) == 0


@pytest.mark.parametrize(
    "unidades",
    [0, -1, None],
)
def test_unidades_invalidas(unidades):
    """Comprueba varios valores inválidos para unidades."""

    df = pd.DataFrame([
        {
            "fecha": "2026-01-09",
            "region": "Sur",
            "producto": "Cable Kit",
            "unidades": unidades,
            "precio_unitario": 12.5,
            "cliente_id": "C005",
        }
    ])

    validas, invalidas = validar_dataset(df)

    assert len(validas) == 0
    assert len(invalidas) == 1


@pytest.mark.integration
def test_dataset_real():
    """Comprueba el resultado esperado del dataset completo."""

    df = load("data/ventas.csv")

    validas, invalidas = validar_dataset(df)

    assert len(validas) == 140
    assert len(invalidas) == 10