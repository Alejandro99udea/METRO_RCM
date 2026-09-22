import base64
import pandas as pd
import streamlit as st
import json
import os
import io
from pathlib import Path

# --- 1. CONFIGURACIÓN DE PÁGINA ---

BASE_DIR = Path(__file__).resolve().parents[1]
ARCHIVO_DATOS = BASE_DIR / "data" / "activos_obsolescencia.json"
URL_LOGO_UDEA = "https://th.bing.com/th/id/R.c5ba91156246b1773bb2e50750bca7aa?rik=zeczkjrO5Hwfcg&riu=http%3a%2f%2f1.bp.blogspot.com%2f-i-a8Vk0uKKQ%2fUaRlpJICDuI%2fAAAAAAAABh0%2fj0sTjvOv-9k%2fs1600%2flogotipo%2budea.png&ehk=fVM6Blb6HOp%2fNG8SyeWNxwQQZ6BPrPgZmAA9pjGeAFM%3d&risl=&pid=ImgRaw&r=0"
URL_LOGO_METRO = "https://conconcreto.com/wp-content/uploads/2023/01/1200px-Logo_Metro_de_Medellin.svg.png"

# --- 2. MANEJO DEL ESTADO ---
if "vista_actual" not in st.session_state:
    st.session_state.vista_actual = "Inicio"
if "activo_a_editar" not in st.session_state:
    st.session_state.activo_a_editar = None

def cambiar_vista(nueva_vista, activo_edit=None):
    st.session_state.vista_actual = nueva_vista
    st.session_state.activo_a_editar = activo_edit

# --- 3. IMAGEN DE FONDO Y ESTILOS ---
@st.cache_data
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f: return base64.b64encode(f.read()).decode()
    except FileNotFoundError: return ""

# Si tienes la imagen en la misma carpeta, funcionará. Si no, quedará con fondo blanco.
img_base64 = get_base64_of_bin_file(str(BASE_DIR / "assets" / "obsolescencia" / "image_870424.jpg"))

estilos_generales = """
<style>
    h1, h2, h3, h4 { color: #0B5E2C !important; font-family: Arial, sans-serif; }
    p, li, span { color: #222222 !important; font-family: Arial, sans-serif; }
    [data-testid="stMetricValue"] { color: #0B5E2C !important; font-size: 28px !important; font-weight: bold !important; }
    
    button[kind="primary"] { 
        background-color: #0B5E2C !important; 
        border-radius: 12px !important; 
        min-height: 120px !important; 
        border: 2px solid #073b1b !important;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }
    button[kind="primary"] p {
        color: #FFFFFF !important; 
        font-weight: bold !important; 
        font-size: 22px !important; 
    }
    button[kind="primary"]:hover { 
        background-color: #073b1b !important; 
        transform: scale(1.02); 
        transition: 0.3s;
    }
    
    button[kind="secondary"], .stDownloadButton button { 
        background-color: #FFFFFF !important; 
        border: 2px solid #0B5E2C !important; 
        border-radius: 8px !important; 
        min-height: 60px !important; 
        width: 100% !important;
    }
    button[kind="secondary"] p, .stDownloadButton button p { 
        color: #0B5E2C !important; 
        font-weight: bold !important; 
        font-size: 18px !important; 
    }
    button[kind="secondary"]:hover, .stDownloadButton button:hover { 
        background-color: #0B5E2C !important; 
    }
    button[kind="secondary"]:hover p, .stDownloadButton button:hover p { 
        color: #FFFFFF !important; 
    }

    .caja-info { background-color: #F4F8F5; border-left: 5px solid #0B5E2C; padding: 18px 22px; border-radius: 4px; margin-bottom: 20px; font-size: 16px; line-height: 1.5; }
</style>
"""
st.markdown(estilos_generales, unsafe_allow_html=True)

if st.session_state.vista_actual == "Inicio" and img_base64:
    st.markdown(f"""<style>.stApp {{ background: linear-gradient(rgba(255, 255, 255, 0.88), rgba(255, 255, 255, 0.88)), url("data:image/jpeg;base64,{img_base64}"); background-size: cover; background-position: center; background-attachment: fixed; }}</style>""", unsafe_allow_html=True)
