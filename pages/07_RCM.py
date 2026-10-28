# -*- coding: utf-8 -*-
"""Explorador interactivo de funciones y análisis RCM del libro cargado."""

from pathlib import Path
import re

import pandas as pd
import streamlit as st

from data.rcm_repository import (
    RCMWorkbookError,
    decision_columns,
    find_column,
    is_filled,
    load_rcm_workbook,
    normalize_label,
)
from utils.theme import aplicar_tema_udea, encabezado_pagina


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_WORKBOOK = BASE_DIR / "data" / "rcm" / "Funciones_y_Analisis_RCM_Metro_Tren.xlsx"

st.set_page_config(
    page_title="Análisis RCM | METRO_RCM",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)
aplicar_tema_udea(marca_agua=True)
encabezado_pagina(
    "Análisis RCM",
    "Explorador interactivo de funciones, fallas, consecuencias y actividades.",
    "07",
)


@st.cache_data(show_spinner=False)
def _load_cached(file_bytes: bytes) -> dict:
    """Carga el libro una vez por versión de archivo durante la sesión."""
    return load_rcm_workbook(file_bytes)


def _display(value, empty: str = "Vacío en el libro") -> str:
    return str(value).strip() if is_filled(value) else empty


def _value(row: pd.Series, frame: pd.DataFrame, label: str) -> str:
    column = find_column(frame, label, required=False)
    if column is None:
        return "Campo no incluido en el libro"
    return _display(row.get(column))


def _count_filled(frame: pd.DataFrame, label: str) -> int | None:
    column = find_column(frame, label, required=False)
    return int(frame[column].map(is_filled).sum()) if column else None


