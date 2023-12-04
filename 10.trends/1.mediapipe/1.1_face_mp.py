import cv2
import mediapipe as mp

# MediaPipe 얼굴 감지 모듈 초기화
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection()

# 웹캠에서 영상을 받아오기
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # 이미지를 흑백으로 변환
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 얼굴 감지 수행
    results = face_detection.process(image_rgb)

    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(image, detection)

    # 영상 출력
    cv2.imshow('Face Detection', image)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 작업 완료 후 해제
cap.release()
cv2.destroyAllWindows()