else:
    st.markdown("""<style>.stApp { background-color: #FFFFFF !important; }</style>""", unsafe_allow_html=True)

# --- 4. GESTIÓN DE DATOS DINÁMICA ---
def recalcular_prioridades(datos_dict):
    lista_puntajes = []
    for nombre, info in datos_dict.items():
        puntaje_total = 0
        for eval_item in info.get("Evaluacion", []):
            try:
                val = int(eval_item["Puntaje"].split(" ")[0])
                puntaje_total += val
            except:
                pass
        lista_puntajes.append({'nombre': nombre, 'puntaje': puntaje_total})
        
    lista_puntajes.sort(key=lambda x: (x['puntaje'], x['nombre']))
    
    for i, item in enumerate(lista_puntajes):
        datos_dict[item['nombre']]["Prioridad"] = f"PRIORIDAD {i + 1}"
        
    return datos_dict

datos_por_defecto = {
    "Buses GNV (Metroplús)": {
        "Generación": "3ª Gen (22/40)", "TCT": "0 a 1 año",
        "Estrategia": "Renovación a flota 100% Eléctrica.",
        "Contexto": "Operación intensa con paradas frecuentes. La flota a GNV requiere overhaul al alcanzar los 500.000 km.",
        "Justificacion": "Flota de 31 buses articulados y 59 padrones. Apremiante cambio tecnológico por obsolescencia ambiental y mecánica.",
        "Evaluacion": [{"Factor Evaluado": "Integración de software / Datos", "Puntaje": "3 / 5", "Justificación Técnica / Contexto": "Telemetría en buses GNV; BMS en eléctricos."}, {"Factor Evaluado": "Ergonomía y mantenibilidad", "Puntaje": "3 / 5", "Justificación Técnica / Contexto": "Homologación de repuestos."}, {"Factor Evaluado": "Automatización", "Puntaje": "1 / 5", "Justificación Técnica / Contexto": "Operación manual."}, {"Factor Evaluado": "Independencia del hombre", "Puntaje": "1 / 5", "Justificación Técnica / Contexto": "Dependiente del operador."}, {"Factor Evaluado": "Optimización de espacio", "Puntaje": "3 / 5", "Justificación Técnica / Contexto": "Uso de carriles BRT."}, {"Factor Evaluado": "Capacidad y Eficiencia", "Puntaje": "4 / 5", "Justificación Técnica / Contexto": "Alta capacidad."}, {"Factor Evaluado": "Cuidados medioambientales", "Puntaje": "3 / 5", "Justificación Técnica / Contexto": "Transición de Euro V."}, {"Factor Evaluado": "Cumplimiento normativo", "Puntaje": "4 / 5", "Justificación Técnica / Contexto": "Normativas ISO."}]
    },
    "Metrocables (Líneas K, J, L, H, M, P)": {
        "Generación": "3ª Gen (28/40)", "TCT": "1 a 3 años",
        "Estrategia": "Modernización de sistemas de control y sensores.",
        "Contexto": "Alta utilización en laderas urbanas (~65.000 usuarios/día).",
        "Justificacion": "Necesidad de migrar sistemas antiguos hacia tecnologías automatizadas en pinzas y rodamientos.",
        "Evaluacion": [{"Factor Evaluado": "Integración de software / Datos", "Puntaje": "3 / 5", "Justificación Técnica / Contexto": "Líneas antiguas requieren actualización."}, {"Factor Evaluado": "Ergonomía y mantenibilidad", "Puntaje": "3 / 5", "Justificación Técnica / Contexto": "Trabajo en altura."}, {"Factor Evaluado": "Automatización", "Puntaje": "3 / 5", "Justificación Técnica / Contexto": "Bucle continuo automatizado."}, {"Factor Evaluado": "Independencia del hombre", "Puntaje": "2 / 5", "Justificación Técnica / Contexto": "Requiere personal para embarque."}, {"Factor Evaluado": "Optimización de espacio", "Puntaje": "5 / 5", "Justificación Técnica / Contexto": "Excelente huella urbana."}, {"Factor Evaluado": "Capacidad y Eficiencia", "Puntaje": "3 / 5", "Justificación Técnica / Contexto": "Flujo continuo."}, {"Factor Evaluado": "Cuidados medioambientales", "Puntaje": "5 / 5", "Justificación Técnica / Contexto": "Operación eléctrica."}, {"Factor Evaluado": "Cumplimiento normativo", "Puntaje": "4 / 5", "Justificación Técnica / Contexto": "Regulación internacional de cables."}]
    },
    "Trenes (Líneas A, B)": {
        "Generación": "3ª Gen (29/40)", "TCT": "3 a 5 años", 
        "Estrategia": "Actualización de señalización a CBTC.",
        "Contexto": "Núcleo del transporte con más de 310 millones de viajes en la red.",
        "Justificacion": "Flotas con más de 30 años requieren modernización de tracción y control por aumento de modos de falla.",
        "Evaluacion": [{"Factor Evaluado": "Integración de software / Datos", "Puntaje": "3 / 5", "Justificación Técnica / Contexto": "Monitoreo RCM activo."}, {"Factor Evaluado": "Ergonomía y mantenibilidad", "Puntaje": "4 / 5", "Justificación Técnica / Contexto": "Talleres en Bello."}, {"Factor Evaluado": "Automatización", "Puntaje": "3 / 5", "Justificación Técnica / Contexto": "Operación semi-automatizada (GoA2)."}, {"Factor Evaluado": "Independencia del hombre", "Puntaje": "2 / 5", "Justificación Técnica / Contexto": "Dependencia del conductor."}, {"Factor Evaluado": "Optimización de espacio", "Puntaje": "3 / 5", "Justificación Técnica / Contexto": "Infraestructura ferroviaria."}, {"Factor Evaluado": "Capacidad y Eficiencia", "Puntaje": "5 / 5", "Justificación Técnica / Contexto": "Máxima capacidad."}, {"Factor Evaluado": "Cuidados medioambientales", "Puntaje": "5 / 5", "Justificación Técnica / Contexto": "100% eléctrico."}, {"Factor Evaluado": "Cumplimiento normativo", "Puntaje": "4 / 5", "Justificación Técnica / Contexto": "Alto cumplimiento normativo."}]
    },
    "Tranvía de Ayacucho": {
        "Generación": "3ª Gen (28/40)", "TCT": "3 a 5 años", 
        "Estrategia": "Homologación local de repuestos e ingeniería inversa.",
        "Contexto": "Alta efectividad con 9,8 millones de viajes esperados.",
        "Justificacion": "Tecnología propietaria (Translohr). Riesgo principal por obsolescencia de proveedor único.",
        "Evaluacion": [{"Factor Evaluado": "Integración de software / Datos", "Puntaje": "3 / 5", "Justificación Técnica / Contexto": "Diagnóstico a bordo."}, {"Factor Evaluado": "Ergonomía y mantenibilidad", "Puntaje": "4 / 5", "Justificación Técnica / Contexto": "Accesibilidad nivelada."}, {"Factor Evaluado": "Automatización", "Puntaje": "2 / 5", "Justificación Técnica / Contexto": "Conducción manual en vía urbana."}, {"Factor Evaluado": "Independencia del hombre", "Puntaje": "2 / 5", "Justificación Técnica / Contexto": "Dependiente del control de tráfico."}, {"Factor Evaluado": "Optimización de espacio", "Puntaje": "4 / 5", "Justificación Técnica / Contexto": "Plataforma compacta."}, {"Factor Evaluado": "Capacidad y Eficiencia", "Puntaje": "4 / 5", "Justificación Técnica / Contexto": "3.807 pax/h/sentido."}, {"Factor Evaluado": "Cuidados medioambientales", "Puntaje": "5 / 5", "Justificación Técnica / Contexto": "Cero emisiones directas."}, {"Factor Evaluado": "Cumplimiento normativo", "Puntaje": "4 / 5", "Justificación Técnica / Contexto": "Regulado por el código de tránsito."}]
    }
}

