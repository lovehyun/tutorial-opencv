import boto3
import sys
from s3_wrapper import upload_image, delete_image

BUCKET = 'shpark-rekognition' # put your own bucket here
KEY = ''

# https://docs.aws.amazon.com/ko_kr/rekognition/latest/dg/labels-detect-labels-image.html
def get_labels(bucket, key, max_labels=10, min_confidence=90, region='ap-northeast-2'):
    client = boto3.client('rekognition', region)
    response = client.detect_labels(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": key,
            }
        },
        MaxLabels=max_labels,
        MinConfidence=min_confidence,
    )

    return response['Labels']


if __name__ == '__main__':
    KEY = sys.argv[1]
    print('File to analyze: ', KEY)

    upload_image(BUCKET, KEY)
    labels = get_labels(BUCKET, KEY)
    # delete_image(BUCKET, KEY)
    print(labels)

    for label in labels:
        print('{Name} - {Confidence:.3f}%'.format(**label))
