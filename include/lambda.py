#!/usr/bin/python

import boto3
import botocore
from datetime import datetime
import os

ec2_client = boto3.client('ec2')
asg_client = boto3.client('autoscaling')

# what tag should we look for
eni_tag_name, eni_tag_value = os.environ['ENI_TAG'].split(':')


def lambda_handler(event, context):
 
    if event["detail-type"] == "EC2 Instance-launch Lifecycle Action":
        instance_id = event["detail"]["EC2InstanceId"]
        subnet_id = get_subnet_id(instance_id)
        interface_id = get_eni(subnet_id, eni_tag_name, eni_tag_value)
        attachment = attach_interface(interface_id, instance_id)

        if interface_id == None or attachment == None:

            try:

                asg_client.complete_lifecycle_action(
                    LifecycleHookName = event['detail']['LifecycleHookName'],
                    AutoScalingGroupName = event['detail']['AutoScalingGroupName'],
                    LifecycleActionToken = event['detail']['LifecycleActionToken'],
                    LifecycleActionResult = 'CONTINUE'
                )
  
                log('{"Error": "1"}')


            except botocore.exceptions.ClientError as e:

                log("Error completing life cycle hook for instance {}: {}".format(instance_id, e.response['Error']['Code']))

                log('{"Error": "1"}')
        else:
            log('{"Error": "0"}')


def get_subnet_id(instance_id):

    try:
        result = ec2_client.describe_instances(InstanceIds=[instance_id])
        vpc_subnet_id = result['Reservations'][0]['Instances'][0]['SubnetId']
        log("Subnet id: {}".format(vpc_subnet_id))

    except botocore.exceptions.ClientError as e:
        log("Error describing the instance {}: {}".format(instance_id, e.response['Error']['Code']))
        vpc_subnet_id = None
    
    return vpc_subnet_id


def attach_interface(network_interface_id, instance_id):

    attachment = None

    if network_interface_id and instance_id:
        try:
            attach_interface = ec2_client.attach_network_interface(
                NetworkInterfaceId=network_interface_id,
                InstanceId=instance_id,
                DeviceIndex=1
            )
            attachment = attach_interface['AttachmentId']

            log("Created network attachment: {}".format(attachment))

        except botocore.exceptions.ClientError as e:
            log("Error attaching network interface: {}".format(e.response['Error']['Code']))
    
    return attachment


def get_eni(subnet_id, eni_tag_name, eni_tag_value):

    try:
        response = ec2_client.describe_network_interfaces(
            Filters=[
                {
                    'Name': 'subnet-id',
                    'Values': [
                        subnet_id,
                    ]
                },
                {
                    'Name': 'tag:{}'.format(eni_tag_name),
                    'Values': [
                        eni_tag_value
                    ]
                },
                {
                    'Name': 'status',
                    'Values': [
                        'available'
                    ]
                }
            ]
        )
        eni_id = response['NetworkInterfaces'][0]['NetworkInterfaceId']

    except:
        eni_id = None

    return eni_id
