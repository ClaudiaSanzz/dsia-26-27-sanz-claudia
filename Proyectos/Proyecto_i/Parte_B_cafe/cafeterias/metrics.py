def numero_reviews_por_cafeteria(df):
    """Calcula cuántas reseñas tiene cada cafetería."""

    resultado = df.groupby("name")["reviewId"].count()

    return resultado


def rating_medio_por_cafeteria(df):
    """Calcula el rating medio de las reseñas de cada cafetería."""

    resultado = df.groupby("name")["rating_review"].mean()

    return resultado


def cafeterias_por_precio(df):
    """Calcula cuántas cafeterías hay en cada rango de precio."""

    cafeterias = df.drop_duplicates(subset="itemId")

    resultado = cafeterias.groupby("priceInterval")["itemId"].count()

    return resultado


def rating_cafeteria_por_precio(df):
    """Calcula el rating medio de las cafeterías según su rango de precio."""

    cafeterias = df.drop_duplicates(subset="itemId")

    resultado = cafeterias.groupby("priceInterval")["rating_cafeteria"].mean()

    return resultado


def numero_reviews_por_idioma(df):
    """Calcula cuántas reseñas hay en cada idioma."""

    resultado = df.groupby("language")["reviewId"].count()

    return resultado


def numero_reviews_por_rating(df):
    """Calcula cuántas reseñas hay para cada valoración."""

    resultado = df.groupby("rating_review")["reviewId"].count()

    return resultado


def numero_reviews_por_ano(df):
    """Calcula cuántas reseñas se publicaron cada año."""

    datos = df.copy()

    datos["ano"] = datos["fecha_review"].apply(lambda fecha: fecha.year)

    resultado = datos.groupby("ano")["reviewId"].count()

    return resultado