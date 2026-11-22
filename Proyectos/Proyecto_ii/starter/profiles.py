from pathlib import Path

import pandas as pd


class CafeProfiles:

    def __init__(self):
        # Expresiones para identificar características en las reseñas
        self.patterns = {
            "focus_ruidoso": (
                r"mucho ruido|demasiado ruido|muy ruidos|"
                r"imposible concentrarse|nada tranquil|"
                r"no se puede concentrar|excesivamente ruidos"
            ),
            "focus_no_trabajar": (
                r"no dejan trabajar|no permiten trabajar|"
                r"no se puede trabajar|no dejan estudiar|"
                r"no se puede estudiar|prohibido.*portátil|"
                r"prohibido.*portatil|no permiten.*portátil|"
                r"no permiten.*portatil|no hay wifi|"
                r"wifi no funciona|sin wifi|no hay enchufes|"
                r"sin enchufes|no dejan usar.*ordenador"
            ),
            "focus_tranquilo": (
                r"sitio tranquil|lugar tranquil|ambiente tranquil|"
                r"muy tranquil|bastante tranquil|sin ruido|"
                r"poco ruido|silencios|ideal para concentrarse|"
                r"perfecto para concentrarse|relajado y tranquil"
            ),
            "focus_trabajar": (
                r"ideal para estudiar|perfecto para estudiar|"
                r"ideal para trabajar|perfecto para trabajar|"
                r"se puede estudiar|se puede trabajar|"
                r"pude estudiar|pude trabajar|"
                r"estuve estudiando|estuve trabajando|"
                r"teletrabajar|trabajar con el portátil|"
                r"trabajar con el portatil|estudiar con el portátil|"
                r"estudiar con el portatil|"
                r"buen wifi|wifi funciona|wifi gratis|"
                r"enchufes disponibles|hay enchufes|"
                r"mesas para trabajar|trabajar con ordenador"
            ),
            "social_mal_ambiente": (
                r"mal ambiente|ambiente desagradable|"
                r"no se puede hablar|imposible conversar|"
                r"imposible charlar|ambiente incómodo"
            ),
            "social_no_grupos": (
                r"no admiten grupos|no aceptan grupos|"
                r"no hay sitio para grupos|no cabíamos|"
                r"no cabiamos|no permiten grupos"
            ),
            "social_ambiente": (
                r"buen ambiente|ambiente agradable|"
                r"ambiente acogedor|ambiente animado|"
                r"ideal para charlar|perfecto para charlar|"
                r"ideal para conversar|perfecto para conversar|"
                r"sitio acogedor|lugar acogedor"
            ),
            "social_grupos": (
                r"ideal para grupos|perfecto para grupos|"
                r"para ir con amigos|con los amigos|"
                r"quedar con amigos|fuimos en grupo|"
                r"brunch delicioso|brunch buenísimo|"
                r"brunch buenisimo|ideal para brunch"
            ),
            "trending_matcha": (
                r"matcha|flat white|cold brew|"
                r"café de especialidad|cafe de especialidad|"
                r"specialty coffee|chai latte"
            ),
            "trending_brunch": (
                r"brunch|pancakes|tostadas francesas|"
                r"avocado toast|açaí|acai|"
                r"eggs benedict|huevos benedictinos"
            ),
            "discovery_original": (
                r"sitio original|lugar original|muy original|"
                r"decoración especial|decoracion especial|"
                r"sitio diferente|lugar diferente|"
                r"cafetería temática|cafeteria tematica|"
                r"decoración curiosa|decoracion curiosa|"
                r"experiencia diferente|concepto original"
            ),
            "discovery_escondido": (
                r"joya escondida|rincón escondido|rincon escondido|"
                r"poco conocido|poco conocida|"
                r"lugar secreto|sitio escondido|"
                r"hidden gem|joya oculta"
            )
        }

    def create_basic_profiles(self, reviews):
        # Calculamos las estadísticas de cada cafetería
        profiles = reviews.groupby("itemId").agg(
            name=("name", "first"),
            num_resenas=("rating_review", "count"),
            valoracion_media=("rating_review", "mean")
        ).reset_index()

        profiles["valoracion_media"] = (
            profiles["valoracion_media"] / 10
        ).round(2)

        return profiles

    def add_features(self, reviews):
        # Buscamos las características en las reseñas
        data = reviews.copy()
        data["texto_review"] = data["texto_review"].fillna("")

        text = data["texto_review"].str.lower()

        for feature, pattern in self.patterns.items():
            data[feature] = text.str.contains(
                pattern, regex=True, na=False
            )

        # Evitamos contar señales contradictorias como favorables
        data["focus_tranquilo"] &= ~data["focus_ruidoso"]
        data["focus_trabajar"] &= ~data["focus_no_trabajar"]
        data["social_ambiente"] &= ~data["social_mal_ambiente"]
        data["social_grupos"] &= ~data["social_no_grupos"]

        return data

    def count_features(self, reviews):
        # Contamos las menciones por cafetería
        columns = list(self.patterns.keys())

        return reviews.groupby("itemId")[columns].sum().reset_index()

    def add_examples(self, profiles, reviews):
        # Guardamos una reseña de ejemplo por característica
        for feature in self.patterns:
            examples = reviews.loc[
                reviews[feature], ["itemId", "texto_review"]
            ].drop_duplicates(subset=["itemId"]).copy()

            examples["texto_review"] = (
                examples["texto_review"].str.slice(0, 220)
            )

            examples = examples.rename(
                columns={"texto_review": "ejemplo_" + feature}
            )

            profiles = profiles.merge(
                examples, on="itemId", how="left"
            )

        return profiles

    def create_profiles(self, reviews):
        # Unimos las estadísticas y las características
        basic = self.create_basic_profiles(reviews)
        reviews_features = self.add_features(reviews)
        features = self.count_features(reviews_features)

        profiles = basic.merge(
            features, on="itemId", how="left"
        )

        profiles = self.add_examples(profiles, reviews_features)

        return profiles

    def save(self, profiles, path="outputs/perfiles_cafeterias.csv"):
        # Guardamos los perfiles en CSV
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        profiles.to_csv(path, index=False)


def main():
    from starter.loader import CafeLoader
    from starter.validator import CafeValidator

    # Cargamos y validamos las reseñas
    reviews = CafeLoader().load_csv("data/cafeterias_limpias.csv")
    reviews = CafeValidator().validate_columns(reviews)

    # Generamos y guardamos los perfiles
    creator = CafeProfiles()
    profiles = creator.create_profiles(reviews)
    creator.save(profiles)

    print("Cafeterías:", len(profiles))
    print("Reseñas:", len(reviews))
    print("Perfiles guardados en outputs/perfiles_cafeterias.csv")


if __name__ == "__main__":
    main()
