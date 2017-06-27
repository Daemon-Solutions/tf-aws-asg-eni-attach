# tf-aws-asg-eni-attach

This module will attach ENI to instances in ASG based on tags. 
Currently only one ENI per instance is supported.
Attach of an additional network interface may require you to manually bring up the second interface, configure the private IPv4 address, and modify the route table accordingly. Instances running Amazon Linux or Windows Server automatically recognize the warm or hot attach and configure themselves. You may also try https://git.bashton.net/pawel/ec2-net-utils although it is not fully tested yet.


## Usage

```
# create your ENIs
resource "aws_network_interface" "tranzaxis_proxy_eni_a" {
  subnet_id   = "${data.terraform_remote_state.corporate.app-access-vpc-private-subnets[0]}"
  private_ips = ["192.168.135.20"]

  tags {
    Name    = "tranzaxis_proxy_eni_a"
    Service = "tranzaxis_proxy"
  }
}

resource "aws_network_interface" "tranzaxis_proxy_eni_b" {
  subnet_id   = "${data.terraform_remote_state.corporate.app-access-vpc-private-subnets[1]}"
  private_ips = ["192.168.135.84"]

  tags {
    Name    = "tranzaxis_proxy_eni_b"
    Service = "tranzaxis_proxy"
  }
}

# attache ENIs to ASG instances
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
```