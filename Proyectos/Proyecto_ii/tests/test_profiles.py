
import pandas as pd
import pytest

from starter.profiles import CafeProfiles


@pytest.fixture
def sample_reviews():
    # Creamos reseñas pequeñas para las pruebas
    return pd.DataFrame({
        "itemId": [1, 1, 2],
        "name": ["Cafe A", "Cafe A", "Cafe B"],
        "rating_review": [50, 40, 30],
        "texto_review": [
            "Un sitio tranquilo, ideal para estudiar",
            "Muy buen ambiente y brunch delicioso",
            "Demasiado ruido, imposible concentrarse"
        ]
    })


def test_basic_profiles(sample_reviews):
    profiles = CafeProfiles().create_basic_profiles(sample_reviews)

    assert len(profiles) == 2
    assert profiles.loc[0, "valoracion_media"] == 4.5
    assert profiles.loc[1, "valoracion_media"] == 3.0


def test_focus_features(sample_reviews):
    reviews = CafeProfiles().add_features(sample_reviews)

    assert reviews.loc[0, "focus_tranquilo"]
    assert reviews.loc[2, "focus_ruidoso"]
    assert not reviews.loc[2, "focus_tranquilo"]


def test_social_features(sample_reviews):
    reviews = CafeProfiles().add_features(sample_reviews)

    assert reviews.loc[1, "social_ambiente"]
    assert reviews.loc[1, "social_grupos"]


def test_create_profiles(sample_reviews):
    profiles = CafeProfiles().create_profiles(sample_reviews)

    assert len(profiles) == 2
    assert "focus_tranquilo" in profiles.columns
    assert "social_ambiente" in profiles.columns
    assert "ejemplo_focus_tranquilo" in profiles.columns

