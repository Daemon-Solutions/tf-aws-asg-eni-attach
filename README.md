# Usage

module "attach_eni" {
  source                     = "../modules/tf-aws-asg-eni-attach"
  envname                    = "${var.envname}"
  service                    = "tranzaxis_proxy"
  lambda_function_name       = "${var.envname}-tranzaxis-proxy-eni-attach"
  cloudwatch_event_rule_name = "${var.envname}-tranzaxis-proxy-eni-attach"
  asg_arn                    = "${module.tranzaxis_proxy.asg_arn}"
  asg_name                   = "${module.tranzaxis_proxy.asg_name}"
  eni_tag                    = "Service:tranzaxis_proxy"
  lambda_log_level           = "DEBUG"
}