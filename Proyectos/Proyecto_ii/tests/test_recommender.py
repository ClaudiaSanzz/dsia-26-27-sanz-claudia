import pandas as pd

from starter.recommender import CafeRecommender


class FakeAI:
    def interpret_preferences(self, text):
        return {
            "quiet": True,
            "work": True,
            "wifi": False,
            "matcha": False,
            "brunch": False
        }


class FakeSearch:
    def rank_cafes(self, query, top_n=100):
        return pd.DataFrame({
            "itemId": [10, 20],
            "name": ["Cafe A", "Cafe B"],
            "relevant_reviews": [3, 2],
            "total_reviews": [20, 15],
            "score": [0.4, 0.2]
        })


def test_personalized_recommendations():
    # Creamos dos cafeterías
    profiles = pd.DataFrame({
        "itemId": [10, 20],
        "num_resenas": [20, 15],
        "valoracion_media": [4.5, 4.0]
    })

    recommender = CafeRecommender()

    results, preferences = recommender.recommend_from_text(
        profiles,
        FakeSearch(),
        FakeAI(),
        "Quiero estudiar en un sitio tranquilo"
    )

    assert len(results) == 2
    assert results.iloc[0]["name"] == "Cafe A"
    assert preferences["quiet"] is True
    assert preferences["work"] is True


def test_personalized_without_matches():
    # Simulamos una búsqueda sin resultados
    class EmptySearch:
        def rank_cafes(self, query, top_n=100):
            return pd.DataFrame()

    profiles = pd.DataFrame({
        "itemId": [10],
        "num_resenas": [20],
        "valoracion_media": [4.5]
    })

    recommender = CafeRecommender()

    results, preferences = recommender.recommend_from_text(
        profiles,
        EmptySearch(),
        FakeAI(),
        "Quiero una cafetería para estudiar"
    )

    assert results.empty
    assert preferences["work"] is True


def test_preferences_added_to_search():
    # Comprobamos que las preferencias amplían la búsqueda
    class RecordingSearch:
        def __init__(self):
            self.query = None

        def rank_cafes(self, query, top_n=100):
            self.query = query
            return pd.DataFrame()

    search = RecordingSearch()
    recommender = CafeRecommender()

    profiles = pd.DataFrame({
        "itemId": [10],
        "num_resenas": [20],
        "valoracion_media": [4.5]
    })

    recommender.recommend_from_text(
        profiles,
        search,
        FakeAI(),
        "Quiero estudiar"
    )

    assert "tranquilo" in search.query
    assert "ordenador" in search.query
    assert "matcha" not in search.query
