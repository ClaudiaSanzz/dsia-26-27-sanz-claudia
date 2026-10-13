from pathlib import Path

import pandas as pd


class DataLoadError(Exception):
    """Error relacionado con la carga del archivo de cafeterías."""


def load(path):
    """Carga el archivo CSV de reseñas de cafeterías y devuelve un DataFrame."""

    ruta = Path(path)

    if not ruta.exists():
        raise DataLoadError(f"No existe el archivo: {path}")

    try:
        df = pd.read_csv(ruta)

    except (OSError, pd.errors.ParserError, UnicodeDecodeError) as error:
        raise DataLoadError(
            f"No se ha podido cargar el archivo: {path}"
        ) from error

    return df