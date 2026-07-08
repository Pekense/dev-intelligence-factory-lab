# Caso infraestructura — Eventos de temperatura con SQS

## Objetivo

Simular el envío de eventos de temperatura a una cola SQS local gestionada por Terraform y LocalStack.

## Cola utilizada

temperature-events-dev

## Flujo validado

Sistema logístico o sensor DEV
↓
scripts/send-temperature-event.sh
↓
LocalStack SQS
↓
temperature-events-dev

## Script creado

scripts/send-temperature-event.sh

## Ejemplo de uso

./scripts/send-temperature-event.sh

## Ejemplo con parámetros

./scripts/send-temperature-event.sh 1 7.8 WARNING

## Evento enviado

{
  "shipment_id": 1,
  "temperature": 7.8,
  "status": "WARNING",
  "source": "temperature-sensor-dev"
}

## Validaciones realizadas

- LocalStack activo.
- Cola SQS creada con Terraform.
- Mensaje enviado correctamente.
- Mensaje recibido correctamente desde la cola.

## Evidencia

El envío devolvió un MessageId válido.

El mensaje recibido contenía:

- shipment_id
- temperature
- status
- source

## Restricciones respetadas

- Solo DEV.
- Sin AWS real.
- Sin producción.
- Sin secretos reales.
- Sin terraform apply automático.
- Cambio realizado en rama controlada.
- Revisión humana mediante Pull Request.

## Conclusión

El laboratorio ya permite simular eventos de temperatura mediante SQS local, reforzando el caso funcional de mercancías sensibles a temperatura.