def guardar_datos(datos_nuevos):
    datos_ordenados = recalcular_prioridades(datos_nuevos)
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos_ordenados, f, ensure_ascii=False, indent=4)
    return datos_ordenados

def cargar_datos():
    if not os.path.exists(ARCHIVO_DATOS):
        datos_base = recalcular_prioridades(datos_por_defecto.copy())
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
            json.dump(datos_base, f, ensure_ascii=False, indent=4)
        return datos_base
    
    with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
        datos_guardados = json.load(f)
    
    cambios = False
    for key, val in datos_por_defecto.items():
        if key not in datos_guardados:
            datos_guardados[key] = val
            cambios = True
    
    if cambios:
        datos_guardados = guardar_datos(datos_guardados)
    else:
        datos_guardados = recalcular_prioridades(datos_guardados)
    
    return datos_guardados

# --- FUNCIÓN PARA EXPORTAR A EXCEL ---
def generar_excel(datos_dict):
    filas = []
    for nombre, info in datos_dict.items():
        fila = {
            "Sistema / Activo": nombre,
            "Orden de Reemplazo": info.get("Prioridad", ""),
            "Generación Tecnológica": info.get("Generación", ""),
            "Vida Útil Remanente": info.get("TCT", ""),
            "Estrategia de Intervención": info.get("Estrategia", ""),
            "Contexto Operacional": info.get("Contexto", ""),
            "Justificación Técnica": info.get("Justificacion", "")
        }
        for eval_item in info.get("Evaluacion", []):
            factor = eval_item.get("Factor Evaluado", "")
            fila[f"Puntaje: {factor}"] = eval_item.get("Puntaje", "")
            fila[f"Detalle: {factor}"] = eval_item.get("Justificación Técnica / Contexto", "")
            
        filas.append(fila)
        
    df = pd.DataFrame(filas)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Base_Activos')
    
    return output.getvalue()

