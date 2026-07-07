# Gobierno de IA — DEV Intelligence Factory Lab

## Principio operativo

La IA propone, el pipeline valida y el equipo técnico decide.

## Objetivo

Definir un modelo de uso gobernado de IA para acelerar cambios técnicos y funcionales en entornos DEV sin perder control, trazabilidad ni seguridad.

## Reglas obligatorias

1. La IA no trabaja directamente sobre main.
2. Todo cambio debe realizarse en una rama controlada.
3. Todo cambio debe tener una explicación técnica.
4. Todo cambio debe pasar por pipeline.
5. Todo cambio debe ser revisado por una persona.
6. La IA no puede usar secretos reales.
7. La IA no puede ejecutar terraform apply contra entornos reales.
8. La IA no aprueba su propio cambio.
9. La IA debe indicar riesgos e impacto.
10. La IA debe generar resumen para Pull Request.

## Flujo aprobado

Solicitud técnica o funcional.

Análisis de impacto mediante prompt corporativo.

Creación de rama controlada.

Propuesta de cambio.

Validación por pipeline.

Revisión humana.

Pull Request.

Decisión técnica.

## Lo que la IA puede hacer

- Analizar impacto.
- Proponer cambios.
- Generar código inicial.
- Generar tests.
- Revisar errores de pipeline.
- Preparar documentación.
- Preparar resumen de Pull Request.

## Lo que la IA no puede hacer

- Hacer merge directo.
- Aprobar cambios.
- Usar secretos reales.
- Saltarse el pipeline.
- Ejecutar cambios en producción.
- Ejecutar terraform apply contra infraestructura real.
- Tomar decisiones sin revisión humana.

## Riesgos controlados

| Riesgo | Control |
|---|---|
| Código incorrecto | Tests y revisión humana |
| Cambio no trazable | Rama y Pull Request |
| Configuración insegura | Validación de variables |
| Infraestructura errónea | Terraform plan obligatorio |
| Dependencias peligrosas | Revisión controlada |
| Uso de secretos reales | Prohibición explícita |

## Criterio de aceptación

Un cambio solo puede considerarse válido si:

- Está en una rama feature.
- Tiene descripción clara.
- Ha pasado pipeline.
- Tiene revisión humana.
- No contiene secretos.
- No afecta producción.
- Tiene plan de rollback.
