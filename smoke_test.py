# -*- coding: utf-8 -*-
"""Validación estática y de recursos para la entrega METRO_RCM."""
from pathlib import Path
import ast
import json
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
ERRORS = []


def check(condition, message):
    if condition:
        print(f"[OK] {message}")
    else:
        print(f"[FAIL] {message}")
        ERRORS.append(message)


# Python
for path in ROOT.rglob("*.py"):
    if ".venv" in path.parts or "__pycache__" in path.parts:
        continue
    try:
        ast.parse(path.read_text(encoding="utf-8"))
    except Exception as exc:
        ERRORS.append(f"Sintaxis: {path}: {exc}")
check(not ERRORS, "Sintaxis Python")

# JSON
for path in (ROOT / "data").glob("*.json"):
    try:
        json.loads(path.read_text(encoding="utf-8"))
        print(f"[OK] JSON {path.relative_to(ROOT)}")
    except Exception as exc:
        ERRORS.append(f"JSON {path}: {exc}")

# Navegación declarada en utils/theme.py
text = (ROOT / "utils" / "theme.py").read_text(encoding="utf-8")
nav = re.findall(r'\("([^"]+\.py)",\s*"([^"]+)"', text)
check(len(nav) == 11, "Navegación: Inicio + 10 módulos")
for route, label in nav:
    check((ROOT / route).exists(), f"Ruta de navegación: {label}")

# Recursos críticos
critical = [
    "app.py",
    "utils/theme.py",
    "utils/reportes.py",
    "matriz_criticidad_sitva.html",
    "assets/encuesta_ponderacion.html",
    "backend_google_apps_script.js",
    ".streamlit/config.toml",
    "assets/ui/hero_city_train.jpg",
    "assets/ui/udea_crest_white.png",
]
for rel in critical:
    check((ROOT / rel).exists(), f"Recurso crítico: {rel}")

# Equipo: no debe fallar aunque algunos perfiles históricos no tengan foto/CV.
team = json.loads((ROOT / "data/equipo_rcm.json").read_text(encoding="utf-8"))
missing = []
for member in team.get("miembros", []):
    for field in ("foto", "hoja_de_vida"):
        value = member.get(field, "")
        if not value:
            continue
        name = Path(value).name
        sub = "fotos" if field == "foto" else "documentos"
        candidates = [ROOT / "assets/equipo_rcm" / sub / name]
        fallback = "Fotos" if field == "foto" else "Documentos"
        candidates.append(ROOT / "assets" / fallback / name)
        if not any(p.exists() for p in candidates):
            missing.append(f"{member.get('nombre')} -> {field}")
# Missing media is non-fatal because the UI explicitly provides a fallback state.
print(f"[INFO] Recursos de perfiles no disponibles: {len(missing)} (la interfaz usa fallback)")

# PDF generator
try:
    sys.path.insert(0, str(ROOT))
    from utils.reportes import generar_informe_pdf
    pdf = generar_informe_pdf("QA", "METRO_RCM", [{"titulo": "Prueba", "datos": [["Estado", "OK"]]}])
    check(pdf[:5] == b"%PDF-", "Generación de informe PDF")
except Exception as exc:
    ERRORS.append(f"PDF: {exc}")

# JavaScript syntax when Node is available.
node = shutil.which("node")
if node:
    result = subprocess.run([node, "--check", str(ROOT / "backend_google_apps_script.js")], capture_output=True, text=True)
    check(result.returncode == 0, "Sintaxis backend Google Apps Script")
else:
    print("[INFO] Node.js no está instalado; se omite prueba JS.")

# Matrix bridge and criterion order must match the central survey.
matrix = (ROOT / "matriz_criticidad_sitva.html").read_text(encoding="utf-8")
check("let weights = [...DEFAULT_WEIGHTS];" in matrix, "Puente de pesos de la matriz")
check("__VOTACION_ENDPOINT__" in matrix, "Matriz: marcador de endpoint central")
check('key:"seguridad", name:"Seguridad de las personas", weight:0.30' in matrix, "Criterio 1: Seguridad")
check('key:"cobertura", name:"Impacto a la operación", weight:0.25' in matrix, "Criterio 2: Impacto a la operación")
check('key:"continuidad", name:"Continuidad operacional", weight:0.20' in matrix, "Criterio 3: Continuidad")
check('key:"costo", name:"Costo de reparación", weight:0.15' in matrix, "Criterio 4: Costo")
check('key:"impacto", name:"Impacto ambiental", weight:0.10' in matrix, "Criterio 5: Ambiental")

# Survey HTML: local, centralized and dependency-free in the browser.
survey = (ROOT / "assets" / "encuesta_ponderacion.html").read_text(encoding="utf-8")
check("__VOTACION_ENDPOINT__" in survey, "Encuesta: marcador de endpoint central")
check("fonts.googleapis.com" not in survey and "cdn.jsdelivr.net" not in survey, "Encuesta: sin dependencias externas de UI")
check("setInterval(cargarDatosRemotos,5000)" in survey, "Encuesta: sincronización cada 5 s")
page = (ROOT / "pages" / "07_Criticidad_Integrado.py").read_text(encoding="utf-8")
check("AKfycbx7WSRa1-uPUl2ThljERCQPV996Rnl5Uim8AHQ_PJlXcRDBO4DOjia4TuRcFB1BIxr7vQ" in page, "Endpoint central: despliegue vigente")

# Validate embedded JavaScript when Node is available.
if node:
    import tempfile
    html_js = re.search(r"<script>(.*?)</script>", matrix, flags=re.S)
    survey_js = re.search(r"<script>(.*?)</script>", survey, flags=re.S)
    for label, match in (("Matriz", html_js), ("Encuesta", survey_js)):
        if match:
            with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as tmp:
                tmp.write(match.group(1))
                tmp_path = tmp.name
            result = subprocess.run([node, "--check", tmp_path], capture_output=True, text=True)
            check(result.returncode == 0, f"Sintaxis JavaScript: {label}")

print("\nRESULTADO:", "OK" if not ERRORS else f"{len(ERRORS)} error(es)")
if ERRORS:
    for err in ERRORS:
        print(" -", err)
    raise SystemExit(1)
