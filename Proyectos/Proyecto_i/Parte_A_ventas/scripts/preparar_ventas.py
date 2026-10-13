import pandas as pd

from ventas.loader import load_ventas
from ventas.validator import validar_dataset


def main():
    # Cargar dataset original
    df = load_ventas("data/ventas.csv")

    # Separar filas válidas e inválidas
    validas, invalidas = validar_dataset(df)

    print("Filas totales:", len(df))
    print("Filas válidas:", len(validas))
    print("Filas inválidas:", len(invalidas))

    print("\nFILAS INVÁLIDAS:")
    print(invalidas.to_string())

    # Guardar dataset limpio
    validas.to_csv(
        "data/ventas_limpio.csv",
        index=False
    )

    print("\nDataset limpio guardado en:")
    print("data/ventas_limpio.csv")


if __name__ == "__main__":
    main()