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


def test_nvidia_json_invalido():
    from unittest.mock import MagicMock
    import pytest

    from starter.ia_client import AIClient

    ai = AIClient(mode="mock")
    ai.client = MagicMock()
    ai.client.chat.completions.create.return_value.choices[0].message.content = "Esto no es JSON"

    with pytest.raises(ValueError, match="JSON no válido"):
        ai.ask_nvidia("Analiza esta reseña")


def test_nvidia_error_conexion():
    from unittest.mock import MagicMock
    import pytest

    from starter.ia_client import AIClient

    ai = AIClient(mode="mock")
    ai.client = MagicMock()
    ai.client.chat.completions.create.side_effect = ConnectionError("Sin conexión")

    with pytest.raises(RuntimeError, match="Error al conectar con NVIDIA"):
        ai.ask_nvidia("Analiza esta reseña")

