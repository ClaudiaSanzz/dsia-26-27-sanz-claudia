class CafeValidator:

    def validate_columns(self, reviews):
        # Comprobamos que están las columnas necesarias
        required = ["texto_review", "rating_review", "itemId"]

        missing = set(required) - set(reviews.columns)

        if missing:
            raise ValueError(f"Faltan columnas: {missing}")

        return reviews

    def remove_empty_reviews(self, reviews):
        # Eliminamos reseñas sin texto
        return reviews.dropna(subset=["texto_review"]).copy()
