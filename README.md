# Metro_RCM

Aplicativo Streamlit para Gestión de Activos, Mantenimiento y RCM del Metro de Medellín.

## Ejecución

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Fuente documental

La versión actual usa como base los documentos suministrados en la conversación, especialmente `Investigacion_Metro (2).pdf` y `CONTEXTO OPERACIONAL.pdf`.

La información se clasifica conceptualmente en confirmada, parcial y pendiente. No se inventan MTBF, MTTR, inventarios ni criticidades.
