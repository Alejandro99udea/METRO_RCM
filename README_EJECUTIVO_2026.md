# METRO_RCM — Edición Ejecutiva 2026

## Propósito
Versión de presentación ejecutiva de la plataforma METRO_RCM para gestión de activos, confiabilidad y RCM aplicada al Metro de Medellín.

## Sistema visual
- Paleta institucional sobria: verde profundo, blanco, grises técnicos y acento dorado.
- Navegación lateral numerada por módulos.
- Encabezados internos homogéneos.
- Tarjetas compactas con jerarquía tipográfica y acciones directas.
- Selectores, botones, métricas, tablas, pestañas y alertas con tratamiento visual consistente.
- Diseño responsive para escritorio y pantallas medianas.
- Sin fuentes externas ni dependencias visuales adicionales.

## Módulos incluidos
01. Contexto del Negocio  
02. Contexto Operacional  
03. Gestión de Activos  
04. Mantenimiento  
05. Indicadores  
06. Matriz de Criticidad  
07. RCM  
08. Equipo RCM Integrado  
09. Monitoreo Ambiental  
10. Obsolescencia de Activos

## Ejecución local
Desde la carpeta raíz, es decir, la carpeta que contiene `app.py`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run .\app.py
```

La aplicación queda disponible en `http://localhost:8501`. VS Code no es obligatorio; puede ejecutarse desde PowerShell o CMD.

## Despliegue
El proyecto mantiene `app.py` como entrada y está preparado para Streamlit Community Cloud. La votación centralizada conserva su endpoint mediante Secrets; no se incluye ningún secreto en este paquete.


## Encuesta de ponderación — versión final
La encuesta conserva el flujo centralizado definido para el proyecto:
- cinco criterios: Seguridad de las personas, Impacto a la operación, Continuidad operacional, Costo de reparación e Impacto ambiental;
- distribución obligatoria de exactamente 100 puntos;
- registro inmediato por participante en el repositorio central mediante Google Apps Script;
- lectura compartida y actualización automática cada 5 segundos;
- promedio consolidado, barras comparativas, contador de respuestas, historial y exportación CSV;
- la ponderación central se normaliza a 100 % y puede sincronizarse explícitamente con la matriz para evitar reinicios mientras el usuario edita la matriz.

La interfaz de la encuesta se ejecuta localmente sin Chart.js, Google Fonts ni otras dependencias visuales externas.

## Integridad funcional
La matriz de criticidad y el flujo de votación centralizada se mantienen como módulos independientes. El rediseño actúa sobre la capa visual y de navegación sin modificar la lógica del cuestionario de ponderación.

## Validación de entrega

Antes de publicar esta versión se recomienda ejecutar:

```powershell
python .\smoke_test.py
```

El chequeo valida sintaxis Python, estructura de navegación, datos JSON, archivos críticos, generación de PDF y sintaxis del backend JavaScript cuando Node.js está disponible.

La aplicación requiere una versión moderna de Streamlit porque utiliza `st.page_link`, `st.switch_page`, `st.fragment` y controles con `width="stretch"`.
