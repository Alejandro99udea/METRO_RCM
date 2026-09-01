# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
from pathlib import Path

from data.metro_data import TRANVIA, BUSES, LINEAS
from pages.sistemas.rodadura import mostrar_rodadura


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Contexto Operacional | Metro de Medellín",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# RUTAS
# ============================================================

# ============================================================
# RUTAS DE IMÁGENES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ------------------------------------------------------------
# IMAGEN TRANVÍA
# ------------------------------------------------------------

IMAGEN_TRANVIA = (
    BASE_DIR
    / "assets"
    / "tranvia"
    / "principal.jpg.webp"
)


# ------------------------------------------------------------
# IMAGEN LÍNEA A
# ------------------------------------------------------------

CARPETA_LINEA_A = (
    BASE_DIR
    / "assets"
    / "linea_a"
)

IMAGEN_LINEA_A = None

for nombre_archivo in [
    "principal.jpg",
    "principal.jpeg",
    "principal.png",
    "principal.webp",
]:

    ruta = CARPETA_LINEA_A / nombre_archivo

    if ruta.exists():

        IMAGEN_LINEA_A = ruta

        break


# ------------------------------------------------------------
# IMAGEN LÍNEA B
# ------------------------------------------------------------

CARPETA_LINEA_B = (
    BASE_DIR
    / "assets"
    / "linea_b"
)

IMAGEN_LINEA_B = None

for nombre_archivo in [
    "principal.jpg",
    "principal.jpeg",
    "principal.png",
    "principal.webp",
]:

    ruta = CARPETA_LINEA_B / nombre_archivo

    if ruta.exists():

        IMAGEN_LINEA_B = ruta

        break


# ============================================================
# IMAGEN TRANVÍA
# ============================================================

IMAGEN_TRANVIA = (
    BASE_DIR
    / "assets"
    / "tranvia"
    / "principal.jpg.webp"
)


# ============================================================
# IMAGEN LÍNEA A
# ============================================================

CARPETA_LINEA_A = (
    BASE_DIR
    / "assets"
    / "linea_a"
)

IMAGEN_LINEA_A = None

for nombre_archivo in [
    "principal.jpg",
    "principal.jpeg",
    "principal.png",
    "principal.webp",
]:

    ruta = CARPETA_LINEA_A / nombre_archivo

    if ruta.exists():
        IMAGEN_LINEA_A = ruta
        break

    CARPETA_LINEA_B = (
    BASE_DIR
    / "assets"
    / "linea_b"
)

IMAGEN_LINEA_B = None

for nombre_archivo in [
    "principal.jpg",
    "principal.jpeg",
    "principal.png",
    "principal.webp",
]:

    ruta = CARPETA_LINEA_B / nombre_archivo

    if ruta.exists():
        IMAGEN_LINEA_B = ruta
        break

# ============================================================
# ESTILOS
# ============================================================

