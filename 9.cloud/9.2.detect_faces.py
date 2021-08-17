import boto3
import sys
import pprint

BUCKET = "shpark-rekognition"
KEY = ""

FEATURES_IGNORED = ("Landmarks", "Pose", "Quality", "BoundingBox", "Confidence", "Beard", "Mustache", "EyesOpen", "MouthOpen")

def detect_faces(bucket, key, attributes=['ALL'], region="ap-northeast-2"):
    client = boto3.client("rekognition", region)
    response = client.detect_faces(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": key,
            }
        },
        Attributes=attributes,
    )

    return response['FaceDetails']


if __name__ == "__main__":
    KEY = sys.argv[1]
    print(KEY)

    for face in detect_faces(BUCKET, KEY):
        # pprint.pprint(face)

        # facial features
        for feature, data in face.items():
            if feature not in FEATURES_IGNORED:
                print("\n" + feature + ":")
                pprint.pprint(data)
