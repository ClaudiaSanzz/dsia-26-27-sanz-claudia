import pandas as pd
from pydantic import ValidationError

from cafeterias.contracts import ReviewCafe


def validar_dataset(df):
    """Separa las reseñas válidas de las inválidas."""

    filas_validas = []
    filas_invalidas = []

    review_ids_vistos = set()

    for indice, fila in df.iterrows():

        if fila["reviewId"] in review_ids_vistos:
            filas_invalidas.append(fila.to_dict())
            continue

        try:
            review = ReviewCafe(
                reviewId=fila["reviewId"],
                userId=fila["userId"],
                itemId=fila["itemId"],
                titulo_review=fila["titulo_review"],
                texto_review=fila["texto_review"],
                fecha_review=fila["fecha_review"],
                rating_review=fila["rating_review"],
                language=fila["language"],
                images=fila["images"],
                url_review=fila["url_review"],
                name=fila["name"],
                city=fila["city"],
                priceInterval=fila["priceInterval"],
                url_cafeteria=fila["url_cafeteria"],
                rating_cafeteria=fila["rating_cafeteria"],
                categorias=fila["categorias"],
            )

            filas_validas.append(review.model_dump())
            review_ids_vistos.add(fila["reviewId"])

        except ValidationError:
            filas_invalidas.append(fila.to_dict())

    validas = pd.DataFrame(filas_validas)
    invalidas = pd.DataFrame(filas_invalidas)

    return validas, invalidas