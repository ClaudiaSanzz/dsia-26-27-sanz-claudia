import pytest

from starter.ia_client import AIClient


def test_mock_preferences():
    ai = AIClient("mock")

    result = ai.interpret_preferences(
        "Quiero estudiar en un sitio tranquilo con wifi"
    )

    assert result["quiet"] is True
    assert result["work"] is True
    assert result["wifi"] is True
    assert result["matcha"] is False
    assert result["brunch"] is False


def test_invalid_mode():
    with pytest.raises(ValueError):
        AIClient("incorrecto")


def test_real_preferences(monkeypatch):
    # Simulamos la respuesta de NVIDIA
    expected = {
        "quiet": True,
        "work": True,
        "wifi": False,
        "matcha": True,
        "brunch": False
    }

    ai = AIClient("mock")
    ai.mode = "real"

    monkeypatch.setattr(ai, "ask_nvidia", lambda prompt: expected)

    result = ai.interpret_preferences(
        "Quiero trabajar en un sitio tranquilo con matcha"
    )

    assert result == expected


def test_invalid_nvidia_response(monkeypatch):
    # Simulamos una respuesta con un valor incorrecto
    ai = AIClient("mock")
    ai.mode = "real"

    monkeypatch.setattr(
        ai,
        "ask_nvidia",
        lambda prompt: {"quiet": "sí"}
    )

    with pytest.raises(ValueError):
        ai.interpret_preferences("Quiero una cafetería tranquila")
