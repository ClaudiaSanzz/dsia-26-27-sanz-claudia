from ventas.loader import load
from ventas.validator import validar_dataset
from ventas.metrics import (
    calcular_importe,
    importe_por_region,
    importe_por_producto,
    unidades_por_producto,
)


def main(
    ruta_entrada="data/ventas.csv",
    ruta_salida="data/ventas_limpias.csv",
):
    """Ejecuta el pipeline completo de ventas."""

    # 1. Cargar los datos
    df = load(ruta_entrada)

    # 2. Validar los datos
    validas, invalidas = validar_dataset(df)

    # 3. Calcular el importe de cada venta
    ventas_con_importe = calcular_importe(validas)

    # 4. Guardar el archivo limpio
    ventas_con_importe.to_csv(ruta_salida, index=False)

    # 5. Mostrar resumen
    print("\n--- RESUMEN ---")
    print("Ventas validas:", len(validas))
    print("Ventas invalidas:", len(invalidas))

    # 6. Mostrar algunas ventas con su importe
    print("\n--- VENTAS CON IMPORTE ---")
    print(ventas_con_importe.head())

    # 7. Mostrar métricas
    print("\n--- IMPORTE POR REGION ---")
    print(importe_por_region(validas))

    print("\n--- IMPORTE POR PRODUCTO ---")
    print(importe_por_producto(validas))

    print("\n--- UNIDADES POR PRODUCTO ---")
    print(unidades_por_producto(validas))

    print("\nArchivo limpio guardado en:", ruta_salida)


if __name__ == "__main__":
    main()