
"""Análisis de reseñas de COFI."""

import streamlit as st

from web.cliente_api import ClienteAPI


def mostrar_opinion():
    """Analiza una reseña utilizando nuestra API."""

    st.title("Tu opinión importa")

    st.write(
        "Descubre cómo nuestra inteligencia artificial "
        "interpreta las opiniones de los clientes."
    )

    with st.form("form_opinion"):

        texto = st.text_area(
            "Escribe una reseña",
            placeholder=(
                "El café estaba buenísimo, "
                "el ambiente era tranquilo "
                "y la atención fue excelente."
            ),
            height=150
        )

        enviar = st.form_submit_button(
            "Analizar reseña"
        )

    if enviar:

        if not texto.strip():
            st.warning("Escribe una reseña para analizar.")
            return

        cliente = ClienteAPI()

        with st.spinner("Analizando tu reseña..."):
            resultado, error = cliente.analizar(
                texto.strip()
            )

        if error:
            st.error(error)
            st.session_state.pop("analisis", None)
            return

        st.session_state["analisis"] = resultado

    resultado = st.session_state.get("analisis")

    if resultado is None:
        return

    # Sentimiento detectado
    sentimiento = resultado.get(
        "sentiment", "No disponible"
    )

    st.subheader("Resultado del análisis")

    st.success(
        f"Sentimiento detectado: {sentimiento}"
    )

    # Características detectadas por la IA
    caracteristicas = resultado.get(
        "features", {}
    )

    if caracteristicas:
        st.subheader("Características de la reseña")

        for nombre, valor in caracteristicas.items():
            st.write(
                f"**{nombre.capitalize()}:** {valor}"
            )

    # Información técnica del servicio
    st.divider()

    st.caption(
        f"Proveedor: {resultado.get('provider', '—')} "
        f"· Modelo: {resultado.get('model', '—')} "
        f"· Latencia: {resultado.get('latency_ms', '—')} ms"
    )

    st.info(
        "Esta herramienta analiza el texto de una reseña. "
        "No publica ni guarda automáticamente la opinión "
        "como una valoración de la cafetería."
    )
