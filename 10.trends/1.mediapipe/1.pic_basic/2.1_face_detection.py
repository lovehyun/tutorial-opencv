import cv2, mediapipe as mp

mp_face  = mp.solutions.face_detection
mp_draw  = mp.solutions.drawing_utils

# img = cv2.imread("../../../Resources/Photos/lady.jpg")
img = cv2.imread("../../../Resources/Photos/group2.jpg")
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# model_selection=0, Short-range 모델, 가까운 얼굴 (웹캠, 셀카용) 감지에 최적화 (1m 이내 얼굴)
# model_selection=1, Full-range 모델, 멀리 있는 얼굴 감지 가능 (단체사진, 감시 카메라 등)
# with mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5) as fd:
with mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.5) as fd:

    res = fd.process(rgb)

if res.detections:
    for det in res.detections:
        mp_draw.draw_detection(img, det)

cv2.imshow("Face Detection", img)
cv2.waitKey(0); cv2.destroyAllWindows()
