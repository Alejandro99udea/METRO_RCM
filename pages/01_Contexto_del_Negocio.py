# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd

from data.metro_data import METRO


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Contexto del Negocio | Metro de Medellín",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def numero(valor):
    """
    Formatea números enteros con separador de miles.
    """
    try:
        return f"{int(valor):,}".replace(",", ".")
    except (ValueError, TypeError):
        return str(valor)


def millones(valor):
    """
    Presentación de valores monetarios expresados en millones de COP.
    """
    try:
        return f"${int(valor):,}".replace(",", ".") + " M"
    except (ValueError, TypeError):
        return str(valor)


# ============================================================
# CÁLCULOS FINANCIEROS
# ============================================================

ingresos = METRO.get("ingresos_2025_m", 0)
ingresos_transporte = METRO.get("ingresos_transporte_2025_m", 0)
negocios_asociados = METRO.get("negocios_asociados_2025_m", 0)

ebitda = METRO.get("ebitda_2025_m", 0)
utilidad_neta = METRO.get("utilidad_neta_2025_m", 0)

activos = METRO.get("activos_2025_m", 0)
ppe_neta = METRO.get("ppe_neta_2025_m", 0)

pasivos = METRO.get("pasivos_2025_m", 0)
patrimonio = METRO.get("patrimonio_2025_m", 0)

capex = METRO.get("ppye_adquisiciones_2025_m", 0)


margen_ebitda = (
    ebitda / ingresos * 100
    if ingresos
    else 0
)

roa = (
    utilidad_neta / activos * 100
    if activos
    else 0
)

ppe_activos = (
    ppe_neta / activos * 100
    if activos
    else 0
)

capex_ingresos = (
    capex / ingresos * 100
    if ingresos
    else 0
)

participacion_transporte = (
    ingresos_transporte / ingresos * 100
    if ingresos
    else 0
)

participacion_negocios = (
    negocios_asociados / ingresos * 100
    if ingresos
    else 0
)

pasivos_activos = (
    pasivos / activos * 100
    if activos
    else 0
)


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
        border-radius: 20px;

        padding: 30px 34px;

        margin-bottom: 24px;

        box-shadow: 0 5px 18px rgba(0,0,0,0.05);
    }

    .hero-title {
        font-size: 2.35rem;
        font-weight: 800;
        color: #111827;
        line-height: 1.1;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #6b7280;
        margin-top: 8px;
        line-height: 1.5;
    }

    .section-card {
        background: #ffffff;
        border: 1px solid #e1e5ea;
        border-radius: 16px;

        padding: 20px;

        margin-bottom: 16px;

        box-shadow: 0 3px 12px rgba(0,0,0,0.035);
    }

    .card-title {
        font-size: 1.1rem;
        font-weight: 750;
        color: #111827;
        margin-bottom: 8px;
    }

    .card-text {
        color: #6b7280;
        font-size: 0.92rem;
        line-height: 1.55;
    }

    .value-box {
        background: #f8fafc;

        border: 1px solid #e5e7eb;

        border-radius: 14px;

        padding: 18px;

        min-height: 130px;
    }

    .value-title {
        font-size: 1.1rem;
        font-weight: 750;
        color: #111827;
    }

    .value-text {
        font-size: 0.9rem;
        color: #6b7280;
        margin-top: 8px;
        line-height: 1.45;
    }

    .flow-box {
        background: #ffffff;
        border: 1px solid #dfe3e8;
        border-radius: 14px;

        padding: 18px;

        text-align: center;

        min-height: 115px;
    }

    .flow-title {
        font-size: 1rem;
        font-weight: 750;
        color: #111827;
    }

    .flow-text {
        color: #6b7280;
        font-size: 0.85rem;
        margin-top: 7px;
    }

    .pending {
        background: #fff8e6;
        border: 1px solid #efd28a;

        border-radius: 14px;

        padding: 18px;

        color: #765500;
    }

    </style>
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
            🏢 CONTEXTO DEL NEGOCIO
        </div>

        <div class="hero-subtitle">
            Metro de Medellín · Contexto corporativo, financiero,
            estratégico y de gestión de activos para el análisis RCM
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# IDENTIFICACIÓN CORPORATIVA
# ============================================================

