import pandas as pd
from pydantic import ValidationError

from ventas.contracts import Venta


def validar_dataset(df):
    """Separa las filas válidas de las inválidas."""

    filas_validas = []
    filas_invalidas = []

    for indice, fila in df.iterrows():

        try:
            venta = Venta(
                fecha=fila["fecha"],
                region=fila["region"],
                producto=fila["producto"],
                unidades=fila["unidades"],
                precio_unitario=fila["precio_unitario"],
                cliente_id=fila["cliente_id"],
            )

            filas_validas.append(venta.model_dump())

        except ValidationError:
            filas_invalidas.append(fila.to_dict())

    validas = pd.DataFrame(filas_validas)
    invalidas = pd.DataFrame(filas_invalidas)

    return validas, invalidas