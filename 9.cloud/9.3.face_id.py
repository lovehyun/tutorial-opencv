import boto3
import sys
from s3_wrapper import upload_image, delete_image
from rekog_wrapper import list_collections, list_faces_in_collection

BUCKET = 'shpark-rekognition'
COLLECTION = 'my-faces'

# https://docs.aws.amazon.com/ko_kr/rekognition/latest/dg/API_CompareFaces.html
def compare_faces(bucket, key1, key2, threshold=50, region='ap-northeast-2'):
    client = boto3.client('rekognition', region)
    resp = client.compare_faces(
		SourceImage={
			'S3Object': {
				'Bucket': bucket,
				'Name': key1,
			}
		},
        TargetImage={
            'S3Object': {
                'Bucket': bucket,
                'Name': key2
            }
        },
        SimilarityThreshold=threshold,
    )

    return resp['SourceImageFace'], resp['FaceMatches']

# https://docs.aws.amazon.com/ko_kr/rekognition/latest/dg/API_SearchFacesByImage.html
def search_faces_by_image(bucket, key, collection, threshold=80, region='ap-northeast-2'):
    client = boto3.client('rekognition', region)
    print(key)
    resp = client.search_faces_by_image(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key,
            }
        },
        CollectionId=collection,
        FaceMatchThreshold=threshold,
    )
    return resp['FaceMatches']


def face_compare(KEY1, KEY2):
    upload_image(BUCKET, KEY1)
    upload_image(BUCKET, KEY2)

    src_face, matches = compare_faces(BUCKET, KEY1, KEY2)
    print('Source Face Confidence : {Confidence:.3f} %'.format(**src_face))
    if len(matches) == 0:
        print('No match found')
    else:
        for match in matches:
            print('Target Face Confidence : {Confidence:.3f} %'.format(**match['Face']))
            print('Similarity : {:.3f} %'.format(match['Similarity']))

    delete_image(BUCKET, KEY1)
    delete_image(BUCKET, KEY2)

def face_id(KEY1):
    # faces = list_faces_in_collection(COLLECTION)
    # print('Faces in collection: ', faces)

    upload_image(BUCKET, KEY1)

    faces = search_faces_by_image(BUCKET, KEY1, COLLECTION)
    if len(faces) == 0:
        print('Match not found')
    else:
        for face in faces:
            print('Matched Faces : {} %'.format(face['Similarity']))
            print('  FaceId : {}'.format(face['Face']['FaceId']))
            print('  ImageId : {}'.format(face['Face']['ExternalImageId']))

    delete_image(BUCKET, KEY1)


if __name__ == '__main__':
    OPTION = sys.argv[1]

    if OPTION == 'compare':
        KEY1 = sys.argv[2]
        KEY2 = sys.argv[3]
        print(KEY1, KEY2)
        face_compare(KEY1, KEY2)    
    elif OPTION == 'id':
        KEY1 = sys.argv[2]
        print(KEY1)
        face_id(KEY1)
    else:
        print('unknown option')
        exit(1)
