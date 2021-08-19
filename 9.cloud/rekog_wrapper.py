# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html
import boto3
from botocore.exceptions import ClientError
from log_wrapper import log


# Create a collection
# https://docs.aws.amazon.com/ko_kr/rekognition/latest/dg/create-collection-procedure.html
def create_collection(collection_id):
    client = boto3.client('rekognition')

    # Create a collection
    try:
        resp = client.create_collection(CollectionId=collection_id)
        print('Collection ARN: ' + resp['CollectionArn'])
        if resp['StatusCode'] == 200:
            log.info("Collection '%s' created", collection_id)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
            log.info("Collection '%s' already exists", collection_id)
        else:
            log.error("Collection '%s' creation failed: ", collection_id, e.response['Error']['Code'])
            # print(e)


# Delete a collection
# https://docs.aws.amazon.com/ko_kr/rekognition/latest/dg/delete-collection-procedure.html
def delete_collection(collection_id):
    client = boto3.client('rekognition')

    try:
        resp = client.delete_collection(CollectionId=collection_id)
        log.info("Collection '%s' deleted, resp: %d", collection_id, resp['StatusCode'])

    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            log.info("Collection '%s' was not found", collection_id)
        else:
            log.error("Collection '%s' deletion failed: ", e.response['Error']['Code'])
    

# List collections
# https://docs.aws.amazon.com/ko_kr/rekognition/latest/dg/list-collection-procedure.html
def list_collections():
    client = boto3.client('rekognition')
    max_results = 10

    resp = client.list_collections(MaxResults=max_results)

    ret_colls = []
    ret_colls_count = 0
 
    while True:
        collections = resp['CollectionIds']

        for collection in collections:
            ret_colls.append(collection)
            ret_colls_count += 1
        if 'NextToken' in resp:
            nextToken = resp['NextToken']
            resp = client.list_collections(NextToken=nextToken, MaxResults=max_results)
        else:
            break

    return ret_colls, ret_colls_count

# Add faces to collection
# https://docs.aws.amazon.com/ko_kr/rekognition/latest/dg/add-faces-to-collection-procedure.html
def add_faces_to_collection(bucket, photo, collection_id, path=''):
    client = boto3.client('rekognition')

    resp = client.index_faces(CollectionId=collection_id,
                              Image={'S3Object':{'Bucket':bucket,'Name':path+photo}},
                              ExternalImageId=photo,
                              MaxFaces=1,
                              QualityFilter="AUTO",
                              DetectionAttributes=['ALL'])
    for faceRecord in resp['FaceRecords']:
        face_id = faceRecord['Face']['FaceId']
        location = faceRecord['Face']['BoundingBox']
        log.info("Face in '%s' indexed: %s, %s", path+photo, face_id, location)

    for unindexedFace in resp['UnindexedFaces']:
        location = unindexedFace['FaceDetail']['BoundingBox']
        message = ''
        for reason in unindexedFace['Reasons']:
            message += reason + '. '
        
        log.warn("Face in '%s' NOT indexed: %s, %s", location, message)

    return len(resp['FaceRecords'])

# List faces in collection
# https://docs.aws.amazon.com/ko_kr/rekognition/latest/dg/list-faces-in-collection-procedure.html
def list_faces_in_collection(collection_id):
    max_results = 10

    client = boto3.client('rekognition')
    resp = client.list_faces(CollectionId=collection_id, MaxResults=max_results)

    ret_faces = []
    ret_faces_count = 0
    tokens = True

    while tokens:
        faces = resp['Faces']
        for face in faces:
            ret_faces.append(face)
            ret_faces_count+=1
        if 'NextToken' in resp:
            nextToken = resp['NextToken']
            resp = client.list_faces(CollectionId=collection_id,
                                     NextToken=nextToken, MaxResults=max_results)
        else:
            tokens = False

    return ret_faces, ret_faces_count 

# Delete faces in collection
# https://docs.aws.amazon.com/ko_kr/rekognition/latest/dg/delete-faces-procedure.html
def delete_faces_from_collection(collection_id, faces):
    client = boto3.client('rekognition')

    resp = client.delete_faces(CollectionId=collection_id, FaceIds=faces)
							
    for faceId in resp['DeletedFaces']:
        log.info("Face '%s' deleted", faceId)

    return len(resp['DeletedFaces'])

# MAIN function
if __name__ == '__main__':
    log.info('s3_wapper test')

    BUCKET = 'shpark-rekognition'

    # Step 1. Collections
    COLLECTION = 'my-faces'

    create_collection(COLLECTION)
    collection, _ = list_collections()
    print('Collections: ', collection)

    # Step 2. Add photos
    faces, _ = list_faces_in_collection(COLLECTION)
    for face in faces:
        print("FaceId: {FaceId}, ExternalImageId: {ExternalImageId}, Confidence: {Confidence:.3f}%".format(**face))

    path = 'faces/'
    images = [('shpark1.png', 'shpark'), 
              ('shpark2.jpg', 'shpark')]

    # Step 2-1. Upload photos to S3
    s3 = boto3.resource('s3')
    for image in images:
        file = open(image[0], 'rb')
        object = s3.Object(BUCKET, path+image[0])
        object.put(Body=file, Metadata={'FullName':image[1]})
        add_faces_to_collection(BUCKET, image[0], COLLECTION, path=path)

    faces, _ = list_faces_in_collection(COLLECTION)
    for face in faces:
        print("FaceId: {FaceId}, ExternalImageId: {ExternalImageId}, Confidence: {Confidence:.3f}%".format(**face))

    # Step 3. Search face index
    # Not Implemented Here

    # Step 4. Delete faces from collection
    # faces_tobe_deleted = [f['FaceId'] for f in faces]
    # delete_faces_from_collection(COLLECTION, faces_tobe_deleted)

    # Step 5. Delete collection
    # delete_collection(COLLECTION)
