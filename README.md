# What is boto3 ?

Boto3 is the name of the Python SDK for AWS. It allows you to directly create, update, and delete AWS resources from your Python scripts.
Boto3 makes it easy to integrate your Python application, library, or script with AWS services including Amazon S3, Amazon EC2, Amazon DynamoDB, and more.


Refer to the full documentation - [here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)


# working with boto3

## Installation
- pip install virtualenv
- python3 -m venv myenv
- cd myenv
- cd Scripts
- ./activate

### install boto3
- pip install boto3

### save dependencies in requirements.txt

- pip freeze > requirements.txt

### to install dependencies 

- pip install -r requirements.txt

### give access to aws 

- aws configure

### Launch an ec2 instance

```
import os 
import boto3

ec2_client = boto3.client("ec2")
ec2 = boto3.resource("ec2")

instances = ec2.create_instances(
    ImageId = "ami-0cca134ec43cf708f",
    MinCount = 1,
    MaxCount = 1,
    InstanceType = "t2.micro",
    KeyName = "rxhxl-key-pair"
)

```

### Stop an ec2 instance

```
response = ec2_client.terminate_instances(
    InstanceIds = ['instance id of the ec2 instance']
)

```

### Launch more than one instance

```
def create_instance():
        instances = ec2.create_instances(
            ImageId = "ami-0cca134ec43cf708f",
            MinCount = 1,
            MaxCount = 1,
            InstanceType = "t2.micro",
            KeyName = "rxhxl-key-pair"
        )
        print(instances)

for i in range(5):
    create_instance()

```

## working with ec2
```
import os
import boto3
import json_handler
import json


#specifying arguments as variables

key_name = "rxhxl-key-pair"
ami_id = "ami-0cca134ec43cf708f"
instance_type = "t2.micro"
region_name = "ap-south-1"



#creating ec2_instance

def create_instance():
    instances = ec2_client.run_instances(
        ImageId = ami_id,
        MinCount =1,
        MaxCount = 1,
        InstanceType = instance_type,
        KeyName = key_name
    )
    

#get ip address of the instance

def get_public_ip(instance_id):
    reservations = ec2_client.describe_instances(InstanceIds=[instance_id]).get("Reservations")

    for reservation in reservations:
        for instance in reservation['Instances']:
            print(instance.get('PublicIpAddress'))
            

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


```

## working with s3 buckets

```
import os
import logging
import json
import boto3

from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig

bucket_name = "<your bucket name>"

region_name = "ap-south-1"

#create a bucket

def create_bucket(bucket_name,region=None):
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3',region_name=region)
            location = {'LocationConstraint':region}
            s3_client.create_bucket(Bucket=bucket_name,CreateBucketConfiguration=location)

    except ClientError as e:
        logging.error(e)
        return False
    return True


# create_bucket(bucket_name,region_name)

# list s3_buckets

def list_buckets(region=None):
    s3_client = boto3.client('s3')

    try:
        if region is not None:
            s3_client = boto3.client('s3',region_name=region)
        response = s3_client.list_buckets()
        print("Existing buckets")

        for bucket in response['Buckets']:
            print(f'{bucket["Name"]}')

    except ClientError as e:
        logging.error(e)
        return False

    return True

# list_buckets('ap-south-1')


#upload files in s3

def upload_file(file_name,bucket,object_name=None):

    if object_name is None:
        object_name = os.path.basename(file_name)

    
    # upload the file
    s3_client = boto3.client('s3')

    try:
        response = s3_client.upload_file(file_name,bucket,object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


# upload_file('./file.txt',bucket_name)

# upload file object

def upload_file_object(file_name,bucket,object_name=None):

    if object_name is None:
        object_name = os.path.basename(file_name)

    #upload the file
    s3_client = boto3.client('s3')

    try:
        with open(file_name,"rb") as f:
            s3_client.upload_fileobj(f,bucket,object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


# delete empty buckets

def delete_empty_bucket(bucket):
    s3_client = boto3.client('s3')
    response = s3_client.delete_bucket(Bucket=bucket_name)
    print(response)



# delete not_empty buckets

def delete_non_empty_bucket(bucket):
    s3_client = s3 = boto3.client('s3')
    bucketClient = s3_client.Bucket(bucket)
    bucketClient.objects.all().delete()
    bucketClient.meta.client.delete_bucket(Bucket=bucket)


# delete object

def delete_object(bucket,object_name):
    s3_client = boto3.client('s3')
    response = s3_client.delete_object(Bucket=bucket,Key=object_name)
    print(response)

#downloaded  files

def download_file(file_name,bucket,object_name):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.download_file(bucket,object_name,file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

download_file("<the location and file name where to save>","bucket name","name of the object")


def download_file_object(file_name,bucket,object_name):
    s3_client = boto3.client('s3')

    try:
        with open(file_name,"wb") as f:
            s3_client.download_fileobj(bucket,object_name,f)

    except ClientError as e:
        logging.error(e)
        return False 
    return True

# download_file("<the location and file name where to save>","bucket name","name of the object")

def upload_file_multipart(file_name,bucket,object_name = None):

    GB = 1024 ** 3
    config = TransferConfig(multipart_threshold=5*GB)

    if object_name is None:
        object_name = os.path.basename(file_name)

    s3_client = boto3.client("s3")
    
    try:
        response = s3_client.upload_file(file_name,bucket,object_name,Config=config)
    except ClientError as e:
        logging.error(e)
        return False
    return True


#download file concurrently

def download_file_concurrently(file_name,bucket,object_name):
    config = TransferConfig(max_concurrency=20)
    s3_client = boto3.client('s3')

    try:
        response = s3_client.download_file(bucket,object_name,file_name,Config=config)
    except ClientError as e:
        logging.error(e)
        return False
    return True


#create a pre-signed url

def create_presigned_url(bucket,object_name,expiration=3600):
    s3_client = boto3.client('s3')

    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket':bucket,'Key':object_name},
            ExpiresIn = expiration
        )

    except ClientError as e:
        logging.error(e)
        return None

    return response


responseObject = create_presigned_url(bucket_name,'file.txt')
print(responseObject)


```

