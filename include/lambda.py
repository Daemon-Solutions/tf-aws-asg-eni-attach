#!/usr/bin/python

import boto3
import botocore
from datetime import datetime
import os
import logging

# based on https://aws.amazon.com/premiumsupport/knowledge-center/attach-second-eni-auto-scaling/

# get logger
logger = logging.getLogger()
logger.setLevel(os.environ['LOG_LEVEL'])

# what tag should we look for
eni_tag_name, eni_tag_value = os.environ['ENI_TAG'].split(':')

# get current region, it is in ENV by default
aws_region = os.environ['AWS_DEFAULT_REGION']

# clients
ec2_client = boto3.client('ec2', region_name=aws_region)
asg_client = boto3.client('autoscaling', region_name=aws_region)


def lambda_handler(event, context):

    logger.debug('Event: {}'.format(event))

    if event["detail-type"] == "EC2 Instance-launch Lifecycle Action":
        instance_id = event["detail"]["EC2InstanceId"]
        logger.debug('Instance ID: {}'.format(instance_id))

        subnet_id = get_subnet_id(instance_id)
        logger.debug('Subnet ID: {}'.format(subnet_id))

        interface_id = get_eni(subnet_id, eni_tag_name, eni_tag_value)
        logger.debug('Interface ID: {}'.format(interface_id))

        attachment = attach_interface(interface_id, instance_id)
        logger.debug('Attachment ID: {}'.format(attachment))

        # it any of the above is None we failed
        if not (subnet_id and interface_id and attachment):
            logger.error('Failed to attach interface')

        # complete lifecycle hook
        try:
            asg_client.complete_lifecycle_action(
                LifecycleHookName=event['detail']['LifecycleHookName'],
                AutoScalingGroupName=event['detail']['AutoScalingGroupName'],
                LifecycleActionToken=event['detail']['LifecycleActionToken'],
                LifecycleActionResult='CONTINUE'
            )
        except botocore.exceptions.ClientError as e:
            logger.error('Error completing life cycle hook for instance {}: \
                         {}'.format(instance_id, e.response['Error']['Code']))


def get_subnet_id(instance_id):

    vpc_subnet_id = None

    try:
        result = ec2_client.describe_instances(InstanceIds=[instance_id])
        vpc_subnet_id = result['Reservations'][0]['Instances'][0]['SubnetId']

    except botocore.exceptions.ClientError as e:
        logger.error('Error describing instance {}: {}'.format(
            instance_id, e.response['Error']['Code']))

    return vpc_subnet_id


def attach_interface(network_interface_id, instance_id):

    attachment = None

    if network_interface_id and instance_id:
        try:
            result = ec2_client.attach_network_interface(
                NetworkInterfaceId=network_interface_id,
                InstanceId=instance_id,
                DeviceIndex=1
            )
            attachment = result['AttachmentId']
            logger.info("Created network attachment: {}".format(attachment))

        except botocore.exceptions.ClientError as e:
            logger.error('Error attaching network interface: {}'.format(
                e.response['Error']['Code']))

    return attachment


def get_eni(subnet_id, eni_tag_name, eni_tag_value):

    eni_id = None

    if subnet_id:
        try:
            waiter = ec2_client.get_waiter('network_interface_available')
            waiter.config.delay = 2
            waiter.config.max_attempts = 100
            eni_filters = [
                {
                    'Name': 'subnet-id',
                    'Values': [
                        subnet_id,
                    ]
                },
                {
                    'Name': 'tag:{}'.format(eni_tag_name),
                    'Values': [
                        eni_tag_value,
                    ]
                }
            ]

            # is there ENI we want at all
            response = ec2_client.describe_network_interfaces(Filters=eni_filters)
            if response:
                eni_id = response['NetworkInterfaces'][0]['NetworkInterfaceId']
                logger.debug('Found ENI: {}'.format(eni_id))
                if response['NetworkInterfaces'][0]['Status'] != 'available':
                    # lets wait for ENI to become available.
                    # it might be that previous instance
                    # is still shutting down
                    waiter_filters = [
                        {
                            'Name': 'network-interface-id',
                            'Values': [
                                eni_id,
                            ]
                        },
                        {
                            'Name': 'status',
                            'Values': [
                                'available',
                            ]
                        }
                    ]
                    logger.debug('ENI {} is not available, waiting'.format(eni_id))
                    waiter.wait(Filters=waiter_filters)
            else:
                logger.error('No matching ENI found')

        except botocore.exceptions.ClientError as e:
            logger.error('Failed to discover available ENIs: {}'.format(
                    e.response['Error']['Code']))

    return eni_id
