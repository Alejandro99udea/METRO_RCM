from utils.theme import aplicar_tema_udea
import streamlit as st
from data.metro_data import LINEAS, TRANVIA



aplicar_tema_udea(marca_agua=True)
st.title('🏗️ Jerarquía de activos')
st.write('Explorador inicial de la arquitectura de activos. La jerarquía técnica definitiva requiere inventario oficial.')

linea = st.selectbox('Seleccione una línea', list(LINEAS.keys()))
info = LINEAS[linea]
st.subheader(f"Línea {linea} — {info['modo']}")
st.write(f"**Recorrido:** {info['recorrido']}")

if linea == 'T':
 st.info('La Línea T es el primer sistema que desarrollaremos hasta el nivel RCM.')
 st.code('''Línea T\n│\n├── Material rodante\n├── Guiado y rodadura\n├── Frenado\n├── Tracción\n├── Suspensión\n├── Neumática\n├── Puertas\n├── Alimentación eléctrica\n├── Control y señalización\n├── Comunicaciones\n├── Infraestructura de vía\n└── Seguridad y emergencia''')
 st.write('**Siguiente nivel:** sistema → subsistema → equipo → componente → función.')
