import streamlit as st
import pandas as pd
from data.metro_data import METRO

st.title('🔧 Mantenimiento y confiabilidad')

c=st.columns(4)
c[0].metric('Mantenimiento / planta',f"{METRO['mantenimiento_pct_planta']} %")
c[1].metric('Plan 2025 >','$239.000 M')
c[2].metric('Modos de falla 2016',f"{METRO['mantenimiento']['modos_falla_2016']:,}".replace(',','.'))
c[3].metric('Modos de falla 2024',f"{METRO['mantenimiento']['modos_falla_2024']:,}".replace(',','.'))

st.subheader('Modalidades')
st.write(' · '.join(METRO['mantenimiento']['modalidades']))

st.subheader('Evolución de modos de falla monitoreados')
st.bar_chart(pd.DataFrame({'Modos':[5000,20000]}, index=[2016,2024]))

st.subheader('Regularidad Línea A')
st.line_chart(pd.DataFrame({'Regularidad':[96.71,94.67]}, index=[2022,2023]))

st.info('El documento no contiene una base suficiente para calcular MTBF y MTTR por activo. Esos indicadores se calcularán cuando incorporemos históricos de órdenes de trabajo y fallas.')
