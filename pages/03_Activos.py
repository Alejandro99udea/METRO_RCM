# -*- coding: utf-8 -*-

import streamlit as st
from data.metro_data import LINEAS, TRANVIA
from utils.theme import aplicar_tema_udea, encabezado_pagina

st.set_page_config(
    page_title="Gestión de Activos | METRO_RCM",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)
aplicar_tema_udea(marca_agua=True)

encabezado_pagina(
    "Gestión de Activos",
    "Jerarquía técnica, sistemas, subsistemas y componentes del sistema Metro.",
    "🏗️",
)

st.markdown(
    """
    <div class="section-intro">
        <div class="section-kicker">ARQUITECTURA DE ACTIVOS</div>
        <div class="section-title">Explorador de jerarquía técnica</div>
        <div class="section-description">
            La navegación parte del modo de transporte y desciende hacia el nivel
            de sistema, subsistema, equipo y componente para soportar el análisis RCM.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

linea = st.selectbox("Seleccione una línea o modo de transporte", list(LINEAS.keys()))

info = LINEAS[linea]

c1, c2, c3 = st.columns(3, gap="large")
with c1:
    st.metric("Modo", info.get("modo", "N/D"))
with c2:
    st.metric("Recorrido", info.get("recorrido", "N/D"))
with c3:
    st.metric("Estado", "En estructuración")

with st.container(border=True):
    st.subheader(f"Línea {linea} · arquitectura funcional")
    st.write(f"**Recorrido:** {info.get('recorrido', 'N/D')}")
    st.write(
        "La jerarquía técnica definitiva se consolidará con el inventario oficial "
        "y la documentación de activos."
    )

if linea == "T":
    col1, col2 = st.columns([1.4, 1], gap="large")
    with col1:
        with st.container(border=True):
            st.markdown("### 🧩 Descomposición propuesta")
            st.code(
                """Línea T
│
├── Material rodante
├── Guiado y rodadura
├── Frenado
├── Tracción
├── Suspensión
├── Neumática
├── Puertas
├── Alimentación eléctrica
├── Control y señalización
├── Comunicaciones
├── Infraestructura de vía
└── Seguridad y emergencia""",
                language="text",
            )
    with col2:
        with st.container(border=True):
            st.markdown("### 📐 Nivel de análisis")
            st.markdown(
                """
                **Modo → Sistema → Subsistema → Equipo → Componente → Función**

                Esta estructura permite conectar la gestión de activos con las
                funciones requeridas y, posteriormente, con el análisis RCM.
                """
            )
else:
    with st.container(border=True):
        st.markdown("### Próximo nivel")
        st.info(
            "El detalle técnico de este modo se desarrollará cuando se incorpore "
            "el inventario oficial y la evidencia documental correspondiente."
        )
