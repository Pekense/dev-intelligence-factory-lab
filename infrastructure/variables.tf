variable "environment" {
  description = "Target environment for local lab resources"
  type        = string
  default     = "dev"
}

variable "temperature_queue_name" {
  description = "SQS queue name for temperature events"
  type        = string
  default     = "temperature-events-dev"
}
