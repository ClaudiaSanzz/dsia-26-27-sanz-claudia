
"""Blog y galería automática de COFI."""

import base64
from pathlib import Path

import streamlit as st

from web.navegacion import cambiar_pagina


def cargar_fotografias():
    """Carga las fotografías de la galería."""

    raiz = Path(__file__).resolve().parent.parent
    carpeta = raiz / "static" / "galeria"

    imagenes = []

    for numero in range(1, 9):
        ruta = carpeta / f"{numero:02d}.jpg"

        if ruta.is_file():
            contenido = base64.b64encode(
                ruta.read_bytes()
            ).decode("ascii")

            imagenes.append(
                f"data:image/jpeg;base64,{contenido}"
            )

    return imagenes


def mostrar_carrusel():
    """Muestra tres fotografías que avanzan automáticamente."""

    imagenes = cargar_fotografias()

    if len(imagenes) < 3:
        st.info(
            "Añade al menos tres imágenes en "
            "static/galeria para mostrar el carrusel."
        )
        return

    # El carrusel está diseñado para ocho imágenes.
    # Si faltan algunas, repetimos las disponibles.
    while len(imagenes) < 8:
        imagenes.append(
            imagenes[len(imagenes) % len(set(imagenes))]
        )

    # Repetimos las tres primeras para cerrar el círculo.
    fotos = imagenes + imagenes[:3]

    tarjetas = ""

    for imagen in fotos:
        tarjetas += (
            '<div class="cofi-foto">'
            f'<img src="{imagen}" alt="Fotografía de café">'
            '</div>'
        )

    st.markdown(
        f"""
<div class="cofi-carrusel">
    <div class="cofi-pista">
        {tarjetas}
    </div>
</div>
""",
        unsafe_allow_html=True
    )


def mostrar_blog_inicio():
    """Sección del blog en la portada."""

    st.markdown(
        """
<div class="cofi-seccion cofi-seccion-beige">
    <div class="cofi-titulo">
        Un café siempre tiene una historia
    </div>

    <div class="cofi-intro">
        Descubre nuevos rincones, ideas y momentos
        alrededor de una buena taza de café.
    </div>
</div>
""",
        unsafe_allow_html=True
    )

    mostrar_carrusel()

    izquierda, centro, derecha = st.columns(
        [1.4, 1.2, 1.4]
    )

    with centro:
        if st.button(
            "Descubrir el blog",
            use_container_width=True
        ):
            cambiar_pagina("blog")


def mostrar_blog():
    """Página del blog de COFI."""

    st.title("Blog COFI")

    st.write(
        "Un espacio para descubrir historias, "
        "tendencias y curiosidades sobre el café."
    )

    mostrar_carrusel()

    st.subheader("Próximamente en COFI")

    columnas = st.columns(3)

    articulos = [
        (
            "El arte de preparar café",
            "Descubre distintas formas de preparar "
            "una buena taza de café."
        ),
        (
            "Cafeterías para desconectar",
            "Rincones acogedores donde disfrutar "
            "de un momento de tranquilidad."
        ),
        (
            "Cultura del café",
            "Historias y curiosidades sobre "
            "el mundo de las cafeterías."
        )
    ]

    for columna, (titulo, descripcion) in zip(
        columnas, articulos
    ):
        with columna:
            st.markdown(
                f"""
<div class="cofi-blog-tarjeta">
    <h3>{titulo}</h3>
    <p>{descripcion}</p>
    <small>Artículo próximamente</small>
</div>
""",
                unsafe_allow_html=True
            )
