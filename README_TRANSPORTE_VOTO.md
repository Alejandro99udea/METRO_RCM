# Corrección de sincronización de la encuesta

La encuesta ahora registra votos hacia Google Apps Script mediante un formulario HTML GET oculto, en lugar de depender del callback JSONP para la operación de escritura. Esto evita que el guardado dependa de la ejecución de un script cross-origin dentro del iframe de Streamlit.

La lectura de resultados sigue utilizando JSONP (`doGet?action=list`) para poder consultar los registros centrales desde el iframe.

Endpoint esperado en Streamlit Secrets:
`VOTACION_ENDPOINT = "https://script.google.com/macros/s/AKfycbzYoswF3hk5Kx5y00CXlWIcKIddYgZ5ZZbYvF09a8B2wxIJs0Z4S5mMHnnUPmZTkUCP4w/exec"`
