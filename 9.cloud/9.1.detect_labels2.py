import boto3
import sys
from s3_wrapper import upload_image, delete_image
import numpy as np
import cv2

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


def process_labels(file, labels):
    print('----------')
    print('Detected labels for ' + file)
    
    # Load the image from S3 using Boto3
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=BUCKET, Key=file)
    image_data = response['Body'].read()

    # Decode the image
    image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)

    for label in labels:
        print('---')
        print("Label: " + label['Name'])
        print("Confidence: " + str(label['Confidence']))
        print("Instances:")

        for instance in label['Instances']:
            print("  Bounding box")
            print("    Top: " + str(instance['BoundingBox']['Top']))
            print("    Left: " + str(instance['BoundingBox']['Left']))
            print("    Width: " + str(instance['BoundingBox']['Width']))
            print("    Height: " + str(instance['BoundingBox']['Height']))
            print("    Confidence: " + str(instance['Confidence']))
            print()

            # Extract bounding box coordinates
            left = int(instance['BoundingBox']['Left'] * image.shape[1])
            top = int(instance['BoundingBox']['Top'] * image.shape[0])
            width = int(instance['BoundingBox']['Width'] * image.shape[1])
            height = int(instance['BoundingBox']['Height'] * image.shape[0])

            # Draw bounding box on the image
            cv2.rectangle(image, (left, top), (left + width, top + height), (0, 255, 0), 2)

            # Display label text below the bounding box
            label_text = label['Name']
            cv2.putText(image, label_text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        print("Parents:")
        for parent in label['Parents']:
            print("  " + parent['Name'])

    # Display the image with bounding boxes and labels
    cv2.imshow('Image with Bounding Boxes and Labels', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    KEY = sys.argv[1]
    print('File to analyze: ', KEY)

    upload_image(BUCKET, KEY)
    labels = get_labels(BUCKET, KEY)
    # delete_image(BUCKET, KEY)

    for label in labels:
        print('{Name} - {Confidence:.3f}%'.format(**label))

    process_labels(KEY, labels)