st.markdown(
    """
    <style>

    .hero {
        background: linear-gradient(
            135deg,
            #ffffff 0%,
            #f4f6f8 100%
        );
        border: 1px solid #dfe3e8;
        border-radius: 18px;
        padding: 26px 32px;
        margin-bottom: 24px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.04);
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 750;
        color: #111827;
        line-height: 1.15;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #6b7280;
        margin-top: 6px;
    }

    .system-card {
        background: #ffffff;
        border: 1px solid #dfe3e8;
        border-radius: 16px;
        padding: 20px;
        min-height: 145px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }

    .system-card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 8px;
    }

    .system-card-text {
        font-size: 0.9rem;
        color: #6b7280;
        line-height: 1.45;
    }

    .pending-box {
        background: #fff8e6;
        border: 1px solid #efd28a;
        border-radius: 14px;
        padding: 18px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def formatear_numero(valor):
    try:
        return f"{int(valor):,}".replace(",", ".")
    except (ValueError, TypeError):
        return str(valor)


def mostrar_linea_pendiente(nombre_linea, modo):
    st.title(f"{modo} — {nombre_linea}")

    st.info(
        f"""
        La línea **{nombre_linea}** se encuentra registrada dentro
        de la arquitectura del Sistema Metro de Medellín.

        El contexto operacional detallado de esta línea todavía
        está pendiente de consolidación documental específica.
        """
    )

    datos = LINEAS.get(
        nombre_linea.replace("Línea ", ""),
        {}
    )

    st.subheader("Información general")

    c1, c2 = st.columns(2)

    with c1:
        st.write(f"**Modo:** {modo}")

    with c2:
        st.write(
            f"**Recorrido:** {datos.get('recorrido', 'Pendiente')}"
        )

    st.divider()

    st.markdown(
        """
        <div class="pending-box">

        <strong>Información pendiente de consolidación</strong>

        <br><br>

        Para desarrollar esta línea como módulo RCM se requiere
        documentación operacional, técnica y de mantenimiento
        específica del activo.

        </div>
        """,
        unsafe_allow_html=True,
    )


def tarjeta_sistema(icono, nombre, descripcion):
    st.markdown(
        f"""
        <div class="system-card">
            <div class="system-card-title">
                {icono} {nombre}
            </div>

            <div class="system-card-text">
                {descripcion}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# CABECERA
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">
            ⚙️ CONTEXTO OPERACIONAL
        </div>

        <div class="hero-subtitle">
            Sistema integrado de consulta operacional y gestión
            de activos — Metro de Medellín
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# INFORME COMPLETO DE INVESTIGACIÓN
# ============================================================

st.markdown("### 📚 Informe completo de investigación")

st.caption(
    "Consulta el informe de investigación utilizado como base "
    "para la construcción del contexto operacional."
)

st.link_button(
    "📖 Abrir informe completo en Canva →",
    "https://www.canva.com/design/DAHSxqUCCKM/zPJ8-JzQHxjnWaObShsMAg/view?utm_content=DAHSxqUCCKM&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hef7e6573db",
    width="stretch",
)

st.divider()
# ============================================================
# SELECTOR PRINCIPAL
# ============================================================

st.subheader("Seleccionar modo de transporte")

modo_seleccionado = st.selectbox(
    "Seleccione el modo",
    [
        "🚇 Metro",
        "🚋 Tranvía",
        "🚌 Buses",
        "🚡 Metrocables",
    ],
)


# ============================================================
# LÍNEAS DISPONIBLES
# ============================================================

LINEAS_POR_MODO = {

    "🚇 Metro": [
        "Línea A",
        "Línea B",
    ],

    "🚋 Tranvía": [
        "Línea T",
    ],

    "🚌 Buses": [
        "Línea 1",
        "Línea 2",
        "Línea O",
    ],

    "🚡 Metrocables": [
        "Línea H",
        "Línea J",
        "Línea K",
        "Línea L",
        "Línea M",
        "Línea P",
    ],
}


linea_seleccionada = st.selectbox(
    "Seleccione la línea",
    LINEAS_POR_MODO[modo_seleccionado],
)


# ============================================================
# ============================================================
# LÍNEA A — METRO
# ============================================================
# ============================================================

if linea_seleccionada == "Línea A":

    A = LINEAS["A"]

        # ========================================================
    # CABECERA DE LÍNEA A
    # ========================================================

    col_info, col_imagen = st.columns(
        [1.8, 1],
        gap="large"
    )

    with col_info:

        st.markdown(
            """
            <div style="
                padding-top: 15px;
            ">
            """,
            unsafe_allow_html=True
        )

        st.title(
            "🚇 LÍNEA A"
        )

        st.subheader(
            "Metro de Medellín"
        )

        st.markdown(
            "**Niquía ↔ La Estrella**"
        )

        st.write(
            "Línea ferroviaria principal del sistema Metro "
            "de Medellín, con operación norte–sur."
        )

        st.markdown(
            f"""
            **Longitud:** {A['longitud_km']} km  
            **Estaciones:** {len(A['estaciones'])}  
            **Inicio de operación:** {A['inicio_operacion']}
            """
        )

    with col_imagen:

        if IMAGEN_LINEA_A is not None:

            st.image(
                str(IMAGEN_LINEA_A),
                width=360,
                caption="Línea A — Metro de Medellín"
            )

        else:

            st.info(
                "Imagen de Línea A no disponible."
            )
    # --------------------------------------------------------
    # INDICADORES
    # --------------------------------------------------------

    st.subheader("Parámetros operacionales")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Longitud",
        f"{A['longitud_km']} km"
    )

    c2.metric(
    "Estaciones",
    len(A["estaciones"])
)

    c3.metric(
        "Tiempo de recorrido",
        f"{A['tiempo_recorrido_min']} min"
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "Velocidad comercial",
        f"{A['velocidad_comercial_kmh']} km/h"
    )

    c5.metric(
        "Velocidad máxima",
        f"{A['velocidad_maxima_kmh']} km/h"
    )

    c6.metric(
        "Frecuencia mínima",
        A["frecuencia_minima_texto"]
    )

    c7, c8, c9 = st.columns(3)

    c7.metric(
        "Capacidad",
        f"{formatear_numero(A['capacidad_pax_hora_sentido'])} pax/h/sentido"
    )

    c8.metric(
        "Estaciones elevadas",
        A["estaciones_elevadas"]
    )

    c9.metric(
        "Inicio operación",
        A["inicio_operacion"]
    )

    # --------------------------------------------------------
    # RESUMEN / ESTACIONES / TRANSFERENCIAS / RÉGIMEN / RCM
    # --------------------------------------------------------

    st.divider()

    tabs_a = st.tabs(
        [
            "Resumen",
            "Estaciones",
            "Transferencias",
            "Régimen de marcha",
            "Contexto RCM",
            "Fuentes",
        ]
    )

    # --------------------------------------------------------
    # RESUMEN
    # --------------------------------------------------------

    with tabs_a[0]:

        resumen_a = [
            ["Modo", A["modo"]],
            ["Recorrido", A["recorrido"]],
            ["Longitud", f"{A['longitud_km']} km"],
["Estaciones", len(A["estaciones"])],            ["Estaciones elevadas", A["estaciones_elevadas"]],
            ["Sistema", A["tipo_sistema"]],
            ["Configuración", A["configuracion_tren"]],
            [
                "Trenes conjunto A+B",
                A["trenes_ab"]
            ],
            [
                "Vagones conjunto A+B",
                A["vagones_ab"]
            ],
            [
                "Tiempo de recorrido",
                f"{A['tiempo_recorrido_min']} min/sentido"
            ],
            [
                "Velocidad comercial",
                f"{A['velocidad_comercial_kmh']} km/h"
            ],
            [
                "Velocidad máxima",
                f"{A['velocidad_maxima_kmh']} km/h"
            ],
            [
                "Frecuencia mínima",
                A["frecuencia_minima_texto"]
            ],
            [
                "Capacidad",
                f"{formatear_numero(A['capacidad_pax_hora_sentido'])} pax/h/sentido"
            ],
            [
                "Inicio operación comercial",
                A["inicio_operacion"]
            ],
        ]

        st.dataframe(
            pd.DataFrame(
                resumen_a,
                columns=["Característica", "Valor"]
            ),
            width="stretch",
            hide_index=True,
        )

        st.info(
            "La cifra de trenes y vagones corresponde al conjunto "
            "de las líneas A y B, no exclusivamente a Línea A."
        )

    # --------------------------------------------------------
    # ESTACIONES
    # --------------------------------------------------------

    with tabs_a[1]:

        st.subheader(
            f"Estaciones de Línea A ({len(A['estaciones'])})"
        )

        estacion = st.selectbox(
            "Seleccione una estación",
            A["estaciones"],
            key="estacion_linea_a"
        )

        numero = A["estaciones"].index(estacion) + 1

        st.metric(
            "Posición en el recorrido",
            f"{numero} / {len(A['estaciones'])}"
        )

        st.write(
            f"**Estación seleccionada:** {estacion}"
        )

        st.markdown("### Secuencia de estaciones")

        for indice, nombre in enumerate(
            A["estaciones"],
            start=1
        ):

            marcador = "🔹"

            if nombre == estacion:
                marcador = "🔴"

            st.markdown(
                f"{marcador} **{indice}. {nombre}**"
            )

    # --------------------------------------------------------
    # TRANSFERENCIAS
    # --------------------------------------------------------

    with tabs_a[2]:

        st.subheader(
            "Estaciones de transferencia"
        )

        transferencias = A[
            "estaciones_transferencia"
        ]

        for transferencia in transferencias:

            st.markdown(
                f"""
                <div class="system-card">
                    <div class="system-card-title">
                        🔄 {transferencia}
                    </div>

                    <div class="system-card-text">
                        Estación identificada como punto de
                        transferencia dentro de la información
                        operacional de Línea A.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.write("")

    # --------------------------------------------------------
    # RÉGIMEN DE MARCHA
    # --------------------------------------------------------

    with tabs_a[3]:

        st.subheader("Régimen de marcha")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Recorrido",
            f"{A['tiempo_recorrido_min']} min"
        )

        c2.metric(
            "Velocidad comercial",
            f"{A['velocidad_comercial_kmh']} km/h"
        )

        c3.metric(
            "Velocidad máxima",
            f"{A['velocidad_maxima_kmh']} km/h"
        )

        c4.metric(
            "Frecuencia mínima",
            A["frecuencia_minima_texto"]
        )

        st.metric(
            "Capacidad",
            f"{formatear_numero(A['capacidad_pax_hora_sentido'])} pax/h/sentido"
        )

        st.write(
            """
            El régimen de marcha deberá complementarse posteriormente
            con horarios operacionales, intervalos por franja horaria,
            ciclos de operación y comportamiento de la demanda.
            """
        )

    # --------------------------------------------------------
    # RCM
    # --------------------------------------------------------

    with tabs_a[4]:

        st.subheader(
            "Contexto operacional para RCM"
        )

        st.info(
            """
            Línea A será desarrollada posteriormente a nivel de
            sistemas, subsistemas, equipos y componentes.
            """
        )

        st.code(
            """
LÍNEA A
   ↓
Sistemas
   ↓
Subsistemas
   ↓
Activos
   ↓
Funciones
   ↓
Fallas funcionales
   ↓
Modos de falla
   ↓
Efectos
   ↓
Consecuencias
   ↓
Tareas RCM
            """,
            language="text"
        )

    # --------------------------------------------------------
    # FUENTES
    # --------------------------------------------------------

    with tabs_a[5]:

        st.subheader("Fuente principal")

        st.markdown(
            """
            **Metro de Medellín — Línea A**

            Información oficial del sistema integrado,
            complementada posteriormente con documentación
            técnica y operacional del proyecto RCM.
            """
        )

        st.code(
            "https://www.metrodemedellin.gov.co/usuarios/sistema-integrado/linea-a",
            language="text"
        )


# ============================================================
# ============================================================
# LÍNEA T — TRANVÍA
# ============================================================
# ============================================================

elif linea_seleccionada == "Línea T":

    st.title(
        "🚋 LÍNEA T — TRANVÍA DE AYACUCHO"
    )

    st.caption(
        "San Antonio ↔ Oriente"
    )

    col_img, col_info = st.columns(
        [1.45, 1],
        gap="large",
    )

    with col_img:

        if IMAGEN_TRANVIA.exists():

            st.image(
                str(IMAGEN_TRANVIA),
                width=650,
            )

        else:

            st.warning(
                "No se encontró la fotografía principal del Tranvía."
            )

    with col_info:

        st.subheader(
            "Identificación operacional"
        )

        st.write(
            f"**Código:** {TRANVIA['codigo']}"
        )

        st.write(
            f"**Nombre:** {TRANVIA['nombre']}"
        )

        st.write(
            f"**Modo:** {TRANVIA['modo']}"
        )

        st.write(
            f"**Recorrido:** {TRANVIA['recorrido']}"
        )

        st.write(
            f"**Inicio:** {TRANVIA['inicio']}"
        )

    st.subheader("Parámetros operacionales")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Longitud",
        f"{TRANVIA['longitud_km']} km"
    )

    c2.metric(
        "Vehículos",
        TRANVIA["vehiculos"]
    )

    c3.metric(
        "Recorrido",
        f"{TRANVIA['recorrido_min']} min"
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "Velocidad comercial",
        f"{TRANVIA['vel_comercial']} km/h"
    )

    c5.metric(
        "Frecuencia",
        f"{TRANVIA['frecuencia_pico']} min"
    )

    c6.metric(
        "Capacidad",
        f"{formatear_numero(TRANVIA['capacidad_pax_hs'])} pax/h/sentido"
    )

    # --------------------------------------------------------
    # SISTEMAS TRANVÍA
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "Explorar sistemas del Tranvía"
    )

    if "tranvia_sistema" not in st.session_state:
        st.session_state["tranvia_sistema"] = None

    col1, col2, col3 = st.columns(3)

    with col1:

        tarjeta_sistema(
            "🛞",
            "Rodadura",
            "Interacción vehículo–vía y elementos de rodadura."
        )

        if st.button(
            "Explorar Rodadura →",
            key="tranvia_rodadura"
        ):

            st.session_state[
                "tranvia_sistema"
            ] = "Rodadura"

    with col2:

        tarjeta_sistema(
            "🛑",
            "Frenado",
            "Desaceleración y detención controlada del vehículo."
        )

        if st.button(
            "Explorar Frenado →",
            key="tranvia_frenado"
        ):

            st.session_state[
                "tranvia_sistema"
            ] = "Frenado"

    with col3:

        tarjeta_sistema(
            "⚡",
            "Tracción",
            "Generación de la fuerza necesaria para el movimiento."
        )

        if st.button(
            "Explorar Tracción →",
            key="tranvia_traccion"
        ):

            st.session_state[
                "tranvia_sistema"
            ] = "Tracción"

    sistema_tranvia = st.session_state[
        "tranvia_sistema"
    ]

    if sistema_tranvia == "Rodadura":

        st.divider()

        mostrar_rodadura()

    elif sistema_tranvia == "Frenado":

        st.divider()

        st.subheader(
            "🛑 Sistema de frenado"
        )

        st.info(
            "Módulo preparado para desarrollo posterior."
        )

    elif sistema_tranvia == "Tracción":

        st.divider()

        st.subheader(
            "⚡ Sistema de tracción"
        )

        st.info(
            "Módulo preparado para desarrollo posterior."
        )

    # --------------------------------------------------------
    # TABS TRANVÍA
    # --------------------------------------------------------

    st.divider()

    tabs_t = st.tabs(
        [
            "Resumen",
            "Normas y leyes",
            "Período de servicio",
            "Capacitación",
            "Mercado",
            "Régimen de marcha",
            "RCM",
        ]
    )

    with tabs_t[0]:

        datos = [
            ["Código", TRANVIA["codigo"]],
            ["Nombre", TRANVIA["nombre"]],
            ["Modo", TRANVIA["modo"]],
            ["Recorrido", TRANVIA["recorrido"]],
            ["Longitud", f"{TRANVIA['longitud_km']} km"],
            ["Vehículos", TRANVIA["vehiculos"]],
            ["Estaciones", TRANVIA["estaciones"]],
            ["Paradas", TRANVIA["paradas"]],
            [
                "Capacidad por vehículo",
                f"{TRANVIA['capacidad_vehiculo']} usuarios"
            ],
            [
                "Tiempo de recorrido",
                f"{TRANVIA['recorrido_min']} min/sentido"
            ],
            [
                "Velocidad comercial",
                f"{TRANVIA['vel_comercial']} km/h"
            ],
            [
                "Velocidad máxima",
                f"{TRANVIA['vel_max']} km/h"
            ],
            [
                "Frecuencia mínima",
                f"{TRANVIA['frecuencia_pico']} min"
            ],
            [
                "Capacidad",
                f"{TRANVIA['capacidad_pax_hs']} pax/h/sentido"
            ],
        ]

        st.dataframe(
            pd.DataFrame(
                datos,
                columns=["Característica", "Valor"]
            ),
            width="stretch",
            hide_index=True,
        )

    with tabs_t[1]:

        st.dataframe(
            pd.DataFrame(
                {
                    "Norma": TRANVIA["normas"]
                }
            ),
            width="stretch",
            hide_index=True,
        )

    with tabs_t[2]:

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Inicio",
            TRANVIA["inicio"]
        )

        c2.metric(
            "Edad",
            TRANVIA["edad"]
        )

        c3.metric(
            "Km acumulados",
            f"{TRANVIA['km_acum_m']} M km"
        )

    with tabs_t[3]:

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Formación seguridad",
            "6.018"
        )

        c2.metric(
            "Horas promedio",
            "62,8 h/persona"
        )

        c3.metric(
            "Índice conducción",
            "100 %"
        )

    with tabs_t[4]:

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Viajes 2025",
            f"{TRANVIA['viajes_2025_m']} M"
        )

        c2.metric(
            "Meta",
            f"{TRANVIA['meta_2025_m']} M"
        )

        c3.metric(
            "Cumplimiento",
            f"{TRANVIA['cumplimiento_meta']} %"
        )

    with tabs_t[5]:

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Recorrido",
            f"{TRANVIA['recorrido_min']} min"
        )

        c2.metric(
            "Velocidad comercial",
            f"{TRANVIA['vel_comercial']} km/h"
        )

        c3.metric(
            "Velocidad máxima",
            f"{TRANVIA['vel_max']} km/h"
        )

        for sentido, horarios in TRANVIA["horarios"].items():

            st.markdown(
                f"#### {sentido}"
            )

            st.dataframe(
                pd.DataFrame(
                    [
                        {
                            "Día": dia,
                            "Primera salida": horario[0],
                            "Última salida": horario[1],
                        }
                        for dia, horario in horarios.items()
                    ]
                ),
                width="stretch",
                hide_index=True,
            )

    with tabs_t[6]:

        for sistema_rcm in TRANVIA["sistemas_rcm"]:

            st.markdown(
                f"- {sistema_rcm}"
            )


# ============================================================
# ============================================================
# BUSES
# ============================================================
# ============================================================

elif modo_seleccionado == "🚌 Buses":

    st.title("🚌 SISTEMA DE BUSES")

    st.caption(
        "BRT — Contexto operacional"
    )

    st.write(
        """
        Sistema de buses integrado al sistema de transporte del Metro
        de Medellín.
        """
    )

    flota = BUSES.get("flota", {})

    st.subheader("Flota")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Flota total",
        flota.get("total_buses", "N/D")
    )

    c2.metric(
        "Articulados",
        flota.get("articulados", "N/D")
    )

    c3.metric(
        "Padrones",
        flota.get("padrones", "N/D")
    )

    c4.metric(
        "Pasajeros/día",
        formatear_numero(
            flota.get(
                "pasajeros_dia_aprox",
                "N/D"
            )
        )
    )

    st.metric(
        "IPK",
        flota.get(
            "ipk",
            "N/D"
        )
    )

    st.divider()

    # --------------------------------------------------------
    # LÍNEA DE BUSES
    # --------------------------------------------------------

    lineas_buses = BUSES.get(
        "lineas",
        {}
    )

    if not lineas_buses:

        st.warning(
            "No hay líneas de buses cargadas en la base de datos."
        )

    else:

        st.subheader(
            "Línea seleccionada"
        )

        linea_bus = st.selectbox(
            "Seleccione la línea",
            list(lineas_buses.keys()),
            key="linea_bus_principal"
        )

        linea = lineas_buses[
            linea_bus
        ]

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Longitud",
            f"{linea.get('longitud_km', 'N/D')} km"
        )

        c2.metric(
            "Estaciones",
            linea.get("estaciones", "N/D")
        )

        c3.metric(
            "Tipo de corredor",
            linea.get(
                "tipo_corredor",
                "N/D"
            )
        )

        if linea.get("descripcion"):

            st.info(
                linea["descripcion"]
            )

        if linea_bus == "Línea 1":

            st.subheader(
                "Régimen operacional — Línea 1"
            )

            datos = []

            campos = [
                ("Inicio", "inicio"),
                ("Final", "final"),
                ("Velocidad máxima", "velocidad_maxima_kmh"),
                (
                    "Pendiente máxima estación/paradero",
                    "pendiente_max_estacion_paradero_pct"
                ),
                (
                    "Pendiente máxima trazado",
                    "pendiente_max_trazado_pct"
                ),
                (
                    "Radio horizontal mínimo",
                    "radio_horizontal_min_m"
                ),
                (
                    "Altitud mínima",
                    "altitud_min_msnm"
                ),
                (
                    "Altitud máxima",
                    "altitud_max_msnm"
                ),
                (
                    "Ancho mínimo",
                    "ancho_min_via_m"
                ),
            ]

            for nombre, clave in campos:

                if clave not in linea:
                    continue

                valor = linea[clave]

                if "velocidad" in clave:
                    valor = f"{valor} km/h"

                elif "pendiente" in clave:
                    valor = f"{valor} %"

                elif "radio" in clave:
                    valor = f"{valor} m"

                elif "altitud" in clave:
                    valor = f"{valor} msnm"

                elif "ancho" in clave:
                    valor = f"{valor} m"

                datos.append(
                    [nombre, valor]
                )

            if datos:

                st.dataframe(
                    pd.DataFrame(
                        datos,
                        columns=[
                            "Parámetro",
                            "Valor"
                        ]
                    ),
                    width="stretch",
                    hide_index=True,
                )

        elif linea_bus == "Línea 2":

            st.subheader(
                "Régimen operacional — Línea 2"
            )

            datos = [
                [
                    "Longitud",
                    f"{linea.get('longitud_km', 'N/D')} km"
                ],
                [
                    "Estaciones",
                    linea.get('estaciones', 'N/D')
                ],
                [
                    "Tipo de tráfico",
                    linea.get(
                        'tipo_trafico',
                        'N/D'
                    )
                ]
            ]

            st.dataframe(
                pd.DataFrame(
                    datos,
                    columns=[
                        "Parámetro",
                        "Valor"
                    ]
                ),
                width="stretch",
                hide_index=True,
            )

        elif linea_bus == "Línea O":

            st.info(
                """
                La Línea O está registrada en la arquitectura del
                sistema, pero la documentación específica suministrada
                hasta ahora desarrolla principalmente las Líneas 1 y 2.
                """
            )

    # --------------------------------------------------------
    # VEHÍCULOS
    # --------------------------------------------------------

    tipos = BUSES.get(
        "tipos",
        {}
    )

    if tipos:

        st.divider()

        st.subheader(
            "Tipos de vehículo"
        )

        tipo_bus = st.selectbox(
            "Seleccione el tipo",
            list(tipos.keys()),
            key="tipo_bus_principal"
        )

        bus = tipos[tipo_bus]

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Cantidad",
            bus.get("cantidad", "N/D")
        )

        c2.metric(
            "Motor",
            bus.get(
                "modelo_motor",
                "N/D"
            )
        )

        c3.metric(
            "Potencia",
            f"{bus.get('potencia_hp', 'N/D')} HP"
        )

        c4.metric(
            "Capacidad",
            f"{bus.get('capacidad_pasajeros', 'N/D')} pasajeros"
        )

        especificaciones = []

        campos = [
            ("Marca motor", "marca_motor"),
            ("Modelo motor", "modelo_motor"),
            ("Potencia", "potencia_hp"),
            ("RPM potencia", "rpm_potencia"),
            ("Torque", "torque_nm"),
            ("RPM torque", "rpm_torque"),
            ("RPM máximas", "rpm_max"),
            ("Combustible", "combustible"),
            ("Tanque GNV", "tanque_gnv_l"),
            ("Masa admisible", "masa_admisible_kg"),
            ("Transmisión", "modelo_transmision"),
            ("Convertidor", "modelo_convertidor"),
            ("Relación diferencial", "relacion_diferencial"),
        ]

        for nombre, clave in campos:

            if clave not in bus:
                continue

            valor = bus[clave]

            if clave == "potencia_hp":
                valor = f"{valor} HP"

            elif clave == "torque_nm":
                valor = f"{valor} N·m"

            elif clave == "tanque_gnv_l":
                valor = f"{valor} L"

            elif clave == "masa_admisible_kg":
                valor = f"{formatear_numero(valor)} kg"

            especificaciones.append(
                [nombre, valor]
            )

        st.dataframe(
            pd.DataFrame(
                especificaciones,
                columns=[
                    "Parámetro",
                    "Valor"
                ]
            ),
            width="stretch",
            hide_index=True,
        )

    # --------------------------------------------------------
    # SISTEMAS DE BUSES
    # --------------------------------------------------------

    sistemas_bus = BUSES.get(
        "sistemas",
        []
    )

    if sistemas_bus:

        st.divider()

        st.subheader(
            "Sistemas del vehículo"
        )

        sistema_bus = st.selectbox(
            "Seleccione el sistema",
            sistemas_bus,
            key="sistema_bus_principal"
        )

        st.info(
            f"""
            **Sistema seleccionado:** {sistema_bus}

            La siguiente fase será desarrollar la jerarquía:

            Sistema → Subsistema → Componente → Función →
            Falla funcional → Modo de falla → Efecto →
            Consecuencia → Tarea RCM.
            """
        )

    # --------------------------------------------------------
    # ADMISIÓN Y ESCAPE
    # --------------------------------------------------------

    adm = BUSES.get(
        "admision_escape",
        {}
    )

    if adm:

        st.divider()

        st.subheader(
            "Sistema de admisión y escape"
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Filtración",
            f"{adm.get('filtracion_particulas_pct', 'N/D')} %"
        )

        c2.metric(
            "Presión admisión",
            f"{adm.get('presion_max_admision_kpa', 'N/D')} kPa"
        )

        c3.metric(
            "Presión escape",
            f"{adm.get('presion_max_escape_kpa', 'N/D')} kPa"
        )

        datos_adm = []

        campos_adm = [
            ("Partículas", "tamano_particula_um"),
            ("Flujo máximo", "flujo_max_lb_min"),
            ("Norma de emisiones", "norma_emisiones"),
            ("Restricción filtro", "restriccion_max_filtro_in_h2o"),
            (
                "Diferencia máxima intercooler",
                "diferencia_max_intercooler_c"
            ),
            (
                "Restricción intercooler",
                "restriccion_intercooler_kpa"
            ),
            (
                "Temperatura máxima EGR",
                "temperatura_max_egr_c"
            ),
            (
                "Protección entrada turbina",
                "temperatura_proteccion_entrada_turbina_c"
            ),
            (
                "Derating catalizador",
                "temperatura_derrateo_catalizador_c"
            ),
            (
                "Apagado catalizador",
                "temperatura_apagado_catalizador_c"
            ),
            (
                "Ruido máximo",
                "ruido_max_escape_db"
            ),
        ]

        for nombre, clave in campos_adm:

            if clave in adm:

                datos_adm.append(
                    [nombre, adm[clave]]
                )

        st.dataframe(
            pd.DataFrame(
                datos_adm,
                columns=[
                    "Parámetro",
                    "Valor"
                ]
            ),
            width="stretch",
            hide_index=True,
        )

    # --------------------------------------------------------
    # MANTENIMIENTO MAYOR
    # --------------------------------------------------------

    mantenimiento = BUSES.get(
        "mantenimiento_mayor",
        {}
    )

    if mantenimiento:

        st.divider()

        st.subheader(
            "Mantenimiento mayor"
        )

        st.metric(
            "Kilometraje de referencia",
            f"{formatear_numero(mantenimiento.get('kilometraje_aprox', 'N/D'))} "
            f"{mantenimiento.get('unidad', '')}"
        )

        st.write(
            "Aplicaciones principales:"
        )

        for item in mantenimiento.get(
            "aplicaciones",
            []
        ):

            st.markdown(
                f"- {item}"
            )

    # --------------------------------------------------------
    # RCM BUSES
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "Estructura para análisis RCM"
    )

    st.code(
        """
SISTEMA BUSES
      ↓
LÍNEA
      ↓
TIPO DE VEHÍCULO
      ↓
SISTEMA
      ↓
SUBSISTEMA
      ↓
COMPONENTE
      ↓
FUNCIÓN
      ↓
FALLA FUNCIONAL
      ↓
MODO DE FALLA
      ↓
EFECTO
      ↓
CONSECUENCIA
      ↓
TAREA RCM
        """,
        language="text",
    )


# ============================================================
# METROCABLES Y LÍNEAS TODAVÍA PENDIENTES
# ============================================================

# ============================================================
# LÍNEA B — METRO
# ============================================================

else:

    codigo = None

    mapa_codigos = {
        "Línea B": "B",
        "Línea H": "H",
        "Línea J": "J",
        "Línea K": "K",
        "Línea L": "L",
        "Línea M": "M",
        "Línea P": "P",
    }

    codigo = mapa_codigos.get(
        linea_seleccionada
    )


    # ========================================================
    # LÍNEA B
    # ========================================================

    if linea_seleccionada == "Línea B":

        B = LINEAS["B"]

        st.title(
            "🚇 LÍNEA B — METRO DE MEDELLÍN"
        )

        st.caption(
            "San Antonio ↔ San Javier"
        )


        # ----------------------------------------------------
        # CABECERA VISUAL
        # ----------------------------------------------------

        st.subheader(
            "Información operacional"
        )

        col_info, col_imagen = st.columns(
            [1.8, 1],
            gap="large"
        )

        with col_info:

            st.markdown(
                """
                ### 🚇 Línea B

                **Metro de Medellín**

                Recorrido:

                **San Antonio ↔ San Javier**

                Línea ferroviaria que conecta el centro
                de Medellín con el sector occidental de la ciudad.
                """
            )

            st.markdown(
                f"""
                **Longitud:** {B['longitud_km']} km

                **Estaciones en el inventario publicado:** {len(B['estaciones'])}

                **Inicio de operación:** {B['inicio_operacion']}
                """
            )

        with col_imagen:

            if IMAGEN_LINEA_B is not None:

                st.image(
                    str(IMAGEN_LINEA_B),
                    width=360,
                    caption="Línea B — Metro de Medellín"
                )

            else:

                st.info(
                    "Imagen de Línea B no disponible."
                )


        # ----------------------------------------------------
        # PARÁMETROS OPERACIONALES
        # ----------------------------------------------------

        st.subheader(
            "Parámetros operacionales"
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Longitud",
            f"{B['longitud_km']} km"
        )

        c2.metric(
            "Estaciones publicadas",
            len(B["estaciones"])
        )

        c3.metric(
            "Tiempo de recorrido",
            f"{B['tiempo_recorrido_min']} min"
        )


        c4, c5, c6 = st.columns(3)

        c4.metric(
            "Velocidad comercial",
            f"{B['velocidad_comercial_kmh']} km/h"
        )

        c5.metric(
            "Velocidad máxima",
            f"{B['velocidad_maxima_kmh']} km/h"
        )

        c6.metric(
            "Frecuencia mínima",
            B["frecuencia_minima_texto"]
        )


        c7, c8, c9 = st.columns(3)

        c7.metric(
            "Capacidad",
            f"{formatear_numero(B['capacidad_pax_hora_sentido'])} "
            "pax/h/sentido"
        )

        c8.metric(
            "Estaciones elevadas",
            B["estaciones_elevadas"]
        )

        c9.metric(
            "Inicio operación",
            B["inicio_operacion"]
        )


        # ----------------------------------------------------
        # TABS
        # ----------------------------------------------------

        st.divider()

        tabs_b = st.tabs(
            [
                "Resumen",
                "Estaciones",
                "Transferencias",
                "Régimen de marcha",
                "Servicios",
                "Contexto RCM",
                "Fuentes",
            ]
        )


        # ====================================================
        # RESUMEN
        # ====================================================

        with tabs_b[0]:

            resumen_b = [

                ["Modo", B["modo"]],

                ["Recorrido", B["recorrido"]],

                [
                    "Longitud",
                    f"{B['longitud_km']} km"
                ],

                [
                    "Estaciones en inventario publicado",
                    len(B["estaciones"])
                ],

                [
                    "Estaciones según ficha técnica",
                    f"{B['numero_estaciones_ficha']} "
                    f"({B['estaciones_elevadas']} elevadas)"
                ],

                [
                    "Capacidad por coche",
                    f"{B['capacidad_coche']} usuarios"
                ],

                [
                    "Configuración",
                    B["configuracion_tren"]
                ],

                [
                    "Trenes conjunto A+B",
                    B["trenes_ab"]
                ],

                [
                    "Vagones conjunto A+B",
                    B["vagones_ab"]
                ],

                [
                    "Tiempo de recorrido",
                    f"{B['tiempo_recorrido_min']} min/sentido"
                ],

                [
                    "Velocidad comercial",
                    f"{B['velocidad_comercial_kmh']} km/h"
                ],

                [
                    "Velocidad máxima",
                    f"{B['velocidad_maxima_kmh']} km/h"
                ],

                [
                    "Frecuencia mínima",
                    B["frecuencia_minima_texto"]
                ],

                [
                    "Capacidad",
                    f"{formatear_numero(B['capacidad_pax_hora_sentido'])} "
                    "pax/h/sentido"
                ],

                [
                    "Inicio de operación",
                    B["inicio_operacion"]
                ],
            ]

            st.dataframe(
                pd.DataFrame(
                    resumen_b,
                    columns=[
                        "Característica",
                        "Valor"
                    ]
                ),
                width="stretch",
                hide_index=True,
            )

            st.warning(
                """
                Existe una discrepancia en la fuente oficial:
                el inventario de estaciones publicado contiene 7
                estaciones, mientras que la ficha técnica indica
                6 estaciones (5 elevadas). Se conserva la diferencia
                explícitamente para mantener la trazabilidad.
                """
            )


        # ====================================================
        # ESTACIONES
        # ====================================================

        with tabs_b[1]:

            st.subheader(
                f"Estaciones Línea B "
                f"({len(B['estaciones'])})"
            )

            estacion_b = st.selectbox(
                "Seleccione una estación",
                B["estaciones"],
                key="estacion_linea_b"
            )

            numero_b = (
                B["estaciones"].index(estacion_b)
                + 1
            )

            st.metric(
                "Posición en el recorrido",
                f"{numero_b} / {len(B['estaciones'])}"
            )

            st.write(
                f"**Estación seleccionada:** {estacion_b}"
            )

            st.markdown(
                "### Secuencia de estaciones"
            )

            for indice, nombre in enumerate(
                B["estaciones"],
                start=1
            ):

                marcador = "🔹"

                if nombre == estacion_b:

                    marcador = "🔴"

                st.markdown(
                    f"{marcador} **{indice}. {nombre}**"
                )


        # ====================================================
        # TRANSFERENCIAS
        # ====================================================

        with tabs_b[2]:

            st.subheader(
                "Estaciones de transferencia"
            )

            for transferencia in B[
                "estaciones_transferencia"
            ]:

                st.markdown(
                    f"""
                    <div class="system-card">

                        <div class="system-card-title">
                            🔄 {transferencia}
                        </div>

                        <div class="system-card-text">
                            Estación identificada como punto
                            de transferencia de la Línea B.
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.write("")


        # ====================================================
        # RÉGIMEN DE MARCHA
        # ====================================================

        with tabs_b[3]:

            st.subheader(
                "Régimen de marcha"
            )

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "Recorrido",
                f"{B['tiempo_recorrido_min']} min"
            )

            c2.metric(
                "Velocidad comercial",
                f"{B['velocidad_comercial_kmh']} km/h"
            )

            c3.metric(
                "Velocidad máxima",
                f"{B['velocidad_maxima_kmh']} km/h"
            )

            c4.metric(
                "Frecuencia mínima",
                B["frecuencia_minima_texto"]
            )

            st.metric(
                "Capacidad",
                f"{formatear_numero(B['capacidad_pax_hora_sentido'])} "
                "pax/h/sentido"
            )

            st.write(
                """
                El régimen de marcha deberá complementarse
                posteriormente con horarios detallados por estación,
                intervalo operativo, demanda por franja horaria
                y comportamiento histórico del servicio.
                """
            )


        # ====================================================
        # SERVICIOS
        # ====================================================

        with tabs_b[4]:

            st.subheader(
                "Servicios y características de estaciones"
            )

            st.info(
                """
                La fuente oficial contiene información específica
                de servicios, accesibilidad, horarios, rutas
                integradas y sitios de interés por estación.

                Esta información se incorporará progresivamente
                a la ficha individual de cada estación.
                """
            )

            st.write(
                "Ejemplo de información disponible:"
            )

            st.markdown(
                """
                - Servicios de atención al usuario.
                - Máquinas de recarga Cívica.
                - Elementos de accesibilidad.
                - Cajeros electrónicos.
                - Parqueaderos de bicicletas.
                - Baños públicos en algunas estaciones.
                - Rutas integradas.
                - Sitios de interés.
                """
            )


        # ====================================================
        # RCM
        # ====================================================

        with tabs_b[5]:

            st.subheader(
                "Contexto operacional para RCM"
            )

            st.info(
                """
                Línea B será desarrollada posteriormente a nivel
                de sistemas, subsistemas, equipos y componentes.
                """
            )

            st.code(
                """
LÍNEA B
   ↓
Sistemas
   ↓
Subsistemas
   ↓
Activos
   ↓
Funciones
   ↓
Fallas funcionales
   ↓
Modos de falla
   ↓
Efectos
   ↓
Consecuencias
   ↓
Tareas RCM
                """,
                language="text"
            )


        # ====================================================
        # FUENTES
        # ====================================================

        with tabs_b[6]:

            st.subheader(
                "Fuente principal"
            )

            st.markdown(
                """
                **Metro de Medellín — Línea B**

                Información oficial del sistema integrado,
                complementada posteriormente con documentación
                técnica y operacional del proyecto RCM.
                """
            )

            st.code(
                "https://www.metrodemedellin.gov.co/usuarios/sistema-integrado/linea-b",
                language="text"
            )

    # ========================================================
    # OTRAS LÍNEAS PENDIENTES
    # ========================================================

    else:

        if codigo and codigo in LINEAS:

            datos_linea = LINEAS[codigo]

            st.title(
                f"{modo_limpio if 'modo_limpio' in locals() else modo_seleccionado} "
                f"— {linea_seleccionada}"
            )

            st.subheader(
                "Información actualmente registrada"
            )

            st.write(
                f"**Modo:** {datos_linea.get('modo', modo_seleccionado)}"
            )

            st.write(
                f"**Recorrido:** "
                f"{datos_linea.get('recorrido', 'Pendiente')}"
            )

        st.divider()

        st.markdown(
            """
            <div class="pending-box">

            <strong>Estado del módulo</strong>

            <br><br>

            Esta línea ya forma parte de la arquitectura general
            del aplicativo, pero su contexto operacional específico
            todavía debe consolidarse con documentación técnica
            y operacional.

            </div>
            """,
            unsafe_allow_html=True,
        )

    codigo = mapa_codigos.get(
        linea_seleccionada
    )

    modo_limpio = (
        modo_seleccionado
        .replace("🚇 ", "")
        .replace("🚋 ", "")
        .replace("🚌 ", "")
        .replace("🚡 ", "")
    )

    st.title(
        f"{modo_limpio} — {linea_seleccionada}"
    )

    if codigo and codigo in LINEAS:

        datos_linea = LINEAS[codigo]

        st.subheader(
            "Información actualmente registrada"
        )

        c1, c2 = st.columns(2)

        with c1:

            st.write(
                f"**Modo:** {datos_linea.get('modo', modo_limpio)}"
            )

        with c2:

            st.write(
                f"**Recorrido:** {datos_linea.get('recorrido', 'Pendiente')}"
            )

    st.divider()

    st.markdown(
        """
        <div class="pending-box">

        <strong>Estado del módulo</strong>

        <br><br>

        Esta línea ya forma parte de la arquitectura general del
        aplicativo, pero su contexto operacional específico todavía
        debe consolidarse con documentación técnica y operacional.

        <br><br>

        No se presentan aquí parámetros que no hayan sido
        documentados y verificados para la línea correspondiente.

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader(
        "Información requerida para desarrollar el módulo"
    )

    pendientes = pd.DataFrame(
        [
            [
                "Contexto operacional",
                "Pendiente"
            ],
            [
                "Régimen de marcha",
                "Pendiente"
            ],
            [
                "Inventario de activos",
                "Pendiente"
            ],
            [
                "Sistemas y subsistemas",
                "Pendiente"
            ],
            [
                "Histórico de fallas",
                "Pendiente"
            ],
            [
                "MTBF / MTTR",
                "Pendiente"
            ],
            [
                "Plan de mantenimiento",
                "Pendiente"
            ],
            [
                "Criticidad",
                "Pendiente"
            ],
        ],
        columns=[
            "Información",
            "Estado"
        ],
    )

    st.dataframe(
        pendientes,
        width="stretch",
        hide_index=True,
    )


# ============================================================
# PIE DE PÁGINA
# ============================================================

st.divider()

st.caption(
    "Metro de Medellín — Proyecto académico de Gestión de Activos y RCM"
)