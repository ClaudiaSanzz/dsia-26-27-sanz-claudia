
"""Exploración y recomendaciones de cafeterías."""

import streamlit as st

from web.cliente_api import ClienteAPI


MODOS = {
    "Focus · Estudiar o trabajar": (
        "focus",
        {
            "Ambiente tranquilo": "quiet",
            "Estudiar o trabajar": "work"
        }
    ),
    "Social · Compartir un café": (
        "social",
        {
            "Conversar": "chat",
            "Ir con amigos": "friends"
        }
    ),
    "Trendy · Nuevas tendencias": (
        "trendy",
        {
            "Café o matcha": "coffee",
            "Brunch": "brunch"
        }
    ),
    "Sorpresa · Nuevos rincones": (
        "surprise",
        {
            "Sitios originales": "original",
            "Sitios poco conocidos": "hidden"
        }
    )
}


def mostrar_recomendaciones(resultado):
    """Muestra las cafeterías que devuelve Flask."""

    if resultado is None:
        return

    cafeterias = resultado.get("recommendations", [])

    if not cafeterias:
        st.info("No se encontraron cafeterías.")
        return

    st.subheader("Tus cafeterías recomendadas")

    for posicion, cafe in enumerate(cafeterias, 1):

        with st.container(border=True):

            st.subheader(
                f"{posicion}. {cafe.get('name', 'Cafetería')}"
            )

            col1, col2, col3 = st.columns(3)

            valoracion = cafe.get("valoracion_media")
            numero = cafe.get("num_resenas")
            compatibilidad = cafe.get("compatibilidad")

            with col1:
                if isinstance(valoracion, (float, int)):
                    st.metric(
                        "Valoración",
                        f"{valoracion:.2f}/5"
                    )
                else:
                    st.metric("Valoración", "—")

            with col2:
                st.metric(
                    "Reseñas",
                    numero if numero is not None else "—"
                )

            with col3:
                if isinstance(
                    compatibilidad, (float, int)
                ):
                    st.metric(
                        "Compatibilidad",
                        f"{compatibilidad * 100:.1f}%"
                    )
                else:
                    st.metric("Compatibilidad", "—")

            if cafe.get("explanation"):
                st.write(cafe["explanation"])

    if resultado.get("latency_ms") is not None:
        st.caption(
            f"Tiempo de respuesta: "
            f"{resultado['latency_ms']} ms"
        )


def mostrar_explorar():
    """Página para buscar cafeterías personalizadas."""

    st.title("Encuentra tu cafetería ideal")

    st.write(
        "Cada plan necesita su cafetería. "
        "Cuéntanos qué te apetece hacer y descubre "
        "los mejores rincones de Madrid para ti."
    )

    cliente = ClienteAPI()

    with st.form("form_explorar"):

        elegido = st.selectbox(
            "¿Qué plan tienes hoy?",
            list(MODOS.keys())
        )

        modo, opciones = MODOS[elegido]

        preferencias = st.multiselect(
            "¿Qué valoras más?",
            list(opciones.keys()),
            default=list(opciones.keys())[:1]
        )

        enviar = st.form_submit_button(
            "Encontrar mi cafetería"
        )

    if enviar:

        if not preferencias:
            st.warning(
                "Selecciona al menos una preferencia."
            )
        else:
            seleccionadas = [
                opciones[p] for p in preferencias
            ]

            with st.spinner(
                "Buscando cafeterías para ti..."
            ):
                resultado, error = cliente.recomendar(
                    modo,
                    seleccionadas
                )

            if error:
                st.error(error)
            else:
                st.session_state["recomendaciones"] = (
                    resultado
                )

    mostrar_recomendaciones(
        st.session_state.get("recomendaciones")
    )
