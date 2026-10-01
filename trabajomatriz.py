import streamlit as st

# --- Configuración de página: ancho completo, necesario para que el layout
#     de la app (máx. 1180px centrado) no se vea comprimido ---
st.set_page_config(page_title="Matriz de Criticidad — SITVA", layout="wide")

# --- Cargar el HTML autocontenido (colócalo en la misma carpeta que este script) ---
with open("matriz_criticidad_sitva.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# --- Incrustar la app completa (sliders, mapa de calor, tabla editable, todo) ---
st.components.v1.html(html_code, height=2600, scrolling=True)
