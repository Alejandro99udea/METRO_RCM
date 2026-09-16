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
- Se conservaron las 12 entradas de navegación del proyecto.


## Navegación actualizada
- Se eliminó la pestaña/página independiente **Criticidad** (`06_Criticidad.py`).
- Se conserva **Matriz de Criticidad** (`07_Criticidad_Integrado.py`).
- Se eliminó la pestaña/página independiente **Fuentes** (`08_Fuentes.py`).
- No se eliminó ni modificó la información de criticidad o fuentes que forma parte del contenido de otros módulos.


### Ajuste final de portada
- Los módulos de navegación de la portada se presentan en una cuadrícula uniforme de 3 columnas por fila.
- Los contenedores de las tarjetas usan una altura mínima consistente para evitar módulos visualmente más grandes que otros.
- Se conserva la eliminación de las pestañas independientes Criticidad y Fuentes; Matriz de Criticidad permanece disponible.
