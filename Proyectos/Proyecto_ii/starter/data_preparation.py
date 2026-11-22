
class DataPreparation:

    def classify_sentiment(self, rating):
        # Convertimos la valoración en sentimiento
        if rating <= 20:
            return "negativo"
        elif rating == 30:
            return "neutro"
        else:
            return "positivo"

    def prepare(self, reviews):
        # Seleccionamos los datos para entrenar
        data = reviews[["texto_review", "rating_review"]].dropna().copy()

        # Eliminamos textos repetidos
        data = data.drop_duplicates(subset=["texto_review"])

        # Creamos las etiquetas de sentimiento
        data["sentimiento"] = data["rating_review"].apply(
            self.classify_sentiment
        )

        return data
