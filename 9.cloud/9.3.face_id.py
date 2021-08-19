import boto3
import sys

from s3_wrapper import upload_image, delete_image
from rekog_wrapper import list_faces_in_collection
from pil_wrapper import mark_face_image, merge_two_images

BUCKET = 'shpark-rekognition'
COLLECTION = 'my-faces'

# https://docs.aws.amazon.com/ko_kr/rekognition/latest/dg/faces-detect-images.html
def detect_faces(bucket, key, attributes=['ALL'], region='ap-northeast-2'):
    client = boto3.client('rekognition', region)
    resp = client.detect_faces(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key,
            }
        },
        Attributes=attributes,
    )

    return resp['FaceDetails']

# https://docs.aws.amazon.com/ko_kr/rekognition/latest/dg/API_CompareFaces.html
# https://docs.aws.amazon.com/ko_kr/rekognition/latest/dg/faces-comparefaces.html
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
def search_faces_by_image(bucket, key, collection, threshold=70, region='ap-northeast-2'):
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

def face_compare(image1, image2):
    upload_image(BUCKET, image1)
    upload_image(BUCKET, image2)

    src_face, matches = compare_faces(BUCKET, image1, image2)
    print('Source Face Confidence : {Confidence:.3f}%, location: {BoundingBox}'.format(**src_face))
    image1_location = src_face['BoundingBox']
    image1_marked = mark_face_image(image1, image1_location, 'match1.png')

    if len(matches) == 0:
        print('No match found')
    else:
        for match in matches:
            print('Target Face Confidence : {Confidence:.3f}%, Location: {BoundingBox}'.format(**match['Face']))
            print('Similarity : {:.3f} %'.format(match['Similarity']))
            similarity = 'Similarity: {:.3f}%'.format(match['Similarity'])
            image2_location = match['Face']['BoundingBox']
            image2_marked = mark_face_image(image2, image2_location, 'match2.png')
            merge_two_images(image1_marked, image1_location, image2_marked, image2_location, similarity)

    delete_image(BUCKET, image1)
    delete_image(BUCKET, image2)

def face_id(image, collection):
    upload_image(BUCKET, image)
    faces = detect_faces(BUCKET, image, attributes=["DEFAULT"])
    print('Checking %d faces' % len(faces))

    for idx, face in enumerate(faces):
        filename = 'output%d.jpg' % idx
        mark_face_image(image, face['BoundingBox'], filename, crop=True)
        upload_image(BUCKET, filename)

        faces = search_faces_by_image(BUCKET, filename, collection)
        if len(faces) == 0:
            print('Match not found')
        else:
            for face in faces:
                print('Matched Faces : {}%'.format(face['Similarity']))
                print('  FaceId : {}'.format(face['Face']['FaceId']))
                print('  ImageId : {}'.format(face['Face']['ExternalImageId']))

        delete_image(BUCKET, filename)

    delete_image(BUCKET, image)


if __name__ == '__main__':
    try:
        OPTION = sys.argv[1]
    except IndexError:
        print('No option given')
        exit(1)

    if OPTION == 'compare':
        image1 = sys.argv[2]
        KEY2 = sys.argv[3]
        print(image1, KEY2)
        face_compare(image1, KEY2)    
    elif OPTION == 'id':
        image1 = sys.argv[2]
        print(image1)
        face_id(image1, COLLECTION)
    elif OPTION == 'list':
        faces, _ = list_faces_in_collection(COLLECTION)
        for face in faces:
            print(face)
    else:
        print('unknown option')
        exit(1)
