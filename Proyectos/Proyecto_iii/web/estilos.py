
"""Carga los estilos CSS de COFI."""

from pathlib import Path

import streamlit as st


def aplicar_estilo():
    """Carga los estilos de cada sección."""

    raiz = Path(__file__).resolve().parent.parent
    carpeta = raiz / "static"

    archivos = [
        "estilos.css",
        "club.css",
        "comunidad.css",
        "etapas.css",
        "blog.css"
    ]

    for nombre in archivos:
        ruta = carpeta / nombre

        if ruta.is_file():
            css = ruta.read_text(encoding="utf-8")
            st.html(f"<style>{css}</style>")
