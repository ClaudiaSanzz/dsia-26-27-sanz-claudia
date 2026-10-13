def calcular_importe(df):
    """Añade el importe de cada venta."""

    datos = df.copy()

    datos["importe"] = (
        datos["unidades"] * datos["precio_unitario"]
    )

    return datos


def importe_por_region(df):
    """Calcula el importe total vendido en cada región."""

    datos = calcular_importe(df)

    resultado = datos.groupby("region")["importe"].sum()

    return resultado


def importe_por_producto(df):
    """Calcula el importe total vendido de cada producto."""

    datos = calcular_importe(df)

    resultado = datos.groupby("producto")["importe"].sum()

    return resultado


def unidades_por_producto(df):
    """Calcula las unidades vendidas de cada producto."""

    resultado = df.groupby("producto")["unidades"].sum()

    return resultado