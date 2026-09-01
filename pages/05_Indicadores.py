# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
from data.metro_data import METRO
from utils.theme import aplicar_tema_udea, encabezado_pagina

st.set_page_config(
    page_title="Indicadores | METRO_RCM",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
aplicar_tema_udea(marca_agua=True)

encabezado_pagina(
    "Indicadores",
    "Lectura integrada de desempeño financiero, demanda y madurez de gestión de activos.",
    "📊",
)

with st.container(border=True):
    st.markdown("### 💼 Desempeño financiero")
    fin = pd.DataFrame({
        "Indicador": [
            "Ingresos", "EBITDA", "Utilidad neta",
            "Activos", "PP&E neta", "Adquisiciones PP&E",
        ],
        "2025 (M COP)": [
            METRO["ingresos_2025_m"],
            METRO["ebitda_2025_m"],
            METRO["utilidad_neta_2025_m"],
            METRO["activos_2025_m"],
            METRO["ppe_neta_2025_m"],
            METRO["ppye_adquisiciones_2025_m"],
        ],
    })
    st.dataframe(fin, use_container_width=True, hide_index=True)

c = st.columns(3, gap="large")
c[0].metric("Margen EBITDA", f"{METRO['ebitda_2025_m']/METRO['ingresos_2025_m']*100:.2f} %")
c[1].metric("ROA simplificado", f"{METRO['utilidad_neta_2025_m']/METRO['activos_2025_m']*100:.2f} %")
c[2].metric("PP&E / activos", f"{METRO['ppe_neta_2025_m']/METRO['activos_2025_m']*100:.2f} %")

with st.container(border=True):
    st.markdown("### 🚇 Demanda")
    mov = pd.DataFrame(METRO["afluencia_integral_2025"]).T
    st.dataframe(mov, use_container_width=True)
    st.bar_chart(mov)

with st.container(border=True):
    st.markdown("### 🧭 Madurez de gestión de activos")
    mad = pd.DataFrame({
        "Año": list(METRO["madurez_activos"].keys()),
        "Nivel": list(METRO["madurez_activos"].values()),
    }).set_index("Año")
    st.line_chart(mad)