st.subheader(
    "Metro de Medellín"
)

st.caption(
    METRO.get(
        "empresa",
        "Empresa de Transporte Masivo del Valle de Aburrá Ltda."
    )
)


# ============================================================
# KPI PRINCIPALES
# ============================================================

st.subheader(
    "Magnitud del negocio"
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Empleados 2025",
    numero(
        METRO.get(
            "empleados_2025",
            0
        )
    )
)

c2.metric(
    "Red integrada",
    f"{METRO.get('red_integrada_km', 0)} km"
)

c3.metric(
    "Ingresos 2025",
    millones(ingresos)
)

c4.metric(
    "EBITDA 2025",
    millones(ebitda)
)


c5, c6, c7, c8 = st.columns(4)

c5.metric(
    "Viajes corporativos 2025",
    f"{METRO.get('viajes_corporativos_2025_m', 0)} M"
)

c6.metric(
    "Margen EBITDA",
    f"{margen_ebitda:.2f} %"
)

c7.metric(
    "Madurez de activos",
    METRO.get(
        "madurez_activos",
        {}
    ).get(
        2025,
        "N/D"
    )
)

c8.metric(
    "Satisfacción",
    METRO.get(
        "satisfaccion",
        "N/D"
    )
)


# ============================================================
# NAVEGACIÓN INTERNA
# ============================================================

st.divider()

tabs = st.tabs(
    [
        "🏢 Perfil",
        "💰 Finanzas",
        "🧩 Modelo de negocio",
        "🎯 Estrategia",
        "👥 Organización",
        "🌎 Entorno",
        "💎 Creación de valor",
        "⚙️ Gestión de activos",
        "🗂️ Información",
    ]
)


# ============================================================
# TAB 1 — PERFIL
# ============================================================

