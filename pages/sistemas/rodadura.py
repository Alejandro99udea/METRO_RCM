# -*- coding: utf-8 -*-

import streamlit as st


def mostrar_rodadura():
    """Renderiza el módulo técnico del sistema de rodadura."""

    st.subheader("🛞 Sistema de rodadura")

    st.markdown(
        """
        El sistema de rodadura constituye uno de los sistemas
        identificados para el análisis técnico y posterior estudio RCM
        de la Línea T — Tranvía de Ayacucho.
        """
    )

    st.divider()

    # ============================================================
    # FUNCIÓN
    # ============================================================

    st.markdown("### 1. Función del sistema")

    st.info(
        """
        La función operacional definitiva del sistema deberá establecerse
        a partir de la documentación técnica disponible del vehículo,
        los estándares de desempeño requeridos y la información del
        fabricante.

        En esta fase se mantiene como información preliminar y no se
        presenta todavía como una función RCM definitiva.
        """
    )

    # ============================================================
    # ESTRUCTURA
    # ============================================================

    st.markdown("### 2. Estructura preliminar")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 🛞 Rodadura")
        st.write(
            "Elementos relacionados con la interacción del vehículo "
            "con la vía y la rodadura."
        )

    with col2:
        st.markdown("#### 🧭 Guiado")
        st.write(
            "Elementos asociados al mantenimiento de la trayectoria "
            "del vehículo."
        )

    with col3:
        st.markdown("#### ⚙️ Componentes")
        st.write(
            "Componentes específicos que deberán definirse mediante "
            "la documentación técnica del activo."
        )

    st.divider()

    # ============================================================
    # INFORMACIÓN DISPONIBLE
    # ============================================================

    st.markdown("### 3. Información disponible")

    disponible = [
        "Sistema identificado dentro del contexto operacional de la Línea T.",
        "Configuración de rodadura con neumáticos.",
        "Interacción con infraestructura de guiado.",
        "Condiciones de operación urbana de alta frecuencia.",
    ]

    for item in disponible:
        st.markdown(f"- {item}")

    st.divider()

    # ============================================================
    # INFORMACIÓN PENDIENTE
    # ============================================================

    st.markdown("### 4. Información técnica pendiente")

    pendiente = [
        "Inventario detallado del sistema.",
        "Fabricante y modelo de los componentes.",
        "Fichas técnicas.",
        "Planos y despieces.",
        "Históricos de fallas.",
        "Históricos de mantenimiento.",
        "MTBF.",
        "MTTR.",
        "Costos asociados a las fallas.",
    ]

    for item in pendiente:
        st.markdown(f"- {item}")

    st.warning(
        """
        La información pendiente no será sustituida por supuestos.
        Se incorporará cuando dispongamos de documentación técnica
        o registros verificables.
        """
    )

    st.divider()

    # ============================================================
    # ESTRUCTURA RCM
    # ============================================================

    st.markdown("### 5. Estructura para el análisis RCM")

    st.code(
        """
FUNCIÓN
   ↓
FALLA FUNCIONAL
   ↓
MODO DE FALLA
   ↓
EFECTO
   ↓
CONSECUENCIA
   ↓
TAREA DE MANTENIMIENTO
        """,
        language="text",
    )

    st.info(
        """
        Este módulo está preparado para incorporar posteriormente
        la información funcional y de fallas una vez se disponga
        de la documentación técnica e histórica necesaria.
        """
    )