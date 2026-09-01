from utils.theme import aplicar_tema_udea
import streamlit as st



aplicar_tema_udea(marca_agua=True)
st.title('🔍 RCM')
st.subheader('Flujo de análisis')
st.code('''Activo\n  ↓\nFunción\n  ↓\nFalla funcional\n  ↓\nModo de falla\n  ↓\nEfecto\n  ↓\nConsecuencia\n  ↓\nDecisión RCM\n  ↓\nTarea de mantenimiento''')

st.subheader('Consecuencias')
for x in ['Seguridad','Ambiental','Operacional','Económica','No operacional']:
 st.markdown(f'- **{x}**')

st.info('El módulo quedará conectado a la jerarquía técnica y a la base de fallas. No se generarán modos de falla definitivos sin evidencia técnica/documental.')
