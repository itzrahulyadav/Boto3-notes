import boto3

from botocore.exceptions import ClientError
BUCKET_NAME = "boto-tutorial"

s3 = boto3.client("s3")

# list all the buckets

# buckets_resp = s3.list_buckets()

# for buckets in buckets_resp["Buckets"]:
#     print(buckets)


# # list all the objects in a bucket


# response = s3.list_objects_v2(Bucket=BUCKET_NAME)


# for obj in response["Contents"]:
#     print(obj)


# upload the file to the bucket

# with open("./names.txt","rb") as f:
#     print(f.name)
#     s3.upload_fileobj(f,BUCKET_NAME,"file.txt")

def download_file():
    try:
        s3.download_file(BUCKET_NAME,"file.txt","downloaded_file.txt")
    except:
        print("error occured")
        return False
    else:
        print("nothing uncertain happend")
    finally:
        print("process finished")

    return True



# download file with refernce

def download_with_ref():
    with open("download_file.txt","wb") as f:
        s3.download_fileobj(BUCKET_NAME,"file.txt",f)


# presigned url 

def create_pre_signed_url():
    url = s3.generate_presigned_url(
        "get_object",Params = {"Bucket":BUCKET_NAME,"Key":"file.txt"},ExpiresIn=30
    )

    print(url)

# create_pre_signed_url()

# create bucket

def create_bucket():
    try:
        bucket_location = s3.create_bucket(Bucket="new-copy-dest12222", CreateBucketConfiguration={'LocationConstraint':'ap-south-1'})
        print(bucket_location)
    except ClientError as e:
        print(e)
        return False
    return True


# create_bucket()

# copy object

def copy_object():
    response = s3.copy_object(
        Bucket = "new-copy-dest12222",
        CopySource = f"/{BUCKET_NAME}/file.txt",
        Key = "copiedfile.txt"
    )

    print(response)

# copy_object()

# Get Object

def get_object():
    response = s3.get_object(Bucket=BUCKET_NAME,Key="file.txt")
    print(response)

# get_object()





