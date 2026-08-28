# -*- coding: utf-8 -*-

from pathlib import Path
import json
import math

import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Equipo RCM | METRO_RCM",
    page_icon="👥",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "equipo_rcm.json"
ASSETS_DIR = BASE_DIR / "assets" / "equipo_rcm"


# ============================================================
# CARGA DE DATOS
# ============================================================

@st.cache_data

def cargar_datos():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


data = cargar_datos()
competencias = data.get("competencias", [])
miembros = data.get("miembros", [])


# ============================================================
# FUNCIONES
# ============================================================

def ruta_foto(miembro):
    nombre = Path(miembro.get("foto", "")).name
    ruta = ASSETS_DIR / "fotos" / nombre
    return ruta if ruta.exists() else None


def ruta_cv(miembro):
    nombre = Path(miembro.get("hoja_de_vida", "")).name
    ruta = ASSETS_DIR / "documentos" / nombre
    return ruta if ruta.exists() else None


def promedio_competencias():
    promedios = []
    for i, competencia in enumerate(competencias):
        valores = []
        for m in miembros:
            puntajes = m.get("puntajes", [])
            if i < len(puntajes):
                try:
                    valores.append(float(puntajes[i]))
                except (TypeError, ValueError):
                    pass
        promedios.append(sum(valores) / len(valores) if valores else 0)
    return promedios


def competencia_frame(miembro):
    filas = []
    puntajes = miembro.get("puntajes", [])
    for i, competencia in enumerate(competencias):
        valor = puntajes[i] if i < len(puntajes) else None
        filas.append({"#": i + 1, "Competencia": competencia, "Puntaje": valor})
    return pd.DataFrame(filas)


def top_competencias(n=5):
    promedios = promedio_competencias()
    datos = list(zip(competencias, promedios))
    datos.sort(key=lambda x: x[1], reverse=True)
    return datos[:n]


# ============================================================
# ESTILOS VISUALES
# ============================================================

