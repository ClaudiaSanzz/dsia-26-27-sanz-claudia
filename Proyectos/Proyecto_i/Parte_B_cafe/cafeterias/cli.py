from cafeterias.loader import load
from cafeterias.validator import validar_dataset
from cafeterias.metrics import (
    numero_reviews_por_cafeteria,
    rating_medio_por_cafeteria,
    cafeterias_por_precio,
    rating_cafeteria_por_precio,
    numero_reviews_por_idioma,
    numero_reviews_por_rating,
    numero_reviews_por_ano,
)


def main(
    ruta_entrada="data/cafeterias_reviews_madrid.csv",
    ruta_salida="data/cafeterias_limpias.csv",
):
    """Ejecuta el pipeline completo de cafeterías."""

    # 1. Cargar los datos originales
    df = load(ruta_entrada)

    # 2. Validar y limpiar los datos
    validas, invalidas = validar_dataset(df)

    # 3. Mostrar resumen
    print("\n--- RESUMEN ---")
    print("Reseñas validas:", len(validas))
    print("Reseñas invalidas:", len(invalidas))
    print("Cafeterias unicas validas:", validas["itemId"].nunique())

    # 4. Calcular y mostrar métricas
    print("\n--- NUMERO DE REVIEWS POR CAFETERIA ---")
    print(
        numero_reviews_por_cafeteria(validas)
        .sort_values(ascending=False)
        .head(10)
    )

    print("\n--- RATING MEDIO POR CAFETERIA ---")
    print(
        rating_medio_por_cafeteria(validas)
        .sort_values(ascending=False)
        .head(10)
    )

    print("\n--- CAFETERIAS POR PRECIO ---")
    print(cafeterias_por_precio(validas))

    print("\n--- RATING MEDIO POR PRECIO ---")
    print(rating_cafeteria_por_precio(validas))

    print("\n--- NUMERO DE REVIEWS POR IDIOMA ---")
    print(
        numero_reviews_por_idioma(validas)
        .sort_values(ascending=False)
        .head(10)
    )

    print("\n--- NUMERO DE REVIEWS POR RATING ---")
    print(numero_reviews_por_rating(validas))

    print("\n--- NUMERO DE REVIEWS POR AÑO ---")
    print(numero_reviews_por_ano(validas))

    # 5. Quitar saltos de línea de los textos para que
    # el CSV sea más fácil de visualizar
    validas["titulo_review"] = (
        validas["titulo_review"]
        .str.replace("\n", " ")
        .str.replace("\r", " ")
    )

    validas["texto_review"] = (
        validas["texto_review"]
        .str.replace("\n", " ")
        .str.replace("\r", " ")
    )

    # 6. Guardar el dataset limpio
    validas.to_csv(ruta_salida, index=False)

    print("\nArchivo limpio guardado en:", ruta_salida)


if __name__ == "__main__":
    main()