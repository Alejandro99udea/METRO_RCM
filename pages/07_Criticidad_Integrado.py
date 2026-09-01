# -*- coding: utf-8 -*-

from utils.theme import aplicar_tema_udea
import pandas as pd
import streamlit as st

from data.criticidad_data import ACTIVOS


st.set_page_config(
    page_title="Matriz de Criticidad | METRO_RCM",
    page_icon="⚠️",
    layout="wide",
)
aplicar_tema_udea(marca_agua=True)


# ============================================================
# CONFIGURACIÓN
# ============================================================

CRITERIOS = [
    ("seguridad", "Seguridad de las personas", 0.30),
    ("continuidad", "Continuidad operacional", 0.25),
    ("cobertura", "Cobertura / usuarios", 0.20),
    ("costo", "Costo de reparación", 0.15),
    ("impacto", "Impacto ambiental", 0.10),
]

ZONAS = [
    ("Muy Alta", 20, 25),
    ("Alta", 12, 20),
    ("Media", 6, 12),
    ("Baja", 0, 6),
]


# ============================================================
# FUNCIONES
# ============================================================

def calcular_pesos(pesos):
    total = sum(pesos.values())

    if total <= 0:
        return {key: 0 for key in pesos}

    return {
        key: value / total
        for key, value in pesos.items()
    }


def consecuencia_ponderada(activo, pesos):
    pesos_norm = calcular_pesos(pesos)

    return sum(
        pesos_norm[key] * activo[key]
        for key, _, _ in CRITERIOS
    )


def indice_criticidad(activo, pesos):
    return (
        consecuencia_ponderada(activo, pesos)
        * activo["probabilidad"]
    )


def zona_criticidad(indice):
    if indice >= 20:
        return "Muy Alta"

    if indice >= 12:
        return "Alta"

    if indice >= 6:
        return "Media"

    return "Baja"


def color_zona(zona):
    colores = {
        "Baja": "#008037",
        "Media": "#E8B93B",
        "Alta": "#D97706",
        "Muy Alta": "#C0272D",
    }

    return colores[zona]


def construir_dataframe(pesos, activos):
    registros = []

    for activo in activos:

        consecuencia = consecuencia_ponderada(
            activo,
            pesos
        )

        indice = consecuencia * activo["probabilidad"]

        registros.append({
            "Modo": activo["modo"],
            "Línea": activo["linea"],
            "Activo": activo["activo"],
            "Función": activo["funcion"],
            "Seguridad": activo["seguridad"],
            "Continuidad": activo["continuidad"],
            "Cobertura": activo["cobertura"],
            "Costo": activo["costo"],
            "Impacto": activo["impacto"],
            "Consecuencia": round(consecuencia, 2),
            "Probabilidad": activo["probabilidad"],
            "Índice": round(indice, 2),
            "Zona": zona_criticidad(indice),
        })

    return pd.DataFrame(registros)


# ============================================================
# ESTADO
# ============================================================

if "pesos_criticidad" not in st.session_state:

    st.session_state.pesos_criticidad = {
        key: weight
        for key, _, weight in CRITERIOS
    }


if "activos_criticidad" not in st.session_state:

    st.session_state.activos_criticidad = [
        activo.copy()
        for activo in ACTIVOS
    ]


# ============================================================
# ENCABEZADO
# ============================================================

st.title("Matriz de Criticidad de Activos")

st.subheader("Gestión de Activos")

st.write(
    "Evaluación interactiva de activos del SITVA mediante "
    "criterios de consecuencia y probabilidad de falla."
)

st.caption(
    "Inventario y calificaciones provenientes del aplicativo "
    "de matriz de criticidad suministrado para integración."
)


# ============================================================
# PESOS
# ============================================================

