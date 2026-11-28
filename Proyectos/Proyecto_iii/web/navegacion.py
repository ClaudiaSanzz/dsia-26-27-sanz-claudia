
"""Menú y navegación de COFI."""

import streamlit as st


def cambiar_pagina(pagina):
    """Cambia la página que se está mostrando."""

    st.query_params["pagina"] = pagina
    st.rerun()


def mostrar_menu():
    """Muestra el menú superior de COFI."""

    columnas = st.columns(
        [2.4, 1, 1.5, 1.1, 1, 1.5, 1.1],
        gap="small",
        vertical_alignment="center"
    )

    with columnas[0]:
        st.markdown(
            '<div class="cofi-logo">cofi.</div>',
            unsafe_allow_html=True
        )

    paginas = [
        ("Inicio", "inicio"),
        ("Cafeterías", "explorar"),
        ("Ranking", "ranking"),
        ("Blog", "blog"),
        ("Tu opinión", "opinion"),
        ("Estado", "estado")
    ]

    for columna, (nombre, pagina) in zip(
        columnas[1:], paginas
    ):

        with columna:
            if st.button(
                nombre,
                key=f"menu_{pagina}",
                use_container_width=True
            ):
                cambiar_pagina(pagina)

    st.markdown(
        '<div class="cofi-menu-separador"></div>',
        unsafe_allow_html=True
    )
