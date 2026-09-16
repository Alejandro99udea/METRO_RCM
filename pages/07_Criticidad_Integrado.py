# -*- coding: utf-8 -*-
from pathlib import Path
import json
import pandas as pd
import requests
import streamlit as st
import streamlit.components.v1 as components
from utils.theme import aplicar_tema_udea
from data.criticidad_data import ACTIVOS

st.set_page_config(page_title="Matriz de Criticidad | METRO_RCM", page_icon="⚠️", layout="wide")
aplicar_tema_udea(marca_agua=True)

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

# Correspondencia temporal con la base de activos actual: el archivo de activos
# no contiene un campo independiente de "Impacto a la operación"; se utiliza la
# variable existente "cobertura" como aproximación operativa, claramente rotulada.
ASSET_FIELD_MAP = {
    "seguridad": "seguridad",
    "operacion": "cobertura",
    "continuidad": "continuidad",
    "costo": "costo",
    "impacto": "impacto",
}

ZONAS = [("Muy Alta", 20), ("Alta", 12), ("Media", 6), ("Baja", 0)]


def normalize_weights(weights):
    total = sum(weights.values())
    if total <= 0:
        return {k: 0.0 for k in weights}
    return {k: v / total for k, v in weights.items()}


def consequence(asset, weights):
    w = normalize_weights(weights)
    return sum(w[k] * int(asset[ASSET_FIELD_MAP[k]]) for k, _ in CRITERIOS)


def zone(index):
    if index >= 20: return "Muy Alta"
    if index >= 12: return "Alta"
    if index >= 6: return "Media"
    return "Baja"


def build_df(weights, assets):
    rows = []
    for a in assets:
        c = consequence(a, weights)
        idx = c * int(a["probabilidad"])
        rows.append({
            "Modo": a["modo"], "Línea": a["linea"], "Activo": a["activo"], "Función": a["funcion"],
            "Seguridad": int(a["seguridad"]), "Impacto operación": int(a["cobertura"]),
            "Continuidad": int(a["continuidad"]), "Costo": int(a["costo"]), "Impacto ambiental": int(a["impacto"]),
            "Probabilidad": int(a["probabilidad"]), "Consecuencia": round(c,2), "Índice": round(idx,2), "Zona": zone(idx)
        })
    return pd.DataFrame(rows)


def seed_weights():
    # Valores visibles en el cuestionario entregado: 5 respuestas de 100 puntos.
    rows = [
        [40,15,25,5,15], [40,25,20,5,10], [25,27,22,15,11], [47,9,22,13,9], [40,15,30,10,5]
    ]
    df = pd.DataFrame(rows, columns=[k for k,_ in CRITERIOS])
    means = df.mean().to_dict()
    return normalize_weights(means)

if "activos_criticidad" not in st.session_state:
    st.session_state.activos_criticidad = [a.copy() for a in ACTIVOS]
if "modo_pesos" not in st.session_state:
    st.session_state.modo_pesos = "Encuesta"
if "pesos_encuesta" not in st.session_state:
    st.session_state.pesos_encuesta = seed_weights()
if "pesos_base" not in st.session_state:
    st.session_state.pesos_base = BASE_WEIGHTS.copy()

st.markdown("""
<div class="metro-header">
  <div class="metro-header-title">⚠️ MATRIZ DE CRITICIDAD DE ACTIVOS</div>
  <div class="metro-header-subtitle">Pesos definidos por encuesta · Consecuencia ponderada · Probabilidad de falla</div>
</div><div class="metro-accent"></div>
""", unsafe_allow_html=True)

ENDPOINT_DEFAULT = "https://script.google.com/macros/s/AKfycbxnD56RbYrRxpgo8K1EKCTJSrN23c5GFLsHvaPr6sWLhmA1O0vEm7T-OrI0lJdknLSA/exec"


def get_votation_endpoint():
    try:
        value = str(st.secrets.get("VOTACION_ENDPOINT", "")).strip()
        return value or ENDPOINT_DEFAULT
    except Exception:
        return ENDPOINT_DEFAULT