with st.container(border=True):

    st.subheader("Pesos de los criterios de consecuencia")

    st.write(
        "Los pesos se normalizan automáticamente para sumar 100 %. "
        "La consecuencia ponderada se multiplica por la probabilidad "
        "de falla para obtener el índice de criticidad."
    )

    peso_cols = st.columns(5)

    nuevos_pesos = {}

    for i, (key, nombre, valor_default) in enumerate(CRITERIOS):

        with peso_cols[i]:

            nuevos_pesos[key] = (
                st.slider(
                    nombre,
                    min_value=1,
                    max_value=60,
                    value=round(
                        st.session_state.pesos_criticidad[key] * 100
                    ),
                    step=1,
                    key=f"peso_{key}",
                ) / 100
            )

    st.session_state.pesos_criticidad = nuevos_pesos

    suma_pesos = sum(nuevos_pesos.values()) * 100

    st.metric(
        "Suma de pesos",
        f"{suma_pesos:.0f} %"
    )

    if st.button(
        "Restablecer pesos originales",
        width="stretch",
        key="reset_pesos"
    ):

        st.session_state.pesos_criticidad = {
            key: value
            for key, _, value in CRITERIOS
        }

        st.rerun()


# ============================================================
# DATAFRAME CALCULADO
# ============================================================

df = construir_dataframe(
    st.session_state.pesos_criticidad,
    st.session_state.activos_criticidad,
)


# ============================================================
# FILTRO
# ============================================================

st.divider()

st.subheader("Resumen por modo")

modos_disponibles = [
    "Todos"
] + sorted(
    df["Modo"].unique().tolist()
)

modo_seleccionado = st.selectbox(
    "Modo de transporte",
    modos_disponibles,
    key="modo_criticidad"
)

if modo_seleccionado != "Todos":

    df_visible = df[
        df["Modo"] == modo_seleccionado
    ].copy()

else:

    df_visible = df.copy()


# ============================================================
# RESUMEN DE ZONAS
# ============================================================

zona_cols = st.columns(4)

orden_zonas = [
    "Muy Alta",
    "Alta",
    "Media",
    "Baja",
]

for i, zona in enumerate(orden_zonas):

    cantidad = int(
        (df_visible["Zona"] == zona).sum()
    )

    porcentaje = (
        cantidad / len(df_visible) * 100
        if len(df_visible) > 0
        else 0
    )

    with zona_cols[i]:

        st.metric(
            zona,
            cantidad,
            f"{porcentaje:.1f} % del total"
        )


# ============================================================
# RANKING
# ============================================================

st.divider()

st.subheader(
    "Ranking de criticidad"
)

ranking = (
    df_visible
    .sort_values(
        "Índice",
        ascending=False
    )
    .head(12)
    .copy()
)

ranking["Ranking"] = range(
    1,
    len(ranking) + 1
)

ranking = ranking[
    [
        "Ranking",
        "Modo",
        "Activo",
        "Índice",
        "Zona",
    ]
]

st.dataframe(
    ranking,
    width="stretch",
    hide_index=True,
    column_config={
        "Índice": st.column_config.NumberColumn(
            format="%.2f"
        ),
    },
)


# ============================================================
# MATRIZ 5 × 5 DE REFERENCIA
# ============================================================

st.divider()

st.subheader(
    "Mapa de criticidad"
)

st.caption(
    "Eje X: consecuencia ponderada. Eje Y: probabilidad de falla."
)

mapa = pd.DataFrame(
    index=[5, 4, 3, 2, 1],
    columns=[1, 2, 3, 4, 5],
)

for probabilidad in [1, 2, 3, 4, 5]:

    for consecuencia in [1, 2, 3, 4, 5]:

        indice = probabilidad * consecuencia

        mapa.loc[
            probabilidad,
            consecuencia
        ] = f"{indice:.0f}"


st.dataframe(
    mapa,
    width="stretch",
)

st.caption(
    "La matriz muestra el producto de referencia probabilidad × consecuencia. "
    "Los índices calculados en esta aplicación utilizan la consecuencia ponderada."
)


