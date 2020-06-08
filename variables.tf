variable "lambda_function_name" {
  type = string
}

variable "cloudwatch_event_rule_name" {
  type = string
}

variable "asg_arn" {
  type        = string
  description = "ARN of AutoscalingGroup to attach this Lambda function to"
}

variable "asg_name" {
  type        = string
  description = "ARN of AutoscalingGroup to attach this Lambda function to"
}

variable "service" {
  type        = string
  description = "Name of service"
}

variable "eni_tag" {
  type        = string
  description = "Tag:Value to filter ENIs"
}

variable "envname" {
  type = string
}

variable "lambda_logs_retention_in_days" {
  type    = number
  default = 30
}

variable "lambda_log_level" {
  type        = string
  description = "Log level for lambda function. Valid options are those of python logging module: CRITICAL, ERROR, WARNING, INFO, DEBUG"
  default     = "INFO"
}

variable "lifecycle_hook_default_result" {
  type        = string
  description = "Default behaviour for lifecycle hook. Valid values are ABANDON and CONTINUE"
  default     = "CONTINUE"
}

variable "lifecycle_hook_heartbeat_timeout" {
  type        = number
  description = "Heartbeat timeout for lifecycle hook"
  default     = 300
}
