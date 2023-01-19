import os
import boto3
import json_handler
import json


#specifying arguments as variables

key_name = "rxhxl-key-pair"
ami_id = "ami-0cca134ec43cf708f"
instance_type = "t2.micro"
region_name = "ap-south-1"

#loading data from json

config_data = json_handler.loadJsonData("./configs/config.json")
key_name = config_data["key_name"]
ami_id = config_data["ami_id"]
instance_type = config_data["instance_type"]
region_name = config_data["region_name"]
ec2_json_data_path = config_data["ec2_data_path"]
ec2_data = json_handler.loadJsonData(ec2_json_data_path)
#create boto3 client for ec2

ec2_client = boto3.client("ec2",region_name=region_name)

#creating ec2_instance

def create_instance():
    instances = ec2_client.run_instances(
        ImageId = ami_id,
        MinCount =1,
        MaxCount = 1,
        InstanceType = instance_type,
        KeyName = key_name
    )
    
    instance_id = instances["Instances"][0]["InstanceId"]
    print(instances)

    if "ec2_instance_ids" in ec2_data:
        ec2_data["ec2_instance_ids"].append(instance_id)
    else:
        ec2_data["ec2_instance_ids"] = [instance_id]


# create_instance()


#get ip address of the instance

def get_public_ip(instance_id):
    reservations = ec2_client.describe_instances(InstanceIds=[instance_id]).get("Reservations")

    for reservation in reservations:
        for instance in reservation['Instances']:
            print(instance.get('PublicIpAddress'))


# get_public_ip("i-044357ec25690f947")

def get_running_instances():
    reservations = ec2_client.describe_instances(Filters=[
        {
            "Name":"instance-state-name",
            "Values":["running"],
        }
    ]).get("Reservations")

    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            public_ip = instance["PublicIpAddress"]
            private_ip = instance["PrivateIpAddress"]
            print(f"{instance_id}, {instance_type}, {public_ip}, {private_ip}")


# get_running_instances()

def reboot_instance(instance_id):
    response = ec2_client.reboot_instances(InstanceIds=[instance_id])
    print(response)



# stop-instance

def stop_instance(instance_id):
    response = ec2_client.stop_instances(InstanceIds=[instance_id])

    print(response)


#start instances

def start_instance(instance_id):
    response = ec2_client.start_instances(InstanceIds=[instance_id])
    print(response)


#terminate a single instance

def terminate_instance(instance_id):
    response = ec2_client.terminate_instances(InstanceIds=[instance_id])
    print(response)


#terminate multiple ec2 instances

def terminate_instances(instance_ids):
    response = ec2_client.terminate_instances(InstanceIds=instance_ids)
    print(response)

    final_instance_list = list(filter(lambda item:(item not in instance_ids),ec2_data["ec2_instance_ids"]))
    ec2_data["ec2_instance_ids"] = final_instance_list
    print(json.dumps(ec2_data["ec2_instance_ids"]))



#saving final ec2 instance data in json

savedEc2data = json_handler.saveJsonData(ec2_json_data_path,ec2_data)

if savedEc2data:
    print("Updated EC2 instanced ddata saved saved")






