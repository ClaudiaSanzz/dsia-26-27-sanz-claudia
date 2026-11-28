
"""COFI - Aplicación web del Proyecto III.

El dashboard conecta los módulos de la interfaz.
Los modelos y la lógica de IA se ejecutan en la API Flask.
"""

import streamlit as st
from web.cafeterias.ficha import mostrar_ficha
from web.estilos import aplicar_estilo
from web.navegacion import mostrar_menu
from web.inicio import mostrar_inicio
from web.cafeterias.explorar import mostrar_explorar
from web.ranking import mostrar_ranking
from web.blog import mostrar_blog
from web.opinion import mostrar_opinion
from web.monitorizacion import mostrar_monitorizacion

def mostrar_pagina_ficha():
    """Muestra la ficha técnica de una cafetería."""

    item_id = st.query_params.get("id")

    if item_id:
        mostrar_ficha(item_id)
    else:
        st.warning("Selecciona una cafetería.")

def main():
    """Inicia la aplicación web de COFI."""

    st.set_page_config(
        page_title="COFI · Tu café, tu momento",
        page_icon="☕",
        layout="wide"
    )

    # Cargamos el diseño y el menú
    aplicar_estilo()
    mostrar_menu()

    # Páginas de la aplicación
    paginas = {
        "inicio": mostrar_inicio,
        "explorar": mostrar_explorar,
        "ficha": mostrar_pagina_ficha,
        "ranking": mostrar_ranking,
        "blog": mostrar_blog,
        "opinion": mostrar_opinion,
        "estado": mostrar_monitorizacion
    }

    # Seleccionamos la página
    pagina = st.query_params.get("pagina", "inicio")

    # Mostramos la página correspondiente
    paginas.get(pagina, mostrar_inicio)()


if __name__ == "__main__":
    main()
