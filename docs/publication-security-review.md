# Revisión de seguridad para publicación

Fecha: 2026-10-06. Revisiones: `main` en `826a869142d76b49c3de2bb73d809ced205ef4fc`; `develop` en `3ccc4ebe4da20ad80fb7a93a41fcdf4c09d0104f`.

## Alcance y método

Se clonó el repositorio con sus ramas y etiquetas disponibles. Se revisaron 36 commits únicos alcanzables y sus 80 blobs, incluyendo versiones antiguas y archivos eliminados del estado actual. Gitleaks `8.30.1` se ejecutó sobre el historial (`--log-opts=--all`) y sobre los blobs extraídos; los informes se generaron con redacción completa.

Se inspeccionaron además Compose, configuración de entorno, proveedor Terraform, API, conector del modelo y pipeline. No se incluyen objetos Git inalcanzables, archivos locales sin seguimiento, conversaciones/adjuntos de PR e issues, secretos de GitHub, artifacts de CI ni infraestructura real. Esta comprobación no es una auditoría de vulnerabilidades de dependencias ni un pentest.

## Resultado de secretos

No se detectaron coincidencias de Gitleaks en el contenido de este repositorio. Las credenciales PostgreSQL son valores de ejemplo del laboratorio; las claves AWS `test` se emplean contra los endpoints de LocalStack. No se encontraron referencias conocidas de la empresa en las comprobaciones adicionales.

Los archivos `config/backend.dev.env` y `config/frontend.dev.env` están versionados deliberadamente como configuración de ejemplo. El hecho de que un archivo termine en `.env` no demuestra que contenga una credencial operativa. No añadir valores reales a estos archivos ni reutilizar los valores de ejemplo.

## Hallazgos de configuración y presentación

| Hallazgo | Consecuencia / acción recomendada |
| --- | --- |
| `main` contiene la estructura inicial; la implementación está en `develop` | El README debe enlazar `develop`; promover el código mediante una revisión independiente |
| PostgreSQL y LocalStack publican puertos en todas las interfaces | Limitar `5432` y `4566` a `127.0.0.1` en equipos accesibles por red |
| LocalStack monta `/var/run/docker.sock` | Acceso amplio al motor Docker; revisar si la demo SQS necesita ese montaje y usar un entorno dedicado |
| API sin autenticación | Arrancar en loopback y añadir controles antes de ofrecer acceso compartido |
| Modelo personalizado `qwen-devsecops:latest` sin Modelfile versionado | Documentar preparación o modelo alternativo; la demo no es reconstruible automáticamente con ese nombre |
| `.github/workflows/` sin pipeline implementado | Hablar de pipeline local, sin atribuir CI alojada al proyecto |

Estos hallazgos se documentan; no se han modificado permisos, redes, infraestructura ni comportamiento del conector. La revisión humana y las instrucciones del prompt son medidas de proceso, no una barrera técnica completa.

## Validación realizada

- `bash scripts/validate-env.sh`: correcto.
- `git diff --check`: correcto para los cambios de documentación.
- README contrastado con API, Compose, scripts, ramas y requisitos reales.

No se ejecutaron pytest del backend porque requieren PostgreSQL inicializado; Docker no está disponible en este entorno. Tampoco se ejecutaron el pipeline completo, Terraform, frontend o inferencia del modelo. No se atribuye una validación integral de la aplicación.

## Valoración para publicación

No se identificó un bloqueo por secretos operativos dentro del alcance. El repositorio ya es público. La documentación debe presentar las capacidades de `develop` y las limitaciones locales con precisión, sin describirlo como producto listo para producción.
