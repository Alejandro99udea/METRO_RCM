# -*- coding: utf-8 -*-

import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Monitoreo Ambiental | METRO_RCM",
    page_icon="📡",
    layout="wide",
)


# ============================================================
# CABECERA
# ============================================================

st.markdown(
    """
    <div class="metro-header">

        <div class="metro-header-title">
            📡 MONITOREO AMBIENTAL
        </div>

        <div class="metro-header-subtitle">
            SIATA · Condiciones hidrometeorológicas
            del Valle de Aburrá
        </div>

    </div>

    <div class="metro-accent"></div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# INTRODUCCIÓN
# ============================================================

st.title("Monitoreo ambiental")

st.write(
    """
    Este módulo integra información pública del Sistema de Alerta
    Temprana de Medellín y el Valle de Aburrá (SIATA) para consultar
    condiciones hidrometeorológicas y productos de monitoreo
    ambiental relevantes para la operación y gestión de activos.
    """
)


# ============================================================
# ESTADO DE FUENTE
# ============================================================

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Fuente",
        "SIATA"
    )

with c2:
    st.metric(
        "Cobertura",
        "Valle de Aburrá"
    )

with c3:
    st.metric(
        "Consulta",
        datetime.now().strftime("%d/%m/%Y %H:%M")
    )


# ============================================================
# TABS
# ============================================================

tabs = st.tabs(
    [
        "🌦️ SIATA en tiempo real",
        "🌧️ Precipitación",
        "🌡️ Variables meteorológicas",
        "🗺️ Radar",
        "⚙️ Impacto sobre activos",
        "ℹ️ Fuente",
    ]
)


# ============================================================
# SIATA EN TIEMPO REAL
# ============================================================

with tabs[0]:

    st.subheader(
        "Portal de monitoreo SIATA"
    )

    st.write(
        """
        El portal oficial de SIATA ofrece visualizaciones de
        monitoreo en tiempo real para el Valle de Aburrá.
        """
    )

    components.iframe(
        "https://siata.gov.co/portal_dividido/",
        height=850,
        scrolling=True,
    )

    st.caption(
        "Fuente: Sistema de Alerta Temprana de Medellín — SIATA."
    )


# ============================================================
# PRECIPITACIÓN
# ============================================================

with tabs[1]:

    st.subheader(
        "Monitoreo de precipitación"
    )

    st.write(
        """
        SIATA publica información de estaciones pluviométricas
        y acumulados de precipitación en diferentes horizontes
        temporales.
        """
    )

    components.iframe(
        "https://www.siata.gov.co/boletinnp.php",
        height=850,
        scrolling=True,
    )

    st.info(
        """
        La información mostrada corresponde al monitoreo publicado
        por SIATA. Para el análisis de mantenimiento, estos datos
        deben interpretarse como condiciones ambientales del entorno
        operacional, no como mediciones internas del Metro.
        """
    )


# ============================================================
# VARIABLES METEOROLÓGICAS
# ============================================================

with tabs[2]:

    st.subheader(
        "Variables meteorológicas"

    )

    st.write(
        """
        SIATA publica series gráficas de estaciones meteorológicas
        para variables como:
        temperatura, humedad, presión atmosférica y velocidad
        del viento.
        """
    )

    componentes = [
        "Temperatura",
        "Humedad",
        "Presión",
        "Velocidad del viento",
    ]

    variable = st.selectbox(
        "Seleccione una variable",
        componentes,
    )

    urls = {

        "Temperatura":
            "https://www.siata.gov.co/meteorologia/Geoportal/meteos/Figuras/24h/",

        "Humedad":
            "https://www.siata.gov.co/meteorologia/Geoportal/meteos/Figuras/24h/",

        "Presión":
            "https://www.siata.gov.co/meteorologia/Geoportal/meteos/Figuras/24h/",

        "Velocidad del viento":
            "https://www.siata.gov.co/meteorologia/Geoportal/meteos/Figuras/24h/",
    }

    components.iframe(
        urls[variable],
        height=800,
        scrolling=True,
    )


# ============================================================
# RADAR
# ============================================================

with tabs[3]:

    st.subheader(
        "Radar meteorológico"
    )

    st.write(
        """
        SIATA dispone de productos de radar meteorológico y
        visualizaciones de precipitación para el Valle de Aburrá.
        """
    )

    components.iframe(
        "https://siata.gov.co/portal_dividido/",
        height=850,
        scrolling=True,
    )


# ============================================================
# IMPACTO SOBRE ACTIVOS
# ============================================================

with tabs[4]:

    st.subheader(
        "Condiciones ambientales y activos"
    )

    st.write(
        """
        El objetivo de esta sección es conectar las condiciones
        ambientales con los riesgos potenciales para la operación
        y los activos.
        """
    )

    condicion = st.selectbox(
        "Seleccione la condición ambiental",
        [
            "Lluvia intensa",
            "Inundación",
            "Tormenta eléctrica",
            "Viento fuerte",
            "Ola de calor",
            "Condición normal",
        ],
    )


    impactos = {

        "Lluvia intensa": [
            "Drenajes",
            "Vía férrea",
            "Estaciones",
            "Accesos",
            "Infraestructura vial",
        ],

        "Inundación": [
            "Estaciones",
            "Drenajes",
            "Sistemas eléctricos",
            "Equipos de control",
            "Infraestructura subterránea",
        ],

        "Tormenta eléctrica": [
            "Sistemas eléctricos",
            "Comunicaciones",
            "Señalización",
            "Metrocables",
            "Infraestructura expuesta",
        ],

        "Viento fuerte": [
            "Metrocables",
            "Infraestructura elevada",
            "Elementos exteriores",
            "Cubiertas",
            "Señalización",
        ],

        "Ola de calor": [
            "Sistemas eléctricos",
            "Equipos electrónicos",
            "Sistemas de ventilación",
            "Infraestructura",
        ],

        "Condición normal": [
            "Sin condición ambiental extraordinaria seleccionada.",
        ],
    }


    st.markdown(
        "### Activos potencialmente expuestos"
    )

    for activo in impactos[condicion]:

        st.markdown(
            f"- {activo}"
        )


    st.divider()

    st.subheader(
        "Cadena para análisis RCM"
    )

    st.code(
        """
CONDICIÓN AMBIENTAL
        ↓
EXPOSICIÓN DEL ACTIVO
        ↓
DEGRADACIÓN
        ↓
FALLA FUNCIONAL
        ↓
CONSECUENCIA
        ↓
TAREA DE MANTENIMIENTO
        """,
        language="text",
    )


# ============================================================
# FUENTE
# ============================================================

with tabs[5]:

    st.subheader(
        "Fuente de información"
    )

    st.markdown(
        """
        **Sistema de Alerta Temprana de Medellín y el Valle
        de Aburrá — SIATA**

        El aplicativo utiliza productos públicos del SIATA
        exclusivamente como fuente externa de información ambiental.
        """
    )

    st.markdown(
        """
        **Portal SIATA**

        https://siata.gov.co/portalWeb

        **Monitoreo SIATA**

        https://siata.gov.co/portal_dividido/

        **Boletín pluviométrico**

        https://siata.gov.co/boletinnp.php
        """
    )

    st.caption(
        "La información ambiental mostrada no sustituye los "
        "procedimientos oficiales de operación o seguridad del Metro."
    )