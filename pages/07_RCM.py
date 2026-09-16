# -*- coding: utf-8 -*-

import streamlit as st
from utils.theme import aplicar_tema_udea, encabezado_pagina

st.set_page_config(
    page_title="RCM | METRO_RCM",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)
aplicar_tema_udea(marca_agua=True)

encabezado_pagina(
    "Reliability Centered Maintenance",
    "Flujo metodológico desde la función del activo hasta la decisión de mantenimiento.",
    "🔍",
)

col1, col2 = st.columns([1.3, 1], gap="large")

with col1:
    with st.container(border=True):
        st.markdown("### 🔄 Flujo de análisis")
        st.code(
            """Activo
  ↓
Función
  ↓
Falla funcional
  ↓
Modo de falla
  ↓
Efecto
  ↓
Consecuencia
  ↓
Decisión RCM
  ↓
Tarea de mantenimiento""",
            language="text",
        )

with col2:
    with st.container(border=True):
        st.markdown("### 🎯 Consecuencias")
        for x in ["Seguridad", "Ambiental", "Operacional", "Económica", "No operacional"]:
            st.markdown(f"• **{x}**")

with st.container(border=True):
    st.markdown("### Estado metodológico")
    st.info(
        "El módulo quedará conectado a la jerarquía técnica y a la base de fallas. "
        "No se generarán modos de falla definitivos sin evidencia técnica o documental."
    )
