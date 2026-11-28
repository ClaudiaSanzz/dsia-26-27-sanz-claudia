
"""Página de inicio de COFI."""

import base64
from pathlib import Path

import streamlit as st

from web.navegacion import cambiar_pagina
from web.club import mostrar_club
from web.blog import mostrar_blog_inicio
from web.participacion import mostrar_participacion


def cargar_imagen(ruta):
    """Convierte una fotografía en una imagen HTML."""

    if not ruta.is_file():
        return None

    contenido = base64.b64encode(
        ruta.read_bytes()
    ).decode("ascii")

    return f"data:image/jpeg;base64,{contenido}"


def mostrar_portada():
    """Muestra la fotografía principal de COFI."""

    raiz = Path(__file__).resolve().parent.parent
    ruta = raiz / "static" / "portada.jpg"

    imagen = cargar_imagen(ruta)

    foto = (
        f'<img src="{imagen}" alt="Cafetería acogedora">'
        if imagen else ""
    )

    st.markdown(
        f"""
<div class="cofi-hero">
    {foto}
    <div class="cofi-oscuro"></div>

    <div class="cofi-hero-texto">
        <h1>Descubre tu cafetería ideal<br>en Madrid.</h1>

        <p>
            Encuentra tu rincón favorito,
            comparte tus experiencias y ayuda a descubrir
            los mejores cafés de la ciudad.
        </p>

        <p><strong>Tu café, tu momento.</strong></p>
    </div>
</div>
""",
        unsafe_allow_html=True
    )

    st.write("")

    izquierda, centro, derecha = st.columns([1.3, 1.4, 1.3])

    with centro:
        if st.button(
            "Explorar cafeterías",
            type="primary",
            use_container_width=True
        ):
            cambiar_pagina("explorar")


def mostrar_como_funciona():
    """Explica los tres pasos de COFI."""

    st.markdown(
        """
<div class="cofi-seccion cofi-seccion-beige">
    <div class="cofi-titulo">Así funciona COFI</div>
    <div class="cofi-intro">
        Encontrar una cafetería que encaje contigo
        nunca había sido tan sencillo.
    </div>
</div>
""",
        unsafe_allow_html=True
    )

    columnas = st.columns(3)

    pasos = [
        (
            "01 · Explora",
            "Elige un plan o describe el tipo de cafetería que buscas."
        ),
        (
            "02 · Descubre",
            "Recibe recomendaciones basadas en reseñas reales."
        ),
        (
            "03 · Comparte",
            "Analiza una opinión y descubre qué valoran otros clientes."
        )
    ]

    for columna, (titulo, descripcion) in zip(columnas, pasos):
        with columna:
            st.markdown(
                f"""
<div class="cofi-paso">
    <strong>{titulo}</strong>
    <p>{descripcion}</p>
</div>
""",
                unsafe_allow_html=True
            )


def mostrar_inicio():
    """Reúne todas las secciones de la página principal."""

    mostrar_portada()
    mostrar_club()
    mostrar_como_funciona()
    mostrar_blog_inicio()
    mostrar_participacion()
