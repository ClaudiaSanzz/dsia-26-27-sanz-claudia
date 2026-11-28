
"""Ranking de cafeterías de Madrid."""

from pathlib import Path
import html

import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def cargar_ranking(ruta):
    """Calcula el ranking a partir de las reseñas."""

    datos = pd.read_csv(
        ruta,
        usecols=["itemId", "name", "rating_review"]
    )

    # Nos quedamos con valoraciones válidas
    datos["rating_review"] = pd.to_numeric(
        datos["rating_review"],
        errors="coerce"
    )

    datos = datos.dropna(
        subset=["itemId", "name", "rating_review"]
    )

    datos = datos[
        datos["rating_review"].between(1, 5)
    ]

    # Calculamos la media y el número de reseñas
    ranking = datos.groupby(
        ["itemId", "name"],
        as_index=False
    ).agg(
        valoracion=("rating_review", "mean"),
        num_resenas=("rating_review", "size")
    )

    # Exigimos un mínimo de 10 reseñas
    ranking = ranking[
        ranking["num_resenas"] >= 10
    ].copy()

    if ranking.empty:
        return ranking

    # Media general de todas las reseñas
    media_general = datos["rating_review"].mean()

    # Puntuación ponderada
    ranking["puntuacion"] = (
        (
            ranking["num_resenas"] * ranking["valoracion"]
            + 20 * media_general
        )
        / (ranking["num_resenas"] + 20)
    )

    return ranking.sort_values(
        ["puntuacion", "num_resenas"],
        ascending=False
    ).reset_index(drop=True)


def mostrar_ranking():
    """Muestra el ranking con buscador y filtros."""

    st.title("Ranking de cafeterías")

    st.write(
        "Descubre las cafeterías mejor valoradas de Madrid "
        "según las reseñas disponibles en nuestro dataset."
    )

    # Buscamos el CSV del proyecto
    raiz = Path(__file__).resolve().parent.parent

    ruta = raiz / "data" / "cafeterias_limpias.csv"

    if not ruta.is_file():
        ruta = raiz / "data" / "cafeterias_muestra.csv"

    if not ruta.is_file():
        st.error("No se encuentra el dataset de cafeterías.")
        return

    try:
        ranking = cargar_ranking(str(ruta))
    except (ValueError, KeyError) as error:
        st.error(f"No se pudo preparar el ranking: {error}")
        return

    if ranking.empty:
        st.info("No hay suficientes reseñas para el ranking.")
        return

    # Buscador y filtros
    columna1, columna2 = st.columns([3, 1])

    with columna1:
        busqueda = st.text_input(
            "Buscar cafetería",
            placeholder="Escribe el nombre..."
        )

    with columna2:
        minimo = st.selectbox(
            "Mínimo de reseñas",
            [10, 25, 50, 100]
        )

    filtrado = ranking[
        ranking["num_resenas"] >= minimo
    ].copy()

    if busqueda.strip():
        filtrado = filtrado[
            filtrado["name"].str.contains(
                busqueda,
                case=False,
                regex=False,
                na=False
            )
        ]

    st.caption(
        f"{len(filtrado)} cafeterías encontradas"
    )

    if filtrado.empty:
        st.info("No hay cafeterías con esos filtros.")
        return

    # Mostramos las primeras 30 cafeterías
    for posicion, (_, cafe) in enumerate(
        filtrado.head(30).iterrows(),
        1
    ):
        nombre = html.escape(str(cafe["name"]))

        st.markdown(
            f"""
<div class="cofi-ranking">
    <strong>{posicion}. {nombre}</strong>
    <div style="float:right; color:#904713;">
        ★ {cafe["puntuacion"]:.2f}/5
    </div>
    <div class="cofi-aviso">
        {int(cafe["num_resenas"])} reseñas
        · Media original: {cafe["valoracion"]:.2f}/5
    </div>
</div>
""",
            unsafe_allow_html=True
        )

    st.caption(
        "La puntuación combina la valoración media "
        "con el número de reseñas. No representa "
        "una votación oficial del Club COFI."
    )
