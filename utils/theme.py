# -*- coding: utf-8 -*-
"""Tema visual compartido de METRO_RCM.

El módulo evita dependencias externas para los elementos visuales:
las imágenes institucionales usadas por el tema se empaquetan dentro
del proyecto y se incrustan como data URI en el CSS.
"""

from pathlib import Path
import base64
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[1]
UI_DIR = BASE_DIR / "assets" / "ui"


def _data_uri(nombre: str, mime: str) -> str:
    ruta = UI_DIR / nombre
    if not ruta.exists():
        return ""
    datos = base64.b64encode(ruta.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{datos}"


HERO_URI = _data_uri("hero_city_train.jpg", "image/jpeg")
SIDEBAR_URI = HERO_URI
CREST_URI = _data_uri("udea_crest_white.png", "image/png")


def aplicar_tema_udea(mostrar_marca_sidebar: bool = True, marca_agua: bool = True) -> None:
    """Aplica la identidad visual UdeA + METRO_RCM de forma segura."""
    watermark_css = ""
    if marca_agua and CREST_URI:
        watermark_css = """
        [data-testid="stAppViewContainer"] > .main::before {
            content: "";
            position: fixed;
            pointer-events: none;
            z-index: 0;
            width: 520px;
            height: 520px;
            left: 62%;
            top: 57%;
            transform: translate(-50%, -50%);
            background-image: url("__CREST_URI__");
            background-repeat: no-repeat;
            background-position: center;
            background-size: contain;
            opacity: .028;
            filter: grayscale(1);
        }
        """.replace("__CREST_URI__", CREST_URI)

    css = """
    <style>
    :root {
        --udea-green: #004F3D;
        --udea-green-2: #006B54;
        --udea-green-3: #118567;
        --udea-green-soft: #EAF4F0;
        --udea-border: #D7E2DD;
        --udea-text: #20312D;
        --udea-muted: #6B7A75;
        --udea-bg: #F4F7F5;
        --udea-white: #FFFFFF;
        --udea-gold: #D9B44A;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: var(--udea-bg);
        color: var(--udea-text);
    }

    [data-testid="stAppViewContainer"] > .main {
        background:
            radial-gradient(circle at 87% 7%, rgba(17,133,103,.045), transparent 22rem),
            var(--udea-bg);
    }

    .block-container {
        max-width: 1480px;
        padding-top: 1.4rem;
        padding-bottom: 3.5rem;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, rgba(0,63,49,.97) 0%, rgba(0,79,61,.96) 58%, rgba(0,55,42,.985) 100%),
            url("__SIDEBAR_URI__");
        background-size: cover;
        background-position: center;
        background-blend-mode: multiply;
        border-right: 1px solid rgba(255,255,255,.10);
    }

    section[data-testid="stSidebar"] > div:first-child {
        padding: .7rem .65rem 1.1rem;
    }

    section[data-testid="stSidebar"] * {
        color: #fff !important;
    }

    /* Ocultamos la navegación automática y usamos navegación institucional propia. */
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
        display: none;
    }

    .metro-sidebar-nav {
        display: flex;
        flex-direction: column;
        gap: 4px;
        margin-top: 2px;
    }

    .metro-sidebar-nav-label {
        color: rgba(255,255,255,.58) !important;
        font-size: .68rem;
        font-weight: 800;
        letter-spacing: .13em;
        text-transform: uppercase;
        margin: 5px 10px 2px;
    }

    section[data-testid="stSidebar"] [data-testid="stPageLink"] a {
        min-height: 38px;
        padding: 7px 10px;
        border-radius: 10px;
        color: #fff !important;
        font-size: .82rem;
        font-weight: 620;
        text-decoration: none !important;
        transition: background .16s ease, transform .16s ease;
    }

    section[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {
        background: rgba(255,255,255,.095);
        transform: translateX(2px);
    }

    section[data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"] {
        background: linear-gradient(90deg, rgba(45,201,130,.30), rgba(255,255,255,.11));
        box-shadow: inset 4px 0 0 #39C982;
    }

    .udea-sidebar-brand {
        text-align: center;
        padding: 8px 8px 16px;
    }

    .udea-sidebar-brand img {
        width: 132px;
        max-width: 78%;
        height: auto;
        margin: 0 auto 7px;
        display: block;
        border-radius: 3px;
    }

    .udea-sidebar-title {
        font-size: 1.12rem;
        font-weight: 800;
        letter-spacing: .045em;
        line-height: 1.1;
    }

    .udea-sidebar-subtitle {
        font-size: .74rem;
        line-height: 1.35;
        margin-top: 5px;
        color: rgba(255,255,255,.73) !important;
    }

    /* ---------- Tipografía ---------- */
    h1, h2, h3, h4 {
        color: var(--udea-text);
        font-weight: 780;
        letter-spacing: -.022em;
    }

    p, li, label, .stCaption {
        color: #455853;
    }

    h1 {
        font-size: clamp(1.9rem, 2.7vw, 2.55rem);
        margin-bottom: .5rem;
    }

    h2 {
        font-size: clamp(1.35rem, 2vw, 1.8rem);
        margin-top: .3rem;
    }

    h3 {
        font-size: 1.18rem;
    }

    /* ---------- Encabezado institucional reutilizable ---------- */
    .metro-header {
        background: linear-gradient(135deg, #004F3D 0%, #006B54 100%);
        color: #FFFFFF;
        border-radius: 18px;
        padding: 24px 28px;
        margin-bottom: 0;
        box-shadow: 0 7px 22px rgba(0,79,61,.11);
    }

    .metro-header-title {
        color: #FFFFFF !important;
        font-size: 1.9rem;
        font-weight: 830;
        line-height: 1.08;
    }

    .metro-header-subtitle {
        color: rgba(255,255,255,.82) !important;
        font-size: .92rem;
        margin-top: 6px;
        line-height: 1.45;
    }

    .metro-accent {
        height: 4px;
        border-radius: 999px;
        background: linear-gradient(90deg, #118567, #39C982);
        margin: 11px 0 20px;
    }

    /* ---------- Encabezado interno ---------- */
    .udea-page-heading {
        display: flex;
        align-items: center;
        gap: 13px;
        padding: 2px 0 12px;
        margin-bottom: 15px;
        border-bottom: 1px solid var(--udea-border);
    }

    .udea-page-heading .accent {
        width: 7px;
        min-width: 7px;
        height: 44px;
        border-radius: 999px;
        background: linear-gradient(180deg, var(--udea-green-3), var(--udea-green));
    }

    .udea-page-heading .title {
        color: var(--udea-green);
        font-size: 2rem;
        line-height: 1.05;
        font-weight: 820;
    }

    .udea-page-heading .subtitle {
        color: var(--udea-muted);
        font-size: .9rem;
        margin-top: 4px;
        line-height: 1.35;
    }

    /* ---------- Tarjetas / bloques ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid var(--udea-border) !important;
        border-radius: 16px !important;
        background: rgba(255,255,255,.94);
        box-shadow: 0 5px 18px rgba(26,53,45,.045);
        overflow: hidden;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #C4D7CF !important;
    }

    div[data-testid="column"] > div {
        gap: .7rem;
    }

    /* Separación uniforme de los bloques verticales */
    [data-testid="stVerticalBlock"] > [data-testid="element-container"] {
        margin-bottom: .18rem;
    }

    /* ---------- Métricas ---------- */
    div[data-testid="stMetric"] {
        min-height: 106px;
        background: #fff;
        border: 1px solid var(--udea-border);
        border-left: 4px solid var(--udea-green-2);
        border-radius: 14px;
        padding: 13px 15px;
        box-shadow: 0 4px 12px rgba(26,53,45,.035);
    }

    div[data-testid="stMetricLabel"] {
        color: #64746F;
        font-size: .8rem;
    }

    div[data-testid="stMetricValue"] {
        color: var(--udea-text);
        font-weight: 800;
    }

    /* ---------- Tabs ---------- */
    div[data-baseweb="tab-list"] {
        gap: 7px;
        border-bottom: 1px solid var(--udea-border);
        margin-bottom: 14px;
    }

    button[data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 8px 14px;
        font-weight: 700;
        color: #5D6E68;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--udea-green-2);
        background: rgba(0,107,84,.06);
    }

    div[data-baseweb="tab-highlight"] {
        height: 3px;
        border-radius: 999px;
        background: var(--udea-green-2);
    }

    /* ---------- Botones ---------- */
    .stButton > button, .stDownloadButton > button,
    .stLinkButton > a {
        border-radius: 10px;
        border: 1px solid #BCD3C9;
        font-weight: 700;
        min-height: 40px;
        background: #fff;
    }

    .stButton > button:hover, .stDownloadButton > button:hover,
    .stLinkButton > a:hover {
        border-color: var(--udea-green-2);
        color: var(--udea-green) !important;
        box-shadow: 0 3px 10px rgba(0,107,84,.10);
    }

    /* ---------- Selectores ---------- */
    div[data-baseweb="select"] > div {
        border-radius: 10px;
        border-color: #C9D9D3;
    }

    /* ---------- Tablas y dataframes ---------- */
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--udea-border);
        border-radius: 13px;
        overflow: hidden;
        background: #fff;
    }

    /* ---------- Alertas ---------- */
    div[data-testid="stAlert"] {
        border-radius: 13px;
        border-width: 1px;
    }

    /* ---------- Expander ---------- */
    details {
        border: 1px solid var(--udea-border) !important;
        border-radius: 13px !important;
        background: rgba(255,255,255,.9);
    }

    /* ---------- Imágenes ---------- */
    img {
        border-radius: 12px;
    }

    /* ---------- Portada: hero del diseño de referencia ---------- */
    .st-key-hero_portada {
        min-height: 355px;
        display: flex;
        align-items: center;
        background:
            linear-gradient(90deg, rgba(0,67,52,.98) 0%, rgba(0,79,61,.92) 40%, rgba(0,79,61,.65) 66%, rgba(0,53,41,.42) 100%),
            url("__HERO_URI__");
        background-position: center right;
        background-size: cover;
        border-radius: 0 0 24px 24px;
        padding: 40px 42px 38px;
        margin-top: -1.4rem;
        margin-bottom: 28px;
        color: #fff;
        box-shadow: 0 9px 28px rgba(16,53,44,.12);
        overflow: hidden;
    }

    .st-key-hero_portada h1,
    .st-key-hero_portada h2,
    .st-key-hero_portada h3,
    .st-key-hero_portada p {
        color: #fff !important;
    }

    .st-key-hero_portada .stMarkdown {
        max-width: 820px;
    }

    /* Portada: tarjetas */
    .metro-card,
    .kpi-card,
    .flow-box {
        border: 1px solid var(--udea-border);
        background: #fff;
        border-radius: 15px;
        box-shadow: 0 4px 13px rgba(26,53,45,.035);
    }

    .metro-card {
        padding: 20px;
        min-height: 205px;
    }

    .metro-card-title {
        color: var(--udea-text);
        font-weight: 800;
        font-size: 1.04rem;
    }

    .metro-card-text {
        color: #64746F;
        line-height: 1.5;
        font-size: .9rem;
    }

    .kpi-card {
        padding: 15px 17px;
        border-left: 4px solid var(--udea-green-2);
        min-height: 100px;
    }

    .kpi-label {
        color: #6C7C77;
        font-size: .77rem;
        text-transform: uppercase;
        letter-spacing: .045em;
    }

    .kpi-value {
        color: var(--udea-text);
        font-size: 1.55rem;
        font-weight: 820;
        margin-top: 4px;
    }

    .flow-box {
        padding: 15px;
        min-height: 105px;
        text-align: center;
    }

    .flow-title {
        color: var(--udea-green);
        font-weight: 820;
    }

    .flow-text {
        color: #677772;
        font-size: .8rem;
        line-height: 1.4;
        margin-top: 7px;
    }

    .metro-footer {
        color: #70827C;
        text-align: center;
        font-size: .78rem;
        padding: 20px 0 8px;
    }

    __WATERMARK_CSS__
    </style>
    """
    css = css.replace("__SIDEBAR_URI__", SIDEBAR_URI)
    css = css.replace("__HERO_URI__", HERO_URI)
    css = css.replace("__WATERMARK_CSS__", watermark_css)

    st.markdown(css, unsafe_allow_html=True)

    if mostrar_marca_sidebar:
        brand_src = ""
        if CREST_URI:
            brand_src = CREST_URI
        elif SIDEBAR_URI:
            brand_src = SIDEBAR_URI

        st.sidebar.markdown(
            """
            <div class="udea-sidebar-brand">
                <img src="%s" alt="Universidad de Antioquia">
                <div class="udea-sidebar-title">METRO_RCM</div>
                <div class="udea-sidebar-subtitle">
                    Gestión de Activos · Confiabilidad · RCM
                </div>
            </div>
            """ % brand_src,
            unsafe_allow_html=True,
        )
        st.sidebar.divider()
        st.sidebar.markdown(
            '<div class="metro-sidebar-nav-label">NAVEGACIÓN DEL PROYECTO</div>',
            unsafe_allow_html=True,
        )

        # Los iconos se incluyen dentro de la etiqueta y no en el parámetro
        # `icon=` de st.sidebar.page_link. Esto evita incompatibilidades entre
        # versiones de Streamlit con caracteres que no son emojis válidos.
        nav_items = [
            ("app.py", "Inicio", "⌂"),
            ("pages/01_Contexto_del_Negocio.py", "Contexto del Negocio", "▦"),
            ("pages/02_Contexto_Operacional.py", "Contexto Operacional", "▣"),
            ("pages/03_Activos.py", "Gestión de Activos", "◇"),
            ("pages/04_Mantenimiento.py", "Mantenimiento", "⚙"),
            ("pages/05_Indicadores.py", "Indicadores", "▥"),
            ("pages/07_Criticidad_Integrado.py", "Matriz de Criticidad", "◈"),
            ("pages/07_RCM.py", "RCM", "↻"),
            ("pages/08_Equipo_RCM_Integrado.py", "Equipo RCM Integrado", "♙"),
            ("pages/09_Monitoreo_Ambiental.py", "Monitoreo Ambiental", "⌁"),
        ]

        for ruta, etiqueta, icono in nav_items:
            # Solo crear enlaces a páginas que realmente existen en el paquete.
            if ruta == "app.py" or (BASE_DIR / ruta).exists():
                st.sidebar.page_link(ruta, label=f"{icono}  {etiqueta}")

        st.sidebar.markdown(
            '''
            <div style="margin:16px 10px 0;padding-top:13px;border-top:1px solid rgba(255,255,255,.16);text-align:center;">
                <div style="color:#4BD18E;font-size:.76rem;font-weight:800;">RCM · Metro de Medellín</div>
                <div style="color:rgba(255,255,255,.72);font-size:.70rem;margin-top:3px;">Gestión de la Confiabilidad para la Sostenibilidad</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )


def encabezado_pagina(titulo: str, subtitulo: str = "", icono: str = "") -> None:
    """Encabezado reutilizable para páginas internas."""
    etiqueta = f"{icono} {titulo}".strip()
    st.markdown(
        """
        <div class="udea-page-heading">
            <div class="accent"></div>
            <div>
                <div class="title">%s</div>
                <div class="subtitle">%s</div>
            </div>
        </div>
        """
        % (etiqueta, subtitulo),
        unsafe_allow_html=True,
    )
