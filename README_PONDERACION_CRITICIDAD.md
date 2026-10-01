# METRO_RCM — Ponderacion de criterios centralizada

Esta versión integra la encuesta de ponderación de cinco criterios solicitada:

1. Seguridad de las personas
2. Impacto a la operación
3. Continuidad operacional
4. Costo de reparación
5. Impacto ambiental

La encuesta distribuye exactamente 100 puntos. Se incorporan como datos iniciales los cinco registros mostrados en la referencia visual del usuario.

## Google Apps Script
- Hoja central: `1TaD-4tvKPTdAO6r0mGmihyv7OTFcYYDKfZPU8lYNga8`
- Pestaña de datos: `Ponderacion`
- Ejecutar una vez `sembrar_votaciones_iniciales()` para cargar los cinco registros iniciales.
- Mantener la misma URL `/exec` y actualizar la implementación para usar el backend incluido.

## Matriz
Los pesos de la encuesta se aplican directamente al cálculo de consecuencia e índice. La base actual de activos no tiene un campo independiente de impacto a la operación; por eso la integración usa `cobertura` como aproximación operativa y lo deja explicitamente indicado en la interfaz.
