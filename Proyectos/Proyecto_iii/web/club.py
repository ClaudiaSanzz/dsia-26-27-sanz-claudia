
"""Sistema de puntos y niveles de COFI."""

import streamlit as st


def mostrar_club():
    """Muestra los cuatro niveles del Club COFI."""

    niveles = [
        {
            "numero": "01",
            "nombre": "Coffee Lover",
            "puntos": "0 - 200 puntos",
            "descripcion": (
                "¡Tu aventura cafetera comienza aquí! "
                "Descubre rincones increíbles, encuentra "
                "nuevos favoritos y empieza a dejar tu huella."
            ),
            "recompensa": "Acceso a sorteos básicos.",
            "color": "#F5E7D4"
        },
        {
            "numero": "02",
            "nombre": "Coffee Explorer",
            "puntos": "200 - 500 puntos",
            "descripcion": (
                "¡Ya eres todo un explorador! Comparte tus "
                "descubrimientos y ayuda a otros a encontrar "
                "auténticas joyas cafeteras."
            ),
            "recompensa": (
                "Acceso a sorteos y descuentos "
                "en cafeterías colaboradoras."
            ),
            "color": "#E9DDC5"
        },
        {
            "numero": "03",
            "nombre": "Coffee Master",
            "puntos": "500 - 1000 puntos",
            "descripcion": (
                "¡Tu criterio marca la diferencia! "
                "Tus recomendaciones inspiran a la comunidad "
                "y dan visibilidad a grandes cafeterías."
            ),
            "recompensa": (
                "Acceso a sorteos exclusivos "
                "y eventos de COFI."
            ),
            "color": "#E1D5C7"
        },
        {
            "numero": "04",
            "nombre": "Coffee Legend",
            "puntos": "Más de 1000 puntos",
            "descripcion": (
                "¡Has llegado a la élite del café! "
                "Eres una referencia para otros amantes "
                "del café y tus opiniones marcan tendencia."
            ),
            "recompensa": "Promociones VIP.",
            "color": "#D7C6B3"
        }
    ]

    st.html("""
    <div class="club-encabezado">
        <h2>Sistema de Puntos y Niveles</h2>
        <p>
            ¡Cada votación suma <strong>50 puntos</strong>!
            Comparte tus cafeterías favoritas, ayuda a otros
            amantes del café y desbloquea cada vez más
            beneficios mientras avanzas de nivel.
        </p>
    </div>
    """)

    columnas = st.columns(4, gap="medium")

    for columna, nivel in zip(columnas, niveles):
        with columna:
            st.html(f"""
            <div class="club-tarjeta"
                 style="background-color: {nivel['color']};">

                <div class="club-numero">
                    NIVEL {nivel['numero']}
                </div>

                <h3>{nivel['nombre']}</h3>

                <div class="club-puntos">
                    {nivel['puntos']}
                </div>

                <p class="club-descripcion">
                    {nivel['descripcion']}
                </p>

                <div class="club-beneficio">
                    <strong>Tu recompensa</strong>
                    <p>{nivel['recompensa']}</p>
                </div>

            </div>
            """)
        # Botón de registro del Club COFI
    st.write("")

    izquierda, centro, derecha = st.columns([1.5, 1, 1.5])

    with centro:
        if st.button(
            "Registrarse ahora",
            key="registro_club",
            use_container_width=True
        ):
            st.session_state["mostrar_registro"] = True

    if st.session_state.get("mostrar_registro", False):
        with st.form("form_registro_club"):
            st.subheader("Únete a COFI")

            nombre = st.text_input("Tu nombre")
            correo = st.text_input("Correo electrónico")

            enviar = st.form_submit_button("Crear mi cuenta")

            if enviar:
                st.info(
                    "Este formulario es una demostración visual. "
                    "El registro de usuarios todavía no está conectado."
                )