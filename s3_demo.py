import os
import logging
import json
import boto3

from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig

bucket_name = "rxhxl-demo-bucket"

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