st.markdown(
    """
    <style>
    .hero-equipo {
        background: linear-gradient(135deg, #004F3D, #006B54);
        border-radius: 20px;
        padding: 28px 34px;
        margin-bottom: 22px;
        color: white;
    }
    .hero-equipo .eyebrow {
        font-size: .80rem;
        font-weight: 700;
        letter-spacing: .12em;
        text-transform: uppercase;
        opacity: .90;
    }
    .hero-equipo .title {
        font-size: 2.15rem;
        font-weight: 800;
        line-height: 1.15;
        margin-top: 7px;
    }
    .hero-equipo .subtitle {
        font-size: 1rem;
        margin-top: 8px;
        max-width: 900px;
        opacity: .88;
    }
    .member-photo {
        border-radius: 50%;
        width: 112px;
        height: 112px;
        object-fit: cover;
        border: 3px solid #006B54;
    }
    .role-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        background: #E8F3EF;
        color: #004F3D;
        font-size: .78rem;
        font-weight: 700;
        margin-top: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    """
    <div class="hero-equipo">
        <div class="eyebrow">METRO_RCM · Gestión de Activos</div>
        <div class="title">Equipo de Gestión de Activos</div>
        <div class="subtitle">
            Estructura organizacional, perfiles profesionales y diagnóstico
            de competencias del equipo RCM.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# RESUMEN EJECUTIVO
# ============================================================

promedios = promedio_competencias()
top5 = top_competencias(5)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Integrantes", len(miembros))
with c2:
    st.metric("Competencias", len(competencias))
with c3:
    st.metric("Roles Belbin", len(set(m.get("rol_belbin", "") for m in miembros)))
with c4:
    promedio_general = sum(promedios) / len(promedios) if promedios else 0
    st.metric("Promedio general", f"{promedio_general:.2f} / 5")


# ============================================================
# PESTAÑAS
# ============================================================

tab1, tab2, tab3 = st.tabs([
    "🏢 Organigrama",
    "👤 Perfil individual",
    "📊 Competencias",
])


# ============================================================
# TAB 1 — ORGANIGRAMA
# ============================================================

with tab1:

    st.subheader("Estructura del equipo")
    st.caption("Seleccione un integrante para consultar su perfil y competencias.")

    niveles = sorted({m.get("nivel", 99) for m in miembros})

    for nivel in niveles:
        miembros_nivel = [m for m in miembros if m.get("nivel") == nivel]
        if not miembros_nivel:
            continue

        st.markdown(f"### Nivel {nivel}")
        cols = st.columns(min(4, len(miembros_nivel)))

        for idx, miembro in enumerate(miembros_nivel):
            with cols[idx % len(cols)]:
                with st.container(border=True):
                    foto = ruta_foto(miembro)
                    if foto:
                        st.image(str(foto), width=112)
                    else:
                        st.markdown("👤")

                    st.markdown(f"**{miembro.get('nombre', 'Sin nombre')}**")
                    st.caption(miembro.get("cargo", ""))
                    st.markdown(
                        f"<span class='role-pill'>{miembro.get('rol_belbin', 'Sin rol')}</span>",
                        unsafe_allow_html=True,
                    )
                    st.write(miembro.get("mision", ""))
                    if st.button(
                        "Ver perfil →",
                        key=f"perfil_{miembro.get('id')}",
                        width="stretch",
                    ):
                        st.session_state["miembro_seleccionado"] = miembro.get("id")
                        st.session_state["ir_tab_perfil"] = True
                        st.rerun()


# ============================================================
# TAB 2 — PERFIL
# ============================================================

with tab2:

    opciones = {m.get("nombre", "Sin nombre"): m.get("id") for m in miembros}

    nombres = list(opciones.keys())
    seleccionado_id = st.session_state.get("miembro_seleccionado", miembros[0].get("id") if miembros else None)

    nombre_por_defecto = next(
        (nombre for nombre, mid in opciones.items() if mid == seleccionado_id),
        nombres[0] if nombres else None,
    )

    nombre = st.selectbox(
        "Seleccione un integrante",
        nombres,
        index=nombres.index(nombre_por_defecto) if nombre_por_defecto in nombres else 0,
    )

    miembro = next(
        (m for m in miembros if m.get("id") == opciones[nombre]),
        miembros[0] if miembros else {},
    )

    foto = ruta_foto(miembro)
    cv = ruta_cv(miembro)

    izquierda, derecha = st.columns([1, 1.5], gap="large")

    with izquierda:
        with st.container(border=True):
            if foto:
                st.image(str(foto), width=150)
            else:
                st.info("Fotografía no disponible en el archivo suministrado.")

            st.markdown(f"## {miembro.get('nombre', 'Sin nombre')}")
            st.markdown(f"**{miembro.get('cargo', 'Sin cargo')}**")
            st.markdown(
                f"<span class='role-pill'>{miembro.get('rol_belbin', 'Sin rol')}</span>",
                unsafe_allow_html=True,
            )

            st.markdown("### Perfil profesional")
            st.write(miembro.get("descripcion", "Sin descripción disponible."))

            st.markdown("### Habilidades principales")
            st.write(miembro.get("habilidades", "Sin información disponible."))

            st.markdown("### Especialidad")
            st.write(miembro.get("especialidad", "Sin información disponible."))

            st.markdown("### Contacto")
            correo = miembro.get("correo", "").strip()
            linkedin = miembro.get("linkedin", "").strip()

            if correo:
                st.markdown(f"**Correo:** {correo}")
            if linkedin:
                st.markdown(f"**LinkedIn:** {linkedin}")
            if cv:
                st.download_button(
                    "📄 Descargar hoja de vida",
                    data=cv.read_bytes(),
                    file_name=cv.name,
                    mime="application/pdf",
                    width="stretch",
                    key=f"cv_{miembro.get('id')}",
                )
            else:
                st.caption("Hoja de vida no disponible en el archivo suministrado.")

    with derecha:
        st.markdown("### Evaluación de competencias")
        df_persona = competencia_frame(miembro)
        st.dataframe(
            df_persona,
            width="stretch",
            hide_index=True,
            column_config={
                "Puntaje": st.column_config.ProgressColumn(
                    "Puntaje",
                    min_value=0,
                    max_value=5,
                    format="%.1f",
                )
            },
        )

        st.markdown("### Fortalezas principales")
        top_persona = []
        puntajes = miembro.get("puntajes", [])
        for i, comp in enumerate(competencias):
            if i < len(puntajes):
                try:
                    top_persona.append((comp, float(puntajes[i])))
                except (TypeError, ValueError):
                    pass
        top_persona.sort(key=lambda x: x[1], reverse=True)
        for comp, val in top_persona[:5]:
            st.write(f"**{comp}** — {val:.1f} / 5")


# ============================================================
# TAB 3 — COMPETENCIAS
# ============================================================

with tab3:

    st.subheader("Diagnóstico consolidado del equipo")
    st.caption("Promedio de cada competencia a partir de los puntajes registrados en la base suministrada.")

    df_equipo = pd.DataFrame({
        "N°": list(range(1, len(competencias) + 1)),
        "Competencia": competencias,
        "Promedio": [round(v, 2) for v in promedios],
    })
    df_equipo = df_equipo.sort_values("Promedio", ascending=False).reset_index(drop=True)

    ctop1, ctop2, ctop3 = st.columns(3)
    for col, (comp, val) in zip([ctop1, ctop2, ctop3], top5[:3]):
        with col:
            st.metric(comp, f"{val:.2f} / 5")

    st.markdown("### Ranking de competencias")
    st.dataframe(
        df_equipo,
        width="stretch",
        hide_index=True,
        column_config={
            "Promedio": st.column_config.ProgressColumn(
                "Promedio",
                min_value=0,
                max_value=5,
                format="%.2f",
            )
        },
    )

    st.markdown("### Perfil de competencias del equipo")
    st.line_chart(
        pd.DataFrame({"Promedio": promedios}, index=[str(i + 1) for i in range(len(promedios))]),
        height=360,
    )

    st.info(
        "Los números del eje horizontal corresponden al orden original de las 35 competencias. "
        "La descripción completa se consulta en la tabla superior."
    )


# ============================================================
# INFORME
# ============================================================

st.divider()
st.subheader("Informe")
st.caption("Generación de un informe PDF del módulo se incorporará al sistema común de reportes de METRO_RCM.")
