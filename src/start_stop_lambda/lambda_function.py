"""
AWS Lambda function to start or stop EC2 instances based on tags.

This function filters EC2 instances by specified tags and performs start/stop operations
based on the configured state.
"""

import boto3
import os
import logging
from typing import List, Dict, Any
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class EC2ControlError(Exception):
    """Custom exception for EC2 control operations."""
    pass

def get_environment_variables() -> Dict[str, str]:
    """
    Retrieve and validate required environment variables.
    
    Returns:
        Dict[str, str]: Dictionary containing the environment variables
    
    Raises:
        ValueError: If any required environment variable is missing
    """
    required_vars = {
        "TAG_KEY": os.environ.get("TAG_KEY"),
        "TAG_VALUE": os.environ.get("TAG_VALUE"),
        "INST_STATE": os.environ.get("INST_STATE"),
        "INST_REGION": os.environ.get("INST_REGION")
    }
    
    missing_vars = [key for key, value in required_vars.items() if not value]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return required_vars

def get_instances_by_tag(ec2_client: Any, tag_key: str, tag_value: str) -> List[str]:
    """
    Get EC2 instance IDs that match the specified tag.
    
    Args:
        ec2_client: Boto3 EC2 client
        tag_key: The tag key to filter by
        tag_value: The tag value to filter by
    
    Returns:
        List[str]: List of instance IDs
    
    Raises:
        ClientError: If AWS API call fails
    """
    instance_ids = []
    try:
        ec2_filter = [{
            'Name': f"tag:{tag_key}",
            'Values': [tag_value]
        }]
        
        response = ec2_client.describe_instances(Filters=ec2_filter)
        
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_ids.append(instance['InstanceId'])
        
        if not instance_ids:
            logger.warning(f"No instances found with tag {tag_key}={tag_value}")
        else:
            logger.info(f"Found {len(instance_ids)} instances: {instance_ids}")
            
        return instance_ids
            
    except ClientError as e:
        logger.error(f"Error describing instances: {str(e)}")
        raise EC2ControlError(f"Failed to get instances: {str(e)}")

def control_instances(ec2_client: Any, instance_ids: List[str], desired_state: str) -> None:
    """
    Start or stop EC2 instances.
    
    Args:
        ec2_client: Boto3 EC2 client
        instance_ids: List of instance IDs to control
        desired_state: Desired state ('Start' or 'Stop')
    
    Raises:
        EC2ControlError: If the operation fails or state is invalid
        ClientError: If AWS API call fails
    """
    if not instance_ids:
        logger.warning("No instances to process")
        return
        
    try:
        if desired_state == "Start":
            ec2_client.start_instances(InstanceIds=instance_ids)
            logger.info(f"Started instances: {instance_ids}")
        elif desired_state == "Stop":
            ec2_client.stop_instances(InstanceIds=instance_ids)
            logger.info(f"Stopped instances: {instance_ids}")
        else:
            raise EC2ControlError(f"Invalid state '{desired_state}'. Must be 'Start' or 'Stop'")
            
    except ClientError as e:
        logger.error(f"Error controlling instances: {str(e)}")
        raise EC2ControlError(f"Failed to {desired_state.lower()} instances: {str(e)}")

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler function.
    
    Args:
        event: Lambda event data
        context: Lambda context object
    
    Returns:
        Dict[str, Any]: Response containing execution status and details
    """
    try:
        # Get and validate environment variables
        env_vars = get_environment_variables()
        
        # Initialize EC2 client
        ec2_client = boto3.client("ec2", region_name=env_vars["INST_REGION"])
        
        # Get instances matching the tag
        instance_ids = get_instances_by_tag(
            ec2_client,
            env_vars["TAG_KEY"],
            env_vars["TAG_VALUE"]
        )
        
        # Control instances
        control_instances(ec2_client, instance_ids, env_vars["INST_STATE"])
        
        return {
            "statusCode": 200,
            "body": {
                "message": f"Successfully processed {env_vars['INST_STATE'].lower()} operation",
                "instances": instance_ids
            }
        }
        
    except (ValueError, EC2ControlError) as e:
        logger.error(str(e))
        return {
            "statusCode": 400,
            "body": {
                "error": str(e)
            }
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "statusCode": 500,
            "body": {
                "error": "Internal server error"
            }
        }

