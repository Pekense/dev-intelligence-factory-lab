resource "aws_sqs_queue" "temperature_events" {
  name = var.temperature_queue_name

  tags = {
    Environment = var.environment
    Project     = "dev-intelligence-factory-lab"
    ManagedBy   = "terraform"
  }
}
