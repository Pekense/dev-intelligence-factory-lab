output "temperature_queue_url" {
  description = "LocalStack SQS queue URL"
  value       = aws_sqs_queue.temperature_events.url
}

output "temperature_queue_arn" {
  description = "LocalStack SQS queue ARN"
  value       = aws_sqs_queue.temperature_events.arn
}
