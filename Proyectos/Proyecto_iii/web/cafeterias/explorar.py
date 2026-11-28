
"""Página para descubrir cafeterías en COFI."""

import base64
import html
from pathlib import Path

import streamlit as st

from starter.recommender import CafeRecommender
from web.cafeterias.cliente_api import ClienteAPI
from web.cafeterias.resultados import mostrar_resultados


# Iconos de línea, como los del boceto
ICONOS = {
    "focus": """
        <svg viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="1.6"
             stroke-linecap="round" stroke-linejoin="round">
            <rect x="4" y="4" width="16" height="12" rx="1.5"/>
            <path d="M2 20h20l-2-4H4l-2 4z"/>
        </svg>
    """,
    "social": """
        <svg viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="1.6"
             stroke-linecap="round" stroke-linejoin="round">
            <circle cx="9" cy="7" r="3"/>
            <circle cx="18" cy="8" r="2.5"/>
            <path d="M2 20v-2a7 7 0 0 1 14 0v2"/>
            <path d="M17 14a5 5 0 0 1 5 5v1"/>
        </svg>
    """,
    "trendy": """
        <svg viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="1.6"
             stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 17C2 12 7 5 12 5s10 7 8 12"/>
            <path d="M4 17c3 3 6 3 8 0 2 3 5 3 8 0"/>
            <path d="M12 5v12M8 7l2 9M16 7l-2 9"/>
        </svg>
    """,
    "surprise": """
        <svg viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="1.6"
             stroke-linecap="round" stroke-linejoin="round">
            <path d="m9 2 1.8 5.2L16 9l-5.2 1.8L9 16l-1.8-5.2L2 9l5.2-1.8L9 2z"/>
            <path d="m18 13 1.2 3.8L23 18l-3.8 1.2L18 23l-1.2-3.8L13 18l3.8-1.2L18 13z"/>
        </svg>
    """
}


MODOS = [
    {
        "id": "focus",
        "titulo": "Para estudiar",
        "descripcion": (
            "Cafeterías tranquilas, con buen ambiente, "
            "enchufes y Wi-Fi."
        ),
        "imagen": "estudiar.jpg",
        "alternativa": "03.jpg"
    },
    {
        "id": "social",
        "titulo": "Plan social",
        "descripcion": (
            "Cafeterías acogedoras para charlar, "
            "ponerse al día y compartir un café."
        ),
        "imagen": "social.jpg",
        "alternativa": "06.jpg"
    },
    {
        "id": "trendy",
        "titulo": "Brunch & relax",
        "descripcion": (
            "Un buen brunch, ambiente relajado "
            "y tiempo sin prisas."
        ),
        "imagen": "brunch.jpg",
        "alternativa": "07.jpg"
    },
    {
        "id": "surprise",
        "titulo": "Déjate sorprender",
        "descripcion": (
            "Descubre cafeterías especiales, "
            "diferentes y con mucho encanto."
        ),
        "imagen": "sorpresa.jpg",
        "alternativa": "08.jpg"
    }
]


def cargar_imagen(modo):
    """Carga la foto del modo o una foto de la galería."""

    raiz = Path(__file__).resolve().parent.parent.parent
    ruta = raiz / "static" / "cafeterias" / modo["imagen"]

    if not ruta.is_file():
        ruta = raiz / "static" / "galeria" / modo["alternativa"]

    if not ruta.is_file():
        return ""

    contenido = base64.b64encode(
        ruta.read_bytes()
    ).decode("ascii")

    return f"data:image/jpeg;base64,{contenido}"


def mostrar_encabezado():
    """Muestra el título y el subtítulo."""

    st.html("""
    <div class="explorar-encabezado">
        <h1>Encuentra tu cafetería ideal</h1>
        <p>
            Elige el tipo de plan de café que te apetece hoy
            y descubre cafeterías de Madrid que encajan contigo.
        </p>
    </div>
    """)


