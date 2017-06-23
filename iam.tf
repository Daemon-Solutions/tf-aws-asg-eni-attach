# Lambda role
resource "aws_iam_role" "lambda_role" {
  name = "${var.envname}-${var.service}-eni-attach-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "lambda_logging_policy" {
  name = "${var.envname}-${var.service}-lambda-eni-attach-logging"
  role = "${aws_iam_role.lambda_role.id}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
EOF
}

# Lambda policy for managing snapshots
resource "aws_iam_role_policy" "lambda_eni_attach_policy" {
  name = "${var.envname}-${var.service}-lambda-eni-attach"
  role = "${aws_iam_role.lambda_role.id}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:CreateNetworkInterface",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DetachNetworkInterface",
        "ec2:DeleteNetworkInterface",
        "ec2:AttachNetworkInterface",
        "ec2:DescribeInstances",
        "autoscaling:CompleteLifecycleAction"
      ],
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_lambda_permission" "asg_sns" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.eni_attach.arn}"
  principal     = "sns.amazonaws.com"
  source_arn    = "${aws_sns_topic.asg_sns.arn}"
}
