# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
from data.metro_data import METRO
from utils.theme import aplicar_tema_udea, encabezado_pagina

st.set_page_config(
    page_title="Mantenimiento | METRO_RCM",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)
aplicar_tema_udea(marca_agua=True)

encabezado_pagina(
    "Mantenimiento y confiabilidad",
    "Estrategias, indicadores y evolución de la gestión del mantenimiento.",
    "🔧",
)

c = st.columns(4, gap="large")
c[0].metric("Mantenimiento / planta", f"{METRO['mantenimiento_pct_planta']} %")
c[1].metric("Plan 2025", "$239.000 M")
c[2].metric(
    "Modos de falla 2016",
    f"{METRO['mantenimiento']['modos_falla_2016']:,}".replace(",", "."),
)
c[3].metric(
    "Modos de falla 2024",
    f"{METRO['mantenimiento']['modos_falla_2024']:,}".replace(",", "."),
)

col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container(border=True):
        st.markdown("### 🛠️ Modalidades de mantenimiento")
        st.write(" · ".join(METRO["mantenimiento"]["modalidades"]))

with col2:
    with st.container(border=True):
        st.markdown("### 📈 Evolución de modos de falla monitoreados")
        fallas = pd.DataFrame({"Modos": [5000, 20000]}, index=[2016, 2024])
        st.bar_chart(fallas)

with st.container(border=True):
    st.markdown("### 📊 Regularidad de la Línea A")
    regularidad = pd.DataFrame({"Regularidad": [96.71, 94.67]}, index=[2022, 2023])
    st.line_chart(regularidad)

st.info(
    "El documento no contiene una base suficiente para calcular MTBF y MTTR por activo. "
    "Esos indicadores se calcularán cuando incorporemos históricos de órdenes de trabajo y fallas."
)
