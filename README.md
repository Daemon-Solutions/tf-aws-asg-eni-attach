# tf-aws-asg-eni-attach

This module will attach ENI to instances in ASG based on tags.

Currently only one ENI per instance is supported. Attach of an additional network interface may require you to manually bring up the second interface, configure the private IPv4 address, and modify the route table accordingly. Instances running Amazon Linux or Windows Server automatically recognize the warm or hot attach and configure themselves. You may also try https://git.bashton.net/Bashton/ec2-net-utils although it is not fully tested yet.

## Terraform Version Compatibility

-----

Module Version|Terraform Version
---|---
v1.0.0|0.12.x
v0.1.0|0.11.x

## Usage

-----

```
# Create your ENIs
resource "aws_network_interface" "tranzaxis_proxy_eni_a" {
  subnet_id   = data.terraform_remote_state.corporate.app-access-vpc-private-subnets[0]
  private_ips = ["192.168.135.20"]

  tags {
    Name    = "tranzaxis_proxy_eni_a"
    Service = "tranzaxis_proxy"
  }
}

resource "aws_network_interface" "tranzaxis_proxy_eni_b" {
  subnet_id   = data.terraform_remote_state.corporate.app-access-vpc-private-subnets[1]
  private_ips = ["192.168.135.84"]

  tags {
    Name    = "tranzaxis_proxy_eni_b"
    Service = "tranzaxis_proxy"
  }
}

# Attach ENIs to ASG instances
module "attach_eni" {
  source                     = "../modules/tf-aws-asg-eni-attach"
  envname                    = var.envname
  service                    = "tranzaxis_proxy"
  lambda_function_name       = "${var.envname}-tranzaxis-proxy-eni-attach"
  cloudwatch_event_rule_name = "${var.envname}-tranzaxis-proxy-eni-attach"
  asg_arn                    = module.tranzaxis_proxy.asg_arn
  asg_name                   = module.tranzaxis_proxy.asg_name
  eni_tag                    = "Service:tranzaxis_proxy"
  lambda_log_level           = "DEBUG"
}
```

## Variables

-----

_Variables marked with **[*]** are mandatory._

### Naming

* `envname` - Used to build the name for resources created by this module (position 1). Also becomes the value for the `environment` tag. __[*]__
* `service` - Used to build the name for resources created by this module (position 2). Also becomes the value for the `service` tag. __[*]__

### Lambda

* `lambda_function_name` - The name for the Lambda function that is created to attach the network interface(s). __[*]__
* `lambda_log_level` - Log level for the Lambda function. Valid options are those of python logging module: `CRITICAL`, `ERROR`, `WARNING`, `INFO` and `DEBUG`. [Default: `INFO`]
* `lambda_logs_retention_in_days` - Count of how many days to retain the Lambda function logs for. [Default: `30`]
* `cloudwatch_event_rule_name` - The name for the CloudWatch rule that triggers Lambda to attach the ENI. __[*]__
* `eni_tag` - The tag and value to filter ENIs in the format of `tag:value`. __[*]__

### Autoscale Group

* `asg_arn` - The AWS ARN for the Autoscale group you wish to attach ENIs on. __[*]__
* `asg_name` - The ID for the Autoscale group you wish to attach ENIs on. __[*]__

## Outputs

-----

_None_
