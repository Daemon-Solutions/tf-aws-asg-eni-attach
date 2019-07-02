data "aws_iam_policy_document" "lambda" {
  statement {
    actions = [
      "ec2:CreateNetworkInterface",
      "ec2:DescribeNetworkInterfaces",
      "ec2:DetachNetworkInterface",
      "ec2:DeleteNetworkInterface",
      "ec2:AttachNetworkInterface",
      "ec2:DescribeInstances",
      "autoscaling:CompleteLifecycleAction"
    ]

    resources = ["*"]
  }
}
