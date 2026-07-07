# Arquitectura — DEV Intelligence Factory Lab

## Visión general

DEV Intelligence Factory Lab simula una empresa que transforma solicitudes técnicas y funcionales en cambios gobernados dentro de un entorno DEV.

El laboratorio combina aplicación, infraestructura, pipeline y uso controlado de IA.

## Componentes principales

| Componente | Tecnología | Objetivo |
|---|---|---|
| Backend | FastAPI | Exponer API de seguimiento de mercancía |
| Frontend | React | Mostrar dashboard operativo |
| Base de datos | PostgreSQL | Persistir datos logísticos |
| Infraestructura | Terraform | Definir recursos como código |
| AWS local | LocalStack | Simular servicios AWS en local |
| CI/CD | GitHub Actions | Validar cambios automáticamente |
| IA | Claude Code o Codex | Proponer cambios bajo gobierno |
| Documentación | Markdown | Mantener trazabilidad y contexto |

## Flujo de cambio

Solicitud técnica o funcional.

Análisis de impacto mediante prompt corporativo.

Creación de rama controlada.

Propuesta de cambio.

Validación por pipeline.

Pull Request.

Revisión humana.

Merge controlado.

## Entornos

Este laboratorio solo contempla entorno DEV.

No existe producción.

No se usan secretos reales.

No se ejecuta terraform apply contra infraestructura real.

## Caso funcional principal

Aplicación de seguimiento de mercancía con:

- Cliente.
- Destino.
- Ubicación.
- Estado.
- Servicio de transporte.
- ETA.
- Temperatura actual.
- Estado de alerta.
- Último evento logístico.

## Caso técnico principal

Añadir variable de entorno DEV:

DASHBOARD_REFRESH_INTERVAL_SECONDS=30

## Caso infraestructura principal

Crear una cola SQS local en LocalStack para eventos de temperatura:

temperature-events-dev

## Principio de diseño

La IA acelera la propuesta, pero no sustituye la validación técnica ni la decisión humana.
