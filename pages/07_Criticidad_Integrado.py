# -*- coding: utf-8 -*-
"""Matriz de criticidad y encuesta centralizada de ponderación."""
from pathlib import Path
import json
import pandas as pd
import requests
import streamlit as st
import streamlit.components.v1 as components

from utils.theme import aplicar_tema_udea, encabezado_pagina
from data.criticidad_data import ACTIVOS

st.set_page_config(
    page_title="Matriz de Criticidad | METRO_RCM",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)
aplicar_tema_udea(marca_agua=True)
encabezado_pagina(
    "Matriz de Criticidad",
    "Priorización de activos mediante consecuencia ponderada y probabilidad de falla. La ponderación se define mediante encuesta centralizada.",
)

BASE_WEIGHTS = {
    "seguridad": 0.30,
    "operacion": 0.25,
    "continuidad": 0.20,
    "costo": 0.15,
    "impacto": 0.10,
}
CRITERIOS = [
    ("seguridad", "Seguridad de las personas"),
    ("operacion", "Impacto a la operación"),
    ("continuidad", "Continuidad operacional"),
    ("costo", "Costo de reparación"),
    ("impacto", "Impacto ambiental"),
]

# Correspondencia con la base de activos actual: no existe un campo independiente
# de impacto a la operación, por lo que se utiliza "cobertura" como aproximación.
ASSET_FIELD_MAP = {
    "seguridad": "seguridad",
    "operacion": "cobertura",
    "continuidad": "continuidad",
    "costo": "costo",
    "impacto": "impacto",
}

ENDPOINT_DEFAULT = "https://script.google.com/macros/s/AKfycbx7WSRa1-uPUl2ThljERCQPV996Rnl5Uim8AHQ_PJlXcRDBO4DOjia4TuRcFB1BIxr7vQ/exec"
SURVEY_HTML_PATH = Path(__file__).resolve().parents[1] / "assets" / "encuesta_ponderacion.html"
MATRIX_HTML_PATH = Path(__file__).resolve().parents[1] / "matriz_criticidad_sitva.html"


def get_votation_endpoint() -> str:
    try:
        value = str(st.secrets.get("VOTACION_ENDPOINT", "")).strip()
        return value or ENDPOINT_DEFAULT
    except Exception:
        return ENDPOINT_DEFAULT


def normalize_weights(weights: dict) -> dict:
    total = sum(float(v) for v in weights.values())
    if total <= 0:
        return {k: 0.0 for k in weights}
    return {k: float(v) / total for k, v in weights.items()}


def seed_weights() -> dict:
    """Ponderación inicial de referencia cuando aún no hay datos centrales."""
    rows = [
        [40, 15, 25, 5, 15],
        [40, 25, 20, 5, 10],
        [25, 27, 22, 15, 11],
        [47, 9, 22, 13, 9],
        [40, 15, 30, 10, 5],
    ]
    df = pd.DataFrame(rows, columns=[k for k, _ in CRITERIOS])
    return normalize_weights(df.mean().to_dict())


@st.cache_data(ttl=3, show_spinner=False)
def fetch_central_votations(endpoint: str):
    """Consulta el repositorio central y valida que realmente haya JSON.

    Google Apps Script puede responder mediante redirecciones o con una página HTML
    cuando el despliegue no es público. No convertimos esos casos en "0 respuestas"
    porque eso oculta la causa real de la falla de integración.
    """
    response = requests.get(
        endpoint,
        params={"action": "list", "t": pd.Timestamp.utcnow().value},
        timeout=15,
        allow_redirects=True,
        headers={"Accept": "application/json", "User-Agent": "METRO_RCM/2026"},
    )
    response.raise_for_status()
    content_type = str(response.headers.get("content-type", "")).lower()
    body = response.text.lstrip()
    if not body.startswith("{"):
        preview = body[:180].replace("\n", " ").replace("\r", " ")
        raise RuntimeError(
            "El endpoint no devolvió JSON. "
            f"Content-Type={content_type or 'no informado'}; respuesta={preview!r}"
        )
    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError("La respuesta del endpoint no es JSON válido.") from exc
    if not data.get("ok"):
        raise RuntimeError(data.get("error", "El backend devolvió un error."))
    return data


def normalize_remote_rows(rows):
    out = []
    for i, row in enumerate(rows or []):
        out.append(
            {
                "id": row.get("id", i + 1),
                "fecha": str(row.get("fecha", "")),
                "nombre": str(row.get("nombre", row.get("evaluador", ""))),
                "seguridad": float(row.get("seguridad", 0)),
                "operacion": float(row.get("operacion", 0)),
                "continuidad": float(row.get("continuidad", 0)),
                "costo": float(row.get("costo", 0)),
                "impacto": float(row.get("ambiental", 0)),
            }
        )
    return out


def get_central_weights() -> tuple[dict, int, str, str]:
    endpoint = get_votation_endpoint()
    try:
        data = fetch_central_votations(endpoint)
        registros = normalize_remote_rows(data.get("registros", []))
        if not registros:
            return seed_weights(), 0, "Conexión correcta, pero el repositorio no contiene respuestas.", "empty"
        keys = [k for k, _ in CRITERIOS]
        means = {
            key: sum(float(row[key]) for row in registros) / len(registros)
            for key in keys
        }
        return normalize_weights(means), len(registros), "Conectado al repositorio central; ponderación calculada con las respuestas recibidas.", "ok"
    except Exception as exc:
        return seed_weights(), 0, f"ERROR DE CONEXIÓN: {exc}", "error"


