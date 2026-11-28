
"""Página principal de COFI."""

import base64
from pathlib import Path

import streamlit as st

from web.navegacion import cambiar_pagina
from web.club import mostrar_club
from web.etapas import mostrar_etapas
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
    """Muestra la portada principal de COFI."""

    raiz = Path(__file__).resolve().parent.parent
    ruta = raiz / "static" / "portada.jpg"

    imagen = cargar_imagen(ruta)

    foto = (
        f'<img src="{imagen}" alt="Cafetería acogedora">'
        if imagen else ""
    )

    st.html(f"""
    <div class="cofi-hero">
        {foto}

        <div class="cofi-oscuro"></div>

        <div class="cofi-hero-texto">

            <div class="cofi-hero-superior">
                Encuentra en Madrid tu
            </div>

            <h1>Cafetería Ideal</h1>

            <h2>Tu café, tu momento.</h2>

            <p>
                Descubre, compara y encuentra
                el rincón perfecto para cada ocasión.
            </p>

        </div>
    </div>
    """)

    st.write("")

    izquierda, centro, derecha = st.columns(
        [1.3, 1.4, 1.3]
    )

    with centro:
        if st.button(
            "Explorar cafeterías",
            type="primary",
            use_container_width=True
        ):
            cambiar_pagina("explorar")


def mostrar_como_funciona():
    """Explica la propuesta de COFI y su comunidad."""

    st.html("""
    <div class="cofi-comunidad">

        <div class="cofi-comunidad-texto">

            <p>
                <strong>
                    COFI es mucho más que un buscador de cafeterías.
                </strong>
                Es un espacio pensado para conectar a quienes
                disfrutan descubriendo nuevos rincones de Madrid.
            </p>

            <p>
                Nuestra plataforma utiliza reseñas y recomendaciones
                inteligentes para ayudarte a encontrar tu cafetería
                ideal. Pero queremos ir un paso más allá:
                que tú también puedas recomendar tus lugares
                favoritos, compartir tus experiencias y ayudar
                a otras personas a encontrar su próximo café.
            </p>

            <p>
                En el futuro Club COFI, cada participación
                podrá sumar puntos para avanzar de nivel,
                conseguir insignias y acceder a beneficios
                dentro de nuestra comunidad.
            </p>

            <p class="cofi-comunidad-frase">
                Porque los mejores cafés se descubren juntos.
            </p>

        </div>

        <div class="cofi-comunidad-grid">

            <div class="cofi-comunidad-tarjeta">
                <div class="cofi-comunidad-icono">📍</div>
                <h3>Explora cafeterías</h3>
                <p>
                    Descubre nuevos espacios de Madrid
                    adaptados a tus gustos y a cada momento.
                </p>
            </div>

            <div class="cofi-comunidad-tarjeta">
                <div class="cofi-comunidad-icono">⭐</div>
                <h3>Comparte tu experiencia</h3>
                <p>
                    Próximamente podrás recomendar cafeterías,
                    publicar tus opiniones y ayudar a otros
                    usuarios a descubrir sus favoritos.
                </p>
            </div>

            <div class="cofi-comunidad-tarjeta">
                <div class="cofi-comunidad-icono">🎁</div>
                <h3>Consigue recompensas</h3>
                <p>
                    Nuestro futuro sistema de puntos permitirá
                    avanzar de nivel y acceder a beneficios
                    por participar en la comunidad.
                </p>
            </div>

        </div>

    </div>
    """)


def mostrar_inicio():
    """Reúne todas las secciones de Inicio."""

    mostrar_portada()

    # 1. Beige: Club COFI
    with st.container(key="cofi_club"):
        mostrar_club()

    # 2. Marfil: etapas
    with st.container(key="cofi_etapas"):
        mostrar_etapas()

    # 3. Beige: explicación y tarjetas
    with st.container(key="cofi_como"):
        mostrar_como_funciona()

    # 4. Marfil: blog
    with st.container(key="cofi_blog"):
        mostrar_blog_inicio()

    # 5. Beige: participación
    with st.container(key="cofi_participa"):
        mostrar_participacion()
