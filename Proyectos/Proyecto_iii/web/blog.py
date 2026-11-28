
"""Blog y galería automática de COFI."""

import base64
from pathlib import Path

import streamlit as st

from web.navegacion import cambiar_pagina


def cargar_fotografias():
    """Carga las ocho fotografías de la galería."""

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
    """Muestra tres fotografías con movimiento automático."""

    imagenes = cargar_fotografias()

    if len(imagenes) < 3:
        st.info(
            "Añade al menos tres imágenes en "
            "static/galeria para mostrar el carrusel."
        )
        return

    # El CSS realiza ocho desplazamientos.
    # Si hay menos de ocho fotos, repetimos las disponibles.
    originales = imagenes.copy()

    while len(imagenes) < 8:
        imagenes.append(
            originales[len(imagenes) % len(originales)]
        )

    # Repetimos las tres primeras fotografías al final
    # para que el carrusel pueda volver a empezar.
    fotos = imagenes + imagenes[:3]

    tarjetas = ""

    for imagen in fotos:
        tarjetas += f"""
        <div class="cofi-foto">
            <img src="{imagen}" alt="Fotografía de café">
        </div>
        """

    carrusel = f"""
    <div class="cofi-carrusel">
        <div class="cofi-pista">
            {tarjetas}
        </div>
    </div>
    """

    # st.html evita que las etiquetas se muestren como código
    st.html(carrusel)


def mostrar_blog_inicio():
    """Sección del blog en la página principal."""

    st.html("""
    <div class="cofi-seccion cofi-seccion-beige">
        <div class="cofi-titulo">
            Un café siempre tiene una historia
        </div>

        <div class="cofi-intro">
            Descubre nuevos rincones, ideas y momentos
            alrededor de una buena taza de café.
        </div>
    </div>
    """)

    # Carrusel de fotografías
    mostrar_carrusel()

    st.write("")

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
    """Página completa del blog de COFI."""

    st.html("""
    <div class="cofi-seccion cofi-seccion-clara">
        <div class="cofi-titulo">
            Blog COFI
        </div>

        <div class="cofi-intro">
            Un espacio para descubrir historias,
            tendencias y curiosidades sobre el café.
        </div>
    </div>
    """)

    # Carrusel automático
    mostrar_carrusel()

    st.write("")
    st.write("")

    st.html("""
    <div class="cofi-titulo">
        Próximamente en COFI
    </div>

    <div class="cofi-intro">
        Historias para disfrutar del café
        más allá de cada taza.
    </div>
    """)

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

    columnas = st.columns(3, gap="medium")

    for columna, (titulo, descripcion) in zip(
        columnas, articulos
    ):
        with columna:
            st.html(f"""
            <div class="cofi-blog-tarjeta">
                <h3>{titulo}</h3>
                <p>{descripcion}</p>
                <small>Artículo próximamente</small>
            </div>
            """)
