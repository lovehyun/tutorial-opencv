# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
import boto3
from botocore.exceptions import ClientError
from log_wrapper import log

# Upload image to S3 bucket
def upload_image(bucket, filename):
    s3 = boto3.client('s3')
    resp = s3.upload_file(filename, bucket, filename)
    if resp is None:
        log.info("Image '%s' upload successful", filename)

# Delete image from S3 bucket
def delete_image(bucket, filename):
    s3 = boto3.client('s3')
    resp = s3.delete_object(Bucket=bucket, Key=filename)
    if resp['ResponseMetadata']['HTTPStatusCode'] == 204:
        log.info("Image '%s' delete successful", filename)

# List all my S3 buckets
def list_buckets():
    s3 = boto3.client('s3')
    resp = s3.list_buckets()
    buckets = [bucket['Name'] for bucket in resp['Buckets']]
    return buckets

# Create a S3 bucket
def create_bucket(bucket):
    s3 = boto3.client('s3')
    try:
        s3.create_bucket(Bucket=bucket , CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-2'})
        log.info("Bucket '%s' created", bucket)
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            log.info("Bucket '%s' already exists", bucket)
        else:
            log.error("Bucket '%s' creation failed: %s", bucket, e.response['Error']['Code'])
            # print(e)


if __name__ == '__main__':
    log.info('s3_wapper test')

    # Step 1. Buckets
    BUCKET = 'shpark-rekognition'

    create_bucket(BUCKET)
    bucket = list_buckets()
    print('Buckets: ', bucket)
