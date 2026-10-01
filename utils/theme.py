# -*- coding: utf-8 -*-
"""Sistema visual corporativo compartido para METRO_RCM.

Principios de diseño:
- Identidad UdeA/METRO sobria y técnica.
- Jerarquía visual clara y orientada a gestión ejecutiva.
- Componentes compactos, consistentes y con bajo ruido visual.
- Sin dependencias externas ni fuentes remotas.
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
    """Aplica el sistema visual corporativo en cualquier página Streamlit."""
    watermark_css = ""
    if marca_agua and CREST_URI:
        watermark_css = f"""
        [data-testid=\"stAppViewContainer\"] > .main::before {{
            content: \"\";
            position: fixed;
            pointer-events: none;
            z-index: 0;
            width: 560px;
            height: 560px;
            right: 3%;
            bottom: 2%;
            background-image: url(\"{CREST_URI}\");
            background-repeat: no-repeat;
            background-position: center;
            background-size: contain;
            opacity: .018;
            filter: grayscale(1);
        }}
        """

    css = f"""
    <style>
    :root {{
        --metro-green-900: #003D30;
        --metro-green-800: #00513F;
        --metro-green-700: #00614D;
        --metro-green-600: #08755E;
        --metro-green-500: #0C8A6D;
        --metro-green-100: #EAF4F0;
        --metro-green-050: #F5FAF8;
        --metro-ink: #18322B;
        --metro-body: #41554F;
        --metro-muted: #73817D;
        --metro-border: #DCE5E1;
        --metro-border-2: #CBD8D3;
        --metro-bg: #F4F6F5;
        --metro-surface: #FFFFFF;
        --metro-gold: #CBA94D;
        --metro-shadow: 0 6px 18px rgba(16, 49, 41, .055);
    }}

    html, body, [data-testid=\"stAppViewContainer\"] {{
        background: var(--metro-bg);
        color: var(--metro-ink);
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif;
    }}

    [data-testid=\"stAppViewContainer\"] > .main {{
        background:
            radial-gradient(circle at 88% 5%, rgba(8,117,94,.035), transparent 20rem),
            var(--metro-bg);
    }}

    .block-container {{
        max-width: 1480px;
        padding-top: 1.15rem;
        padding-bottom: 3rem;
    }}

    /* ============================ SIDEBAR ============================ */
    section[data-testid=\"stSidebar\"] {{
        background:
            linear-gradient(180deg, rgba(0,47,37,.985) 0%, rgba(0,61,48,.985) 55%, rgba(0,48,38,.995) 100%),
            url(\"{SIDEBAR_URI}\");
        background-size: cover;
        background-position: center;
        background-blend-mode: multiply;
        border-right: 1px solid rgba(255,255,255,.08);
    }}

    section[data-testid=\"stSidebar\"] > div:first-child {{
        padding: .65rem .58rem 1rem;
    }}

    section[data-testid=\"stSidebar\"] * {{ color: #fff !important; }}
    section[data-testid=\"stSidebar\"] [data-testid=\"stSidebarNav\"] {{ display: none; }}

    .udea-sidebar-brand {{
        padding: 7px 9px 13px;
        text-align: left;
        border-bottom: 1px solid rgba(255,255,255,.10);
        margin-bottom: 11px;
    }}

    .udea-sidebar-brand img {{
        display: block;
        width: 108px;
        max-width: 68%;
        height: auto;
        margin: 0 0 10px 2px;
    }}

    .udea-sidebar-title {{
        font-size: 1.0rem;
        font-weight: 820;
        letter-spacing: .055em;
        line-height: 1.1;
    }}

    .udea-sidebar-subtitle {{
        margin-top: 4px;
        font-size: .68rem;
        line-height: 1.35;
        color: rgba(255,255,255,.62) !important;
        text-transform: uppercase;
        letter-spacing: .065em;
    }}

    .metro-sidebar-nav-label {{
        color: rgba(255,255,255,.50) !important;
        font-size: .62rem;
        font-weight: 800;
        letter-spacing: .15em;
        text-transform: uppercase;
        padding: 3px 10px 8px;
    }}

    section[data-testid=\"stSidebar\"] [data-testid=\"stPageLink\"] a {{
        min-height: 36px;
        padding: 6px 9px;
        border-radius: 7px;
        font-size: .77rem;
        font-weight: 630;
        text-decoration: none !important;
        color: rgba(255,255,255,.88) !important;
        border-left: 3px solid transparent;
        transition: background .14s ease, border-color .14s ease;
    }}

    section[data-testid=\"stSidebar\"] [data-testid=\"stPageLink\"] a:hover {{
        background: rgba(255,255,255,.07);
        border-left-color: rgba(203,169,77,.60);
    }}

    section[data-testid=\"stSidebar\"] [data-testid=\"stPageLink\"] a[aria-current=\"page\"] {{
        background: rgba(255,255,255,.095);
        border-left-color: #D4B75A;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,.045);
    }}

    /* ============================ TYPOGRAPHY ============================ */
    h1, h2, h3, h4 {{
        color: var(--metro-ink);
        font-weight: 760;
        letter-spacing: -.018em;
    }}

    h1 {{ font-size: clamp(1.9rem, 2.8vw, 2.45rem); }}
    h2 {{ font-size: clamp(1.36rem, 2vw, 1.8rem); }}
    h3 {{ font-size: 1.15rem; }}

    p, li, label, .stCaption {{ color: var(--metro-body); }}

    /* ============================ PAGE HEADER ============================ */
    .metro-page-context {{
        display: flex;
        gap: 8px;
        align-items: center;
        color: #73817D;
        font-size: .64rem;
        font-weight: 800;
        letter-spacing: .14em;
        text-transform: uppercase;
        margin: 0 0 7px;
    }}

    .metro-page-context .brand {{ color: var(--metro-green-700); }}
    .metro-page-context .dot {{ color: #B3BFBB; }}

    .udea-page-heading {{
        display: flex;
        align-items: stretch;
        gap: 14px;
        padding: 0 0 14px;
        margin-bottom: 20px;
        border-bottom: 1px solid var(--metro-border);
    }}

    .udea-page-heading .accent {{
        width: 5px;
        min-width: 5px;
        border-radius: 3px;
        background: linear-gradient(180deg, var(--metro-green-500), var(--metro-green-800));
    }}

    .udea-page-heading .title {{
        color: var(--metro-green-800);
        font-size: clamp(1.55rem, 2.2vw, 2.05rem);
        font-weight: 810;
        line-height: 1.08;
    }}

    .udea-page-heading .subtitle {{
        color: var(--metro-muted);
        font-size: .82rem;
        margin-top: 5px;
        line-height: 1.38;
    }}

    /* ============================ SURFACES / CARDS ============================ */
    div[data-testid=\"stVerticalBlockBorderWrapper\"] {{
        border: 1px solid var(--metro-border) !important;
        border-radius: 10px !important;
        background: rgba(255,255,255,.97);
        box-shadow: var(--metro-shadow);
        overflow: hidden;
    }}

    div[data-testid=\"stVerticalBlockBorderWrapper\"]:hover {{
        border-color: var(--metro-border-2) !important;
    }}

    div[data-testid=\"column\"] > div {{ gap: .62rem; }}

    [data-testid=\"stVerticalBlock\"] > [data-testid=\"element-container\"] {{ margin-bottom: .16rem; }}

    /* ============================ METRICS ============================ */
    div[data-testid=\"stMetric\"] {{
        min-height: 96px;
        background: #fff;
        border: 1px solid var(--metro-border);
        border-radius: 9px;
        padding: 12px 14px;
        box-shadow: 0 3px 11px rgba(16,49,41,.03);
    }}

    div[data-testid=\"stMetricLabel\"] {{
        color: var(--metro-muted);
        font-size: .73rem;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: .035em;
    }}

    div[data-testid=\"stMetricValue\"] {{
        color: var(--metro-green-800);
        font-weight: 820;
    }}

    /* ============================ BUTTONS ============================ */
    .stButton > button, .stDownloadButton > button, .stLinkButton > a {{
        border-radius: 7px !important;
        border: 1px solid var(--metro-border-2) !important;
        min-height: 38px !important;
        font-size: .78rem !important;
        font-weight: 720 !important;
        letter-spacing: .01em;
        background: #fff !important;
        box-shadow: none !important;
        transition: background .14s ease, border-color .14s ease, color .14s ease, transform .14s ease;
    }}

    .stButton > button:hover, .stDownloadButton > button:hover, .stLinkButton > a:hover {{
        border-color: var(--metro-green-700) !important;
        color: var(--metro-green-800) !important;
        background: var(--metro-green-050) !important;
        transform: translateY(-1px);
    }}

    .stButton > button[kind=\"primary\"] {{
        background: var(--metro-green-800) !important;
        border-color: var(--metro-green-800) !important;
        color: #fff !important;
    }}

    .stButton > button[kind=\"primary\"]:hover {{
        background: var(--metro-green-900) !important;
        border-color: var(--metro-green-900) !important;
        color: #fff !important;
    }}

    /* ============================ SELECTORS ============================ */
    div[data-baseweb=\"select\"] > div,
    div[data-baseweb=\"input\"] > div,
    textarea {{
        border-radius: 7px !important;
        border-color: var(--metro-border-2) !important;
        background: #fff !important;
    }}

    div[data-baseweb=\"select\"] > div:focus-within,
    div[data-baseweb=\"input\"] > div:focus-within,
    textarea:focus {{
        border-color: var(--metro-green-600) !important;
        box-shadow: 0 0 0 1px rgba(12,138,109,.12) !important;
    }}

    /* ============================ TABS ============================ */
    div[data-baseweb=\"tab-list\"] {{
        gap: 3px;
        border-bottom: 1px solid var(--metro-border);
        margin-bottom: 14px;
    }}

    button[data-baseweb=\"tab\"] {{
        border-radius: 6px 6px 0 0;
        padding: 8px 13px;
        font-size: .79rem;
        font-weight: 700;
        color: #5E7069;
    }}

    button[data-baseweb=\"tab\"][aria-selected=\"true\"] {{
        color: var(--metro-green-800);
        background: rgba(0,97,77,.045);
    }}

    div[data-baseweb=\"tab-highlight\"] {{
        height: 2px;
        background: var(--metro-green-700);
    }}

    /* ============================ TABLES ============================ */
    div[data-testid=\"stDataFrame\"] {{
        border: 1px solid var(--metro-border);
        border-radius: 9px;
        overflow: hidden;
        background: #fff;
    }}

    /* ============================ EXPANDERS / ALERTS ============================ */
    details {{
        border: 1px solid var(--metro-border) !important;
        border-radius: 8px !important;
        background: rgba(255,255,255,.96);
    }}

    div[data-testid=\"stAlert\"] {{
        border-radius: 8px;
        border-width: 1px;
    }}

    /* ============================ GENERIC CONTENT ============================ */
    img {{ border-radius: 8px; }}

    .metro-section-kicker {{
        color: var(--metro-green-700);
        font-size: .66rem;
        font-weight: 800;
        letter-spacing: .14em;
        text-transform: uppercase;
        margin-bottom: 3px;
    }}

    .metro-section-title {{
        color: var(--metro-ink);
        font-size: 1.45rem;
        font-weight: 800;
        letter-spacing: -.02em;
        margin-bottom: 2px;
    }}

    .metro-section-subtitle {{
        color: var(--metro-muted);
        font-size: .82rem;
        line-height: 1.4;
    }}

    .metro-status {{
        display: inline-flex;
        align-items: center;
        padding: 4px 8px;
        border: 1px solid var(--metro-border);
        border-radius: 5px;
        background: #F8FBFA;
        color: var(--metro-green-800);
        font-size: .62rem;
        font-weight: 800;
        letter-spacing: .08em;
        text-transform: uppercase;
    }}

    /* ============================ HOME HERO ============================ */
    .st-key-hero_portada {{
        min-height: 350px;
        display: flex;
        align-items: center;
        background:
            linear-gradient(90deg, rgba(0,56,44,.985) 0%, rgba(0,61,48,.94) 42%, rgba(0,61,48,.64) 66%, rgba(0,52,41,.34) 100%),
            url("{HERO_URI}");
        background-position: center right;
        background-size: cover;
        border-radius: 0 0 16px 16px;
        padding: 38px 40px 36px;
        margin-top: -1.15rem;
        margin-bottom: 26px;
        color: #fff;
        box-shadow: 0 8px 24px rgba(16,53,44,.10);
        overflow: hidden;
    }}

    .st-key-hero_portada h1,
    .st-key-hero_portada h2,
    .st-key-hero_portada h3,
    .st-key-hero_portada p {{ color: #fff !important; }}

    .st-key-hero_portada .stMarkdown {{ max-width: 840px; }}

    .metro-cover-eyebrow {{
        color: #D8B85B !important;
        font-size: .69rem;
        font-weight: 820;
        letter-spacing: .17em;
        text-transform: uppercase;
    }}

    .metro-cover-kicker {{
        color: #7BE0B1 !important;
        font-size: 1.05rem;
        font-weight: 820;
        letter-spacing: .13em;
        text-transform: uppercase;
        margin-top: 2px;
    }}

    .metro-cover-udea {{
        color: rgba(255,255,255,.82) !important;
        font-size: .72rem;
        font-weight: 720;
        letter-spacing: .13em;
        text-transform: uppercase;
        margin-top: 5px;
    }}

    .metro-cover-rule {{
        width: 122px;
        height: 2px;
        margin: 17px 0 20px;
        background: #D8B85B;
        border-radius: 1px;
    }}

    .metro-cover-title {{
        color: #fff !important;
        font-size: clamp(2.2rem, 4vw, 3.65rem);
        line-height: .97;
        font-weight: 860;
        letter-spacing: -.043em;
        margin-bottom: 12px;
    }}

    .metro-cover-description {{
        max-width: 820px;
        color: rgba(255,255,255,.86) !important;
        font-size: .91rem;
        line-height: 1.54;
    }}

    .metro-cover-kpis {{
        display: grid;
        grid-template-columns: repeat(4, minmax(0,1fr));
        margin-top: 28px;
        max-width: 950px;
    }}

    .metro-cover-kpi {{
        padding: 0 20px 0 0;
        margin-right: 20px;
        border-right: 1px solid rgba(255,255,255,.17);
    }}

    .metro-cover-kpi:last-child {{
        border-right: none;
        margin-right: 0;
    }}

    .metro-cover-kpi .value {{
        color: #fff;
        font-size: 1.48rem;
        font-weight: 840;
        line-height: 1;
    }}

    .metro-cover-kpi .label {{
        color: rgba(255,255,255,.66);
        font-size: .60rem;
        font-weight: 760;
        line-height: 1.25;
        text-transform: uppercase;
        letter-spacing: .065em;
        margin-top: 5px;
    }}

    /* ============================ MODULE CARDS ============================ */
    .metro-module-card {{
        min-height: 205px;
        display: flex;
        flex-direction: column;
    }}

    .metro-module-meta {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;
    }}

    .metro-module-number {{
        color: var(--metro-green-700);
        font-size: .64rem;
        font-weight: 830;
        letter-spacing: .14em;
        text-transform: uppercase;
    }}

    .metro-module-mark {{
        color: #A0ACA8;
        font-size: .74rem;
        letter-spacing: .22em;
    }}

    .metro-module-title {{
        color: var(--metro-ink) !important;
        font-size: 1.02rem !important;
        line-height: 1.16 !important;
        font-weight: 810 !important;
        margin: 0 0 7px !important;
    }}

    .metro-module-description {{
        color: #687872 !important;
        font-size: .78rem !important;
        line-height: 1.46 !important;
        margin: 0 !important;
        min-height: 58px;
    }}

    .metro-module-divider {{
        height: 1px;
        background: var(--metro-border);
        margin: 15px 0 11px;
    }}

    .metro-module-status {{
        color: var(--metro-muted);
        font-size: .61rem;
        font-weight: 760;
        letter-spacing: .075em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}

    .metro-cover-footer {{
        color: #7A8984;
        font-size: .67rem;
        text-align: center;
        padding: 22px 0 8px;
        letter-spacing: .025em;
    }}

    .metro-footer {{
        color: #7A8984;
        text-align: center;
        font-size: .67rem;
        padding: 22px 0 8px;
    }}

    @media (max-width: 900px) {{
        .metro-cover-kpis {{ grid-template-columns: repeat(2, 1fr); row-gap: 18px; }}
        .metro-cover-kpi:nth-child(2) {{ border-right: none; }}
        .st-key-hero_portada {{ padding: 30px 26px; }}
    }}

    @media (prefers-reduced-motion: reduce) {{
        *, *::before, *::after {{ transition: none !important; }}
    }}

    {watermark_css}
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)

    if mostrar_marca_sidebar:
        brand_src = CREST_URI or SIDEBAR_URI
        st.sidebar.markdown(
            f"""
            <div class=\"udea-sidebar-brand\">
                <img src=\"{brand_src}\" alt=\"Universidad de Antioquia\">
                <div class=\"udea-sidebar-title\">METRO_RCM</div>
                <div class=\"udea-sidebar-subtitle\">Gestión de activos · confiabilidad · RCM</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.sidebar.markdown(
            '<div class="metro-sidebar-nav-label">NAVEGACIÓN DEL PROYECTO</div>',
            unsafe_allow_html=True,
        )

        nav_items = [
            ("app.py", "Inicio", "⌂"),
            ("pages/01_Contexto_del_Negocio.py", "Contexto del Negocio", "01"),
            ("pages/02_Contexto_Operacional.py", "Contexto Operacional", "02"),
            ("pages/03_Activos.py", "Gestión de Activos", "03"),
            ("pages/04_Mantenimiento.py", "Mantenimiento", "04"),
            ("pages/05_Indicadores.py", "Indicadores", "05"),
            ("pages/07_Criticidad_Integrado.py", "Matriz de Criticidad", "06"),
            ("pages/07_RCM.py", "RCM", "07"),
            ("pages/08_Equipo_RCM_Integrado.py", "Equipo RCM Integrado", "08"),
            ("pages/09_Monitoreo_Ambiental.py", "Monitoreo Ambiental", "09"),
            ("pages/10_Obsolescencia_Activos.py", "Obsolescencia de Activos", "10"),
        ]

        for ruta, etiqueta, icono in nav_items:
            if ruta == "app.py" or (BASE_DIR / ruta).exists():
                st.sidebar.page_link(ruta, label=f"{icono}  {etiqueta}")

        st.sidebar.markdown(
            '''
            <div style="margin:14px 8px 0;padding:12px 4px 0;border-top:1px solid rgba(255,255,255,.10);text-align:left;">
                <div style="color:#D4B75A;font-size:.61rem;font-weight:820;letter-spacing:.11em;text-transform:uppercase;">RCM · Metro de Medellín</div>
                <div style="color:rgba(255,255,255,.52);font-size:.61rem;margin-top:4px;line-height:1.4;">Gestión de la confiabilidad para la sostenibilidad</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )


def encabezado_pagina(titulo: str, subtitulo: str = "", icono: str = "") -> None:
    """Encabezado ejecutivo homogéneo para páginas internas."""
    etiqueta = f"{icono} {titulo}".strip()
    st.markdown(
        '<div class="metro-page-context"><span class="brand">METRO_RCM</span><span class="dot">•</span><span>GESTIÓN DE ACTIVOS Y CONFIABILIDAD</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class=\"udea-page-heading\">
            <div class=\"accent\"></div>
            <div>
                <div class=\"title\">{etiqueta}</div>
                <div class=\"subtitle\">{subtitulo}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
