import pandas as pd

from starter.review_search import ReviewSearch


def test_search_returns_results():
    # Comprobamos que encuentra reseñas relacionadas
    reviews = pd.DataFrame({
        "reviewId": [1, 2, 3],
        "itemId": [10, 20, 30],
        "name": ["Cafe A", "Cafe B", "Cafe C"],
        "texto_review": [
            "Sitio tranquilo para estudiar con el ordenador",
            "Buen brunch y deliciosas tartas",
            "Cafetería con mucho ruido"
        ]
    })

    search = ReviewSearch(reviews)
    results = search.search("tranquilo para estudiar", top_n=2)

    assert len(results) == 2
    assert results.iloc[0]["name"] == "Cafe A"


def test_no_duplicate_cafes():
    # Comprobamos que no se repiten cafeterías
    reviews = pd.DataFrame({
        "reviewId": [1, 2, 3],
        "itemId": [10, 10, 20],
        "name": ["Cafe A", "Cafe A", "Cafe B"],
        "texto_review": [
            "Sitio tranquilo para estudiar",
            "Perfecto para estudiar con ordenador",
            "Buen café y tartas"
        ]
    })

    search = ReviewSearch(reviews)
    results = search.search_cafes("estudiar", top_n=3)

    assert results["itemId"].is_unique


def test_ranking_order(monkeypatch):
    # Creamos dos cafeterías con cinco reseñas cada una
    reviews = pd.DataFrame({
        "reviewId": list(range(1, 11)),
        "itemId": [10] * 5 + [20] * 5,
        "name": ["Cafe A"] * 5 + ["Cafe B"] * 5,
        "texto_review": [
            "Tranquilo para estudiar",
            "Buen sitio para estudiar",
            "Ideal para estudiar",
            "Perfecto para estudiar",
            "Ambiente tranquilo para estudiar",
            "Comida deliciosa",
            "Tartas muy buenas",
            "Café excelente",
            "Buenos desayunos",
            "Servicio amable"
        ],
        "url_review": [f"https://example.com/review/{i}" for i in range(1, 11)]
    })

    # Simulamos el modelo de sentimientos
    class FakePredictor:
        def predict_reviews(self, data):
            data = data.copy()
            data["sentimiento_predicho"] = "positivo"
            return data

    monkeypatch.setattr(
        "starter.review_search.SentimentPredictor",
        FakePredictor
    )

    search = ReviewSearch(reviews)
    results = search.rank_cafes("estudiar", top_n=2)

    assert not results.empty
    assert results.iloc[0]["name"] == "Cafe A"
    assert results["score"].is_monotonic_decreasing


def test_search_without_matches():
    # Comprobamos una búsqueda sin coincidencias
    reviews = pd.DataFrame({
        "reviewId": [1, 2],
        "itemId": [10, 20],
        "name": ["Cafe A", "Cafe B"],
        "texto_review": [
            "Café y tartas",
            "Desayuno delicioso"
        ]
    })

    search = ReviewSearch(reviews)
    results = search.search("astronautas", top_n=5)

    assert (results["similarity"] == 0).all()


def test_rank_without_matches():
    # No debe recomendar cafeterías sin coincidencias
    reviews = pd.DataFrame({
        "reviewId": list(range(1, 6)),
        "itemId": [10] * 5,
        "name": ["Cafe A"] * 5,
        "texto_review": ["Café y tartas"] * 5
    })

    search = ReviewSearch(reviews)
    results = search.rank_cafes("astronautas")

    assert results.empty


def test_rank_excludes_negative_reviews(monkeypatch):
    # Comprobamos que se descartan opiniones negativas
    reviews = pd.DataFrame({
        "reviewId": list(range(1, 11)),
        "itemId": [10] * 5 + [20] * 5,
        "name": ["Cafe A"] * 5 + ["Cafe B"] * 5,
        "texto_review": (
            ["Sitio tranquilo para estudiar"] * 5
            + ["Buen sitio para estudiar"] * 5
        ),
        "url_review": [
        f"https://example.com/review/{i}"
        for i in range(1, 11)
        ]
    })

    class FakePredictor:
        def predict_reviews(self, data):
            data = data.copy()
            data["sentimiento_predicho"] = data["itemId"].map({
                10: "negativo",
                20: "positivo"
            })
            return data

    monkeypatch.setattr(
        "starter.review_search.SentimentPredictor",
        FakePredictor
    )

    search = ReviewSearch(reviews)
    results = search.rank_cafes("estudiar")

    assert len(results) == 1
    assert results.iloc[0]["name"] == "Cafe B"

