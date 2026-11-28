
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
    """Explica COFI y las ventajas de participar."""

    st.html("""
    <div class="comunidad-intro">

        <p>
            <strong>
                COFI reúne a cafeterías y amantes del café
                en una misma comunidad.
            </strong>
            Descubre nuevos rincones de Madrid gracias
            a nuestras recomendaciones inteligentes,
            comparte tus cafeterías favoritas y ayuda
            a otros a encontrar su próximo café.
            Cada votación suma 50 puntos para subir
            de nivel y desbloquear beneficios.
        </p>

        <p class="comunidad-frase">
            Porque los mejores cafés no solo se descubren,
            también se comparten.
        </p>

    </div>

    <div class="comunidad-grid">

        <div class="comunidad-tarjeta">

            <div class="comunidad-icono">
                <svg viewBox="0 0 24 24"
                     fill="none"
                     stroke="currentColor"
                     stroke-width="1.7"
                     stroke-linecap="round"
                     stroke-linejoin="round">
                    <path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z"/>
                    <circle cx="12" cy="10" r="2.5"/>
                </svg>
            </div>

            <h3>Explora cafeterías</h3>

            <p>
                Encuentra lugares increíbles para cada plan:
                estudiar, quedar con amigos o disfrutar
                de un buen café. ¡Siempre hay un nuevo
                rincón por descubrir!
            </p>

        </div>

        <div class="comunidad-tarjeta">

            <div class="comunidad-icono">
                <svg viewBox="0 0 24 24"
                     fill="none"
                     stroke="currentColor"
                     stroke-width="1.7"
                     stroke-linecap="round"
                     stroke-linejoin="round">
                    <path d="m12 2 3.1 6.4 7.1 1-5.1 5 .9 7-6-3.3-6 3.3.9-7-5.1-5 7.1-1L12 2Z"/>
                </svg>
            </div>

            <h3>Comparte tu experiencia</h3>

            <p>
                ¿Tienes una cafetería favorita?
                ¡Recomiéndala! Puntúa el ambiente,
                el servicio y el café, e inspira
                a otros con tus descubrimientos.
            </p>

        </div>

        <div class="comunidad-tarjeta">

            <div class="comunidad-icono">
                <svg viewBox="0 0 24 24"
                     fill="none"
                     stroke="currentColor"
                     stroke-width="1.7"
                     stroke-linecap="round"
                     stroke-linejoin="round">
                    <rect x="3" y="9" width="18" height="12" rx="1"/>
                    <path d="M12 9v12M3 13h18"/>
                    <path d="M12 9C7 9 5 7 6 4c1-3 6-1 6 5Z"/>
                    <path d="M12 9c5 0 7-2 6-5-1-3-6-1-6 5Z"/>
                </svg>
            </div>

            <h3>Consigue recompensas</h3>

            <p>
                ¡Tus opiniones tienen premio!
                Suma puntos, consigue insignias,
                alcanza nuevos niveles y disfruta
                de experiencias especiales en COFI.
            </p>

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
