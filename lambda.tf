# Lambda function
module "lambda" {
  source        = "github.com/claranet/terraform-aws-lambda?ref=v1.1.0"
  function_name = var.lambda_function_name
  description   = "Lambda function that attaches ENIs to instances in ${var.asg_name} ASG"
  handler       = "lambda.lambda_handler"
  runtime       = "python2.7"
  timeout       = 300
  source_path   = "${path.module}/include/lambda.py"

  policy = {
    json = data.aws_iam_policy_document.lambda.json
  }

  environment = {
    variables = {
      LOG_LEVEL = var.lambda_log_level
      ENI_TAG   = var.eni_tag
    }
  }
}
