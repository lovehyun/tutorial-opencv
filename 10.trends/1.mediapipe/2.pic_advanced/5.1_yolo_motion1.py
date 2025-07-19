# pip install ultralytics opencv-python mediapipe

import cv2
from ultralytics import YOLO
import mediapipe as mp

# 초기화
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
model = YOLO("yolov8n.pt")  # 가장 가벼운 모델

# 오른팔 올림 판단 함수
def is_right_arm_raised(landmarks):
    rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    re = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
    rw = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
    return rw.y < rs.y and re.y < rs.y

# 웹캠 시작
cap = cv2.VideoCapture(0)

# Mediapipe Pose 객체
with mp_pose.Pose(static_image_mode=True) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h_img, w_img, _ = frame.shape

        # YOLO로 사람 감지
        results = model(frame)

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                if cls_id != 0:
                    continue  # 사람만 처리

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)

                # 박스 내 사람 영역만 골라내기
                roi_rgb = rgb[y1:y2, x1:x2]
                result = pose.process(roi_rgb)

                if result.pose_landmarks:
                    for lm in result.pose_landmarks.landmark:
                        cx = int(x1 + lm.x * (x2 - x1))
                        cy = int(y1 + lm.y * (y2 - y1))
                        cv2.circle(frame, (cx, cy), 2, (0, 255, 0), -1)

                    # 행동 인식
                    if is_right_arm_raised(result.pose_landmarks.landmark):
                        label = "Right Arm Raised"
                        color = (0, 0, 255)
                    else:
                        label = "Arm Down"
                        color = (255, 0, 0)

                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow("Webcam Action Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