VOTACION_ENDPOINT = get_votation_endpoint()


@st.cache_data(ttl=3, show_spinner=False)
def fetch_central_votations(endpoint: str):
    r = requests.get(
        endpoint,
        params={"action": "list", "t": pd.Timestamp.utcnow().value},
        timeout=12,
    )
    r.raise_for_status()
    data = r.json()
    if not data.get("ok"):
        raise RuntimeError(data.get("error", "El backend devolvió un error."))
    return data


def post_central_vote(endpoint: str, nombre: str, votos: list[int]):
    # Apps Script puede responder con una redirección; usamos GET para la acción
    # de escritura porque conserva los parámetros al seguir la redirección.
    r = requests.get(
        endpoint,
        params={
            "action": "add",
            "nombre": nombre,
            "votos": json.dumps(votos, separators=(",", ":")),
            "t": pd.Timestamp.utcnow().value,
        },
        timeout=20,
        allow_redirects=True,
    )
    r.raise_for_status()
    try:
        data = r.json()
    except ValueError as exc:
        preview = r.text[:300].replace("\n", " ")
        raise RuntimeError(f"Respuesta no JSON del registro central: {preview}") from exc
    if not data.get("ok"):
        raise RuntimeError(data.get("error", "No se pudo registrar la respuesta."))
    fetch_central_votations.clear()
    return data


def normalize_remote_rows(rows):
    out = []
    for i, r in enumerate(rows or []):
        out.append(
            {
                "id": r.get("id", i + 1),
                "fecha": str(r.get("fecha", "")),
                "nombre": str(r.get("nombre", r.get("evaluador", ""))),
                "seguridad": float(r.get("seguridad", 0)),
                "operacion": float(r.get("operacion", 0)),
                "continuidad": float(r.get("continuidad", 0)),
                "costo": float(r.get("costo", 0)),
                "impacto": float(r.get("ambiental", 0)),
            }
        )
    return out


def render_central_results():
    try:
        data = fetch_central_votations(VOTACION_ENDPOINT)
        registros = normalize_remote_rows(data.get("registros", []))
        total = len(registros)
        claves = ["seguridad", "operacion", "continuidad", "costo", "impacto"]
        promedios = [sum(r[k] for r in registros) / total for k in claves] if total else [0.0] * 5
        st.success(f"🟢 Registro central conectado · {total} respuestas sincronizadas")

        c = st.columns(5)
        for col, label, value in zip(
            c,
            ["Seguridad", "Imp. operación", "Continuidad", "Costo", "Ambiental"],
            promedios,
        ):
            col.metric(label, f"{value:.1f}")

        st.caption("Los resultados se actualizan automáticamente cada 5 segundos desde el repositorio central.")
        if registros:
            tabla = pd.DataFrame(
                [
                    {
                        "#": i + 1,
                        "Nombre": r["nombre"],
                        "Seguridad": int(r["seguridad"]),
                        "Imp. Operación": int(r["operacion"]),
                        "Continuidad": int(r["continuidad"]),
                        "Costo": int(r["costo"]),
                        "Ambiental": int(r["impacto"]),
                        "Fecha": r["fecha"],
                    }
                    for i, r in enumerate(registros)
                ]
            )
            st.dataframe(tabla, width="stretch", hide_index=True)
        else:
            st.info("Aún no hay respuestas registradas en el repositorio central.")

        return promedios, registros
    except Exception as exc:
        st.error(f"No se pudo consultar el registro central: {exc}")
        return [0.0] * 5, []


