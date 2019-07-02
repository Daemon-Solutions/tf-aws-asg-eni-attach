tf-aws-asg-eni-attach
-----

This module will attach ENI to instances in ASG based on tags.

Currently only one ENI per instance is supported. Attach of an additional network interface may require you to manually bring up the second interface, configure the private IPv4 address, and modify the route table accordingly. Instances running Amazon Linux or Windows Server automatically recognize the warm or hot attach and configure themselves. You may also try https://git.bashton.net/Bashton/ec2-net-utils although it is not fully tested yet.


Usage
-----

```
# Create your ENIs
resource "aws_network_interface" "eni_a" {
  subnet_id   = "subnet-123"
  private_ips = ["192.168.0.10"]

  tags {
    Name    = "eni_a"
    Service = "important"
  }
}

resource "aws_network_interface" "eni_b" {
  subnet_id   = "subnet-456"
  private_ips = ["192.168.0.110"]

  tags {
    Name    = "eni_b"
    Service = "important"
  }
}

# Attach ENIs to ASG instances
module "attach_eni" {
  source                     = "../modules/tf-aws-asg-eni-attach"
  lambda_function_name       = "${var.envname}-eni-attach"
  cloudwatch_event_rule_name = "${var.envname}-eni-attach"
  asg_name                   = "${module.important.asg_name}"
  eni_tag                    = "Service:important"
  lambda_log_level           = "DEBUG"
}
```

Variables
---------
_Variables marked with **[*]** are mandatory._
###### Lambda
* `lambda_function_name` - The name for the Lambda function that is created to attach the network interface(s). __[*]__
* `lambda_log_level` - Log level for the Lambda function. Valid options are those of python logging module: `CRITICAL`, `ERROR`, `WARNING`, `INFO` and `DEBUG`. [Default: `INFO`]
* `lambda_logs_retention_in_days` - Count of how many days to retain the Lambda function logs for. [Default: `30`]
* `cloudwatch_event_rule_name` - The name for the CloudWatch rule that triggers Lambda to attach the ENI. __[*]__
* `eni_tag` - The tag and value to filter ENIs in the format of `tag:value`. __[*]__

###### Autoscale Group
* `asg_name` - The ID for the Autoscale group you wish to attach ENIs on. __[*]__


Outputs
-------
_None_
