# ASG lifecycle hook
resource "aws_autoscaling_lifecycle_hook" "asg_hook" {
  name                    = "${var.envname}-${var.service}-eni-attach-hook"
  autoscaling_group_name  = "${var.asg_name}"
  default_result          = "CONTINUE"
  heartbeat_timeout       = 60
  lifecycle_transition    = "autoscaling:EC2_INSTANCE_LAUNCHING"
  notification_target_arn = "${aws_sns_topic.asg_sns.arn}"
  role_arn                = "${aws_iam_role.asg_role.arn}"

  notification_metadata = <<EOF
{
  "detail-type": "EC2 Instance-launch Lifecycle Action"
}
EOF
}
