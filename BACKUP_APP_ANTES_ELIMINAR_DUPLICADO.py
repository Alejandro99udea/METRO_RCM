# -*- coding: utf-8 -*-

from utils.theme import aplicar_tema_udea, HERO_URI
import streamlit as st

from utils.reportes import generar_informe_pdf
from data.metro_data import METRO, LINEAS, TRANVIA


st.set_page_config(
    page_title="METRO_RCM | Inicio",
    page_icon="ðŸš‡",
    layout="wide",
    initial_sidebar_state="expanded",
)

aplicar_tema_udea(marca_agua=False)


def mostrar_boton_informe(
    key: str,
    titulo: str,
    subtitulo: str,
    secciones: list,
    nombre_archivo: str,
) -> None:
    """Genera el PDF del mÃ³dulo sin alterar la navegaciÃ³n."""
    if st.button("Generar informe", key=key, width="stretch"):
        pdf = generar_informe_pdf(
            titulo=titulo,
            subtitulo=subtitulo,
            secciones=secciones,
        )
        st.download_button(
            label="Descargar informe PDF",
            data=pdf,
            file_name=nombre_archivo,
            mime="application/pdf",
            width="stretch",
            key=f"{key}_download",
        )


st.markdown(
    """
    <style>
    .metro-cover-kicker {
        font-size: 1.65rem;
        font-weight: 820;
        letter-spacing: .01em;
        color: #4BD18E !important;
        margin-bottom: 1px;
    }

    .metro-cover-udea {
        font-size: .98rem;
        font-weight: 720;
        color: rgba(255,255,255,.93) !important;
        letter-spacing: .01em;
    }

    .metro-cover-rule {
        width: 57%;
        height: 2px;
        margin: 19px 0 22px;
        background: rgba(74,211,143,.82);
        border-radius: 999px;
    }

    .metro-cover-title {
        font-size: clamp(2.35rem, 4vw, 4rem);
        line-height: .98;
        font-weight: 850;
        letter-spacing: -.04em;
        color: #FFFFFF !important;
        margin: 0 0 13px;
    }

    .metro-cover-description {
        max-width: 820px;
        font-size: 1.02rem;
        line-height: 1.55;
        color: rgba(255,255,255,.91) !important;
    }

    .metro-cover-kpis {
        display: grid;
        grid-template-columns: repeat(4, minmax(0,1fr));
        gap: 0;
        margin-top: 29px;
        max-width: 940px;
    }

    .metro-cover-kpi {
        padding: 2px 22px 0 0;
        border-right: 1px solid rgba(255,255,255,.23);
        margin-right: 22px;
    }

    .metro-cover-kpi:last-child {
        border-right: none;
        margin-right: 0;
    }

    .metro-cover-kpi .value {
        color: #FFFFFF;
        font-size: 1.62rem;
        line-height: 1;
        font-weight: 850;
    }

    .metro-cover-kpi .label {
        color: rgba(255,255,255,.80);
        font-size: .70rem;
        font-weight: 760;
        text-transform: uppercase;
        letter-spacing: .04em;
        margin-top: 5px;
    }

    .metro-section-head {
        margin: 5px 0 17px;
    }

    .metro-section-head .title {
        color: #1E312B;
        font-size: 1.58rem;
        font-weight: 820;
        margin-bottom: 2px;
    }

    .metro-section-head .title::before {
        content: "â–¦";
        color: #118567;
        font-size: 1.15rem;
        margin-right: 9px;
    }

    .metro-section-head .subtitle {
        color: #71807B;
        font-size: .88rem;
    }

    /* Tarjetas de navegaciÃ³n del proyecto: tamaño uniforme */
    [data-testid="stVerticalBlockBorderWrapper"] {
        height: 100%;
        min-height: 365px;
        box-sizing: border-box;
    }

    .metro-nav-card {
        min-height: 205px;
        display: flex;
        flex-direction: column;
    }

    .metro-nav-card p {
        min-height: 68px;
        margin-bottom: 0 !important;
    }

    .metro-nav-card h3 {
        color: #1F302B !important;
        font-size: 1.03rem !important;
        margin-bottom: 5px !important;
    }

    .metro-nav-card p {
        color: #687772 !important;
        font-size: .80rem !important;
        line-height: 1.42 !important;
        min-height: 68px;
        margin-bottom: 0 !important;
    }

    .metro-nav-card .icon {
        width: 38px;
        height: 38px;
        border-radius: 999px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: #E4F3EC;
        color: #007052;
        font-size: 1.05rem;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .metro-cover-footer {
        color: #74847F;
        font-size: .77rem;
        text-align: center;
        padding: 22px 0 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# HERO / PORTADA
# ------------------------------------------------------------

with st.container(key="hero_portada"):
    st.markdown('<div class="metro-cover-kicker">RCM</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="metro-cover-udea">UNIVERSIDAD DE ANTIOQUIA</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="metro-cover-rule"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="metro-cover-title">CONFIABILIDAD EN MOVIMIENTO</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
<div class="metro-cover-description">
Plataforma interactiva desarrollada para estructurar el contexto del negocio,
contexto operacional, activos, mantenimiento, criticidad y anÃ¡lisis RCM del
Metro de MedellÃ­n.
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
<div class="metro-cover-kpis">
<div class="metro-cover-kpi">
<div class="value">{METRO.get('red_integrada_km', 'N/D'):.1f} km</div>
<div class="label">Red integrada</div>
</div>
<div class="metro-cover-kpi">
<div class="value">{METRO.get('trenes', 'N/D')}</div>
<div class="label">Trenes registrados</div>
</div>
<div class="metro-cover-kpi">
<div class="value">{METRO.get('metrocables', 'N/D')}</div>
<div class="label">Metrocables</div>
</div>
<div class="metro-cover-kpi">
<div class="value">{METRO.get('viajes_corporativos_2025_m', 'N/D')} M</div>
<div class="label">Viajes corporativos 2025</div>
</div>
</div>
""",
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------
# NAVEGACIÃ“N
# ------------------------------------------------------------

st.markdown(
    """
<div class="metro-section-head">
<div class="title">NavegaciÃ³n del proyecto</div>
<div class="subtitle">Seleccione un mÃ³dulo para acceder directamente a la informaciÃ³n.</div>
</div>
""",
    unsafe_allow_html=True,
)

cards = [
    {
        "icon": "â–¦",
        "titulo": "Contexto del negocio",
        "descripcion": "Empresa, modelo de negocio, estrategia, finanzas y creaciÃ³n de valor.",
        "ruta": "pages/01_Contexto_del_Negocio.py",
        "button": "btn_negocio",
        "report_key": "btn_informe_negocio",
        "report_title": "Contexto del Negocio",
        "report_subtitle": "Metro de MedellÃ­n Â· GestiÃ³n de Activos y RCM",
        "report_file": "Informe_Contexto_del_Negocio.pdf",
        "sections": [
            {"titulo": "Perfil empresarial", "datos": [
                ["Empresa", METRO.get("empresa", "N/D")],
                ["Empleados 2025", METRO.get("empleados_2025", "N/D")],
                ["Red integrada", f"{METRO.get('red_integrada_km', 'N/D')} km"],
                ["Red fÃ©rrea", f"{METRO.get('red_ferrea_km', 'N/D')} km"],
            ]},
            {"titulo": "Finanzas 2025", "datos": [
                ["Ingresos", f"${METRO.get('ingresos_2025_m', 'N/D')} millones"],
                ["Ingresos de transporte", f"${METRO.get('ingresos_transporte_2025_m', 'N/D')} millones"],
                ["Negocios asociados", f"${METRO.get('negocios_asociados_2025_m', 'N/D')} millones"],
                ["EBITDA", f"${METRO.get('ebitda_2025_m', 'N/D')} millones"],
                ["Utilidad neta", f"${METRO.get('utilidad_neta_2025_m', 'N/D')} millones"],
                ["Activos", f"${METRO.get('activos_2025_m', 'N/D')} millones"],
            ]},
            {"titulo": "GestiÃ³n de activos", "datos": [
                ["Trenes", METRO.get("trenes", "N/D")],
                ["Coches", METRO.get("coches_tren", "N/D")],
                ["Metrocables", METRO.get("metrocables", "N/D")],
                ["TranvÃ­a", METRO.get("tranvia", "N/D")],
                ["BRT", METRO.get("brt", "N/D")],
            ]},
            {"titulo": "Estrategia 2026â€“2035", "datos": [
                [f"OE{i+1}", objetivo]
                for i, objetivo in enumerate(METRO.get("estrategia_2026_2035", []))
            ]},
        ],
    },
    {
        "icon": "ðŸš‡",
        "titulo": "Contexto operacional",
        "descripcion": "Modos de transporte, lÃ­neas, rÃ©gimen de marcha y condiciones de operaciÃ³n.",
        "ruta": "pages/02_Contexto_Operacional.py",
        "button": "btn_operacional",
        "report_key": "btn_informe_operacional",
        "report_title": "Contexto Operacional",
        "report_subtitle": "Sistema Metro de MedellÃ­n Â· Condiciones de operaciÃ³n",
        "report_file": "Informe_Contexto_Operacional.pdf",
        "sections": [
            {"titulo": "Modos de transporte", "datos": [
                ["Metro", "LÃ­neas A y B"], ["TranvÃ­a", "LÃ­nea T"],
                ["Buses", "LÃ­neas 1, 2 y O"], ["Metrocables", "H, J, K, L, M y P"],
            ]},
            {"titulo": "LÃ­nea A", "datos": [
                ["Recorrido", LINEAS.get("A", {}).get("recorrido", "N/D")],
                ["Longitud", f"{LINEAS.get('A', {}).get('longitud_km', 'N/D')} km"],
                ["Estaciones", len(LINEAS.get("A", {}).get("estaciones", []))],
                ["Tiempo de recorrido", f"{LINEAS.get('A', {}).get('tiempo_recorrido_min', 'N/D')} min"],
                ["Velocidad comercial", f"{LINEAS.get('A', {}).get('velocidad_comercial_kmh', 'N/D')} km/h"],
                ["Velocidad mÃ¡xima", f"{LINEAS.get('A', {}).get('velocidad_maxima_kmh', 'N/D')} km/h"],
                ["Capacidad", f"{LINEAS.get('A', {}).get('capacidad_pax_hora_sentido', 'N/D')} pax/h/sentido"],
            ]},
            {"titulo": "LÃ­nea B", "datos": [
                ["Recorrido", LINEAS.get("B", {}).get("recorrido", "N/D")],
                ["Longitud", f"{LINEAS.get('B', {}).get('longitud_km', 'N/D')} km"],
                ["Estaciones", len(LINEAS.get("B", {}).get("estaciones", []))],
                ["Tiempo de recorrido", f"{LINEAS.get('B', {}).get('tiempo_recorrido_min', 'N/D')} min"],
                ["Velocidad comercial", f"{LINEAS.get('B', {}).get('velocidad_comercial_kmh', 'N/D')} km/h"],
                ["Velocidad mÃ¡xima", f"{LINEAS.get('B', {}).get('velocidad_maxima_kmh', 'N/D')} km/h"],
                ["Capacidad", f"{LINEAS.get('B', {}).get('capacidad_pax_hora_sentido', 'N/D')} pax/h/sentido"],
            ]},
            {"titulo": "TranvÃ­a LÃ­nea T", "datos": [
                ["Recorrido", TRANVIA.get("recorrido", "N/D")],
                ["Longitud", f"{TRANVIA.get('longitud_km', 'N/D')} km"],
                ["VehÃ­culos", TRANVIA.get("vehiculos", "N/D")],
                ["Velocidad comercial", f"{TRANVIA.get('vel_comercial', 'N/D')} km/h"],
                ["Capacidad", f"{TRANVIA.get('capacidad_pax_hs', 'N/D')} pax/h/sentido"],
            ]},
        ],
    },
    {
        "icon": "â—‡",
        "titulo": "GestiÃ³n de activos",
        "descripcion": "Inventario, clasificaciÃ³n de activos, sistemas y componentes.",
        "ruta": "pages/03_Activos.py",
        "button": "btn_activos",
        "report_key": "btn_informe_activos",
        "report_title": "GestiÃ³n de Activos",
        "report_subtitle": "Inventario y estructura de activos del Metro",
        "report_file": "Informe_Gestion_de_Activos.pdf",
        "sections": [
            {"titulo": "Inventario corporativo", "datos": [
                ["Red integrada", f"{METRO.get('red_integrada_km', 'N/D')} km"],
                ["Red fÃ©rrea", f"{METRO.get('red_ferrea_km', 'N/D')} km"],
                ["Trenes", METRO.get("trenes", "N/D")],
                ["Coches", METRO.get("coches_tren", "N/D")],
                ["Metrocables", METRO.get("metrocables", "N/D")],
                ["TranvÃ­a", METRO.get("tranvia", "N/D")],
                ["BRT", METRO.get("brt", "N/D")],
            ]},
            {"titulo": "Madurez de activos", "datos": [
                [str(año), valor]
                for año, valor in METRO.get("madurez_activos", {}).items()
            ]},
        ],
    },
    {
        "icon": "âš’",
        "titulo": "Mantenimiento",
        "descripcion": "Estrategias, planes, fallas, rutinas y recursos de mantenimiento.",
        "ruta": "pages/04_Mantenimiento.py",
        "button": "btn_mantenimiento",
        "report_key": "btn_informe_mantenimiento",
        "report_title": "Mantenimiento",
        "report_subtitle": "GestiÃ³n del mantenimiento Â· Metro de MedellÃ­n",
        "report_file": "Informe_Mantenimiento.pdf",
        "sections": [
            {"titulo": "Modalidades", "datos": [["Modalidad", m] for m in METRO["mantenimiento"]["modalidades"]]},
            {"titulo": "Indicadores", "datos": [
                ["Modos de falla 2016", METRO["mantenimiento"]["modos_falla_2016"]],
                ["Modos de falla 2024", METRO["mantenimiento"]["modos_falla_2024"]],
                ["Regularidad A 2022", METRO["mantenimiento"]["regularidad_A_2022"]],
                ["Regularidad A 2023", METRO["mantenimiento"]["regularidad_A_2023"]],
                ["Incremento fallas crÃ­ticas", f"{METRO['mantenimiento']['fallas_criticas_incremento_pct']} %"],
            ]},
            {"titulo": "InversiÃ³n", "datos": [
                ["Plan de mantenimiento 2025", f"${METRO.get('mantenimiento_plan_2025_m_mas', 'N/D')} millones"],
                ["Adquisiciones PP&E 2025", f"${METRO.get('ppye_adquisiciones_2025_m', 'N/D')} millones"],
            ]},
        ],
    },
    {
        "icon": "â–¥",
        "titulo": "Indicadores",
        "descripcion": "Disponibilidad, confiabilidad, MTBF, MTTR y desempeÃ±o operacional.",
        "ruta": "pages/05_Indicadores.py",
        "button": "btn_indicadores",
        "report_key": "btn_informe_indicadores",
        "report_title": "Indicadores",
        "report_subtitle": "Indicadores corporativos, operacionales y de gestiÃ³n",
        "report_file": "Informe_Indicadores.pdf",
        "sections": [
            {"titulo": "Indicadores corporativos", "datos": [
                ["Viajes corporativos 2025", f"{METRO.get('viajes_corporativos_2025_m', 'N/D')} millones"],
                ["SatisfacciÃ³n", METRO.get("satisfaccion", "N/D")],
                ["Experiencia", METRO.get("experiencia", "N/D")],
                ["Meta satisfacciÃ³n", METRO.get("meta_satisfaccion", "N/D")],
            ]},
            {"titulo": "Indicadores financieros", "datos": [
                ["Ingresos 2025", f"${METRO.get('ingresos_2025_m', 'N/D')} millones"],
                ["EBITDA 2025", f"${METRO.get('ebitda_2025_m', 'N/D')} millones"],
                ["Utilidad neta 2025", f"${METRO.get('utilidad_neta_2025_m', 'N/D')} millones"],
            ]},
        ],
    },
    {
        "icon": "â–¦",
        "titulo": "Matriz de criticidad",
        "descripcion": "PriorizaciÃ³n de activos mediante consecuencia y probabilidad de falla.",
        "ruta": "pages/07_Criticidad_Integrado.py",
        "button": "btn_matriz_criticidad",
        "report_key": None,
    },
    {
        "icon": "â¬¡",
        "titulo": "RCM",
        "descripcion": "Funciones, fallas, efectos, consecuencias y tareas de mantenimiento.",
        "ruta": "pages/07_RCM.py",
        "button": "btn_rcm",
        "report_key": "btn_informe_rcm",
        "report_title": "AnÃ¡lisis RCM",
        "report_subtitle": "Reliability Centered Maintenance Â· Metro de MedellÃ­n",
        "report_file": "Informe_RCM.pdf",
        "sections": [
            {"titulo": "MetodologÃ­a", "datos": [
                ["FunciÃ³n", "DefiniciÃ³n de la funciÃ³n requerida"],
                ["Falla funcional", "PÃ©rdida total o parcial de la funciÃ³n"],
                ["Modo de falla", "Causa fÃ­sica o tÃ©cnica de la falla"],
                ["Efecto", "Consecuencia observable del modo de falla"],
                ["Consecuencia", "Impacto operacional, econÃ³mico, ambiental o de seguridad"],
                ["Tarea RCM", "AcciÃ³n de mantenimiento tÃ©cnicamente seleccionada"],
            ]},
            {"titulo": "Estado del proyecto", "datos": [
                ["AnÃ¡lisis RCM", "En desarrollo"],
                ["FMECA", "En desarrollo"],
                ["Tareas de mantenimiento", "Pendiente de consolidaciÃ³n por activo"],
            ]},
        ],
    },
    {
        "icon": "â™™",
        "titulo": "Equipo RCM integrado",
        "descripcion": "Integrantes, roles, perfiles, competencias y especialidades.",
        "ruta": "pages/08_Equipo_RCM_Integrado.py",
        "button": "btn_equipo_rcm",
        "report_key": "btn_informe_equipo_rcm",
        "report_title": "Equipo RCM",
        "report_subtitle": "Integrantes, roles y competencias del equipo",
        "report_file": "Informe_Equipo_RCM.pdf",
        "sections": [
            {"titulo": "Equipo de trabajo", "datos": [
                ["Proyecto", "METRO_RCM"],
                ["Ãrea", "GestiÃ³n de Activos y RCM"],
                ["Equipo", "Equipo RCM"],
            ]},
            {"titulo": "Roles y competencias", "datos": [
                ["InformaciÃ³n", "Consultar mÃ³dulo Equipo RCM"],
            ]},
        ],
    },
    {
        "icon": "âŒ",
        "titulo": "Monitoreo ambiental",
        "descripcion": "Condiciones ambientales y variables SIATA asociadas a la operaciÃ³n.",
        "ruta": "pages/09_Monitoreo_Ambiental.py",
        "button": "btn_siata_portada",
        "report_key": "btn_informe_ambiental",
        "report_title": "Monitoreo Ambiental",
        "report_subtitle": "InformaciÃ³n ambiental y meteorolÃ³gica Â· SIATA",
        "report_file": "Informe_Monitoreo_Ambiental.pdf",
        "sections": [
            {"titulo": "Fuente", "datos": [
                ["Sistema", "SIATA"],
                ["Cobertura", "Valle de AburrÃ¡"],
                ["Naturaleza", "InformaciÃ³n ambiental externa"],
            ]},
            {"titulo": "Variables", "datos": [
                ["Temperatura", "Monitoreada"],
                ["Humedad", "Monitoreada"],
                ["PrecipitaciÃ³n", "Monitoreada"],
                ["Viento", "Monitoreado"],
                ["Radar meteorolÃ³gico", "Disponible"],
            ]},
            {"titulo": "RelaciÃ³n con activos", "datos": [
                ["Lluvia intensa", "VÃ­a, drenajes, estaciones e infraestructura"],
                ["Tormentas", "Sistemas elÃ©ctricos y comunicaciones"],
                ["Viento", "Infraestructura elevada y Metrocables"],
            ]},
        ],
    },    {
        "icon": "♻️",
        "titulo": "Obsolescencia de Activos",
        "descripcion": "Evaluación de obsolescencia tecnológica, vida útil, riesgo y priorización de activos.",
        "ruta": "pages/10_Obsolescencia_Activos.py",
        "button": "btn_obsolescencia",
        "report_key": "btn_informe_obsolescencia",
        "report_title": "Obsolescencia de Activos",
        "report_subtitle": "METRO_RCM · Evaluación y priorización de obsolescencia",
        "report_file": "Informe_Obsolescencia_Activos.pdf",
        "sections": [
            {
                "titulo": "Módulo",
                "datos": [
                    ["Aplicación", "Obsolescencia de Activos"],
                    ["Propósito", "Evaluar y priorizar activos según su condición de obsolescencia."]
                ]
            }
        ]
    },
]

# Tres filas de tres tarjetas: ancho, alto y jerarquÃ­a visual uniformes.
# ============================================================
# NAVEGACIÓN DEL PROYECTO
# ============================================================

ICONOS_PORTADA = {
    "pages/01_Contexto_del_Negocio.py": "🏢",
    "pages/02_Contexto_Operacional.py": "🚇",
    "pages/03_Activos.py": "📦",
    "pages/04_Mantenimiento.py": "🔧",
    "pages/05_Indicadores.py": "📊",
    "pages/07_Criticidad_Integrado.py": "🎯",
    "pages/07_RCM.py": "🔄",
    "pages/08_Equipo_RCM_Integrado.py": "👥",
    "pages/09_Monitoreo_Ambiental.py": "📡",
    "pages/10_Obsolescencia_Activos.py": "♻️",
}

for inicio in range(0, len(cards), 3):

    fila = cards[inicio:inicio + 3]

    cols = st.columns(3, gap="medium")

    for idx, card in enumerate(fila):

        with cols[idx]:

            with st.container(border=True):

                icono = ICONOS_PORTADA.get(
                    card.get("ruta"),
                    "•",
                )

                st.markdown(
                    '<div class="metro-nav-card">'
                    f'<div class="icon">{icono}</div>'
                    f'<h3>{card["titulo"]}</h3>'
                    f'<p>{card["descripcion"]}</p>'
                    '</div>',
                    unsafe_allow_html=True,
                )

                if st.button(
                    "Abrir módulo →",
                    key=card["button"],
                    width="stretch",
                ):
                    st.switch_page(card["ruta"])

                if st.button(
                    "Generar informe",
                    key=card["report_key"],
                    width="stretch",
                ):
                    generar_informe(
                        card["report_title"],
                        card["report_subtitle"],
                        card["sections"],
                        card["report_file"],
                    )

ICONOS_PORTADA = {
    "pages/01_Contexto_del_Negocio.py": "\U0001F3E2",
    "pages/02_Contexto_Operacional.py": "\U0001F687",
    "pages/03_Activos.py": "\U0001F4E6",
    "pages/04_Mantenimiento.py": "\U0001F527",
    "pages/05_Indicadores.py": "\U0001F4CA",
    "pages/07_Criticidad_Integrado.py": "\U0001F3AF",
    "pages/07_RCM.py": "\U0001F504",
    "pages/08_Equipo_RCM_Integrado.py": "\U0001F465",
    "pages/09_Monitoreo_Ambiental.py": "\U0001F4E1",
    "pages/10_Obsolescencia_Activos.py": "\u267B\uFE0F",
}

for idx, card in enumerate(fila):
        with cols[idx]:
            with st.container(border=True):
                st.markdown(
                    '<div class="metro-nav-card">'
                    f'<div class="icon">{ICONOS_PORTADA.get(card.get("ruta"), "\u2022")}</div>'
                    f'<h3>{card["titulo"]}</h3>'
                    f'<p>{card["descripcion"]}</p>'
                    '</div>',
                    unsafe_allow_html=True,
                )
                if st.button(
                    "Abrir mÃ³dulo â†’",
                    key=card["button"],
                    width="stretch",
                ):
                    st.switch_page(card["ruta"])

                if card.get("report_key"):
                    mostrar_boton_informe(
                        key=card["report_key"],
                        titulo=card["report_title"],
                        subtitulo=card["report_subtitle"],
                        nombre_archivo=card["report_file"],
                        secciones=card["sections"],
                    )

st.markdown(
    """
<div class="metro-cover-footer">
Â© 2026 Universidad de Antioquia â€” METRO_RCM Â· GestiÃ³n de la Confiabilidad para la Sostenibilidad
</div>
""",
    unsafe_allow_html=True,
)

