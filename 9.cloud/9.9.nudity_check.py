# https://docs.aws.amazon.com/ko_kr/rekognition/latest/dg/procedure-moderate-images.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
import boto3
import sys, getopt
from s3_wrapper import list_buckets, create_bucket, upload_image, delete_image

def moderate_image(bucket, photo):
    client = boto3.client('rekognition')

    response = client.detect_moderation_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}})

    print("\nDetected labels for '" + photo + "'")
    for label in response['ModerationLabels']:
        print("=> " + label['Name'] + ' : ' + str(label['Confidence']))
        print("  => " + label['ParentName'])

    return len(response['ModerationLabels'])

def usage(program):
    print('\nUsage: %s -f <filename> -b <bucketname> -u -d -l -h -c <bucketname>' % program)
    print('       where f = filename')
    print('             b = bucketname')
    print('             u = upload image')
    print('             d = delete image after usage')
    print('             l = list buckets')
    print('             h = help')
    print('             c = create bucket')


def main(program, argv):
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
            usage(program)
            exit(1)
        elif opt == '-f':
            filename = arg
        elif opt == '-b':
            bucket = arg
        elif opt == '-l':
            print(list_buckets())
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
        usage(program)
        exit(1)

    print('bucket: %s, filename: %s' % (bucket, filename))

    # process images
    if upload_flag:
        upload_image(bucket, filename)
 
    label_count = moderate_image(bucket, filename)
    print('Labels detected: ' + str(label_count))

    if delete_flag:
        delete_image(bucket, filename)


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
