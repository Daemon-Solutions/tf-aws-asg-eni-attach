variable "lambda_function_name" {}

variable "cloudwatch_event_rule_name" {}

variable "asg_arn" {
  description = "ARN of AutoscalingGroup to attach this Lambda function to"
}

variable "service" {
  description = "Name of service"
}

variable "eni_tag" {
  description = "Tag:Value to filter ENIs"
}

variable "envname" {}

variable "lambda_logs_retention_in_days" {
  default = "30"
}

variable "lambda_log_level" {
  description = "Log level for lambda function. Valid options are those of python logging module: CRITICAL, ERROR, WARNING, INFO, DEBUG"
  default     = "INFO"
}
