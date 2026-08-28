import streamlit as st

st.title('⚠️ Criticidad')
st.info('Módulo preparado. La matriz se construirá con criterios documentados del proyecto antes de asignar criticidades a activos reales.')

st.subheader('Dimensiones')
cols=st.columns(5)
for c, t in zip(cols,['Seguridad','Operación','Ambiental','Económica','Reputación']):
 c.markdown(f'### {t}')
 c.write('Pendiente de metodología cuantificada.')

st.warning('No se asignan valores de criticidad todavía porque el documento establece que la matriz debe construirse como parte del proyecto y el inventario completo de activos aún está pendiente.')