datos = cargar_datos()

def mostrar_encabezado():
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #0B5E2C; padding-bottom: 10px; margin-bottom: 20px;">
        <img src="{URL_LOGO_UDEA}" style="height: 50px; width: auto;">
        <span style="font-weight: bold; color: #0B5E2C; font-size: 18px;">Gestión de Obsolescencia — Convenio UdeA & Metro de Medellín</span>
        <img src="{URL_LOGO_METRO}" style="height: 50px; width: auto;">
    </div>
    """, unsafe_allow_html=True)

# --- VISTA: INICIO ---
if st.session_state.vista_actual == "Inicio":
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
        <img src="{URL_LOGO_UDEA}" style="height: 110px;">
        <div style="text-align: center;">
            <h1 style="margin: 0; font-size: 34px; color: #0B5E2C !important;">UNIVERSIDAD DE ANTIOQUIA</h1>
            <h3 style="margin: 8px 0 0 0; color: #555555 !important; font-size: 22px;">Gestión de Obsolescencia - Metro de Medellín</h3>
        </div>
        <img src="{URL_LOGO_METRO}" style="height: 100px;">
    </div>
    """, unsafe_allow_html=True)
    
    activos_lista = list(datos.keys())
    for i in range(0, len(activos_lista), 2):
        col1, col2 = st.columns(2)
        with col1:
            if st.button(activos_lista[i], type="primary", use_container_width=True):
                cambiar_vista(activos_lista[i])
                st.rerun()
        with col2:
            if i + 1 < len(activos_lista):
                if st.button(activos_lista[i+1], type="primary", use_container_width=True):
                    cambiar_vista(activos_lista[i+1])
                    st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("¿Cómo se hizo? - Metodología", type="secondary", use_container_width=True):
            cambiar_vista("Metodologia")
            st.rerun()
    with c2:
        if st.button("Síntesis y Recomendaciones", type="secondary", use_container_width=True):
            cambiar_vista("Recomendaciones")
            st.rerun()
    with c3:
        if st.button("➕ Agregar Activo", type="secondary", use_container_width=True):
            cambiar_vista("Formulario")
            st.rerun()
    with c4:
        st.download_button(
            label="📥 Exportar Base de Datos",
            data=generar_excel(datos),
            file_name="Base_Datos_Activos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="secondary",
            use_container_width=True
        )

