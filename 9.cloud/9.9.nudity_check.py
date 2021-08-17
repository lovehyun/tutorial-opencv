# https://docs.aws.amazon.com/ko_kr/rekognition/latest/dg/procedure-moderate-images.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
import boto3
import sys, getopt

def moderate_image(photo, bucket):
    client = boto3.client('rekognition')

    response = client.detect_moderation_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}})

    print("\nDetected labels for '" + photo + "'")
    for label in response['ModerationLabels']:
        print("=> " + label['Name'] + ' : ' + str(label['Confidence']))
        print("  => " + label['ParentName'])

    return len(response['ModerationLabels'])

def upload_image(photo, bucket):
    s3 = boto3.client('s3')
    s3.upload_file(photo, bucket, photo)

def delete_image(photo, bucket):
    s3 = boto3.client('s3')
    s3.delete_object(Bucket=bucket, Key=photo)

def list_buckets():
    s3 = boto3.client('s3')
    resp = s3.list_buckets()
    buckets = [bucket['Name'] for bucket in resp['Buckets']]
    print(buckets)

def create_bucket(bucket):
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket=bucket , CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-2'})
    print('Bucket created')

def usage():
    print('Usage: -f <filename> -b <bucketname> -u -d -l -h -c <bucketname>')
    print('       where u = upload')
    print('             d = delete after usage')
    print('             l = list buckets')
    print('             h = help')
    print('             c = create bucket')

def main(argv):
    filename = ''
    bucket = 'shpark-rekognition' # put your own bucket name
    upload_flag = False
    delete_flag = False

    # input argument check
    try:
        opts, args = getopt.getopt(argv, "hf:b:udlc:")
    except getopt.GetoptError:
        usage()
        exit(1)

    # parse arguments
    for opt, arg in opts:
        if opt == '-h':
            usage()
            exit(1)
        elif opt == '-f':
            filename = arg
        elif opt == '-b':
            bucket = arg
        elif opt == '-l':
            list_buckets()
            exit(1)
        elif opt == '-c':
            create_bucket(bucket)
            exit(1)
        elif opt == '-u':
            upload_flag = True
        elif opt == '-d':
            delete_flag = True
    
    # sanity check
    if bucket == '' or filename == '':
        usage()
        exit(1)

    print('bucket: %s, filename: %s' % (bucket, filename))

    # process images
    if upload_flag:
        upload_image(filename, bucket)
 
    label_count = moderate_image(filename, bucket)
    print('Labels detected: ' + str(label_count))

    if delete_flag:
        delete_image(filename, bucket)


if __name__ == "__main__":
    main(sys.argv[1:])
