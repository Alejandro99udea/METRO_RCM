from pathlib import Path
import streamlit as st

UDEA_LOGO_URL = "https://www.udea.edu.co/wps/wcm/connect/udea/99fc43e7-7a64-45bd-97fc-96639b70813d/logosimbolo-vertical.png?CVID=ljeLvHr&MOD=AJPERES"


def aplicar_tema_udea(mostrar_marca_sidebar=True, marca_agua=True):
    """Aplica la identidad visual UdeA + METRO_RCM a cualquier página Streamlit."""
    st.markdown(
        f"""
        <style>
        :root {{
            --udea-green: #004F3D;
            --udea-green-2: #006B54;
            --udea-green-3: #0B765C;
            --udea-light: #EAF3EF;
            --udea-border: #D8E4DE;
            --metro-dark: #24332F;
            --metro-gray: #64746F;
        }}

        .stApp {{
            background: #F7F9F8;
        }}

        [data-testid="stAppViewContainer"] > .main {{
            background: #F7F9F8;
        }}

        .block-container {{
            max-width: 1480px;
            padding-top: 1.5rem;
            padding-bottom: 3rem;
        }}

        /* Sidebar institucional */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #003F31 0%, #005442 55%, #00392D 100%);
            border-right: 1px solid rgba(255,255,255,.10);
        }}

        section[data-testid="stSidebar"] > div:first-child {{
            padding-top: 0.8rem;
        }}

        section[data-testid="stSidebar"] * {{
            color: #FFFFFF !important;
        }}

        section[data-testid="stSidebar"] hr {{
            border-color: rgba(255,255,255,.18) !important;
        }}

        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
            color: rgba(255,255,255,.84) !important;
        }}

        /* Navegación multipágina */
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {{
            border-radius: 10px;
            margin: 3px 6px;
            padding: 8px 10px;
            transition: background .15s ease;
        }}

        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {{
            background: rgba(255,255,255,.10);
        }}

        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {{
            background: rgba(255,255,255,.16);
            box-shadow: inset 3px 0 0 #FFFFFF;
        }}

        /* Marca dentro del sidebar */
        .udea-sidebar-brand {{
            text-align: center;
            padding: 8px 8px 18px 8px;
        }}

        .udea-sidebar-brand img {{
            width: 112px;
            max-width: 70%;
            height: auto;
            filter: brightness(0) invert(1);
            opacity: .96;
            margin-bottom: 8px;
        }}

        .udea-sidebar-title {{
            color: #FFFFFF !important;
            font-family: Georgia, 'Times New Roman', serif;
            font-size: 1.05rem;
            font-weight: 700;
            line-height: 1.15;
            letter-spacing: .03em;
        }}

        .udea-sidebar-subtitle {{
            color: rgba(255,255,255,.72) !important;
            font-size: .76rem;
            margin-top: 5px;
        }}

        /* Encabezados */
        h1, h2, h3, h4 {{
            color: var(--metro-dark);
            font-weight: 760;
            letter-spacing: -.02em;
        }}

        /* Tarjetas nativas */
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            border-color: var(--udea-border) !important;
            border-radius: 16px !important;
            background: rgba(255,255,255,.93);
            box-shadow: 0 4px 16px rgba(0,0,0,.035);
        }}

        div[data-testid="stMetric"] {{
            background: #FFFFFF;
            border: 1px solid var(--udea-border);
            border-left: 4px solid var(--udea-green-2);
            border-radius: 14px;
            padding: 12px 15px;
            box-shadow: 0 3px 10px rgba(0,0,0,.025);
        }}

        div[data-testid="stMetricLabel"] {{ color: var(--metro-gray); }}
        div[data-testid="stMetricValue"] {{ color: var(--metro-dark); }}

        /* Botones */
        .stButton > button, .stDownloadButton > button {{
            border-radius: 10px;
            border: 1px solid #BFD5CC;
            font-weight: 650;
        }}

        .stButton > button:hover, .stDownloadButton > button:hover {{
            border-color: var(--udea-green-2);
            color: var(--udea-green);
        }}

        /* Tabs */
        button[data-baseweb="tab"] {{
            font-weight: 650;
        }}
        button[data-baseweb="tab"][aria-selected="true"] {{
            color: var(--udea-green-2);
        }}
        div[data-baseweb="tab-highlight"] {{
            background: var(--udea-green-2);
        }}

        /* Tablas */
        div[data-testid="stDataFrame"] {{
            border: 1px solid var(--udea-border);
            border-radius: 12px;
            overflow: hidden;
        }}

        /* Fondo con escudo solo en páginas internas */
        {f'''[data-testid="stAppViewContainer"] > .main::before {{
            content: "";
            position: fixed;
            z-index: 0;
            pointer-events: none;
            width: 680px;
            height: 680px;
            left: 50%;
            top: 52%;
            transform: translate(-50%, -50%);
            background-image: url("{UDEA_LOGO_URL}");
            background-repeat: no-repeat;
            background-position: center;
            background-size: contain;
            opacity: .045;
            filter: grayscale(1);
        }}
        [data-testid="stAppViewContainer"] .main .block-container {{
            position: relative;
            z-index: 1;
        }}''' if marca_agua else ''}

        .udea-page-header {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }}

        .udea-page-header .bar {{
            width: 7px;
            height: 42px;
            border-radius: 999px;
            background: linear-gradient(180deg, var(--udea-green-2), var(--udea-green));
        }}

        .udea-page-header .title {{
            font-size: 2rem;
            font-weight: 800;
            color: var(--udea-green);
            line-height: 1.1;
        }}

        .udea-page-header .subtitle {{
            color: #71817C;
            font-size: .92rem;
            margin-top: 3px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    if mostrar_marca_sidebar:
        st.sidebar.markdown(
            f"""
            <div class="udea-sidebar-brand">
                <img src="{UDEA_LOGO_URL}" alt="Universidad de Antioquia">
                <div class="udea-sidebar-title">METRO_RCM</div>
                <div class="udea-sidebar-subtitle">Universidad de Antioquia · Facultad de Ingeniería</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.sidebar.divider()
