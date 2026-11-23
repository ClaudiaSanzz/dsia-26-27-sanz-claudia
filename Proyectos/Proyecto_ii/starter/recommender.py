import os
import pandas as pd

from starter.ia_client import AIClient
from starter.loader import CafeLoader
from starter.review_search import ReviewSearch


class CafeRecommender:

    def __init__(self):
        # Características de cada modo
        self.options = {
            "focus": {
                "quiet": ("focus_tranquilo", "focus_ruidoso"),
                "work": ("focus_trabajar", "focus_no_trabajar")
            },
            "social": {
                "chat": ("social_ambiente", "social_mal_ambiente"),
                "friends": ("social_grupos", "social_no_grupos")
            },
            "trendy": {
                "coffee": ("trending_matcha", None),
                "brunch": ("trending_brunch", None)
            },
            "surprise": {
                "original": ("discovery_original", None),
                "hidden": ("discovery_escondido", None)
            }
        }

    def filter_cafes(self, profiles):
        # Cafeterías con al menos 10 reseñas
        return profiles[profiles["num_resenas"] >= 10].copy()

    def calculate_base_score(self, cafes):
        # Valoración ponderada
        global_mean = cafes["valoracion_media"].mean()

        cafes["score_base"] = (
            (cafes["num_resenas"] * cafes["valoracion_media"]
             + 20 * global_mean)
            / (cafes["num_resenas"] + 20)
        ) / 5 * 100

        return cafes

    def calculate_compatibility(self, cafes, positive, negative):
        # Compatibilidad de una preferencia
        positive_count = cafes[positive].fillna(0)

        if negative is not None:
            negative_count = cafes[negative].fillna(0)

            compatibility = (
                (positive_count - negative_count)
                / (positive_count + negative_count + 5)
            )

            evidence = positive_count + negative_count

        else:
            compatibility = positive_count / (positive_count + 10)
            evidence = positive_count

        return compatibility, evidence

    def recommend(self, profiles, mode, preferences, top_n=5):
        # Recomendaciones por modo
        if mode not in self.options:
            raise ValueError("Modo no válido")

        if isinstance(preferences, str):
            preferences = [preferences]

        if not preferences:
            raise ValueError("Selecciona una preferencia")

        for preference in preferences:
            if preference not in self.options[mode]:
                raise ValueError("Preferencia no válida")

        cafes = self.filter_cafes(profiles)

        if cafes.empty:
            return cafes

        cafes = self.calculate_base_score(cafes)

        compatibilities = []
        evidences = []

        for preference in preferences:
            positive, negative = self.options[mode][preference]

            compatibility, evidence = self.calculate_compatibility(
                cafes, positive, negative
            )

            compatibilities.append(compatibility)
            evidences.append(evidence)

        cafes["compatibilidad"] = sum(compatibilities) / len(preferences)
        cafes["evidencias"] = sum(evidences)

        cafes["score"] = (
            cafes["score_base"] + cafes["compatibilidad"] * 15
        )

        if mode == "trendy":
            cafes["score"] += (
                cafes["num_resenas"] / cafes["num_resenas"].max()
            ) * 5

        elif mode == "surprise":
            cafes["score"] += (
                1 - cafes["num_resenas"] / cafes["num_resenas"].max()
            ) * 5

        cafes = cafes[cafes["evidencias"] > 0]

        cafes = cafes.sort_values(
            ["compatibilidad", "score"],
            ascending=False
        )

        return cafes.head(top_n)

    def recommend_from_text(self, profiles, search, ai, text, top_n=5):
        # Interpretamos las preferencias
        preferences = ai.interpret_preferences(text)

        keywords = {
            "quiet": "tranquilo silencio",
            "work": "estudiar trabajar ordenador portátil",
            "wifi": "wifi",
            "matcha": "matcha",
            "brunch": "brunch"
        }

        # Ampliamos la búsqueda con las preferencias
        query = text

        for preference, active in preferences.items():
            if active and preference in keywords:
                query += " " + keywords[preference]

        # Buscamos cafeterías relacionadas
        ranking = search.rank_cafes(query, top_n=100)

        if ranking.empty:
            return ranking, preferences

        # Añadimos las valoraciones generales
        columns = ["itemId", "num_resenas", "valoracion_media"]

        cafes = ranking.merge(
            profiles[columns],
            on="itemId",
            how="inner"
        )

        if cafes.empty:
            return cafes, preferences

        cafes = self.calculate_base_score(cafes)

        # Combinamos relevancia y valoración
        max_score = cafes["score"].max()

        if max_score > 0:
            cafes["relevance"] = cafes["score"] / max_score
        else:
            cafes["relevance"] = 0

        cafes["final_score"] = (
            cafes["relevance"] * 0.7
            + (cafes["score_base"] / 100) * 0.3
        )

        cafes = cafes.sort_values(
            "final_score", ascending=False
        )

        # Nos quedamos con las mejores cafeterías
        cafes = cafes.head(top_n).copy()

        # Generamos una explicación basada en una reseña real
        explanations = []

        for _, cafe in cafes.iterrows():
            review = cafe.get("example_review", "")

            if pd.isna(review):
                review = ""

            if not review:
                explanation = "No tenemos una reseña disponible para explicar esta recomendación."
            else:
                explanation = ai.explain_recommendation(
                    text,
                    cafe["name"],
                    review
                )

            explanations.append(explanation)

        cafes["explanation"] = explanations

        return cafes, preferences


def main():
    profiles = pd.read_csv("outputs/perfiles_cafeterias.csv")
    recommender = CafeRecommender()

    print("\nCAFÉ MATCH")
    print("Modos: focus, social, trendy, surprise, libre")

    mode = input("Elige un modo: ").lower().strip()

    if mode == "libre":
        text = input("¿Qué buscas en una cafetería? ")

        # Cargamos las reseñas
        reviews = CafeLoader().load_csv(
            "data/cafeterias_limpias.csv"
        )

        search = ReviewSearch(reviews)
        ai = AIClient(mode=os.getenv("MODO_IA", "mock"))

        results, preferences = recommender.recommend_from_text(
            profiles, search, ai, text, top_n=3
        )

        print("\nPreferencias detectadas:")
        print(preferences)

        if results.empty:
            print("No encontramos cafeterías relacionadas.")

        else:
            print("\nCAFETERÍAS RECOMENDADAS")

            for _, cafe in results.iterrows():
                print(f"\n{cafe['name']}")
                print(
                    f"Valoración: {cafe['valoracion_media']:.2f}/5"
                )
                print(
                    f"Puntuación: {cafe['final_score']:.3f}"
                )
                print(f"Explicación: {cafe['explanation']}")
                print("-" * 50)

    else:
        if mode not in recommender.options:
            raise ValueError("Modo no válido")

        print(
            "Preferencias:",
            ", ".join(recommender.options[mode])
        )

        answer = input(
            "Elige preferencias separadas por coma: "
        )

        preferences = [
            preference.strip().lower()
            for preference in answer.split(",")
        ]

        results = recommender.recommend(
            profiles, mode, preferences, top_n=10
        )

        if results.empty:
            print("No hay cafeterías con información suficiente.")

        else:
            columns = [
                "name", "valoracion_media", "num_resenas",
                "evidencias", "compatibilidad", "score"
            ]

            print(
                results[columns].round(2).to_string(index=False)
            )


if __name__ == "__main__":
    main()