def consequence(asset, weights):
    normalized = normalize_weights(weights)
    return sum(normalized[key] * int(asset[ASSET_FIELD_MAP[key]]) for key, _ in CRITERIOS)


def zone(index):
    if index >= 20:
        return "Muy Alta"
    if index >= 12:
        return "Alta"
    if index >= 6:
        return "Media"
    return "Baja"


def build_df(weights, assets):
    rows = []
    for asset in assets:
        consequence_value = consequence(asset, weights)
        index_value = consequence_value * int(asset["probabilidad"])
        rows.append(
            {
                "Modo": asset["modo"],
                "Línea": asset["linea"],
                "Activo": asset["activo"],
                "Función": asset["funcion"],
                "Seguridad": int(asset["seguridad"]),
                "Impacto operación": int(asset["cobertura"]),
                "Continuidad": int(asset["continuidad"]),
                "Costo": int(asset["costo"]),
                "Impacto ambiental": int(asset["impacto"]),
                "Probabilidad": int(asset["probabilidad"]),
                "Consecuencia": round(consequence_value, 2),
                "Índice": round(index_value, 2),
                "Zona": zone(index_value),
            }
        )
    return pd.DataFrame(rows)


# -----------------------------------------------------------------------------
# ENCUESTA CENTRALIZADA
# -----------------------------------------------------------------------------
endpoint = get_votation_endpoint()

# La lectura de resultados se hace en el proceso Python de Streamlit y se
# inyecta en el iframe. Esto evita depender de CORS/JSONP del navegador: el
# navegador sigue enviando votos al Web App, pero la lectura consolidada usa
# la misma conexión server-side que ya fue validada con diagnostico_votacion.py.
try:
    _central_data_for_iframe = fetch_central_votations(endpoint)
except Exception as _exc:
    _central_data_for_iframe = {
        "ok": False,
        "total": 0,
        "promedios": [0, 0, 0, 0, 0],
        "registros": [],
        "error": str(_exc),
    }

_central_json = json.dumps(_central_data_for_iframe, ensure_ascii=False).replace("<", "\\u003c")

if not SURVEY_HTML_PATH.exists():
    st.error("No se encontró assets/encuesta_ponderacion.html.")
else:
    survey_html = SURVEY_HTML_PATH.read_text(encoding="utf-8")
    survey_html = survey_html.replace("__VOTACION_ENDPOINT__", endpoint)
    survey_html = survey_html.replace("__CENTRAL_DATA__", _central_json)
    components.html(survey_html, height=1810, scrolling=True)

# Sincronización explícita: evita recargar el iframe de la encuesta mientras el
# usuario está votando y, al mismo tiempo, permite aplicar la ponderación central
# a la matriz sin perder las ediciones de la propia matriz.
st.markdown('<div class="metro-section-kicker">SINCRONIZACIÓN DE LA MATRIZ</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="metro-section-title">Ponderación actualmente aplicada</div>',
    unsafe_allow_html=True,
)

if "pesos_encuesta" not in st.session_state:
    st.session_state.pesos_encuesta = seed_weights()
if "votos_centrales" not in st.session_state:
    st.session_state.votos_centrales = 0

peso_actual, total_respuestas, estado_peso, estado_conexion = get_central_weights()
st.session_state.pesos_encuesta = peso_actual
st.session_state.votos_centrales = total_respuestas

if estado_conexion == "ok":
    st.success(f"Repositorio central conectado · {total_respuestas} respuestas recibidas.")
elif estado_conexion == "empty":
    st.warning("El repositorio central respondió correctamente, pero no contiene respuestas.")
else:
    st.error(estado_peso)

cols = st.columns(5)
for col, (key, label) in zip(cols, CRITERIOS):
    with col:
        col.metric(label, f"{peso_actual[key] * 100:.1f}%")

sync_col, info_col = st.columns([1, 4])
with sync_col:
    if st.button("Actualizar ponderación", type="primary", width="stretch"):
        fetch_central_votations.clear()
        st.rerun()
with info_col:
    st.caption(
        f"{estado_peso} Respuestas centrales: {total_respuestas}. "
        "La ponderación se normaliza para sumar 100 %."
    )
    st.caption(f"Endpoint consultado: {endpoint}")

# -----------------------------------------------------------------------------
# MATRIZ DE CRITICIDAD
# -----------------------------------------------------------------------------
st.divider()
st.markdown('<div class="metro-section-kicker">ANÁLISIS DE CRITICIDAD</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="metro-section-title">Matriz de Criticidad de Activos</div>',
    unsafe_allow_html=True,
)
st.caption(
    "Los pesos de la encuesta centralizada se incorporan como entrada de la consecuencia ponderada. "
    "La matriz permite explorar el resultado por modo, ranking, mapa de criticidad y tabla de activos."
)

_pesos_matriz = normalize_weights(st.session_state.get("pesos_encuesta", seed_weights()))
_pesos_js = [float(_pesos_matriz[key]) for key, _ in CRITERIOS]

try:
    matrix_html = MATRIX_HTML_PATH.read_text(encoding="utf-8")
    marker = "let weights = [...DEFAULT_WEIGHTS];"
    if marker in matrix_html:
        matrix_html = matrix_html.replace("__VOTACION_ENDPOINT__", endpoint)
        matrix_html = matrix_html.replace("__CENTRAL_DATA__", _central_json)
        matrix_html = matrix_html.replace(
            marker,
            "let weights = " + json.dumps(_pesos_js, ensure_ascii=False) + ";",
            1,
        )
    components.html(matrix_html, height=2800, scrolling=True)
except FileNotFoundError:
    st.error("No se encontró matriz_criticidad_sitva.html en la raíz del proyecto.")