# --- VISTA: AGREGAR / EDITAR ACTIVO (FORMULARIO ÚNICO) ---
elif st.session_state.vista_actual == "Formulario":
    mostrar_encabezado()
    editando = st.session_state.activo_a_editar is not None
    info_previa = datos.get(st.session_state.activo_a_editar, {}) if editando else {}
    
    if st.button("⬅️ Volver", type="secondary"):
        cambiar_vista("Inicio" if not editando else st.session_state.activo_a_editar)
        st.rerun()
        
    st.markdown(f"<h2>{'Editar Activo: ' + st.session_state.activo_a_editar if editando else 'Agregar Nuevo Activo'}</h2>", unsafe_allow_html=True)
    
    with st.form("form_activo"):
        nombre_activo = st.text_input("Nombre del Sistema / Activo", value=st.session_state.activo_a_editar if editando else "")
        contexto = st.text_area("Contexto Operacional", value=info_previa.get("Contexto", ""))
        justificacion = st.text_area("Justificación Técnica", value=info_previa.get("Justificacion", ""))
        estrategia = st.text_area("Decisión de Estrategia de Intervención", value=info_previa.get("Estrategia", ""))
        
        st.markdown("### Escala de Desarrollo Tecnológico (0 a 5 pts)")
        
        with st.expander("📚 Guía de Evaluación: Criterios del 1 al 5"):
            st.markdown("""
            Esta escala refleja la evolución tecnológica del activo evaluado. Se basa en agrupar la tecnología desde una **Primera Generación (1 punto)** hasta una de **Cuarta Generación (5 puntos)**.
            
            | Factor a Evaluar | 1 - Básico / Manual | 2 - Transición | 3 - Estándar | 4 - Avanzado | 5 - Óptimo / Autónomo |
            | :--- | :--- | :--- | :--- | :--- | :--- |
            | **1. Software y Datos** | Toma manual o inexistente. | Extracción básica, sin red. | Entrega parcial, no en tiempo real. | Datos en tiempo real para decisiones. | Autoconocimiento (IA / Machine Learning). |
            | **2. Limpieza y Ergonomía** | Obsoleto, nula ergonomía. | Requiere alto esfuerzo físico. | Condiciones aceptables/estándar. | Facilita labores con bajo esfuerzo. | Máxima ergonomía, cumple normas sanitarias. |
            | **3. Automatización** | Sistema 100% manual. | Alta intervención humana. | Semiautomático, intervención moderada. | Intervención humana mínima. | Totalmente automatizado con robots. |
            | **4. Independencia** | Dependencia total del operario. | Labores bajo supervisión estricta. | Máquina opera, humano controla. | Alta autonomía ante fallas. | 100% autónoma, humano solo decide. |
            | **5. Máquinas Compactas** | Excesivamente voluminosas. | Dificultad para manipulación. | Tamaño estándar sin optimización. | Reduce costos de instalación. | Altamente compactas y versátiles. |
            | **6. Capacidad/Eficiencia** | No satisface demanda del mercado. | Cumple mínimo con altos costos. | Satisface demanda de forma estable. | Mejora precios y rentabilidad. | Máxima eficiencia basada en datos. |
            | **7. Medioambiente** | Alto impacto, uso indiscriminado. | Controles mínimos obligatorios. | Consumo estándar de energía. | Reducción evidente en consumos. | Uso de materiales eco-amigables. |
            | **8. Normativas** | Incumple o en alto riesgo. | Cumple al límite regulaciones. | Cumplimiento nacional holgado. | Preventivo con normas internacionales. | Excede estándares internacionales. |
            """)
        
        factores = ["Integración de software / Datos", "Ergonomía y mantenibilidad", "Automatización", "Independencia del hombre", "Optimización de espacio", "Capacidad y Eficiencia", "Cuidados medioambientales", "Cumplimiento normativo"]
        
        puntajes, justificaciones_fact = [], []
        
        for i, factor in enumerate(factores):
            c_a, c_b = st.columns([1, 2])
            val_prev = 3
            just_prev = ""
            if editando and "Evaluacion" in info_previa and i < len(info_previa["Evaluacion"]):
                val_prev = int(info_previa["Evaluacion"][i]["Puntaje"].split(" ")[0])
                just_prev = info_previa["Evaluacion"][i]["Justificación Técnica / Contexto"]
                
            with c_a: puntajes.append(st.slider(factor, 0, 5, val_prev))
            with c_b: justificaciones_fact.append(st.text_input(f"Justificación para {factor}", value=just_prev))
                
        if st.form_submit_button("Guardar Activo", type="primary"):
            if not nombre_activo:
                st.error("El nombre es obligatorio.")
            else:
                total_pts = sum(puntajes)
                
                if total_pts <= 8:
                    gen = f"1ª Gen ({total_pts}/40)"
                    tct = "0 a 1 año"
                elif total_pts <= 16:
                    gen = f"2ª Gen ({total_pts}/40)"
                    tct = "0 a 1 año"
                elif total_pts <= 32:
                    gen = f"3ª Gen ({total_pts}/40)"
                    tct = "1 a 3 años" if total_pts <= 26 else "3 a 5 años"
                else:
                    gen = f"4ª Gen ({total_pts}/40)"
                    tct = "Más de 5 años"
                
                evaluacion = [{"Factor Evaluado": f, "Puntaje": f"{p} / 5", "Justificación Técnica / Contexto": j} for f, p, j in zip(factores, puntajes, justificaciones_fact)]
                
                if editando and nombre_activo != st.session_state.activo_a_editar:
                    del datos[st.session_state.activo_a_editar]
                    
                datos[nombre_activo] = {"Generación": gen, "TCT": tct, "Prioridad": "Pendiente", "Estrategia": estrategia, "Contexto": contexto, "Justificacion": justificacion, "Evaluacion": evaluacion}
                
                guardar_datos(datos)
                st.success("Guardado exitoso. Reorganizando prioridades globales...")
                cambiar_vista("Inicio")
                st.rerun()

