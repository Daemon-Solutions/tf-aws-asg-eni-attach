variable "enis" {
  description = "List of ENI IDs available for attachment"
}

variable "lambda_function_name" {}

variable "cloudwatch_event_rule_name" {}

variable "asg_name" {
  description = "Name of AutoscalingGroup to attach this Lambda function to"
}

variable "sns_topic_name" {
  description = "Name for SNS topic"
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

variable "aws_region" {
  default = "eu-west-1"
}

variable "lambda_log_level" {
  description = "Log level for lambda function. Valid options are those of python logging module: CRITICAL, ERROR, WARNING, INFO, DEBUG"
  default     = "INFO"
}
