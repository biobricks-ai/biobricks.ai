import boto3
from botocore.exceptions import ClientError
import os

def get_s3_client():  
    key = os.environ['AWS_ACCESS_KEY_INSDVC']
    secret = os.environ['AWS_SECRET_KEY_INSDVC']
    return boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=secret)

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object"""
    s3 = get_s3_client()
    params = {'Bucket': bucket_name,'Key': object_name}
    return s3.generate_presigned_url('get_object',Params=params, ExpiresIn=expiration)

def resource_size(object_name, bucket_name='ins-dvc'):
    """Retrieve the size of an object in S3"""
    s3 = get_s3_client()
    response = s3.head_object(Bucket=bucket_name, Key=object_name)
    return response['ContentLength']