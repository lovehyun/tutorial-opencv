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
            log.info('Collection %s successfully created', collection_id)
    except ClientError as e:
        print(e)

# Delete a collection
def delete_collection(collection_id):
    client = boto3.client('rekognition')
    status_code=0
    try:
        resp = client.delete_collection(CollectionId=collection_id)
        status_code = resp['StatusCode']
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print('The collection ' + collection_id + ' was not found ')
        else:
            print('Error other than Not Found occurred: ' + e.response['Error']['Message'])
        status_code=e.response['ResponseMetadata']['HTTPStatusCode']
    
    return status_code

# List collections
def list_collections():
    client = boto3.client('rekognition')
    max_results = 10

    resp = client.list_collections(MaxResults=max_results)

    ret_colls = []
    ret_colls_count = 0
    done = False
    
    while done == False:
        collections = resp['CollectionIds']

        for collection in collections:
            ret_colls.append(collection)
            ret_colls_count += 1
        if 'NextToken' in resp:
            nextToken = resp['NextToken']
            resp = client.list_collections(NextToken=nextToken, MaxResults=max_results)
        else:
            done = True

    return ret_colls, ret_colls_count

# Add faces to collection
# https://docs.aws.amazon.com/ko_kr/rekognition/latest/dg/add-faces-to-collection-procedure.html
def add_faces_to_collection(bucket, photo, collection_id):
    client = boto3.client('rekognition')
    resp = client.index_faces(CollectionId=collection_id,
                              Image={'S3Object':{'Bucket':bucket,'Name':'faces/'+photo[0]}},
                              ExternalImageId=photo[0],
                              MaxFaces=1,
                              QualityFilter="AUTO",
                              DetectionAttributes=['ALL'])

    print('Results for ' + photo[0]) 	
    print('Faces indexed:')						
    for faceRecord in resp['FaceRecords']:
         print('  Face ID: ' + faceRecord['Face']['FaceId'])
         print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))
    print('Faces not indexed:')
    for unindexedFace in resp['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('   ' + reason)
    return len(resp['FaceRecords'])

# List faces in collection
def list_faces_in_collection(collection_id):
    max_results = 10

    client = boto3.client('rekognition')
    resp = client.list_faces(CollectionId=collection_id,
                            MaxResults=max_results)

    print('Faces in collection: ' + collection_id)

    ret_faces = []
    ret_faces_count = 0
    tokens = True

    while tokens:
        faces = resp['Faces']
        for face in faces:
            ret_faces.append(faces)
            ret_faces_count+=1
        if 'NextToken' in resp:
            nextToken = resp['NextToken']
            resp = client.list_faces(CollectionId=collection_id,
                                     NextToken=nextToken, MaxResults=max_results)
        else:
            tokens = False

    return ret_faces, ret_faces_count 

def delete_faces_from_collection(collection_id, faces):
    client = boto3.client('rekognition')

    resp = client.delete_faces(CollectionId=collection_id,
                               FaceIds=faces)
    
    print(str(len(resp['DeletedFaces'])) + ' faces deleted:') 							
    for faceId in resp['DeletedFaces']:
         print (faceId)
    return len(resp['DeletedFaces'])
  

if __name__ == '__main__':
    log.info('s3_wapper test')

    BUCKET = 'shpark-rekognition'

    # Step 1. Collections
    COLLECTION = 'my-faces'

    create_collection(COLLECTION)
    collection, _ = list_collections()
    print('Collctions: ', collection)

    # Step 2. Add photos
    faces, _ = list_faces_in_collection(COLLECTION)
    print(faces)

    images = [('shpark1.png', 'shpark'), 
              ('shpark2.jpg', 'shpark')]
    s3 = boto3.resource('s3')
    for image in images:
        file = open(image[0], 'rb')
        object = s3.Object(BUCKET, 'faces/'+image[0])
        resp = object.put(Body=file, Metadata={'FullName':image[1]})
        add_faces_to_collection(BUCKET, image, COLLECTION)

    faces, _ = list_faces_in_collection(COLLECTION)
    print(faces)

    # Step 3. Search face index

    # Step 4. Delete faces from collection
    # faces_tobe_deleted = [f['FaceId'] for f in faces[0]]
    # delete_faces_from_collection(COLLECTION, faces_tobe_deleted)

    # Step 5. Delete collection
    # delete_collection(COLLECTION)
