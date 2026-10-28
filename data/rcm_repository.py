"""Lectura y validación de libros de trabajo RCM."""

from __future__ import annotations

from io import BytesIO
import re
import unicodedata
from typing import Any

import pandas as pd


REQUIRED_SHEETS = (
    "Funciones",
    "Análisis RCM",
    "Calificación consecuencia",
)

REQUIRED_COLUMNS = {
    "Funciones": ("ID", "ID ELEMENTO (TAG)", "FUNCIÓN", "ESTÁNDAR"),
    "Análisis RCM": (
        "ID FUNCIÓN",
        "FALLA FUNCIONAL",
        "MODO DE FALLA",
        "RESULTADO DEL ÁRBOL",
        "TIPO DE MANTENIMIENTO",
    ),
    "Calificación consecuencia": ("ID FUNCIÓN", "MODO DE FALLA"),
}


class RCMWorkbookError(ValueError):
    """Error de estructura o lectura del libro RCM."""


def normalize_label(value: Any) -> str:
    """Normaliza acentos, saltos de línea y espacios para comparar encabezados."""
    text = unicodedata.normalize("NFKD", str(value))
    text = "".join(char for char in text if not unicodedata.combining(char))
    return " ".join(text.replace("\u00a0", " ").casefold().split())


def find_column(
    frame: pd.DataFrame,
    expected: str,
    *,
    required: bool = True,
) -> str | None:
    """Devuelve el encabezado real que corresponde al nombre esperado."""
    wanted = normalize_label(expected)
    for column in frame.columns:
        if normalize_label(column) == wanted:
            return str(column)
    if required:
        raise RCMWorkbookError(
            f"No se encontró la columna requerida «{expected}»."
        )
    return None


def is_filled(value: Any) -> bool:
    """Indica si una celda tiene un valor visible, sin tratar cero como vacío."""
    if value is None:
        return False
    try:
        if pd.isna(value):
            return False
    except (TypeError, ValueError):
        pass
    return bool(str(value).strip())


def _clean_frame(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    frame.columns = [
        str(column).replace("\n", " ").replace("\r", " ").strip()
        for column in frame.columns
    ]
    # Keep named columns even when every response is blank. In this workbook,
    # 1C is a meaningful decision question whose answers are all pending.
    # Drop only fully empty placeholder columns created by formatted Excel ranges.
    empty_placeholders = [
        column
        for column in frame.columns
        if frame[column].isna().all()
        and (not normalize_label(column) or normalize_label(column).startswith("unnamed:"))
    ]
    if empty_placeholders:
        frame = frame.drop(columns=empty_placeholders)
    frame = frame.dropna(axis=0, how="all")
    return frame.reset_index(drop=True)


def _find_sheet(sheet_names: list[str], expected: str) -> str:
    wanted = normalize_label(expected)
    for name in sheet_names:
        if normalize_label(name) == wanted:
            return name
    raise RCMWorkbookError(
        f"Falta la hoja «{expected}». Hojas encontradas: "
        + ", ".join(sheet_names)
    )


def _validate_columns(name: str, frame: pd.DataFrame) -> None:
    missing = []
    for expected in REQUIRED_COLUMNS[name]:
        if find_column(frame, expected, required=False) is None:
            missing.append(expected)
    if missing:
        raise RCMWorkbookError(
            f"La hoja «{name}» no contiene las columnas requeridas: "
            + ", ".join(missing)
        )


def load_rcm_workbook(file_bytes: bytes) -> dict[str, Any]:
    """Lee las tres hojas RCM y conserva sus valores sin escribir el archivo."""
    if not file_bytes:
        raise RCMWorkbookError("El archivo está vacío.")

    try:
        book = pd.ExcelFile(BytesIO(file_bytes), engine="openpyxl")
    except Exception as exc:  # El mensaje se convierte en orientación para el usuario.
        raise RCMWorkbookError(
            "No se pudo abrir el archivo como libro Excel .xlsx."
        ) from exc

    source_sheets = {
        expected: _find_sheet(book.sheet_names, expected)
        for expected in REQUIRED_SHEETS
    }
    frames: dict[str, pd.DataFrame] = {}

    try:
        for expected, source_name in source_sheets.items():
            header_row = 1 if expected == "Calificación consecuencia" else 0
            frame = pd.read_excel(
                BytesIO(file_bytes),
                sheet_name=source_name,
                header=header_row,
                engine="openpyxl",
            )
            frames[expected] = _clean_frame(frame)
    except Exception as exc:
        raise RCMWorkbookError(
            "No se pudieron leer las hojas requeridas del libro."
        ) from exc

    for expected, frame in frames.items():
        _validate_columns(expected, frame)

    weight_row = pd.read_excel(
        BytesIO(file_bytes),
        sheet_name=source_sheets["Calificación consecuencia"],
        header=None,
        nrows=1,
        engine="openpyxl",
    )
    consequence = frames["Calificación consecuencia"]
    weights: dict[str, Any] = {}
    if not weight_row.empty:
        for index, column in enumerate(consequence.columns[2:7], start=2):
            if index < weight_row.shape[1]:
                weights[str(column)] = weight_row.iloc[0, index]

    functions = frames["Funciones"]
    analysis = frames["Análisis RCM"]
    function_id = find_column(functions, "ID")
    tag = find_column(functions, "ID ELEMENTO (TAG)")
    analysis_function_id = find_column(analysis, "ID FUNCIÓN")

    functions = functions.loc[functions[function_id].map(is_filled)].copy()
    analysis = analysis.loc[analysis[analysis_function_id].map(is_filled)].copy()
    frames["Funciones"] = functions.reset_index(drop=True)
    frames["Análisis RCM"] = analysis.reset_index(drop=True)
    frames["Calificación consecuencia"] = consequence.reset_index(drop=True)

    tag_prefixes = sorted(
        {
            str(value).strip().split("-")[0]
            for value in functions[tag].map(lambda item: item if is_filled(item) else None).dropna()
        }
    )

    return {
        "sheets": frames,
        "source_sheets": source_sheets,
        "consequence_weights": weights,
        "tag_prefixes": tag_prefixes,
    }


def decision_columns(frame: pd.DataFrame) -> list[str]:
    """Identifica preguntas 1A–6C sin alterar sus encabezados originales."""
    pattern = re.compile(r"^\s*[1-6][a-c]\b")
    return [
        str(column)
        for column in frame.columns
        if pattern.match(normalize_label(column))
    ]
