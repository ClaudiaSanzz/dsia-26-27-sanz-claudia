
import pandas as pd


def preparar_datos(ruta):
    # Cargamos el dataset limpio de la Parte B
    df = pd.read_csv(ruta)

    # Nos quedamos con las columnas necesarias
    df = df[["texto_review", "rating_review"]].dropna()

    # Convertimos la puntuación en sentimiento
    def clasificar_sentimiento(rating):
        if rating <= 20:
            return "negativo"
        elif rating == 30:
            return "neutro"
        else:
            return "positivo"

    df["sentimiento"] = df["rating_review"].apply(
        clasificar_sentimiento
    )

    # Comprobamos los resultados
    print("Número de reseñas:", len(df))
    print("\nReseñas por sentimiento:")
    print(df["sentimiento"].value_counts())

    return df


