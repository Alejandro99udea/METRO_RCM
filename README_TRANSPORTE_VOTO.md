# Corrección de sincronización de la encuesta

La encuesta ahora registra votos hacia Google Apps Script mediante un formulario HTML GET oculto, en lugar de depender del callback JSONP para la operación de escritura. Esto evita que el guardado dependa de la ejecución de un script cross-origin dentro del iframe de Streamlit.

La lectura de resultados sigue utilizando JSONP (`doGet?action=list`) para poder consultar los registros centrales desde los iframes de Streamlit. La matriz también consulta directamente la ponderación central para que el vínculo encuesta → matriz sea verificable en la propia interfaz.

Endpoint esperado en Streamlit Secrets:
`VOTACION_ENDPOINT = "https://script.google.com/macros/s/AKfycbx7WSRa1-uPUl2ThljERCQPV996Rnl5Uim8AHQ_PJlXcRDBO4DOjia4TuRcFB1BIxr7vQ/exec"`
