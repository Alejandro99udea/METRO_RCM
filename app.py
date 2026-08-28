# -*- coding: utf-8 -*-

import streamlit as st

from utils.reportes import generar_informe_pdf
from data.metro_data import METRO, LINEAS, TRANVIA


st.set_page_config(
    page_title="METRO_RCM | Gestión de Activos",
    page_icon="🚇",
    layout="wide",
    initial_sidebar_state="expanded",
)

ICONOS = {
    "negocio": "​​🟢​​",
    "operacional": "🟢​",
    "activos": "🟢​",
    "mantenimiento": "🟢​",
    "indicadores": "🟢​",
    "criticidad": "🟢​",
    "ambiental": "🟢​",
    "rcm": "🟢​",
}


def mostrar_boton_informe(key: str, titulo: str, subtitulo: str, secciones: list, nombre_archivo: str) -> None:
    if st.button("🖨️ Generar informe", key=key, width="stretch"):
        pdf = generar_informe_pdf(titulo=titulo, subtitulo=subtitulo, secciones=secciones)
        st.download_button(
            label="⬇️ Descargar informe PDF",
            data=pdf,
            file_name=nombre_archivo,
            mime="application/pdf",
            width="stretch",
            key=f"{key}_download",
        )


st.markdown(
    """
    <style>

    /* ======================================================
       VARIABLES VISUALES
       ====================================================== */

    :root {

        --metro-green: #006B54;
        --metro-green-dark: #004F3D;
        --metro-green-light: #E8F3EF;

        --metro-yellow: #F2C94C;
        --metro-yellow-light: #FFF6D8;

        --metro-red: #C62828;
        --metro-red-light: #FDECEC;

        --metro-blue: #2F6F7E;
        --metro-blue-light: #EAF4F6;

        --metro-dark: #263238;
        --metro-gray: #64748B;
        --metro-gray-light: #F4F6F5;

        --metro-border: #DCE3E0;
        --metro-white: #FFFFFF;

    }


    /* ======================================================
       FONDO GENERAL
       ====================================================== */

    .stApp {

        background-color: #F5F7F6;

        color: var(--metro-dark);

    }


    /* ======================================================
       CONTENEDOR PRINCIPAL
       ====================================================== */

    .block-container {

        padding-top: 2rem;

        padding-bottom: 3rem;

        max-width: 1450px;

    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {

        background-color: var(--metro-green-dark);

        border-right: 1px solid #003C2F;

    }


    section[data-testid="stSidebar"] * {

        color: #FFFFFF !important;

    }


    section[data-testid="stSidebar"] hr {

        border-color: rgba(255,255,255,0.18);

    }


    /* ======================================================
       TÍTULOS
       ====================================================== */

    h1, h2, h3, h4 {

        color: var(--metro-dark);

        font-weight: 750;

        letter-spacing: -0.02em;

    }


    h1 {

        font-size: 2.2rem;

    }


    h2 {

        font-size: 1.7rem;

    }


    h3 {

        font-size: 1.3rem;

    }


    /* ======================================================
       TEXTO
       ====================================================== */

    p, li {

        color: #455A64;

    }


    /* ======================================================
       HEADER INSTITUCIONAL
       ====================================================== */

    .metro-header {

        background: linear-gradient(
            90deg,
            var(--metro-green-dark),
            var(--metro-green)
        );

        color: #FFFFFF;

        border-radius: 18px;

        padding: 22px 28px;

        margin-bottom: 25px;

        box-shadow: 0 5px 18px rgba(0,0,0,0.08);

    }


    .metro-header-title {

        font-size: 1.85rem;

        font-weight: 800;

        color: #FFFFFF;

        line-height: 1.1;

    }


    .metro-header-subtitle {

        font-size: 0.95rem;

        color: rgba(255,255,255,0.82);

        margin-top: 6px;

    }


    /* ======================================================
       BARRA DE IDENTIDAD
       ====================================================== */

    .metro-accent {

        height: 5px;

        border-radius: 999px;

        background: linear-gradient(
            90deg,
            var(--metro-green),
            var(--metro-yellow)
        );

        margin-top: 12px;

        margin-bottom: 22px;

    }
/* ======================================================
   PORTADA PRINCIPAL
   ====================================================== */

.st-key-hero_portada {

    background: linear-gradient(
        135deg,
        #004F3D 0%,
        #006B54 100%
    );

    border-radius: 0 0 24px 24px;

    padding: 28px 34px 34px 34px;

    margin-top: -1rem;

    margin-bottom: 30px;

    color: #FFFFFF;

}


/* Títulos dentro de la portada */

.st-key-hero_portada h1,
.st-key-hero_portada h2,
.st-key-hero_portada h3 {

    color: #FFFFFF !important;

}


/* Texto */

.st-key-hero_portada p {

    color: rgba(255,255,255,0.88) !important;

}


/* Línea */

.st-key-hero_portada hr {

    border-color: rgba(255,255,255,0.35) !important;

}

    /* ======================================================
       TARJETAS
       ====================================================== */

    .metro-card {

        background: var(--metro-white);

        border: 1px solid var(--metro-border);

        border-radius: 16px;

        padding: 20px;

        box-shadow: 0 3px 12px rgba(0,0,0,0.035);

        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease;

    }


    .metro-card:hover {

        transform: translateY(-2px);

        box-shadow: 0 6px 18px rgba(0,0,0,0.08);

    }


    .metro-card-title {

        color: var(--metro-dark);

        font-size: 1.05rem;

        font-weight: 750;

        margin-bottom: 7px;

    }


    .metro-card-text {

        color: var(--metro-gray);

        font-size: 0.9rem;

        line-height: 1.5;

    }


    /* ======================================================
       TARJETAS DE INDICADORES
       ====================================================== */

    .kpi-card {

        background: #FFFFFF;

        border: 1px solid var(--metro-border);

        border-left: 5px solid var(--metro-green);

        border-radius: 14px;

        padding: 17px 18px;

        min-height: 105px;

        box-shadow: 0 3px 10px rgba(0,0,0,0.025);

    }


    .kpi-label {

        font-size: 0.78rem;

        color: var(--metro-gray);

        text-transform: uppercase;

        letter-spacing: 0.05em;

    }


    .kpi-value {

        font-size: 1.55rem;

        font-weight: 800;

        color: var(--metro-dark);

        margin-top: 5px;

    }
/* ======================================================
   BLOQUES DE FLUJO
   ====================================================== */

.flow-box {

    background: #FFFFFF;

    border: 1px solid var(--metro-border);

    border-radius: 14px;

    padding: 16px;

    min-height: 105px;

    text-align: center;

    box-shadow: 0 3px 10px rgba(0,0,0,0.025);

}

.flow-title {

    font-size: 0.92rem;

    font-weight: 800;

    color: var(--metro-green-dark);

}

.flow-text {

    font-size: 0.78rem;

    color: var(--metro-gray);

    margin-top: 8px;

    line-height: 1.4;

}

    /* ======================================================
       ESTADOS
       ====================================================== */

    .status-ok {

        display: inline-block;

        padding: 6px 11px;

        border-radius: 999px;

        background: #E8F5E9;

        color: #1B5E20;

        font-size: 0.78rem;

        font-weight: 700;

    }


    .status-warning {

        display: inline-block;

        padding: 6px 11px;

        border-radius: 999px;

        background: var(--metro-yellow-light);

        color: #795548;

        font-size: 0.78rem;

        font-weight: 700;

    }


    .status-danger {

        display: inline-block;

        padding: 6px 11px;

        border-radius: 999px;

        background: var(--metro-red-light);

        color: #B71C1C;

        font-size: 0.78rem;

        font-weight: 700;

    }


    .status-info {

        display: inline-block;

        padding: 6px 11px;

        border-radius: 999px;

        background: var(--metro-blue-light);

        color: #24545F;

        font-size: 0.78rem;

        font-weight: 700;

    }


    /* ======================================================
       BOTONES
       ====================================================== */

    div.stButton > button {

        background-color: var(--metro-green);

        color: #FFFFFF;

        border: 1px solid var(--metro-green);

        border-radius: 10px;

        font-weight: 700;

        min-height: 42px;

        transition:
            background-color 0.15s ease,
            border-color 0.15s ease;

    }


    div.stButton > button:hover {

        background-color: var(--metro-green-dark);

        border-color: var(--metro-green-dark);

        color: #FFFFFF;

    }


    /* ======================================================
       SELECTBOX
       ====================================================== */

    div[data-baseweb="select"] > div {

        border-radius: 10px;

        border-color: var(--metro-border);

        background-color: #FFFFFF;

    }


    /* ======================================================
       MÉTRICAS NATIVAS DE STREAMLIT
       ====================================================== */

    div[data-testid="stMetric"] {

        background-color: #FFFFFF;

        border: 1px solid var(--metro-border);

        border-left: 4px solid var(--metro-green);

        border-radius: 14px;

        padding: 13px 16px;

        box-shadow: 0 3px 10px rgba(0,0,0,0.025);

    }


    div[data-testid="stMetricLabel"] {

        color: var(--metro-gray);

    }


    div[data-testid="stMetricValue"] {

        color: var(--metro-dark);

    }


    /* ======================================================
       TABS
       ====================================================== */

    button[data-baseweb="tab"] {

        color: var(--metro-gray);

        font-weight: 650;

    }


    button[data-baseweb="tab"][aria-selected="true"] {

        color: var(--metro-green);

    }


    div[data-baseweb="tab-highlight"] {

        background-color: var(--metro-green);

    }


    /* ======================================================
       TABLAS
       ====================================================== */

    div[data-testid="stDataFrame"] {

        border: 1px solid var(--metro-border);

        border-radius: 12px;

        overflow: hidden;

    }


    /* ======================================================
       ALERTAS
       ====================================================== */

    div[data-testid="stAlert"] {

        border-radius: 12px;

    }


    /* ======================================================
       SEPARADORES
       ====================================================== */

    hr {

        border-color: #DEE5E2;

    }


    /* ======================================================
       PIE DE PÁGINA
       ====================================================== */

    .metro-footer {

        color: #78909C;

        font-size: 0.78rem;

        text-align: center;

        padding-top: 20px;

        padding-bottom: 10px;

    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# ENCABEZADO + PORTADA
# ============================================================

with st.container(key="hero_portada"):
    st.markdown("## RCM")
    st.write("UNIVERSIDAD DE ANTIOQUIA")
    st.markdown("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    st.title("CONFIABILIDAD EN MOVIMIENTO")
    st.write(
        "Plataforma interactiva desarrollada para estructurar el "
        "contexto del negocio, contexto operacional, activos, "
        "mantenimiento, criticidad y análisis RCM del Metro de Medellín."
    )

st.divider()
st.subheader("Navegación del proyecto")
st.caption("Seleccione un módulo para acceder directamente a la información.")

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    with st.container(border=True):
        st.markdown(f"## {ICONOS['negocio']} Contexto del negocio")
        st.write("Empresa, modelo de negocio, estrategia, finanzas, organización, entorno y creación de valor.")
        if st.button("Abrir módulo →", key="btn_negocio", width="stretch"):
            st.switch_page("pages/01_Contexto_del_Negocio.py")
        mostrar_boton_informe(
            key="btn_informe_negocio",
            titulo="Contexto del Negocio",
            subtitulo="Metro de Medellín · Gestión de Activos y RCM",
            nombre_archivo="Informe_Contexto_del_Negocio.pdf",
            secciones=[
                {"titulo": "Perfil empresarial", "datos": [["Empresa", METRO.get("empresa", "N/D")], ["Empleados 2025", METRO.get("empleados_2025", "N/D")], ["Red integrada", f"{METRO.get('red_integrada_km', 'N/D')} km"], ["Red férrea", f"{METRO.get('red_ferrea_km', 'N/D')} km"]]},
                {"titulo": "Finanzas 2025", "datos": [["Ingresos", f"${METRO.get('ingresos_2025_m', 'N/D')} millones"], ["Ingresos de transporte", f"${METRO.get('ingresos_transporte_2025_m', 'N/D')} millones"], ["Negocios asociados", f"${METRO.get('negocios_asociados_2025_m', 'N/D')} millones"], ["EBITDA", f"${METRO.get('ebitda_2025_m', 'N/D')} millones"], ["Utilidad neta", f"${METRO.get('utilidad_neta_2025_m', 'N/D')} millones"], ["Activos", f"${METRO.get('activos_2025_m', 'N/D')} millones"]]},
                {"titulo": "Gestión de activos", "datos": [["Trenes", METRO.get("trenes", "N/D")], ["Coches", METRO.get("coches_tren", "N/D")], ["Metrocables", METRO.get("metrocables", "N/D")], ["Tranvía", METRO.get("tranvia", "N/D")], ["BRT", METRO.get("brt", "N/D")]]},
                {"titulo": "Estrategia 2026–2035", "datos": [[f"OE{i+1}", objetivo] for i, objetivo in enumerate(METRO.get("estrategia_2026_2035", []))]},
            ],
        )

with col2:
    with st.container(border=True):
        st.markdown(f"## {ICONOS['operacional']} Contexto operacional")
        st.write("Modos de transporte, líneas, régimen de marcha, condiciones operacionales y sistemas.")
        if st.button("Abrir módulo →", key="btn_operacional", width="stretch"):
            st.switch_page("pages/02_Contexto_Operacional.py")
        mostrar_boton_informe(
            key="btn_informe_operacional",
            titulo="Contexto Operacional",
            subtitulo="Sistema Metro de Medellín · Condiciones de operación",
            nombre_archivo="Informe_Contexto_Operacional.pdf",
            secciones=[
                {"titulo": "Modos de transporte", "datos": [["Metro", "Líneas A y B"], ["Tranvía", "Línea T"], ["Buses", "Líneas 1, 2 y O"], ["Metrocables", "H, J, K, L, M y P"]]},
                {"titulo": "Línea A", "datos": [["Recorrido", LINEAS.get("A", {}).get("recorrido", "N/D")], ["Longitud", f"{LINEAS.get('A', {}).get('longitud_km', 'N/D')} km"], ["Estaciones", len(LINEAS.get("A", {}).get("estaciones", []))], ["Tiempo de recorrido", f"{LINEAS.get('A', {}).get('tiempo_recorrido_min', 'N/D')} min"], ["Velocidad comercial", f"{LINEAS.get('A', {}).get('velocidad_comercial_kmh', 'N/D')} km/h"], ["Velocidad máxima", f"{LINEAS.get('A', {}).get('velocidad_maxima_kmh', 'N/D')} km/h"], ["Capacidad", f"{LINEAS.get('A', {}).get('capacidad_pax_hora_sentido', 'N/D')} pax/h/sentido"]]},
                {"titulo": "Línea B", "datos": [["Recorrido", LINEAS.get("B", {}).get("recorrido", "N/D")], ["Longitud", f"{LINEAS.get('B', {}).get('longitud_km', 'N/D')} km"], ["Estaciones", len(LINEAS.get("B", {}).get("estaciones", []))], ["Tiempo de recorrido", f"{LINEAS.get('B', {}).get('tiempo_recorrido_min', 'N/D')} min"], ["Velocidad comercial", f"{LINEAS.get('B', {}).get('velocidad_comercial_kmh', 'N/D')} km/h"], ["Velocidad máxima", f"{LINEAS.get('B', {}).get('velocidad_maxima_kmh', 'N/D')} km/h"], ["Capacidad", f"{LINEAS.get('B', {}).get('capacidad_pax_hora_sentido', 'N/D')} pax/h/sentido"]]},
                {"titulo": "Tranvía Línea T", "datos": [["Recorrido", TRANVIA.get("recorrido", "N/D")], ["Longitud", f"{TRANVIA.get('longitud_km', 'N/D')} km"], ["Vehículos", TRANVIA.get("vehiculos", "N/D")], ["Velocidad comercial", f"{TRANVIA.get('vel_comercial', 'N/D')} km/h"], ["Capacidad", f"{TRANVIA.get('capacidad_pax_hs', 'N/D')} pax/h/sentido"]]},
            ],
        )

with col3:
    with st.container(border=True):
        st.markdown(f"## {ICONOS['activos']} Gestión de activos")
        st.write("Inventario, clasificación de activos, sistemas, subsistemas y componentes.")
        if st.button("Abrir módulo →", key="btn_activos", width="stretch"):
            st.switch_page("pages/03_Activos.py")
        mostrar_boton_informe(
            key="btn_informe_activos",
            titulo="Gestión de Activos",
            subtitulo="Inventario y estructura de activos del Metro",
            nombre_archivo="Informe_Gestion_de_Activos.pdf",
            secciones=[
                {"titulo": "Inventario corporativo", "datos": [["Red integrada", f"{METRO.get('red_integrada_km', 'N/D')} km"], ["Red férrea", f"{METRO.get('red_ferrea_km', 'N/D')} km"], ["Trenes", METRO.get("trenes", "N/D")], ["Coches", METRO.get("coches_tren", "N/D")], ["Metrocables", METRO.get("metrocables", "N/D")], ["Tranvía", METRO.get("tranvia", "N/D")], ["BRT", METRO.get("brt", "N/D")]]},
                {"titulo": "Madurez de activos", "datos": [[str(año), valor] for año, valor in METRO.get("madurez_activos", {}).items()]},
            ],
        )

st.write("")
col4, col5, col6 = st.columns(3, gap="large")

with col4:
    with st.container(border=True):
        st.markdown(f"## {ICONOS['mantenimiento']} Mantenimiento")
        st.write("Planes de mantenimiento, estrategias, fallas, rutinas y recursos.")
        if st.button("Abrir módulo →", key="btn_mantenimiento", width="stretch"):
            st.switch_page("pages/04_Mantenimiento.py")
        mant = METRO.get("mantenimiento", {})
        mostrar_boton_informe(
            key="btn_informe_mantenimiento",
            titulo="Mantenimiento",
            subtitulo="Gestión del mantenimiento · Metro de Medellín",
            nombre_archivo="Informe_Mantenimiento.pdf",
            secciones=[
                {"titulo": "Modalidades de mantenimiento", "datos": [["Modalidad", m] for m in mant.get("modalidades", [])]},
                {"titulo": "Indicadores de mantenimiento", "datos": [["Modos de falla 2016", mant.get("modos_falla_2016", "N/D")], ["Modos de falla 2024", mant.get("modos_falla_2024", "N/D")], ["Regularidad A 2022", mant.get("regularidad_A_2022", "N/D")], ["Regularidad A 2023", mant.get("regularidad_A_2023", "N/D")], ["Incremento fallas críticas", f"{mant.get('fallas_criticas_incremento_pct', 'N/D')} %"]]},
                {"titulo": "Inversión", "datos": [["Plan de mantenimiento 2025", f"${METRO.get('mantenimiento_plan_2025_m_mas', 'N/D')} millones"], ["Adquisiciones PP&E 2025", f"${METRO.get('ppye_adquisiciones_2025_m', 'N/D')} millones"]]},
            ],
        )

with col5:
    with st.container(border=True):
        st.markdown(f"## {ICONOS['indicadores']} Indicadores")
        st.write("Disponibilidad, confiabilidad, MTBF, MTTR, desempeño y comportamiento operacional.")
        if st.button("Abrir módulo →", key="btn_indicadores", width="stretch"):
            st.switch_page("pages/05_Indicadores.py")
        mostrar_boton_informe(
            key="btn_informe_indicadores",
            titulo="Indicadores",
            subtitulo="Indicadores corporativos, operacionales y de gestión",
            nombre_archivo="Informe_Indicadores.pdf",
            secciones=[
                {"titulo": "Indicadores corporativos", "datos": [["Viajes corporativos 2025", f"{METRO.get('viajes_corporativos_2025_m', 'N/D')} millones"], ["Satisfacción", METRO.get("satisfaccion", "N/D")], ["Experiencia", METRO.get("experiencia", "N/D")], ["Meta satisfacción", METRO.get("meta_satisfaccion", "N/D")]]},
                {"titulo": "Indicadores financieros", "datos": [["Ingresos 2025", f"${METRO.get('ingresos_2025_m', 'N/D')} millones"], ["EBITDA 2025", f"${METRO.get('ebitda_2025_m', 'N/D')} millones"], ["Utilidad neta 2025", f"${METRO.get('utilidad_neta_2025_m', 'N/D')} millones"]]},
            ],
        )

with col6:

    with st.container(border=True):

        st.markdown(
            f"## {ICONOS['criticidad']} Criticidad"
        )

        st.write(
            "Evaluación de consecuencias, riesgo, priorización "
            "y activos críticos."
        )

        st.write("")

        if st.button(
            "Abrir módulo →",
            key="btn_criticidad",
            width="stretch"
        ):
            st.switch_page(
                "pages/07_Criticidad_Integrado.py"
            )

st.write("")
col7, col8, col9 = st.columns(3, gap="large")

with col7:
    with st.container(border=True):
        st.markdown(f"## {ICONOS['ambiental']} Monitoreo ambiental")
        st.write("Condiciones hidrometeorológicas en tiempo real mediante información pública del SIATA.")
        if st.button("Abrir monitoreo SIATA →", key="btn_siata_portada", width="stretch"):
            st.switch_page("pages/09_Monitoreo_Ambiental.py")
        mostrar_boton_informe(
            key="btn_informe_ambiental",
            titulo="Monitoreo Ambiental",
            subtitulo="Información ambiental y meteorológica · SIATA",
            nombre_archivo="Informe_Monitoreo_Ambiental.pdf",
            secciones=[
                {"titulo": "Fuente", "datos": [["Sistema", "SIATA"], ["Cobertura", "Valle de Aburrá"], ["Naturaleza", "Información ambiental externa"]]},
                {"titulo": "Variables de interés", "datos": [["Temperatura", "Monitoreada"], ["Humedad", "Monitoreada"], ["Precipitación", "Monitoreada"], ["Viento", "Monitoreado"], ["Radar meteorológico", "Disponible"]]},
                {"titulo": "Relación con activos", "datos": [["Lluvia intensa", "Vía, drenajes, estaciones e infraestructura"], ["Tormentas", "Sistemas eléctricos y comunicaciones"], ["Viento", "Infraestructura elevada y Metrocables"]]},
            ],
        )

with col8:
    with st.container(border=True):
        st.markdown(f"## {ICONOS['rcm']} Análisis RCM")
        st.write("Funciones, fallas funcionales, modos de falla, efectos, consecuencias y tareas de mantenimiento.")
        if st.button("Abrir análisis RCM →", key="btn_rcm", width="stretch"):
            st.switch_page("pages/07_RCM.py")
        mostrar_boton_informe(
            key="btn_informe_rcm",
            titulo="Análisis RCM",
            subtitulo="Reliability Centered Maintenance · Metro de Medellín",
            nombre_archivo="Informe_RCM.pdf",
            secciones=[
                {"titulo": "Metodología", "datos": [["Función", "Definición de la función requerida"], ["Falla funcional", "Pérdida total o parcial de la función"], ["Modo de falla", "Causa física o técnica de la falla"], ["Efecto", "Consecuencia observable del modo de falla"], ["Consecuencia", "Impacto operacional, económico, ambiental o de seguridad"], ["Tarea RCM", "Acción de mantenimiento técnicamente seleccionada"]]},
                {"titulo": "Estado del proyecto", "datos": [["Análisis RCM", "En desarrollo"], ["FMECA", "En desarrollo"], ["Tareas de mantenimiento", "Pendiente de consolidación por activo"]]},
            ],
        )

st.divider()
st.subheader("Cadena de análisis")
st.caption("Secuencia metodológica desde el contexto del negocio hasta la definición de tareas RCM.")

flujo = [
    ("NEGOCIO", "¿Qué valor debe generar?"),
    ("OPERACIÓN", "¿En qué condiciones?"),
    ("ACTIVOS", "¿Qué soporta el servicio?"),
    ("FUNCIONES", "¿Qué deben cumplir?"),
    ("CONFIABILIDAD", "¿Cómo se comportan?"),
    ("RCM", "¿Cómo mantenerlos?"),
]

fila1 = st.columns(3, gap="large")
for i in range(3):
    with fila1[i]:
        titulo, descripcion = flujo[i]
        with st.container(border=True):
            st.markdown(f"### {titulo}")
            st.write(descripcion)

st.write("")
fila2 = st.columns(3, gap="large")
for i in range(3, 6):
    with fila2[i - 3]:
        titulo, descripcion = flujo[i]
        with st.container(border=True):
            st.markdown(f"### {titulo}")
            st.write(descripcion)

st.divider()
st.caption("METRO_RCM · Gestión de Activos y RCM · Universidad de Antioquia")

# ------------------------------------------------------------
# EQUIPO RCM
# ------------------------------------------------------------

with col9:

    with st.container(border=True):

        st.markdown("## 👥 Equipo RCM")

        st.write(
            "Integrantes del equipo, roles, perfiles, "
            "competencias y especialidades."
        )

        if st.button(
            "Abrir Equipo RCM →",
            key="btn_equipo_rcm",
            width="stretch"
        ):
            st.switch_page(
                "pages/08_Equipo_RCM_Integrado.py"
            )

        mostrar_boton_informe(
            key="btn_informe_equipo_rcm",
            titulo="Equipo RCM",
            subtitulo="Integrantes, roles y competencias del equipo",
            nombre_archivo="Informe_Equipo_RCM.pdf",
            secciones=[
                {
                    "titulo": "Equipo de trabajo",
                    "datos": [
                        ["Proyecto", "METRO_RCM"],
                        ["Área", "Gestión de Activos y RCM"],
                        ["Equipo", "Equipo RCM"],
                    ],
                },
                {
                    "titulo": "Roles y competencias",
                    "datos": [
                        ["Información", "Consultar módulo Equipo RCM"],
                    ],
                },
            ],
        )