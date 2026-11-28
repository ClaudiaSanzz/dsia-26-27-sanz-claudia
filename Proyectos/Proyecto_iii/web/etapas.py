
"""Etapas de la plataforma COFI."""

import streamlit as st


def mostrar_etapas():
    """Muestra las tres etapas de COFI."""

    st.html("""
    <div class="cofi-etapas">

        <div class="cofi-titulo">
            Mucho más que encontrar un café
        </div>

        <div class="cofi-intro">
            Queremos conectar a los amantes del café
            con sus rincones favoritos de Madrid.
        </div>

        <div class="cofi-etapas-grid">

            <div class="cofi-etapa">
                <div class="cofi-etapa-circulo">01</div>

                <div class="cofi-etapa-tarjeta">
                    <span>DESCUBRE</span>
                    <h3>Encuentra tu lugar</h3>
                    <p>
                        Explora cafeterías de Madrid y
                        recibe recomendaciones según tus gustos.
                    </p>
                </div>
            </div>

            <div class="cofi-etapa">
                <div class="cofi-etapa-circulo">02</div>

                <div class="cofi-etapa-tarjeta">
                    <span>COMPARTE · PRÓXIMAMENTE</span>
                    <h3>Recomienda y participa</h3>
                    <p>
                        Comparte tus cafeterías favoritas
                        y ayuda a otros a descubrirlas.
                    </p>
                </div>
            </div>

            <div class="cofi-etapa">
                <div class="cofi-etapa-circulo">03</div>

                <div class="cofi-etapa-tarjeta">
                    <span>CLUB COFI · PRÓXIMAMENTE</span>
                    <h3>Consigue puntos</h3>
                    <p>
                        Participa en la comunidad,
                        sube de nivel y desbloquea beneficios.
                    </p>
                </div>
            </div>

        </div>
    </div>
    """)