# ============================================================
# TABLA COMPLETA EDITABLE
# ============================================================

st.divider()

st.subheader(
    "Matriz completa — activos editables"
)

st.write(
    "Los valores de los cinco criterios y la probabilidad de falla "
    "pueden modificarse. El índice y la zona se recalculan automáticamente."
)


# Limitar columnas editables a los datos de la matriz original.
columnas_editor = [
    "Modo",
    "Línea",
    "Activo",
    "Seguridad",
    "Continuidad",
    "Cobertura",
    "Costo",
    "Impacto",
    "Probabilidad",
]

df_edicion = df_visible[columnas_editor].copy()

df_editado = st.data_editor(
    df_edicion,
    width="stretch",
    hide_index=True,
    num_rows="fixed",
    disabled=[
        "Modo",
        "Línea",
        "Activo",
    ],
    column_config={
        "Seguridad": st.column_config.NumberColumn(
            min_value=1,
            max_value=5,
            step=1,
        ),
        "Continuidad": st.column_config.NumberColumn(
            min_value=1,
            max_value=5,
            step=1,
        ),
        "Cobertura": st.column_config.NumberColumn(
            min_value=1,
            max_value=5,
            step=1,
        ),
        "Costo": st.column_config.NumberColumn(
            min_value=1,
            max_value=5,
            step=1,
        ),
        "Impacto": st.column_config.NumberColumn(
            min_value=1,
            max_value=5,
            step=1,
        ),
        "Probabilidad": st.column_config.NumberColumn(
            min_value=1,
            max_value=5,
            step=1,
        ),
    },
)


# ============================================================
# GUARDAR CAMBIOS EN LA SESIÓN
# ============================================================

if st.button(
    "Actualizar matriz con los valores editados",
    width="stretch",
    key="actualizar_matriz"
):

    for _, fila in df_editado.iterrows():

        coincidencias = [
            i
            for i, activo in enumerate(
                st.session_state.activos_criticidad
            )
            if (
                activo["modo"] == fila["Modo"]
                and activo["linea"] == fila["Línea"]
                and activo["activo"] == fila["Activo"]
            )
        ]

        if not coincidencias:
            continue

        indice_activo = coincidencias[0]

        for campo in [
            "Seguridad",
            "Continuidad",
            "Cobertura",
            "Costo",
            "Impacto",
            "Probabilidad",
        ]:

            clave = campo.lower()

            if campo == "Costo":
                clave = "costo"

            if campo == "Impacto":
                clave = "impacto"

            valor = int(
                max(
                    1,
                    min(
                        5,
                        int(fila[campo])
                    )
                )
            )

            st.session_state.activos_criticidad[
                indice_activo
            ][clave] = valor

    st.success(
        "Matriz actualizada correctamente."
    )

    st.rerun()


# ============================================================
# INFORMACIÓN METODOLÓGICA
# ============================================================

st.divider()

with st.expander(
    "Ver metodología y advertencia sobre los datos"
):

    st.write(
        """
        El aplicativo original define cinco criterios de consecuencia:
        Seguridad de las personas, Continuidad operacional,
        Cobertura / usuarios, Costo de reparación e Impacto ambiental.

        La consecuencia ponderada se calcula como la suma de cada
        puntaje multiplicado por su peso normalizado. El índice de
        criticidad se obtiene multiplicando dicha consecuencia por
        la probabilidad de falla.

        El inventario y las calificaciones incorporadas son los que
        fueron suministrados en el aplicativo original. El propio
        aplicativo fuente advierte que son valores ilustrativos,
        basados en criterio experto genérico y fuentes públicas,
        y que deben validarse con información técnica real del operador
        antes de utilizarlos para decisiones reales.
        """
    )


# ============================================================
# PIE
# ============================================================

st.divider()

st.caption(
    "METRO_RCM · Matriz de Criticidad · Integración del aplicativo fuente"
)