def mostrar_tarjetas():
    """Muestra las cuatro tarjetas seleccionables."""

    modo_actual = st.query_params.get("modo", "focus")
    columnas = st.columns(4, gap="medium")

    for columna, modo in zip(columnas, MODOS):
        imagen = cargar_imagen(modo)

        seleccionado = (
            "explorar-seleccionado"
            if modo_actual == modo["id"]
            else ""
        )

        titulo = html.escape(modo["titulo"])
        descripcion = html.escape(modo["descripcion"])
        icono = ICONOS[modo["id"]]

        tarjeta = f"""
        <a class="explorar-tarjeta {seleccionado}"
           href="?pagina=explorar&amp;modo={modo['id']}">

            <div class="explorar-foto">
                <img src="{imagen}" alt="{titulo}">
            </div>

            <div class="explorar-tarjeta-texto">

                <div class="explorar-tarjeta-cabecera">
                    <div class="explorar-icono">
                        {icono}
                    </div>
                    <h3>{titulo}</h3>
                </div>

                <p>{descripcion}</p>

                <span class="explorar-flecha">
                    →
                </span>

            </div>
        </a>
        """

        with columna:
            st.html(tarjeta)

    return modo_actual


def obtener_preferencias(modo):
    """Obtiene opciones válidas para la API."""

    opciones = CafeRecommender().options
    disponibles = opciones.get(modo, [])

    return list(disponibles)[:2]



def mostrar_buscador(modo):
    """Permite elegir preferencias y buscar cafeterías."""

    # Opciones reales definidas en nuestro recomendador
    opciones = CafeRecommender().options
    disponibles = list(opciones.get(modo, []))

    izquierda, centro, derecha = st.columns([1, 8, 1])

    with centro:
        with st.form("form_busqueda_cafeterias"):

            # Preferencias propias del modo elegido
            preferencias = st.multiselect(
                "¿Qué valoras más?",
                options=disponibles,
                placeholder="Selecciona tus preferencias",
                key=f"preferencias_{modo}"
            )

            # Búsqueda personalizada
            texto = st.text_input(
                "¿Buscas algo más concreto?",
                placeholder=(
                    "Ejemplo: matcha, enchufes, terraza, Chamberí..."
                ),
            )

            espacio1, boton, espacio2 = st.columns(
                [1.4, 1.2, 1.4]
            )

            with boton:
                buscar = st.form_submit_button(
                    "Encontrar mi cafetería",
                    type="primary",
                    use_container_width=True
                )

    if buscar:

        if not preferencias and not texto.strip():
            st.warning(
                "Selecciona alguna preferencia o escribe "
                "qué tipo de cafetería estás buscando."
            )
            return

        with st.spinner("Buscando tu cafetería ideal..."):
            cliente = ClienteAPI()

            if texto.strip():
                # Búsqueda en lenguaje natural
                descripciones = {
                    "focus": "para estudiar o trabajar",
                    "social": "para quedar con amigos",
                    "trendy": "para disfrutar de un brunch",
                    "surprise": "para descubrir algo diferente"
                }

                descripcion = descripciones.get(modo, "")

                # Incluimos también las preferencias elegidas
                detalles = ", ".join(preferencias)

                busqueda = (
                    f"Busco una cafetería {descripcion}. "
                    f"Mis preferencias son: {detalles}. "
                    f"Además, quiero: {texto.strip()}."
                )

                resultado = cliente.recomendar(
                    modo=modo,
                    texto=busqueda
                )

            else:
                # Búsqueda mediante preferencias del modelo
                resultado = cliente.recomendar(
                    modo=modo,
                    preferencias=preferencias
                )

        st.session_state["cofi_resultados"] = resultado
        st.session_state["cofi_modo_resultados"] = modo


def mostrar_explorar():
    """Construye la página Cafeterías."""

    with st.container(key="cofi_pagina_cafeterias"):
        mostrar_encabezado()
        modo = mostrar_tarjetas()
        mostrar_buscador(modo)
        mostrar_resultados()
