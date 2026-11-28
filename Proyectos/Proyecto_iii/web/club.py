
"""Sistema de puntos y niveles del Club COFI."""

import streamlit as st


def mostrar_club():
    """Muestra los cuatro niveles previstos de COFI."""

    st.html("""
    <div class="cofi-seccion cofi-seccion-clara">
        <div class="cofi-titulo">
            Sistema de Puntos y Niveles
        </div>

        <div class="cofi-intro">
            Descubre los cuatro niveles de nuestra futura
            comunidad de amantes del café.
        </div>
    </div>
    """)

    niveles = [
        (
            "01",
            "Coffee Lover",
            "0 - 200 puntos",
            "Comienza tu aventura descubriendo cafeterías.",
            "Recomendaciones personalizadas",
            "#F5E7D4"
        ),
        (
            "02",
            "Coffee Explorer",
            "200 - 500 puntos",
            "Explora nuevos rincones y comparte tus impresiones.",
            "Selecciones destacadas",
            "#E9DDC5"
        ),
        (
            "03",
            "Coffee Master",
            "500 - 1000 puntos",
            "Tus opiniones ayudan a descubrir grandes cafeterías.",
            "Reconocimiento de la comunidad",
            "#E1D5C7"
        ),
        (
            "04",
            "Coffee Legend",
            "Más de 1000 puntos",
            "Tus recomendaciones inspiran a otros amantes del café.",
            "Distintivo especial",
            "#D7C6B3"
        )
    ]

    columnas = st.columns(4, gap="medium")

    for columna, nivel in zip(columnas, niveles):

        numero, titulo, puntos, descripcion, beneficio, color = nivel

        with columna:
            tarjeta = f"""
            <div class="cofi-tarjeta"
                 style="background-color: {color};">

                <small>NIVEL {numero}</small>

                <h3>{titulo}</h3>

                <div class="cofi-puntos">
                    {puntos}
                </div>

                <p>{descripcion}</p>

                <div class="cofi-beneficio">
                    <strong>Beneficio previsto</strong>
                    <p>{beneficio}</p>
                </div>

            </div>
            """

            st.html(tarjeta)

    st.write("")

    izquierda, centro, derecha = st.columns(
        [1.4, 1.2, 1.4]
    )

    with centro:
        if st.button(
            "Conocer el Club COFI",
            use_container_width=True
        ):
            st.info(
                "El sistema de puntos y recompensas "
                "todavía no está activo."
            )
