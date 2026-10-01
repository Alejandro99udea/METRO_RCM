# METRO_RCM — Diseño final UdeA

Esta versión parte del proyecto funcional entregado y añade una capa visual
unificada para la portada y los módulos internos.

## Diseño
- Portada con hero verde institucional y fotografía de Metro/ciudad.
- Navegación lateral institucional con fondo visual tenue.
- Marca de agua UdeA únicamente en páginas internas.
- Tarjetas, métricas, tabs, tablas, alertas y selectores unificados.
- Encabezados internos relacionados visualmente con la portada.
- Organización de módulos simples en paneles y secciones jerárquicas.

## Funcionalidad preservada
- Datos del proyecto.
- Fotografías y hojas de vida del equipo RCM.
- Matriz de criticidad.
- Contexto operacional y sus imágenes.
- Generación de informes PDF.
- Monitoreo ambiental/SIATA.

## Validación
Los archivos Python fueron comprobados con `ast.parse` y no presentan errores
de sintaxis. No se realiza `git push` desde este paquete.

## Ejecución local
```powershell
python -m streamlit run .\app.py
```


## Corrección final de navegación
- La navegación lateral usa `st.sidebar.page_link` sin el parámetro `icon=` para evitar el error de Streamlit por caracteres no reconocidos como emoji.
- Los iconos visibles se integran como texto de un solo símbolo dentro de cada etiqueta.
- Se comprueba la existencia de cada archivo de página antes de crear su enlace.
- La navegación actual contiene 11 entradas: Inicio + 10 módulos funcionales.


## Navegación actualizada
- Se eliminó la pestaña/página independiente **Criticidad** (`06_Criticidad.py`).
- Se conserva **Matriz de Criticidad** (`07_Criticidad_Integrado.py`).
- Se eliminó la pestaña/página independiente **Fuentes** (`08_Fuentes.py`).
- No se eliminó ni modificó la información de criticidad o fuentes que forma parte del contenido de otros módulos.


### Ajuste final de portada
- Los módulos de navegación de la portada se presentan en una cuadrícula uniforme de 3 columnas por fila.
- Los contenedores de las tarjetas usan una altura mínima consistente para evitar módulos visualmente más grandes que otros.
- Se conserva la eliminación de las pestañas independientes Criticidad y Fuentes; Matriz de Criticidad permanece disponible.


## Ajuste visual final — octubre 2026
- Se eliminó el uso decorativo de emojis en navegación y encabezados para una presentación técnica y ejecutiva.
- La portada utiliza marcas numéricas 01–10 para identificar módulos.
- La encuesta de ponderación recupera la estructura funcional anterior y adopta el sistema visual UdeA/METRO_RCM.
- La encuesta ya no depende de Chart.js ni de fuentes remotas.
- Se corrigió la correspondencia entre los cinco pesos de la encuesta y los cinco campos utilizados por la matriz: el segundo criterio es **Impacto a la operación**, representado por `cobertura` en la base actual.
- La actualización de pesos de la matriz es explícita para no reiniciar accidentalmente ediciones locales de la matriz mientras se diligencia la encuesta.
