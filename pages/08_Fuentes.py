from utils.theme import aplicar_tema_udea
import streamlit as st
from data.metro_data import FUENTES, PENDIENTES



aplicar_tema_udea(marca_agua=True)
st.title('📚 Fuentes y trazabilidad')
for n,d in FUENTES:
 st.markdown(f'**{n}** — {d}')

st.subheader('Estados de información')
st.markdown('🟢 **Confirmado:** aparece explícitamente en las fuentes.  \n🟡 **Parcial:** existe información, pero no con el nivel necesario.  \n🔴 **Pendiente:** requiere información adicional.')

st.subheader('Información pendiente')
for dato,estado,obs in PENDIENTES:
 st.write(f'**{dato}** — {estado}. {obs}')
