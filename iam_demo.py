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

#detach_custom_iam_policy_with_user("test_policy_1_by_sandip","sandip_poilcy_test_user_1")

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

#detach_managed_iam_policy_with_user("AdministratorAccess", "sandip_poilcy_test_user_1")

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






