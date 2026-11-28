
"""Blog y carrusel automático de COFI."""

import base64
from pathlib import Path

import streamlit as st

from web.navegacion import cambiar_pagina


def cargar_fotografias():
    """Carga las ocho imágenes de static/galeria."""

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
    """Muestra un carrusel continuo de fotografías."""

    imagenes = cargar_fotografias()

    if len(imagenes) < 3:
        st.warning(
            "Necesitamos al menos tres fotografías "
            "en static/galeria."
        )
        return

    # Duplicamos las imágenes para crear el efecto circular.
    imagenes = imagenes + imagenes

    fotos_html = ""

    for imagen in imagenes:
        fotos_html += f"""
        <div class="cofi-blog-slide">
            <img src="{imagen}" alt="Fotografía de café">
        </div>
        """

    st.html(f"""
    <div class="cofi-blog-carousel">
        <div class="cofi-blog-track">
            {fotos_html}
        </div>
    </div>
    """)


def mostrar_blog_inicio():
    """Sección del blog en la portada."""

    st.html("""
    <div class="cofi-blog-encabezado">
        <h2>Cada taza de café esconde una historia</h2>

        <p>
            Descubre curiosidades, inspiración y rincones
            con alma cafetera. Hay todo un mundo detrás de
            cada taza esperando a que lo descubras.
        </p>
    </div>
    """)

    mostrar_carrusel()

    izquierda, centro, derecha = st.columns(
        [1.4, 1.2, 1.4]
    )

    with centro:
        if st.button(
            "Descubrir el blog",
            use_container_width=True,
            key="abrir_blog_inicio"
        ):
            cambiar_pagina("blog")


def mostrar_blog():
    """Página principal del blog."""

    st.html("""
    <div class="cofi-blog-encabezado">
        <h2>Descubre el universo del café</h2>

        <p>
            Desde cómo se prepara un espresso perfecto
            hasta los rincones más acogedores para
            disfrutar de una buena taza.
        </p>
    </div>
    """)

    mostrar_carrusel()

    st.subheader("Historias para descubrir")

    articulos = [
        (
            "El arte de preparar café",
            "Descubre distintas formas de preparar "
            "una buena taza de café."
        ),
        (
            "Cafeterías para desconectar",
            "Los rincones más acogedores para "
            "disfrutar de un momento de tranquilidad."
        ),
        (
            "La cultura del café",
            "Curiosidades y tradiciones que hacen "
            "especial cada taza."
        )
    ]

    columnas = st.columns(3)

    for columna, (titulo, descripcion) in zip(
        columnas, articulos
    ):
        with columna:
            st.html(f"""
            <div class="cofi-blog-tarjeta">
                <h3>{titulo}</h3>
                <p>{descripcion}</p>
                <small>Artículo en preparación</small>
            </div>
            """)
