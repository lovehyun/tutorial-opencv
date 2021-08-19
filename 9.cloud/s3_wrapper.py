# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html
import boto3
from botocore.exceptions import ClientError
from log_wrapper import log

# Upload image to S3 bucket
def upload_image(bucket, filename):
    s3 = boto3.client('s3')
    resp = s3.upload_file(filename, bucket, filename)
    if resp is None:
        log.info('Upload successful')

# Delete image from S3 bucket
def delete_image(bucket, filename):
    s3 = boto3.client('s3')
    resp = s3.delete_object(Bucket=bucket, Key=filename)
    if resp['ResponseMetadata']['HTTPStatusCode'] == 204:
        log.info('Delete successful')

# List all my S3 buckets
def list_buckets():
    s3 = boto3.client('s3')
    resp = s3.list_buckets()
    buckets = [bucket['Name'] for bucket in resp['Buckets']]
    log.info(buckets)
    return buckets

# Create a S3 bucket
def create_bucket(bucket):
    s3 = boto3.client('s3')
    try:
        s3.create_bucket(Bucket=bucket , CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-2'})
        print('Bucket created')
    except ClientError as e:
        print(e)


if __name__ == '__main__':
    log.info('s3_wapper test')

    # Step 1. Buckets
    BUCKET = 'shpark-rekognition'

    create_bucket(BUCKET)
    bucket = list_buckets()
    print('Buckets: ', bucket)
