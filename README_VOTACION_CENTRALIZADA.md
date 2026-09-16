# Votación centralizada de METRO_RCM

Esta versión cambia el almacenamiento de la encuesta de criticidad de `localStorage` a un registro central en Google Sheets mediante Google Apps Script. El envío de nuevas votaciones usa `doGet` + JSONP para evitar problemas de CORS/POST dentro del iframe de Streamlit.

## Comportamiento
- Cada voto se guarda como una fila en la hoja `Votos`.
- Todos los dispositivos consultan el mismo registro central.
- La encuesta refresca los resultados cada 10 segundos.
- El historial y los promedios se ven iguales para todos los usuarios.
- Si no se configura `VOTACION_ENDPOINT`, el aplicativo funciona en modo local como respaldo.
- El botón público de "Reiniciar Datos" se elimina para evitar que un participante borre la encuesta.

## Configuración
1. Cree un Google Sheet.
2. Abra Extensiones -> Apps Script.
3. Pegue `backend_google_apps_script.js`.
4. Sustituya `SPREADSHEET_ID` por el ID del Sheet.
5. Ejecute `publicar_hoja()` una vez.
6. Publique el proyecto como Aplicación web con acceso para cualquier usuario que tenga el enlace.
7. Copie la URL que termina en `/exec`.
8. En Streamlit Cloud agregue en Secrets:

```toml
VOTACION_ENDPOINT = "https://script.google.com/macros/s/XXXXXXXX/exec"
```

No se necesita instalar una librería adicional en Python.
