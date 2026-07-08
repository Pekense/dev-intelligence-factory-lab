# Caso técnico — Variable DEV de refresco del dashboard

## Solicitud

Validar y documentar la variable DEV:

DASHBOARD_REFRESH_INTERVAL_SECONDS=30

## Objetivo

Controlar el intervalo de refresco automático del dashboard desde configuración DEV, evitando valores fijos en código.

## Principio operativo

La IA propone, el pipeline valida y el equipo técnico decide.

## Variables implicadas

Backend:

- DASHBOARD_REFRESH_INTERVAL_SECONDS=30

Frontend:

- VITE_DASHBOARD_REFRESH_INTERVAL_SECONDS=30

## Archivos afectados

- config/backend.dev.env
- config/frontend.dev.env
- frontend/src/config.js
- frontend/src/App.jsx
- scripts/validate-env.sh
- scripts/local-pipeline.sh

## Impacto técnico

El backend expone el valor de configuración mediante el endpoint GET /config.

El frontend usa la variable VITE_DASHBOARD_REFRESH_INTERVAL_SECONDS para configurar el refresco automático del dashboard.

El script validate-env.sh comprueba que las variables existen y que el valor es numérico y mayor o igual a 10 segundos.

## Riesgos

- Valor no numérico.
- Variable mal escrita.
- Diferencia entre backend y frontend.
- Intervalo demasiado bajo que genere demasiadas llamadas a la API.
- Fichero .env local no actualizado.

## Controles

- Validación de variables DEV.
- Build frontend.
- Tests backend.
- Pipeline local.
- Revisión humana mediante Pull Request.

## Validaciones realizadas

Pendiente de ejecutar:

- ./scripts/validate-env.sh
- ./scripts/local-pipeline.sh

## Criterio de aceptación

El cambio se considera válido si:

- La variable existe en backend y frontend.
- El valor es 30.
- El dashboard muestra refresco automático cada 30 segundos.
- El pipeline local finaliza correctamente.
- No se usan secretos reales.
- No se ejecuta terraform apply automáticamente.