def encuesta_en_fragmento():
    st.subheader("🗳️ Ponderación de criterios")
    st.caption(
        "Distribuya exactamente 100 puntos entre los cinco criterios. "
        "Cada respuesta se registra en Google Sheets y se comparte entre todos los dispositivos conectados."
    )

    with st.form("form_votacion_ponderacion", clear_on_submit=True):
        nombre = st.text_input("Nombre del participante", placeholder="Ingresa tu nombre...")
        cols = st.columns(5)
        labels = [
            ("Seguridad de las personas", "voto_seguridad"),
            ("Impacto a la operación", "voto_operacion"),
            ("Continuidad operacional", "voto_continuidad"),
            ("Costo de reparación", "voto_costo"),
            ("Impacto ambiental", "voto_impacto"),
        ]
        valores = []
        for col, (label, key) in zip(cols, labels):
            with col:
                valores.append(st.slider(label, 0, 100, 0, key=key))
        total = sum(valores)
        c1, c2 = st.columns([1, 3])
        with c1:
            st.metric("Puntos asignados", total)
        with c2:
            st.progress(min(total, 100) / 100)
            st.caption(f"Puntos disponibles: {max(0, 100 - total)}")
        enviar = st.form_submit_button("Registrar mi respuesta", type="primary", width="stretch")

    if enviar:
        nombre = nombre.strip()
        if not nombre:
            st.warning("Ingrese el nombre del participante.")
            return
        if total != 100:
            st.warning(f"Debe distribuir exactamente 100 puntos. Actualmente hay {total}.")
            return
        try:
            post_central_vote(VOTACION_ENDPOINT, nombre, valores)
            st.success("✅ Respuesta registrada correctamente en el repositorio central.")
            st.rerun()
        except Exception as exc:
            st.error(f"No se pudo registrar la respuesta central: {exc}")


with st.expander("🗳️ Ponderación de criterios — Encuesta del equipo", expanded=True):
    # El fragmento se actualiza solo, sin recargar toda la página ni perder el estado de la matriz.
    try:
        fragment = st.fragment
    except AttributeError:
        fragment = None

    if fragment is not None:
        @st.fragment(run_every="5s")
        def _encuesta_live():
            encuesta_en_fragmento()
            promedios_encuesta, registros_centrales = render_central_results()
            if registros_centrales:
                st.session_state.pesos_encuesta = normalize_weights(
                    dict(zip([k for k, _ in CRITERIOS], promedios_encuesta))
                )

        _encuesta_live()
    else:
        encuesta_en_fragmento()
        promedios_encuesta, registros_centrales = render_central_results()
        if registros_centrales:
            st.session_state.pesos_encuesta = normalize_weights(
                dict(zip([k for k, _ in CRITERIOS], promedios_encuesta))
            )



# -----------------------------------------------------------------------------
# MATRIZ DE CRITICIDAD — NUEVO MOTOR VISUAL
# Se reemplaza únicamente la sección de matriz. La encuesta anterior queda
# intacta y sigue usando el registro central de Google Sheets.
# -----------------------------------------------------------------------------
MATRIX_HTML_PATH = Path(__file__).resolve().parents[1] / "matriz_criticidad_sitva.html"

st.divider()
st.subheader("📊 Matriz de Criticidad de Activos")
st.caption(
    "Nueva matriz SITVA integrada. La encuesta de ponderación anterior se conserva "
    "sin cambios; sus pesos se utilizan como valores iniciales al abrir la matriz."
)

# Tomar los pesos centrales que ya calculó la encuesta en esta ejecución.
_pesos_matriz = st.session_state.get("pesos_encuesta", seed_weights())
_pesos_matriz = normalize_weights(_pesos_matriz)
_pesos_js = [float(_pesos_matriz[k]) for k, _ in CRITERIOS]

try:
    _matrix_html = MATRIX_HTML_PATH.read_text(encoding="utf-8")
    _marker = "let weights = [...DEFAULT_WEIGHTS];"
    if _marker in _matrix_html:
        _matrix_html = _matrix_html.replace(
            _marker,
            "let weights = " + json.dumps(_pesos_js, ensure_ascii=False) + ";",
            1,
        )
    components.html(_matrix_html, height=2800, scrolling=True)
except FileNotFoundError:
    st.error(
        "No se encontró matriz_criticidad_sitva.html en la raíz del proyecto. "
        "Verifique que el archivo esté junto a app.py."
    )
