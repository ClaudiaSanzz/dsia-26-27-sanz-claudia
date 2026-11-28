
"""Tarjetas de cafeterías recomendadas."""

import html

import streamlit as st


def mostrar_resultados():
    """Muestra las recomendaciones recibidas de Flask."""

    st.html("""
    <div class="explorar-resultados-titulo">
        <h2>Tus cafeterías recomendadas</h2>
    </div>
    """)

    resultado = st.session_state.get("cofi_resultados")

    modo_actual = st.query_params.get("modo", "focus")
    modo_resultados = st.session_state.get("cofi_modo_resultados")

    if modo_resultados != modo_actual:
        resultado = None
    if resultado is None:
        st.info(
            "Elige un tipo de plan y pulsa "
            "'Encontrar mi cafetería' para descubrir "
            "tus recomendaciones."
        )
        return

    if "error" in resultado:
        st.error(resultado["error"])
        return

    cafeterias = resultado.get("recommendations", [])

    if not cafeterias:
        st.info("No hemos encontrado cafeterías para esta búsqueda.")
        return

    columnas = st.columns(3, gap="medium")

    for indice, cafe in enumerate(cafeterias[:6]):

        if not isinstance(cafe, dict):
            continue

        nombre = html.escape(
            str(cafe.get("name", "Cafetería"))
        )

        valoracion = cafe.get("valoracion_media")
        resenas = cafe.get("num_resenas")

        detalles = ""

        if valoracion is not None:
            detalles += (
                "<div class='explorar-dato'>"
                f"Valoración: {html.escape(str(valoracion))}"
                "</div>"
            )

        if resenas is not None:
            detalles += (
                "<div class='explorar-dato'>"
                f"{html.escape(str(resenas))} reseñas"
                "</div>"
            )

        tarjeta = f"""
        <div class="explorar-resultado">
            <span class="explorar-posicion">
                RECOMENDACIÓN {indice + 1}
            </span>

            <h3>{nombre}</h3>

            {detalles}
        </div>
        """

        with columnas[indice % 3]:
            st.html(tarjeta)
