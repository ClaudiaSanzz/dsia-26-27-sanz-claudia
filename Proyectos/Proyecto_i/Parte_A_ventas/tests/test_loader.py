import pytest

from ventas.loader import DataLoadError, load


def test_load_correcto(tmp_path):
    """Comprueba que se carga correctamente un CSV válido."""

    archivo = tmp_path / "ventas.csv"

    archivo.write_text(
        "fecha,region,producto,unidades,precio_unitario,cliente_id\n"
        "2026-01-09,Sur,Cable Kit,7,12.5,C005\n"
    )

    df = load(archivo)

    assert len(df) == 1
    assert list(df.columns) == [
        "fecha",
        "region",
        "producto",
        "unidades",
        "precio_unitario",
        "cliente_id",
    ]


def test_load_archivo_no_existe():
    """Comprueba que se lanza DataLoadError si el archivo no existe."""

    with pytest.raises(DataLoadError):
        load("data/no_existe.csv")