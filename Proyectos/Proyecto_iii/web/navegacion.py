
"""Menú de navegación de COFI."""

import streamlit as st


def cambiar_pagina(pagina):
    """Cambia de página desde otros botones de la web."""
    st.query_params["pagina"] = pagina
    st.rerun()


def mostrar_menu():
    """Muestra el menú superior de COFI."""

    pagina_actual = st.query_params.get("pagina", "inicio")

    paginas = [
        ("Inicio", "inicio"),
        ("Cafeterías", "explorar"),
        ("Ranking", "ranking"),
        ("Blog", "blog"),
        ("Tu opinión", "opinion"),
        ("Estado", "estado")
    ]

    enlaces = ""

    for nombre, pagina in paginas:
        clase = "cofi-nav-activo" if pagina == pagina_actual else ""

        enlaces += (
            f'<a class="cofi-nav-enlace {clase}" '
            f'href="?pagina={pagina}">{nombre}</a>'
        )

    st.html(f"""
    <nav class="cofi-navbar">
        <a class="cofi-navbar-logo" href="?pagina=inicio">
            cofi.
        </a>

        <div class="cofi-navbar-enlaces">
            {enlaces}
        </div>
    </nav>
    """)

    st.html('<div class="cofi-menu-separador"></div>')
