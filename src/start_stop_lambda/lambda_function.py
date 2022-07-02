import boto3
import os

in_key=os.environ.get("TAG_KEY")
in_val=os.environ.get("TAG_VALUE")
in_state=os.environ.get("INST_STATE")
in_region=os.environ.get("INST_REGION")
instances_ids=[]
ec2_filter=[{
    'Name': "tag:"+in_key,
    'Values': [in_val]
}]
client = boto3.client("ec2", region_name=in_region)

def lambda_handler(event, context):
    ec2_data = client.describe_instances(Filters=ec2_filter)
    for reservations in ec2_data['Reservations']:
        for instance in reservations['Instances']:
            instance_id = instance['InstanceId']
        instances_ids.append(instance_id)
    if in_state == "Start":
        client.start_instances(InstanceIds=instances_ids)
        print('started your instances: ' + str(instances_ids))
    elif in_state == "Stop":
        client.stop_instances(InstanceIds=instances_ids)
        print('stopped your instances: ' + str(instances_ids))
    else:
        print('option is now valid! Select another state')

