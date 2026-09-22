from pathlib import Path

p = Path("app.py")
s = p.read_text(encoding="utf-8-sig")

inicio = s.find("# Tres filas de tres tarjetas")
fin = s.find("# PIE", inicio)

if inicio == -1:
    raise RuntimeError("No se encontró el inicio del bloque de tarjetas.")

if fin == -1:
    raise RuntimeError("No se encontró el final del bloque de tarjetas.")

bloque = r'''
# ============================================================
# NAVEGACIÓN DEL PROYECTO
# ============================================================

ICONOS_PORTADA = {
    "pages/01_Contexto_del_Negocio.py": "🏢",
    "pages/02_Contexto_Operacional.py": "🚇",
    "pages/03_Activos.py": "📦",
    "pages/04_Mantenimiento.py": "🔧",
    "pages/05_Indicadores.py": "📊",
    "pages/07_Criticidad_Integrado.py": "🎯",
    "pages/07_RCM.py": "🔄",
    "pages/08_Equipo_RCM_Integrado.py": "👥",
    "pages/09_Monitoreo_Ambiental.py": "📡",
    "pages/10_Obsolescencia_Activos.py": "♻️",
}

# Tres columnas por fila. La última fila puede contener menos de tres tarjetas.
for inicio in range(0, len(cards), 3):
    fila = cards[inicio:inicio + 3]
    cols = st.columns(3, gap="medium")

    for idx, card in enumerate(fila):
        with cols[idx]:
            with st.container(border=True):
                st.markdown(
                    '<div class="metro-nav-card">'
                    f'<div class="icon">{ICONOS_PORTADA.get(card.get("ruta"), "•")}</div>'
                    f'<h3>{card["titulo"]}</h3>'
                    f'<p>{card["descripcion"]}</p>'
                    '</div>',
                    unsafe_allow_html=True,
                )

                if st.button(
                    "Abrir módulo →",
                    key=card["button"],
                    width="stretch",
                ):
                    st.switch_page(card["ruta"])

                if st.button(
                    "Generar informe",
                    key=card["report_key"],
                    width="stretch",
                ):
                    generar_informe(
                        card["report_title"],
                        card["report_subtitle"],
                        card["sections"],
                        card["report_file"],
                    )

'''

s = s[:inicio] + bloque + s[fin:]

p.write_text(s, encoding="utf-8")
print("BLOQUE DE PORTADA REPARADO CORRECTAMENTE.")