with tabs[0]:

    st.subheader(
        "Perfil empresarial"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="section-card">

                <div class="card-title">
                    Identificación
                </div>

                <div class="card-text">

                    <strong>Razón social</strong><br>
                    Empresa de Transporte Masivo del Valle de
                    Aburrá Ltda.

                    <br><br>

                    <strong>Naturaleza</strong><br>
                    Empresa de transporte masivo de carácter público.

                    <br><br>

                    <strong>Actividad principal</strong><br>
                    Prestación del servicio integrado de transporte
                    masivo de pasajeros.

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            """
            <div class="section-card">

                <div class="card-title">
                    Estructura de propiedad
                </div>

                <div class="card-text">

                    La participación institucional está distribuida
                    en partes iguales entre el Distrito de Medellín
                    y el Departamento de Antioquia.

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        socios = pd.DataFrame(
            [
                [
                    "Distrito de Medellín",
                    METRO["socios"].get(
                        "Distrito de Medellín",
                        "N/D"
                    ),
                ],
                [
                    "Departamento de Antioquia",
                    METRO["socios"].get(
                        "Departamento de Antioquia",
                        "N/D"
                    ),
                ],
            ],
            columns=[
                "Socio institucional",
                "Participación (%)",
            ],
        )

        st.dataframe(
            socios,
            width="stretch",
            hide_index=True,
        )


    st.subheader(
        "Modos de transporte"
    )

    modos = [
        ("🚇", "Metro", "Red ferroviaria principal"),
        ("🚋", "Tranvía", "Transporte ferroviario urbano"),
        ("🚡", "Metrocables", "Movilidad por cable"),
        ("🚌", "Buses", "Sistema BRT / alimentación"),
    ]

    columnas = st.columns(4)

    for i, (icono, nombre, descripcion) in enumerate(modos):

        with columnas[i]:

            st.markdown(
                f"""
                <div class="value-box">

                    <div class="value-title">
                        {icono} {nombre}
                    </div>

                    <div class="value-text">
                        {descripcion}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# TAB 2 — FINANZAS
# ============================================================

with tabs[1]:

    st.subheader(
        "Estructura financiera 2025"
    )

    # --------------------------------------------------------
    # KPIs
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Ingresos",
        millones(ingresos)
    )

    c2.metric(
        "EBITDA",
        millones(ebitda)
    )

    c3.metric(
        "Utilidad neta",
        millones(utilidad_neta)
    )

    c4.metric(
        "Activos",
        millones(activos)
    )


    c5, c6, c7, c8 = st.columns(4)

    c5.metric(
        "PP&E neta",
        millones(ppe_neta)
    )

    c6.metric(
        "Pasivos",
        millones(pasivos)
    )

    c7.metric(
        "Patrimonio",
        millones(patrimonio)
    )

    c8.metric(
        "CAPEX / PP&E",
        millones(capex)
    )


    # --------------------------------------------------------
    # INDICADORES FINANCIEROS
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "Indicadores derivados"
    )

    indicadores = pd.DataFrame(
        [
            [
                "Margen EBITDA",
                f"{margen_ebitda:.2f} %",
                "EBITDA / ingresos",
            ],
            [
                "ROA aproximado",
                f"{roa:.2f} %",
                "Utilidad neta / activos",
            ],
            [
                "PP&E / activos",
                f"{ppe_activos:.2f} %",
                "Intensidad física del activo",
            ],
            [
                "CAPEX / ingresos",
                f"{capex_ingresos:.2f} %",
                "Adquisiciones PP&E / ingresos",
            ],
            [
                "Pasivos / activos",
                f"{pasivos_activos:.2f} %",
                "Estructura contable",
            ],
            [
                "Transporte / ingresos",
                f"{participacion_transporte:.2f} %",
                "Participación de transporte",
            ],
            [
                "Negocios asociados / ingresos",
                f"{participacion_negocios:.2f} %",
                "Diversificación de ingresos",
            ],
        ],
        columns=[
            "Indicador",
            "Resultado",
            "Interpretación",
        ],
    )

    st.dataframe(
        indicadores,
        width="stretch",
        hide_index=True,
    )


    st.subheader(
        "Composición de ingresos"
    )

    ingresos_chart = pd.DataFrame(
        {
            "Ingresos 2025 (millones COP)": [
                ingresos_transporte,
                negocios_asociados,
            ]
        },
        index=[
            "Transporte",
            "Negocios asociados",
        ],
    )

    st.bar_chart(
        ingresos_chart,
        width="stretch",
        horizontal=True,
    )


    st.info(
        """
        El transporte representa aproximadamente el 91,46 % de los
        ingresos ordinarios reportados para 2025, mientras que los
        negocios asociados representan aproximadamente el 8,54 %.
        """
    )


    # --------------------------------------------------------
    # INTENSIDAD DE CAPITAL
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "Intensidad de capital"
    )

    intensidad = pd.DataFrame(
        {
            "Participación (%)": [
                ppe_activos,
                capex_ingresos,
            ]
        },
        index=[
            "PP&E / activos",
            "CAPEX / ingresos",
        ],
    )

    st.bar_chart(
        intensidad,
        width="stretch",
    )

    st.warning(
        """
        El patrimonio 2025 registrado en la base de datos es negativo.
        Por ello no se utilizará un ROE convencional como indicador
        central del análisis. El ROA presentado es un indicador
        derivado y debe interpretarse dentro de esta estructura contable.
        """
    )


# ============================================================
# TAB 3 — MODELO DE NEGOCIO
# ============================================================

