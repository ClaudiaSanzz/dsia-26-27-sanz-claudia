
"""Ficha técnica individual de una cafetería."""

import pandas as pd
import streamlit as st
from pathlib import Path


@st.cache_data
def cargar_cafeterias():
    """Carga una única fila por cafetería."""

    ruta = Path("data/cafeterias_limpias.csv")

    if not ruta.exists():
        ruta = Path("data/cafeterias_muestra.csv")

    columnas = [
        "itemId", "name", "city", "priceInterval",
        "url_cafeteria", "rating_cafeteria", "categorias"
    ]

    df = pd.read_csv(ruta, usecols=columnas)

    return df.drop_duplicates(subset="itemId")


def mostrar_ficha(item_id):
    """Muestra la ficha de la cafetería seleccionada."""

    cafeterias = cargar_cafeterias()

    cafe = cafeterias[
        cafeterias["itemId"].astype(str) == str(item_id)
    ]

    if cafe.empty:
        st.warning("No hemos encontrado esta cafetería.")
        return

    cafe = cafe.iloc[0]

    nombre = cafe["name"]
    ciudad = cafe["city"]

    st.title(nombre)
    st.caption(f"📍 {ciudad}")

    st.divider()

    columna1, columna2, columna3 = st.columns(3)

    valoracion = cafe["rating_cafeteria"]

    with columna1:
        st.metric(
            "Valoración",
            f"{valoracion}/5" if pd.notna(valoracion)
            else "No disponible"
        )

    with columna2:
        precio = cafe["priceInterval"]

        st.metric(
            "Precio",
            str(precio) if pd.notna(precio)
            else "No disponible"
        )

    with columna3:
        st.metric(
            "Ciudad",
            str(ciudad)
        )

    st.subheader("Sobre esta cafetería")

    categorias = cafe["categorias"]

    if pd.notna(categorias):
        st.write(categorias)

    st.subheader("Más información")

    url = cafe["url_cafeteria"]

    if pd.notna(url):
        st.link_button(
            "Ver ficha original en TripAdvisor",
            str(url),
            use_container_width=True
        )