# --- VISTA: METODOLOGÍA & RECOMENDACIONES ---
elif st.session_state.vista_actual in ["Metodologia", "Recomendaciones"]:
    mostrar_encabezado()
    if st.button("⬅️ Volver al Inicio", type="secondary"):
        cambiar_vista("Inicio")
        st.rerun()
        
    if st.session_state.vista_actual == "Metodologia":
        st.markdown("<h2>Marco Metodológico Evaluativo</h2><hr>", unsafe_allow_html=True)
        
        st.markdown("<h4>1. Sistema de Ordenamiento de Prioridades Globales</h4><div class='caja-info'>Se utiliza un algoritmo de ordenamiento que evalúa todos los activos registrados. <b>Nunca se repiten prioridades</b>: el sistema con la calificación total más baja siempre tomará el puesto 1 de urgencia.</div>", unsafe_allow_html=True)
        
        st.markdown("<h4>2. Tiempo del Ciclo Tecnológico (TCT)</h4><div class='caja-info'>Se establecieron plazos de intervención basados en la madurez y puntuación: <b>0 a 1 año, 1 a 3 años, 3 a 5 años o Más de 5 años.</b></div>", unsafe_allow_html=True)
        
        st.markdown("<h4>3. Escala del Desarrollo Tecnológico</h4><div class='caja-info'>Calificación de 0 a 40 puntos basada en 8 factores. (1ª Gen: 0-8 pts | 2ª Gen: 9-16 pts | 3ª Gen: 17-32 pts | 4ª Gen: 33-40 pts)</div>", unsafe_allow_html=True)
        
        st.markdown("""
        ### Detalle de los Criterios de Evaluación (Escala 1 a 5)
        Esta matriz define los puntajes exactos para cada uno de los 8 factores evaluados en los activos:
        
        | Factor a Evaluar | 1 - Básico / Manual | 2 - Transición | 3 - Estándar | 4 - Avanzado | 5 - Óptimo / Autónomo |
        | :--- | :--- | :--- | :--- | :--- | :--- |
        | **1. Software y Datos** | Toma manual o inexistente. | Extracción básica, sin red. | Entrega parcial, no en tiempo real. | Datos en tiempo real para decisiones. | Autoconocimiento (IA / Machine Learning). |
        | **2. Limpieza y Ergonomía** | Obsoleto, nula ergonomía. | Requiere alto esfuerzo físico. | Condiciones aceptables/estándar. | Facilita labores con bajo esfuerzo. | Máxima ergonomía, cumple normas sanitarias. |
        | **3. Automatización** | Sistema 100% manual. | Alta intervención humana. | Semiautomático, intervención moderada. | Intervención humana mínima. | Totalmente automatizado con robots. |
        | **4. Independencia** | Dependencia total del operario. | Labores bajo supervisión estricta. | Máquina opera, humano controla. | Alta autonomía ante fallas. | 100% autónoma, humano solo decide. |
        | **5. Máquinas Compactas** | Excesivamente voluminosas. | Dificultad para manipulación. | Tamaño estándar sin optimización. | Reduce costos de instalación. | Altamente compactas y versátiles. |
        | **6. Capacidad/Eficiencia** | No satisface demanda del mercado. | Cumple mínimo con altos costos. | Satisface demanda de forma estable. | Mejora precios y rentabilidad. | Máxima eficiencia basada en datos. |
        | **7. Medioambiente** | Alto impacto, uso indiscriminado. | Controles mínimos obligatorios. | Consumo estándar de energía. | Reducción evidente en consumos. | Uso de materiales eco-amigables. |
        | **8. Normativas** | Incumple o en alto riesgo. | Cumple al límite regulaciones. | Cumplimiento nacional holgado. | Preventivo con normas internacionales. | Excede estándares internacionales. |
        """)
        
    else:
        st.markdown("<h2>Síntesis y Recomendaciones</h2><hr>", unsafe_allow_html=True)
        st.markdown("<div class='caja-info'><b>1. Comité Interdisciplinario:</b> Mesa para mitigar riesgos de proveedor único.</div>", unsafe_allow_html=True)
        st.markdown("<div class='caja-info'><b>2. Homologación Local:</b> Extender estrategia a sistemas electromecánicos.</div>", unsafe_allow_html=True)
        st.markdown("<div class='caja-info'><b>3. Migración Predictiva:</b> Aprovechar telemetría para CBM.</div>", unsafe_allow_html=True)

