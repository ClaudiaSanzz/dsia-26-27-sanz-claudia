import pandas as pd
from pathlib import Path


def main():
    # Cargamos los análisis realizados con NVIDIA
    ruta = Path("outputs/resultados_pipeline_real.csv")
    df = pd.read_csv(ruta)

    # Características que analiza NVIDIA
    caracteristicas = [
        "ruido", "ambiente", "bebidas", "comida",
        "precio", "comodidad", "atencion"
    ]

    # Evitamos contar dos veces la misma reseña
    df = df.drop_duplicates(subset=["reviewId"])

    # Creamos una fila por cafetería
    resumen = df.groupby("itemId").agg(
        name=("name", "first"),
        resenas_analizadas=("reviewId", "count")
    ).reset_index()

    # Contamos las opiniones positivas y negativas
    for caracteristica in caracteristicas:
        for sentimiento in ["positivo", "negativo"]:

            opiniones = df[df[caracteristica] == sentimiento]
            conteo = opiniones.groupby("itemId").size()

            columna = caracteristica + "_" + sentimiento

            resumen[columna] = (
                resumen["itemId"]
                .map(conteo)
                .fillna(0)
                .astype(int)
            )

    # Guardamos el resultado
    Path("outputs").mkdir(exist_ok=True)

    resumen.to_csv("outputs/resumen_opiniones.csv", index=False)

    print("\nRESUMEN DE OPINIONES DE NVIDIA")
    print("Reseñas analizadas:", len(df))
    print("Cafeterías analizadas:", len(resumen))
    print("\nResultados guardados en outputs/resumen_opiniones.csv")


if __name__ == "__main__":
    main()
