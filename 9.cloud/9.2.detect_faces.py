import boto3
import sys
import pprint
from s3_wrapper import upload_image, delete_image
from pil_wrapper import mark_face_image
from PIL import Image

BUCKET = 'shpark-rekognition' # put your own bucket here
KEY = ''

FEATURES_TO_PRINT = ('Emotions', 'Gender', 'AgeRange')

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

    # 여러 얼굴을 표시하기 위해 원본 이미지를 한 번만 열기
    image_with_all_faces = Image.open(KEY)

    # 모든 얼굴에 대해 경계 상자와 텍스트 표시
    for face in detect_faces(BUCKET, KEY):
        # print('---')
        # pprint.pprint(face)
        
        # facial features
        # for feature, data in face.items():
        #     # print(feature)
        #     if feature in FEATURES_TO_PRINT:
        #         print('\n' + feature + ':')
        #         pprint.pprint(data)

        text = ["{Type}: {Confidence:.2f}%".format(**emo) for emo in face['Emotions']]
        mark_face_image(KEY, face['BoundingBox'], text, filename=None, image=image_with_all_faces)

    # 모든 얼굴이 표시된 이미지 저장
    output_filename = 'output_with_all_faces.png'
    image_with_all_faces.save(output_filename)

    delete_image(BUCKET, KEY)
