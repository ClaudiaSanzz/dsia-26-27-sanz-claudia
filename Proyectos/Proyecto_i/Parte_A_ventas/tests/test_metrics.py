import pandas as pd
import pytest

from ventas.metrics import (
    calcular_importe,
    importe_por_region,
    importe_por_producto,
    unidades_por_producto,
)


@pytest.fixture
def datos_prueba():
    """Crea un DataFrame pequeño reutilizable para los tests."""

    return pd.DataFrame([
        {
            "fecha": "2026-01-01",
            "region": "Norte",
            "producto": "Sensor A",
            "unidades": 2,
            "precio_unitario": 10.0,
            "cliente_id": "C001",
        },
        {
            "fecha": "2026-01-02",
            "region": "Norte",
            "producto": "Sensor B",
            "unidades": 3,
            "precio_unitario": 20.0,
            "cliente_id": "C002",
        },
        {
            "fecha": "2026-01-03",
            "region": "Sur",
            "producto": "Sensor A",
            "unidades": 1,
            "precio_unitario": 10.0,
            "cliente_id": "C003",
        },
    ])


def test_calcular_importe(datos_prueba):
    """Comprueba el importe calculado de cada venta."""

    resultado = calcular_importe(datos_prueba)

    assert resultado["importe"].tolist() == [20.0, 60.0, 10.0]


def test_importe_por_region(datos_prueba):
    """Comprueba el importe total por región."""

    resultado = importe_por_region(datos_prueba)

    assert resultado["Norte"] == 80.0
    assert resultado["Sur"] == 10.0


def test_importe_por_producto(datos_prueba):
    """Comprueba el importe total por producto."""

    resultado = importe_por_producto(datos_prueba)

    assert resultado["Sensor A"] == 30.0
    assert resultado["Sensor B"] == 60.0


def test_unidades_por_producto(datos_prueba):
    """Comprueba las unidades totales por producto."""

    resultado = unidades_por_producto(datos_prueba)

    assert resultado["Sensor A"] == 3
    assert resultado["Sensor B"] == 3