def _metric_number(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def _function_label(function_id: str, indexed_functions: pd.DataFrame, name_col, tag_col) -> str:
    row = indexed_functions.loc[function_id]
    name = _display(row.get(name_col), "") if name_col else ""
    tag = _display(row.get(tag_col), "")
    return " · ".join(part for part in (function_id, name, tag) if part)


def _show_fields(row: pd.Series, frame: pd.DataFrame, labels: tuple[str, ...]) -> None:
    for label in labels:
        value = _value(row, frame, label)
        if value != "Campo no incluido en el libro":
            st.markdown(f"**{label}**")
            st.write(value)


st.markdown(
    """
    Consulta la información registrada en el libro y navega desde la función
    hasta sus modos de falla, consecuencias, decisiones y actividades. Esta vista
    es de solo lectura: conserva el contenido del Excel, no completa vacíos y no
    recalcula resultados.
    """
)

with st.expander("Cambiar el libro para esta sesión"):
    uploaded_file = st.file_uploader(
        "Selecciona otra versión del libro RCM (.xlsx)",
        type=["xlsx"],
        max_upload_size=25,
        help=(
            "El libro debe contener las hojas Funciones, Análisis RCM y "
            "Calificación consecuencia. La selección no reemplaza el archivo fuente."
        ),
        key="rcm_workbook_upload",
    )

if uploaded_file is not None:
    workbook_bytes = uploaded_file.getvalue()
    source_name = uploaded_file.name
    source_description = "Archivo seleccionado para esta sesión"
elif DEFAULT_WORKBOOK.is_file():
    workbook_bytes = DEFAULT_WORKBOOK.read_bytes()
    source_name = DEFAULT_WORKBOOK.name
    source_description = "Libro de datos disponible en el módulo"
else:
    workbook_bytes = None
    source_name = ""
    source_description = "Sin libro cargado"

if workbook_bytes is None:
    st.info(
        "Selecciona el archivo Excel para iniciar. Al integrar el módulo, coloca "
        "el libro de trabajo en data/rcm/ o cárgalo para esta sesión."
    )
    st.stop()

try:
    workbook = _load_cached(workbook_bytes)
except RCMWorkbookError as exc:
    st.error(str(exc))
    st.stop()

functions = workbook["sheets"]["Funciones"].copy()
analysis = workbook["sheets"]["Análisis RCM"].copy()
consequences = workbook["sheets"]["Calificación consecuencia"].copy()

function_id_col = find_column(functions, "ID")
tag_col = find_column(functions, "ID ELEMENTO (TAG)")
function_name_col = find_column(functions, "ELEMENTO DE ESTUDIO", required=False)
function_text_col = find_column(functions, "FUNCIÓN", required=False)
analysis_function_id_col = find_column(analysis, "ID FUNCIÓN")
analysis_mode_col = find_column(analysis, "MODO DE FALLA")
analysis_consequence_col = find_column(analysis, "CONSECUENCIA", required=False)
consequence_function_id_col = find_column(consequences, "ID FUNCIÓN")
consequence_mode_col = find_column(consequences, "MODO DE FALLA")

for frame, column in (
    (functions, function_id_col),
    (analysis, analysis_function_id_col),
    (consequences, consequence_function_id_col),
):
    frame[column] = frame[column].astype("string").str.strip()
for frame, column in (
    (analysis, analysis_mode_col),
    (consequences, consequence_mode_col),
):
    frame[column] = frame[column].astype("string").str.strip()

functions = functions.loc[functions[function_id_col].map(is_filled)].copy()
analysis = analysis.loc[analysis[analysis_function_id_col].map(is_filled)].copy()
consequences = consequences.loc[
    consequences[consequence_function_id_col].map(is_filled)
].copy()
if functions.empty:
    st.error("La hoja Funciones no contiene registros con ID.")
    st.stop()

functions = functions.drop_duplicates(function_id_col, keep="first")
function_rows = functions.set_index(function_id_col, drop=False)

with st.container(border=True):
    source_left, source_right = st.columns([2, 1])
    with source_left:
        st.markdown("**Fuente activa**")
        st.write(source_name)
        st.caption(source_description)
    with source_right:
        st.caption("Consulta de solo lectura · el archivo fuente no se modifica")

tag_options = sorted(
    {str(value).strip() for value in functions[tag_col].tolist() if is_filled(value)}
)
function_type_col = find_column(functions, "TIPO DE FUNCIÓN", required=False)
function_types = (
    sorted(
        {
            _display(value)
            for value in functions[function_type_col].tolist()
        }
    )
    if function_type_col
    else []
)

with st.sidebar:
    st.subheader("Filtros del análisis")
    selected_tag = st.selectbox("Activo o TAG", ["Todos los TAG", *tag_options])
    selected_types = (
        st.multiselect("Tipo de función", function_types, default=function_types)
        if function_type_col
        else function_types
    )
    search_text = st.text_input(
        "Buscar función",
        placeholder="ID, activo, TAG o texto de función",
    ).strip()

filtered_functions = functions.copy()
if selected_tag != "Todos los TAG":
    filtered_functions = filtered_functions.loc[
        filtered_functions[tag_col].astype("string").str.strip() == selected_tag
    ]
if function_type_col:
    if selected_types:
        filtered_functions = filtered_functions.loc[
            filtered_functions[function_type_col]
            .map(lambda value: _display(value))
            .isin(selected_types)
        ]
    else:
        filtered_functions = filtered_functions.iloc[0:0]
if search_text:
    searchable_cols = [
        column
        for column in (function_id_col, function_name_col, tag_col, function_text_col)
        if column is not None
    ]
    searchable = filtered_functions[searchable_cols].fillna("").astype(str).agg(" ".join, axis=1)
    filtered_functions = filtered_functions.loc[
        searchable.str.contains(re.escape(search_text), case=False, regex=True)
    ]

filtered_ids = filtered_functions[function_id_col].astype(str).tolist()
if filtered_ids:
    with st.sidebar:
        st.caption(f"{_metric_number(len(filtered_ids))} funciones coinciden con los filtros.")
    current_choice = st.session_state.get("rcm_function_selector")
    if current_choice not in filtered_ids:
        st.session_state["rcm_function_selector"] = filtered_ids[0]
    selected_function_id = st.selectbox(
        "Función para revisar",
        options=filtered_ids,
        format_func=lambda value: _function_label(
            value, function_rows, function_name_col, tag_col
        ),
        key="rcm_function_selector",
    )
    selected_function = function_rows.loc[selected_function_id]
else:
    selected_function_id = None
    selected_function = None
    with st.sidebar:
        st.warning("No hay funciones que coincidan con los filtros.")

prefixes = workbook["tag_prefixes"]
prefixes_text = ", ".join(prefixes) if prefixes else "Sin prefijos TAG diligenciados"
scope_ids = set(filtered_ids)
analysis_scope = analysis.loc[
    analysis[analysis_function_id_col].astype(str).isin(scope_ids)
].copy()
consequence_scope = consequences.loc[
    consequences[consequence_function_id_col].astype(str).isin(scope_ids)
].copy()
activity_col = find_column(analysis, "actividad", required=False)
activity_count = (
    int(analysis_scope[activity_col].map(is_filled).sum())
    if activity_col and not analysis_scope.empty
    else 0
)

metrics = st.columns(4)
metrics[0].metric("Funciones en la vista", _metric_number(len(filtered_functions)))
metrics[1].metric("Registros de falla", _metric_number(len(analysis_scope)))
metrics[2].metric(
    "TAG distintos", _metric_number(filtered_functions[tag_col].nunique(dropna=True))
)
metrics[3].metric("Registros con actividad", _metric_number(activity_count))

tabs = st.tabs(
    ["Resumen", "Función", "Fallas y decisión", "Consecuencias", "Actividades", "Trazabilidad"]
)

with tabs[0]:
    st.subheader("Vista del conjunto filtrado")
    left, right = st.columns(2)
    if function_type_col and not filtered_functions.empty:
        type_summary = (
            filtered_functions[function_type_col]
            .map(lambda value: _display(value))
            .value_counts()
            .rename_axis("Tipo de función")
            .reset_index(name="Funciones")
        )
        with left:
            st.markdown("**Funciones por tipo**")
            st.bar_chart(type_summary, x="Tipo de función", y="Funciones")
    if analysis_consequence_col and not analysis_scope.empty:
        consequence_summary = (
            analysis_scope[analysis_consequence_col]
            .map(lambda value: _display(value))
            .value_counts()
            .rename_axis("Consecuencia registrada")
            .reset_index(name="Registros")
        )
        with right:
            st.markdown("**Consecuencia registrada en el libro**")
            st.bar_chart(
                consequence_summary,
                x="Consecuencia registrada",
                y="Registros",
            )

    table_columns = [
        column
        for column in (
            function_id_col,
            function_name_col,
            tag_col,
            function_text_col,
            find_column(functions, "ESTÁNDAR", required=False),
            find_column(functions, "UNIDAD", required=False),
            find_column(functions, "BASE DEL ESTÁNDAR", required=False),
        )
        if column is not None
    ]
    st.markdown("**Funciones encontradas**")
    st.dataframe(
        filtered_functions[table_columns],
        width="stretch",
        height=420,
        hide_index=True,
    )

with tabs[1]:
    if selected_function is None:
        st.info("Ajusta los filtros para seleccionar una función.")
    else:
        st.subheader(_value(selected_function, functions, "ELEMENTO DE ESTUDIO"))
        st.markdown(f"### {_value(selected_function, functions, 'FUNCIÓN')}")
        left, right = st.columns(2)
        with left:
            _show_fields(
                selected_function,
                functions,
                ("VERBO", "OBJETO", "ESTÁNDAR", "UNIDAD", "TIPO DE FUNCIÓN", "TIPO P/S", "VISIBILIDAD"),
            )
        with right:
            _show_fields(
                selected_function,
                functions,
                (
                    "ID ELEMENTO (TAG)",
                    "DENOMINACIÓN EN TAXONOMÍA",
                    "TAGS CUBIERTOS",
                    "N.º ELEMENTOS CUBIERTOS",
                    "CATEGORÍA RCM",
                    "MÉTODO DE VERIFICACIÓN",
                    "BASE DEL ESTÁNDAR",
                ),
            )
        st.markdown("#### Fuente, observación y definición")
        _show_fields(
            selected_function,
            functions,
            (
                "FUENTE",
                "OBSERVACIÓN",
                "DEFINICIÓN DEL ELEMENTO (punto de partida de la función)",
                "FUENTE DE LA DEFINICIÓN",
                "FUNCIÓN ANTERIOR (tu versión)",
            ),
        )
        with st.expander("Ver registro original de la función"):
            st.dataframe(
                functions.loc[functions[function_id_col] == selected_function_id],
                width="stretch",
                hide_index=True,
            )

with tabs[2]:
    if selected_function is None:
        st.info("Selecciona una función para revisar sus registros de falla.")
    else:
        selected_analysis = analysis_scope.loc[
            analysis_scope[analysis_function_id_col].astype(str) == str(selected_function_id)
        ].reset_index(drop=True)
        if selected_analysis.empty:
            st.info("No hay registros de análisis vinculados con esta función.")
        else:
            def failure_label(index: int) -> str:
                mode = selected_analysis.iloc[index].get(analysis_mode_col)
                return f"Registro {index + 1} · {_display(mode, 'Modo sin dato')}"

            failure_index = st.selectbox(
                "Registro de falla",
                options=list(range(len(selected_analysis))),
                format_func=failure_label,
                key=f"rcm_failure_{selected_function_id}",
            )
            selected_failure = selected_analysis.iloc[failure_index]
            st.subheader(_display(selected_failure.get(analysis_mode_col), "Modo de falla sin diligenciar"))
            _show_fields(
                selected_failure,
                selected_analysis,
                (
                    "FALLA FUNCIONAL",
                    "MODO DE FALLA",
                    "EFECTOS DE FALLA",
                    "FALLA POTENCIAL",
                    "CONSECUENCIA",
                    "CRITERIOS MÁS CRÍTICOS",
                ),
            )
            st.markdown("#### Preguntas del árbol de decisión")
            questions = decision_columns(selected_analysis)
            if questions:
                answers = pd.DataFrame(
                    {
                        "Pregunta": questions,
                        "Respuesta registrada": [
                            _display(selected_failure[column]) for column in questions
                        ],
                    }
                )
                st.dataframe(answers, width="stretch", hide_index=True)
            else:
                st.info("La hoja no contiene columnas identificables del árbol de decisión.")
            result_col = find_column(selected_analysis, "RESULTADO DEL ÁRBOL", required=False)
            maintenance_col = find_column(selected_analysis, "TIPO DE MANTENIMIENTO", required=False)
            if result_col or maintenance_col:
                result_left, result_right = st.columns(2)
                if result_col:
                    with result_left:
                        st.markdown("**Resultado del árbol registrado**")
                        st.write(_display(selected_failure[result_col]))
                if maintenance_col:
                    with result_right:
                        st.markdown("**Tipo de mantenimiento registrado**")
                        st.write(_display(selected_failure[maintenance_col]))

with tabs[3]:
    if selected_function is None:
        st.info("Selecciona una función para consultar sus consecuencias.")
    else:
        selected_analysis = analysis_scope.loc[
            analysis_scope[analysis_function_id_col].astype(str) == str(selected_function_id)
        ].reset_index(drop=True)
        if selected_analysis.empty:
            st.info("No hay registros de falla para consultar consecuencias.")
        else:
            def consequence_failure_label(index: int) -> str:
                mode = selected_analysis.iloc[index].get(analysis_mode_col)
                return f"Registro {index + 1} · {_display(mode, 'Modo sin dato')}"

            consequence_index = st.selectbox(
                "Registro de falla para consultar",
                options=list(range(len(selected_analysis))),
                format_func=consequence_failure_label,
                key=f"rcm_consequence_failure_{selected_function_id}",
            )
            consequence_failure = selected_analysis.iloc[consequence_index]
            selected_mode = consequence_failure.get(analysis_mode_col)
            mode_matches = (
                consequence_scope[consequence_mode_col].astype("string").str.strip()
                == str(selected_mode).strip()
            )
            matching_consequences = consequence_scope.loc[
                (consequence_scope[consequence_function_id_col].astype(str) == str(selected_function_id))
                & mode_matches
            ]
            st.caption(
                "Se presentan las calificaciones e índices tal como aparecen en el "
                "libro. Esta vista no recalcula pesos, puntajes ni categorías."
            )
            if matching_consequences.empty:
                st.info("No hay una calificación vinculada con este registro de falla.")
            else:
                st.dataframe(matching_consequences, width="stretch", hide_index=True)
            if workbook["consequence_weights"]:
                with st.expander("Pesos registrados en el libro"):
                    st.dataframe(
                        pd.DataFrame(
                            [
                                {"Criterio": name, "Peso registrado": value}
                                for name, value in workbook["consequence_weights"].items()
                            ]
                        ),
                        width="stretch",
                        hide_index=True,
                    )

with tabs[4]:
    if selected_function is None:
        st.info("Selecciona una función para revisar las actividades existentes.")
    else:
        selected_analysis = analysis_scope.loc[
            analysis_scope[analysis_function_id_col].astype(str) == str(selected_function_id)
        ].reset_index(drop=True)
        activity_col = find_column(selected_analysis, "actividad", required=False)
        frequency_col = find_column(selected_analysis, "frecuencia (meses)", required=False)
        responsible_col = find_column(selected_analysis, "RESPONSABLE", required=False)
        activity_columns = [
            column
            for column in (activity_col, frequency_col, responsible_col)
            if column is not None
        ]
        if selected_analysis.empty:
            st.info("No hay registros de falla asociados con esta función.")
        elif not activity_columns:
            st.info("La hoja no contiene columnas de actividad, frecuencia o responsable.")
        else:
            available_metrics = [
                (label, column)
                for label, column in (
                    ("Actividad", activity_col),
                    ("Frecuencia", frequency_col),
                    ("Responsable", responsible_col),
                )
                if column
            ]
            activity_metrics = st.columns(len(available_metrics))
            for container, label, column in zip(
                activity_metrics,
                [label for label, _ in available_metrics],
                [column for _, column in available_metrics],
            ):
                if column:
                    container.metric(
                        f"Registros con {label.lower()}",
                        _metric_number(int(selected_analysis[column].map(is_filled).sum())),
                    )
            populated_rows = selected_analysis.loc[
                selected_analysis[activity_columns].apply(
                    lambda row: any(is_filled(value) for value in row.values), axis=1
                )
            ]
            if populated_rows.empty:
                st.info(
                    "No hay actividad, frecuencia ni responsable diligenciados para "
                    "esta función. Los campos permanecen pendientes en el libro."
                )
            else:
                mode_col = find_column(selected_analysis, "MODO DE FALLA", required=False)
                display_columns = [
                    column for column in (mode_col, *activity_columns) if column
                ]
                st.dataframe(
                    populated_rows[display_columns],
                    width="stretch",
                    hide_index=True,
                )
            st.caption(
                "La existencia de algunos valores no implica que el plan de "
                "mantenimiento esté completo o aprobado."
            )

with tabs[5]:
    st.subheader("Completitud y trazabilidad del libro")
    st.caption(
        "Los conteos reflejan celdas diligenciadas en el archivo original; no son "
        "un juicio de aprobación técnica."
    )
    questions = decision_columns(analysis)
    question_1c = next(
        (
            column
            for column in questions
            if normalize_label(column).startswith("1c ")
        ),
        None,
    )
    answer_1c_count = (
        int(analysis[question_1c].map(is_filled).sum())
        if question_1c is not None
        else None
    )
    quality_rows = [
        {"Campo": "FUENTE en Funciones", "Celdas con dato": _count_filled(functions, "FUENTE"), "Total de filas": len(functions)},
        {"Campo": "UNIDAD en Funciones", "Celdas con dato": _count_filled(functions, "UNIDAD"), "Total de filas": len(functions)},
        {"Campo": "actividad en Análisis RCM", "Celdas con dato": _count_filled(analysis, "actividad"), "Total de filas": len(analysis)},
        {"Campo": "frecuencia (meses)", "Celdas con dato": _count_filled(analysis, "frecuencia (meses)"), "Total de filas": len(analysis)},
        {"Campo": "RESPONSABLE", "Celdas con dato": _count_filled(analysis, "RESPONSABLE"), "Total de filas": len(analysis)},
    ]
    if answer_1c_count is not None:
        quality_rows.append(
            {"Campo": "Pregunta 1C", "Celdas con dato": answer_1c_count, "Total de filas": len(analysis)}
        )
    st.dataframe(pd.DataFrame(quality_rows), width="stretch", hide_index=True)
    if question_1c is not None and answer_1c_count == 0:
        st.warning(
            "La columna 1C existe y está vacía en todos los registros. Se mantiene "
            "vacía; no se interpreta como No ni como No aplica."
        )

    with st.expander("Bases del estándar, fuentes y observaciones"):
        basis_col = find_column(functions, "BASE DEL ESTÁNDAR", required=False)
        if basis_col:
            basis_summary = (
                functions[basis_col]
                .map(lambda value: _display(value))
                .value_counts()
                .rename_axis("Base del estándar")
                .reset_index(name="Funciones")
            )
            st.dataframe(basis_summary, width="stretch", hide_index=True)
        source_columns = [
            column
            for column in (
                function_id_col,
                function_name_col,
                tag_col,
                find_column(functions, "FUENTE", required=False),
                find_column(functions, "OBSERVACIÓN", required=False),
            )
            if column is not None
        ]
        st.dataframe(
            functions[source_columns],
            width="stretch",
            height=360,
            hide_index=True,
        )
    st.markdown("**Identidad del conjunto**")
    st.write(f"Prefijos TAG encontrados: {prefixes_text}.")
    st.write(f"Libro utilizado: {source_name}.")
    st.caption(
        "El rótulo de una base o fuente se conserva tal como aparece; no demuestra "
        "por sí solo que su soporte técnico esté adjunto o aprobado."
    )

