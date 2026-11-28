
"""Monitorización del sistema COFI."""

import streamlit as st

from web.cliente_api import ClienteAPI


def mostrar_monitorizacion():
    """Comprueba el estado de nuestra API Flask."""

    st.title("Estado del sistema")

    st.write(
        "Consulta el funcionamiento de los servicios "
        "que utiliza COFI."
    )

    if st.button("Actualizar estado"):
        st.rerun()

    cliente = ClienteAPI()

    resultado, error = cliente.comprobar_estado()

    if error:
        st.error(error)
        return

    if resultado is None:
        st.warning("No hay información del servicio.")
        return

    # Estado general
    estado = resultado.get("status", "unknown")

    if estado == "ok":
        st.success("Todos los servicios están disponibles.")
    else:
        st.warning(
            "El sistema presenta alguna incidencia."
        )

    # Comprobaciones individuales
    st.subheader("Comprobaciones")

    comprobaciones = resultado.get("checks", {})

    nombres = {
        "api": "API Flask",
        "data": "Dataset de cafeterías",
        "model": "Modelo de sentimiento",
        "vectorizer": "Vectorizador"
    }

    for clave, disponible in comprobaciones.items():

        nombre = nombres.get(clave, clave)

        if disponible:
            st.write(f"✅ {nombre}: disponible")
        else:
            st.write(f"❌ {nombre}: no disponible")

    # Respuesta completa para supervisión
    with st.expander("Ver respuesta de la API"):
        st.json(resultado)