## working with iam

```
import json
import boto3
from botocore.exceptions import ClientError

#create IAM user
def create_iam_user(user_name):
    try:
        iam_client = boto3.client('iam')
        response = iam_client.create_user(UserName=user_name)
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print("Object already exist")
        else:
            print("unexpected error")

    return response

# responseObject = create_iam_user('GTR')
# print(responseObject)

#list all users

def list_all_users():
    try:
        iam_client = boto3.client('iam')
        paginator = iam_client.get_paginator('list_users')

        for response in paginator.paginate():
            for user in response['Users']:
                print("User name :",user['UserName'])
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print('Object already exists')
        else:
            print('Unexpected error: %s'%e)

# list_all_users()

#function to update iam user

def update_iam_user(existing_user_name,new_user_name):
    try:
        iam_client = boto3.client('iam')
        iam_client.update_user(UserName=existing_user_name,NewUserName=new_user_name)
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print('Object already exists')
        else:
            print('Unexpected error: %s'%e)

# update_iam_user('GTR','Supraa')


#delete iam user

def delete_iam_user(existing_user_name):
    try:
        iam_client = boto3.client('iam')
        iam_client.delete_user(UserName=existing_user_name)
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print('Object already exists')
        else:
            print('Unexpected error: %s'%e)

delete_iam_user('Supraa')

#function create iam policy

def create_iam_policy(policy_name,policy_json):
    try:
        iam_client = boto3.client('iam')
        iam_client.create_policy(
            PolicyName = policy_name,
            PolicyDocument = json.dumps(policy_json)
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print("Object already exists")
            return False
        else:
            print("Unexpected error: %s" % e)
            return False
    return True


    #example of json policy

custom_policy_json = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": [
                "ec2:*"
            ],
            "Resource": "*"
        }]
    }


#attach policy with the user

def attach_custom_iam_policy_with_user(policy_name,user_name):
    try:
        sts = boto3.client('sts')
        account_id = sts.get_caller_identity()['Account']
        policy_arn = f'arn:aws:iam::{account_id}:policy/{policy_name}'
        iam_client = boto3.client('iam')
        iam_client.attach_user_policy(
            UserName = user_name,
            PolicyArn = policy_arn
        )

    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print("Object already exists")
        else:
            print("Unexpected error: %s" % e)



def attach_managed_iam_policy_with_user(policy_name,user_name):
    try:
        sts = boto3.client('sts')
        policy_arn = f'arn:aws:iam::aws:policy/{policy_name}'
        iam_client = boto3.client('iam')
        iam_client.attach_user_policy(
            UserName=user_name,
            PolicyArn=policy_arn
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print("Object already exists")
        else:
            print("Unexpected error: %s" % e)



def detach_custom_iam_policy_with_user(policy_name, user_name):
    try:
        sts = boto3.client('sts')
        account_id = sts.get_caller_identity()['Account']
        policy_arn = f'arn:aws:iam::{account_id}:policy/{policy_name}'
        iam_client = boto3.client('iam')
        iam_client.detach_user_policy(
            UserName=user_name,
            PolicyArn=policy_arn
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print("Object already exists")
        else:
            print("Unexpected error: %s" % e)

#detach_custom_iam_policy_with_user("test_policy_1_by_sandip","rahul_policy_test")

def detach_managed_iam_policy_with_user(policy_name, user_name):
    try:
        sts = boto3.client('sts')
        policy_arn = f'arn:aws:iam::aws:policy/{policy_name}'
        iam_client = boto3.client('iam')
        iam_client.detach_user_policy(
            UserName=user_name,
            PolicyArn=policy_arn
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print("Object already exists")
        else:
            print("Unexpected error: %s" % e)

#detach_managed_iam_policy_with_user("AdministratorAccess", "rahul_policy_test")

def add_policy_to_role(role_name, policy_arn):
    try:
        iam_client = boto3.client('iam')
        iam_client.attach_role_policy(
        RoleName=role_name,
        PolicyArn=policy_arn
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print("Object already exists")
        else:
            print("Unexpected error: %s" % e)
    
def attach_custom_iam_policy_with_role(policy_name, role_name):
    try:
        sts = boto3.client('sts')
        account_id = sts.get_caller_identity()['Account']
        policy_arn = f'arn:aws:iam::{account_id}:policy/{policy_name}'
        iam_client = boto3.client('iam')
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print("Object already exists")
        else:
            print("Unexpected error: %s" % e)

def create_role(role_name, trust_document):
    try:
        iam_client = boto3.client('iam')
        iam_client.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(trust_document)
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print("Object already exists")
        else:
            print("Unexpected error: %s" % e)


```
