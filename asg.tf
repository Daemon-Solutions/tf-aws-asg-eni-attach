# ASG notification
resource "aws_autoscaling_notification" "asg_notification" {
  group_names = [
    "${var.asg_name}",
  ]

  notifications = [
    "autoscaling:TEST_NOTIFICATION",
    "autoscaling:EC2_INSTANCE_LAUNCH",
  ]

  topic_arn = "${aws_sns_topic.asg_sns.arn}"
}