with tabs[2]:

    st.subheader(
        "Modelo de negocio"
    )

    elemento = st.selectbox(
        "Seleccione un elemento del modelo de negocio",
        [
            "Propuesta de valor",
            "Segmentos de clientes",
            "Actividades clave",
            "Recursos clave",
            "Socios clave",
            "Relaciones con clientes",
            "Canales",
            "Fuentes de ingresos",
            "Estructura de costos",
        ],
    )


    modelo = {

        "Propuesta de valor": (
            "Movilidad pública integrada, segura, eficiente "
            "y sostenible."
        ),

        "Segmentos de clientes": (
            "Usuarios del transporte público y grupos de interés."
        ),

        "Actividades clave": (
            "Planeación, operación, mantenimiento, gestión de "
            "infraestructura, gestión de activos y atención al usuario."
        ),

        "Recursos clave": (
            "Infraestructura, material rodante, energía, tecnología, "
            "información, talento humano y conocimiento."
        ),

        "Socios clave": (
            "Entidades territoriales, Nación, proveedores, contratistas, "
            "aliados y entidades del sistema de transporte."
        ),

        "Relaciones con clientes": (
            "Atención al usuario, prestación continua del servicio, "
            "información y mecanismos de interacción."
        ),

        "Canales": (
            "Sistema integrado de transporte, estaciones, vehículos, "
            "canales de atención e infraestructura de movilidad."
        ),

        "Fuentes de ingresos": (
            "Servicios de transporte y actividades complementarias "
            "como negocios asociados, consultorías, aprovechamiento "
            "de infraestructura y servicios de ciudad."
        ),

        "Estructura de costos": (
            "Personal, mantenimiento, energía, servicios, seguridad, "
            "depreciación, financiación e inversiones."
        ),
    }


    st.markdown(
        f"""
        <div class="section-card">

            <div class="card-title">
                {elemento}
            </div>

            <div class="card-text">
                {modelo[elemento]}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.divider()

    st.subheader(
        "Cadena de generación de valor"
    )

    pasos = [
        ("Planear", "Definir estrategia y capacidad"),
        ("Construir", "Desarrollar infraestructura"),
        ("Operar", "Prestar el servicio"),
        ("Mantener", "Preservar funciones"),
        ("Gestionar activos", "Optimizar costo, riesgo y desempeño"),
        ("Generar movilidad", "Crear servicio de transporte"),
        ("Crear valor", "Resultado financiero, social y ambiental"),
    ]

    for i in range(0, len(pasos), 3):

        columnas = st.columns(3)

        grupo = pasos[i:i + 3]

        for j, (titulo, descripcion) in enumerate(grupo):

            with columnas[j]:

                st.markdown(
                    f"""
                    <div class="flow-box">

                        <div class="flow-title">
                            {titulo}
                        </div>

                        <div class="flow-text">
                            {descripcion}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.write("")


# ============================================================
# TAB 4 — ESTRATEGIA
# ============================================================

with tabs[3]:

    st.subheader(
        "Estrategia corporativa 2026–2035"
    )

    objetivos = METRO.get(
        "estrategia_2026_2035",
        []
    )

    if objetivos:

        for i, objetivo in enumerate(
            objetivos,
            start=1
        ):

            st.markdown(
                f"""
                <div class="section-card">

                    <div class="card-title">
                        OE{i}
                    </div>

                    <div class="card-text">
                        {objetivo}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


    objetivo_seleccionado = st.selectbox(
        "Seleccione un objetivo para analizar su relación con RCM",
        [
            "OE1",
            "OE2",
            "OE3",
            "OE4",
        ],
    )


    implicaciones = {

        "OE1": (
            "La gestión de activos debe contribuir a la continuidad "
            "y calidad del servicio que impacta personas y territorios."
        ),

        "OE2": (
            "El mantenimiento optimizado debe contribuir a menor costo "
            "de ciclo de vida, menor riesgo y mayor disponibilidad."
        ),

        "OE3": (
            "La disponibilidad y confiabilidad de los activos permiten "
            "sostener capacidad, nuevos negocios y expansión."
        ),

        "OE4": (
            "Los activos deben gestionarse considerando resiliencia "
            "climática, exposición a eventos extremos y continuidad."
        ),
    }


    st.info(
        implicaciones[objetivo_seleccionado]
    )


    st.subheader(
        "Relación estrategia → activos"
    )

    st.code(
        """
ESTRATEGIA
    ↓
OBJETIVOS ESTRATÉGICOS
    ↓
CAPACIDADES DEL NEGOCIO
    ↓
REQUERIMIENTOS DE LOS ACTIVOS
    ↓
DESEMPEÑO
    ↓
MANTENIMIENTO
    ↓
RCM
        """,
        language="text",
    )


# ============================================================
# TAB 5 — ORGANIZACIÓN
# ============================================================

with tabs[4]:

    st.subheader(
        "Organización y talento humano"
    )

    empleados_2025 = METRO.get(
        "empleados_2025",
        0
    )

    empleados_documento = METRO.get(
        "empleados_pdf",
        0
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Empleados 2025",
        numero(empleados_2025)
    )

    c2.metric(
        "Empleados reportados en documento",
        numero(empleados_documento)
    )

    c3.metric(
        "Mantenimiento estimado de planta",
        f"{METRO.get('mantenimiento_pct_planta', 0)} %"
    )


    st.subheader(
        "Talento asociado a mantenimiento"
    )

    st.info(
        f"""
        La base consolidada registra una estimación de aproximadamente
        {METRO.get('mantenimiento_personas_aprox_pdf', 'N/D')} personas
        asociadas a mantenimiento.

        Esta cifra debe tratarse como aproximación documental y no como
        distribución oficial definitiva por línea o sistema.
        """
    )


    st.subheader(
        "Gobierno corporativo"
    )

    st.markdown(
        """
        <div class="section-card">

            <div class="card-title">
                Estructura de gobierno
            </div>

            <div class="card-text">

                Junta de Socios → Junta Directiva → Gerencia General

                <br><br>

                Con mecanismos de apoyo para auditoría, riesgos,
                gobierno corporativo, asuntos financieros, estrategia
                y proyectos.

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# TAB 6 — ENTORNO
# ============================================================

with tabs[5]:

    st.subheader(
        "Entorno empresarial — PESTEL"
    )

    pestel = {

        "Político": (
            "Propiedad pública, coordinación con entidades territoriales "
            "y decisiones de política de movilidad."
        ),

        "Económico": (
            "Presión sobre costos, inversión, sostenibilidad financiera, "
            "demanda de transporte y diversificación de ingresos."
        ),

        "Social": (
            "Movilidad masiva, acceso territorial, seguridad, satisfacción "
            "y calidad de experiencia del usuario."
        ),

        "Tecnológico": (
            "Automatización, diagnóstico, analítica, sistemas eléctricos, "
            "señalización, comunicaciones y transformación digital."
        ),

        "Ambiental": (
            "Reducción de emisiones, eficiencia energética y exposición "
            "de activos a eventos climáticos."
        ),

        "Legal": (
            "Cumplimiento del marco regulatorio del transporte masivo, "
            "seguridad, contratación, ambiente y gestión empresarial."
        ),
    }


    factor = st.radio(
        "Seleccione una dimensión",
        list(pestel.keys()),
        horizontal=True,
    )


    st.markdown(
        f"""
        <div class="section-card">

            <div class="card-title">
                {factor}
            </div>

            <div class="card-text">
                {pestel[factor]}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.subheader(
        "Riesgos climáticos relevantes"
    )

    riesgos_climaticos = [
        "Lluvias intensas",
        "Inundaciones",
        "Deslizamientos",
        "Tormentas",
        "Olas de calor",
        "Descargas eléctricas",
    ]

    columnas = st.columns(3)

    for i, riesgo in enumerate(
        riesgos_climaticos
    ):

        with columnas[i % 3]:

            st.warning(
                riesgo
            )


    st.info(
        """
        Los riesgos climáticos identificados tienen implicaciones
        potenciales sobre drenajes, estaciones, accesos, infraestructura
        de ladera, sistemas eléctricos y Metrocables.
        """
    )


# ============================================================
# TAB 7 — CREACIÓN DE VALOR
# ============================================================

with tabs[6]:

    st.subheader(
        "Creación de valor"
    )

    st.write(
        """
        El valor generado por el Metro debe analizarse en cuatro
        dimensiones: financiera, operacional, social y ambiental.
        """
    )


    valor = METRO.get(
        "valor",
        {}
    )


    dimensiones = [

        (
            "💰",
            "Financiera",
            [
                f"Ingresos: {millones(ingresos)}",
                f"EBITDA: {millones(ebitda)}",
                f"Margen EBITDA: {margen_ebitda:.2f} %",
                f"Negocios asociados: {millones(negocios_asociados)}",
            ],
        ),

        (
            "⚙️",
            "Operacional",
            [
                f"Red integrada: {METRO.get('red_integrada_km', 0)} km",
                "Líneas: 12",
                "Modos: 4",
                f"Viajes corporativos: {METRO.get('viajes_corporativos_2025_m', 0)} M",
            ],
        ),

        (
            "👥",
            "Social",
            [
                f"Horas ahorradas: {numero(valor.get('horas_ahorradas', 0))} h/año",
                f"Ahorro usuarios: {millones(valor.get('ahorro_usuarios_m', 0))}/año",
                f"Muertes evitadas: {valor.get('muertes_evitadas', 'N/D')}/año",
                f"Accidentes evitados: {numero(valor.get('accidentes_evitados', 0))}/año",
            ],
        ),

        (
            "🌱",
            "Ambiental",
            [
                f"CO₂ evitado: {numero(valor.get('co2_ev_t', 0))} t/año",
                f"Contaminantes evitados: {numero(valor.get('contaminantes_ev_t', 0))} t/año",
                f"Combustible evitado: {numero(valor.get('combustible_ev_gal', 0))} gal/año",
                f"Energía: {valor.get('energia_tj', 'N/D')} TJ",
            ],
        ),
    ]


    columnas = st.columns(4)

    for i, (icono, titulo, indicadores_valor) in enumerate(
        dimensiones
    ):

        with columnas[i]:

            st.markdown(
                f"""
                <div class="value-box">

                    <div class="value-title">
                        {icono} {titulo}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

            for indicador in indicadores_valor:

                st.write(
                    indicador
                )


    st.divider()

    st.metric(
        "Externalidades positivas valoradas",
        f"${valor.get('externalidades_billones', 'N/D')} billones"
    )


# ============================================================
# TAB 8 — GESTIÓN DE ACTIVOS
# ============================================================

with tabs[7]:

    st.subheader(
        "Gestión de activos"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Red integrada",
        f"{METRO.get('red_integrada_km', 0)} km"
    )

    c2.metric(
        "Red férrea",
        f"{METRO.get('red_ferrea_km', 0)} km"
    )

    c3.metric(
        "Trenes",
        METRO.get('trenes', "N/D")
    )

    c4.metric(
        "Coches",
        METRO.get('coches_tren', "N/D")
    )


    c5, c6, c7, c8 = st.columns(4)

    c5.metric(
        "Metrocables",
        METRO.get('metrocables', "N/D")
    )

    c6.metric(
        "Tranvías",
        METRO.get('tranvia', "N/D")
    )

    c7.metric(
        "BRT",
        METRO.get('brt', "N/D")
    )

    c8.metric(
        "PP&E / activos",
        f"{ppe_activos:.2f} %"
    )


    st.divider()

    st.subheader(
        "Madurez de gestión de activos"
    )

    madurez = METRO.get(
        "madurez_activos",
        {}
    )

    if madurez:

        datos_madurez = pd.DataFrame(
            {
                "Madurez": list(
                    madurez.values()
                )
            },
            index=[
                str(año)
                for año in madurez.keys()
            ],
        )

        st.line_chart(
            datos_madurez,
            width="stretch",
        )


    st.info(
        """
        La madurez reportada aumenta progresivamente entre 2021 y 2025.
        El documento vincula la gestión de activos con criterios de costo,
        riesgo y desempeño.
        """
    )


    st.subheader(
        "Inversión y mantenimiento"
    )

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Adquisiciones de PP&E 2025",
            millones(capex)
        )

    with c2:

        st.metric(
            "Plan de mantenimiento 2025",
            millones(
                METRO.get(
                    "mantenimiento_plan_2025_m_mas",
                    0
                )
            )
        )


    st.code(
        """
COSTO
  +
RIESGO
  +
DESEMPEÑO
       ↓
GESTIÓN DE ACTIVOS
       ↓
DISPONIBILIDAD
       ↓
CONTINUIDAD
       ↓
VALOR
        """,
        language="text",
    )


# ============================================================
# TAB 9 — INFORMACIÓN Y MADUREZ
# ============================================================

with tabs[8]:

    st.subheader(
        "Calidad y disponibilidad de información"
    )

    st.write(
        """
        Esta sección diferencia la información corporativa ya
        disponible de aquella que requiere documentación adicional
        para llegar al nivel de análisis de activos y RCM.
        """
    )


    informacion = pd.DataFrame(
        [
            [
                "Información financiera",
                "Disponible",
                "2025"
            ],
            [
                "Estrategia corporativa",
                "Disponible",
                "2026–2035"
            ],
            [
                "Estructura de propiedad",
                "Disponible",
                "50 % / 50 %"
            ],
            [
                "Red y modos de transporte",
                "Disponible",
                "Consolidado"
            ],
            [
                "Inventario completo de activos",
                "Pendiente",
                "Requiere documentación técnica"
            ],
            [
                "Fichas técnicas",
                "Parcial",
                "Por activo y sistema"
            ],
            [
                "Histórico de fallas",
                "Pendiente",
                "Base detallada requerida"
            ],
            [
                "MTBF / MTTR",
                "Pendiente",
                "Debe calcularse con históricos"
            ],
            [
                "Matriz de criticidad",
                "Pendiente",
                "Será construida en el proyecto"
            ],
            [
                "FMECA / RCM",
                "Pendiente",
                "Etapa posterior"
            ],
        ],
        columns=[
            "Elemento",
            "Estado",
            "Observación",
        ],
    )


    st.dataframe(
        informacion,
        width="stretch",
        hide_index=True,
    )


    st.subheader(
        "Cadena metodológica"
    )

    st.code(
        """
CONTEXTO DEL NEGOCIO
        ↓
CONTEXTO OPERACIONAL
        ↓
MODO
        ↓
LÍNEA
        ↓
SISTEMA
        ↓
SUBSISTEMA
        ↓
EQUIPO
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
# CONEXIÓN CON RCM
# ============================================================

st.divider()

st.subheader(
    "Del contexto del negocio al RCM"
)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:

    st.markdown(
        """
        <div class="flow-box">
            <div class="flow-title">
                Negocio
            </div>
            <div class="flow-text">
                ¿Qué valor debe generar?
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with c2:

    st.markdown(
        """
        <div class="flow-box">
            <div class="flow-title">
                Operación
            </div>
            <div class="flow-text">
                ¿En qué condiciones?
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with c3:

    st.markdown(
        """
        <div class="flow-box">
            <div class="flow-title">
                Activos
            </div>
            <div class="flow-text">
                ¿Qué soporta el servicio?
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with c4:

    st.markdown(
        """
        <div class="flow-box">
            <div class="flow-title">
                Funciones
            </div>
            <div class="flow-text">
                ¿Qué deben cumplir?
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with c5:

    st.markdown(
        """
        <div class="flow-box">
            <div class="flow-title">
                RCM
            </div>
            <div class="flow-text">
                ¿Cómo mantenerlas?
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# FUENTE / NOTA METODOLÓGICA
# ============================================================

st.divider()

st.caption(
    "Fuente base: información corporativa, financiera, estratégica "
    "y de gestión de activos consolidada para el proyecto Metro_RCM."
)

st.caption(
    "Las métricas derivadas son cálculos realizados a partir de los "
    "datos registrados; las cifras no disponibles se mantienen como pendientes."
)