# --- VISTA: DETALLE DE ACTIVO INDIVIDUAL ---
else:
    sistema = st.session_state.vista_actual
    mostrar_encabezado()
    
    col_v, col_e, col_d = st.columns([6, 2, 2])
    with col_v:
        if st.button("⬅️ Volver", type="secondary"):
            cambiar_vista("Inicio")
            st.rerun()
    with col_e:
        if st.button("✏️ Editar", type="secondary", use_container_width=True):
            cambiar_vista("Formulario", activo_edit=sistema)
            st.rerun()
    with col_d:
        if st.button("🗑️ Eliminar", type="primary", use_container_width=True):
            if sistema in datos:
                del datos[sistema]
                guardar_datos(datos)
                cambiar_vista("Inicio")
                st.rerun()
        
    st.markdown(f"<h2>Diagnóstico: {sistema}</h2><hr>", unsafe_allow_html=True)
    
    if sistema in datos:
        info = datos[sistema]
        c1, c2, c3 = st.columns(3)
        c1.metric("Generación Tecnológica", info["Generación"])
        c2.metric("Vida útil remanente", info["TCT"])
        c3.metric("Orden de reemplazo", info["Prioridad"])
        
        st.markdown("<h4>Estrategia de Intervención</h4>", unsafe_allow_html=True)
        st.markdown(f"<div class='caja-info'>{info.get('Estrategia', '')}</div>", unsafe_allow_html=True)
        st.markdown("<h4>Contexto Operacional y Datos</h4>", unsafe_allow_html=True)
        st.markdown(f"<div class='caja-info'>{info.get('Contexto', '')}</div>", unsafe_allow_html=True)
        st.markdown("<h4>Justificación Técnica</h4>", unsafe_allow_html=True)
        st.markdown(f"<div class='caja-info'>{info.get('Justificacion', '')}</div>", unsafe_allow_html=True)

        st.markdown("<h4>Evaluación Técnica</h4>", unsafe_allow_html=True)
        st.table(pd.DataFrame(info["Evaluacion"]))
