variable "enis" {
  description = "List of ENI IDs available for attachment"
}

variable "lambda_function_name" {}

variable "asg_name" {
  description = "Name of AutoscalingGroup to attach this Lambda function to"
}

variable "sns_topic_name" {
  description = "Name for SNS topic"
}

variable "service" {
  description = "Name of service, used to filter ENIs by tag"
}
