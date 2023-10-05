import boto3
import sys
import pprint
from s3_wrapper import upload_image, delete_image
from pil_wrapper import mark_face_image

BUCKET = 'shpark-rekognition' # put your own bucket here
KEY = ''

FEATURES_IGNORED = ('Landmarks', 'Pose', 'Quality', 'BoundingBox', 'Confidence', 'Beard', 'Mustache', 'EyesOpen', 'MouthOpen')

# https://docs.aws.amazon.com/ko_kr/rekognition/latest/dg/faces-detect-images.html
def detect_faces(bucket, key, attributes=['ALL'], region='ap-northeast-2'):
    client = boto3.client('rekognition', region)
    response = client.detect_faces(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key,
            }
        },
        Attributes=attributes,
    )

    return response['FaceDetails']


if __name__ == '__main__':
    KEY = sys.argv[1]
    print('File to check: ', KEY)

    upload_image(BUCKET, KEY)

    for face in detect_faces(BUCKET, KEY):
        # pprint.pprint(face)

        # facial features
        for feature, data in face.items():
            print(feature)
            if feature not in FEATURES_IGNORED:
                print('\n' + feature + ':')
                pprint.pprint(data)

        # save image
        text = []
        for emo in face['Emotions']:
            text.append("{Type:10}: {Confidence:5.2f}%\n".format(**emo))

        mark_face_image(KEY, face['BoundingBox'], text, fontsize=12, filename='output.png')

    delete_image(BUCKET, KEY)
