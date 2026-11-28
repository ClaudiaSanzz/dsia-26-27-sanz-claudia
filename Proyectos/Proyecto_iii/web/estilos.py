
"""Estilos de COFI."""

from pathlib import Path

import streamlit as st


def aplicar_estilo():
    """Carga el CSS de la página web."""

    raiz = Path(__file__).resolve().parent.parent

    ruta_css = raiz / "static" / "estilos.css"

    css = ruta_css.read_text(encoding="utf-8")

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )
