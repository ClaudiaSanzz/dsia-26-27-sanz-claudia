import pandas as pd

from cafeterias.cli import main


def test_cli_crea_archivo(tmp_path):
    """Comprueba que la CLI genera correctamente un archivo limpio."""

    ruta_entrada = tmp_path / "cafeterias.csv"
    ruta_salida = tmp_path / "cafeterias_limpias.csv"

    datos = pd.DataFrame([
        {
            "reviewId": 1,
            "userId": "U001",
            "itemId": 100,
            "titulo_review": "Cafe genial",
            "texto_review": "Muy buen cafe",
            "fecha_review": "2023-05-10",
            "rating_review": 50,
            "language": "es",
            "images": "[]",
            "url_review": "https://review1.com",
            "name": "Cafe Prueba",
            "city": "Madrid",
            "priceInterval": "$",
            "url_cafeteria": "https://cafe1.com",
            "rating_cafeteria": 40,
            "categorias": "Cafe",
        },
        {
            "reviewId": 2,
            "userId": "U002",
            "itemId": 200,
            "titulo_review": "Mala review",
            "texto_review": "No me gusto",
            "fecha_review": "2023-05-11",
            "rating_review": 60,
            "language": "es",
            "images": "[]",
            "url_review": "https://review2.com",
            "name": "Cafe Malo",
            "city": "Madrid",
            "priceInterval": "$",
            "url_cafeteria": "https://cafe2.com",
            "rating_cafeteria": 40,
            "categorias": "Cafe",
        },
    ])

    datos.to_csv(ruta_entrada, index=False)

    main(ruta_entrada, ruta_salida)

    assert ruta_salida.exists()

    resultado = pd.read_csv(ruta_salida)

    assert len(resultado) == 1
    assert resultado.iloc[0]["reviewId"] == 1
    assert "Cafe Prueba" in resultado["name"].values