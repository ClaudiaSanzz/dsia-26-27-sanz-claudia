
"""Formulario de participación en COFI."""

import streamlit as st


def mostrar_participacion():
    """Muestra el formulario para posibles colaboradores."""

    st.markdown(
        """
<div class="cofi-seccion cofi-seccion-crema">
    <div class="cofi-titulo">¿Quieres formar parte de COFI?</div>
    <div class="cofi-intro">
        ¿Tienes una cafetería o quieres colaborar
        con nuestro proyecto? Nos encantaría conocer tu idea.
    </div>
</div>
""",
        unsafe_allow_html=True
    )

    with st.form("form_participacion"):

        columna1, columna2 = st.columns(2)

        with columna1:
            nombre = st.text_input("Tu nombre")

            cafeteria = st.text_input(
                "Nombre de la cafetería (opcional)"
            )

        with columna2:
            correo = st.text_input("Correo electrónico")

            motivo = st.selectbox(
                "¿Cómo quieres participar?",
                [
                    "Quiero colaborar",
                    "Quiero proponer una cafetería",
                    "Quiero participar en la comunidad"
                ]
            )

        mensaje = st.text_area(
            "Cuéntanos tu idea",
            placeholder="Escribe aquí tu propuesta..."
        )

        enviar = st.form_submit_button(
            "Enviar propuesta"
        )

    if enviar:
        st.info(
            "Esta es una demostración visual del formulario. "
            "Todavía no se envían ni guardan los datos."
        )
