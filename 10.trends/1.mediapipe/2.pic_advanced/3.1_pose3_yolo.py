# pip install ultralytics
from ultralytics import YOLO
import cv2
import mediapipe as mp

# 초기화
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

# 사람 감지용 HOG 설정
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# 이미지 읽기
img = cv2.imread("../../../Resources/Photos/fitness1.jpg")
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
h_img, w_img, _ = img.shape

# YOLOv8 모델 로드 (첫 실행 시 자동 다운로드됨)
model = YOLO("yolov8n.pt")  # 가장 가벼운 버전

# 사람 감지 (YOLO 추론 결과 얻기)
results = model(img)

# Pose 추정기
with mp_pose.Pose(static_image_mode=True) as pose:
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            if cls_id != 0:
                continue # 사람 클래스만
            
            # 바운딩 박스 좌표
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 2)  # 박스 표시

            # 사람 영역 자르기
            roi_rgb = rgb[y1:y2, x1:x2]
            result = pose.process(roi_rgb)

            if result.pose_landmarks:
                # 좌표를 원본 이미지 기준으로 조정
                for i, lm in enumerate(result.pose_landmarks.landmark):
                    x_lm = int(x1 + lm.x * (x2 - x1))
                    y_lm = int(y1 + lm.y * (y2 - y1))
                    cv2.circle(img, (x_lm, y_lm), 2, (0, 255, 0), -1)

                # ROI 내에 그리기 (원본 box 기준으로 맞추려면 직접 연결 필요)
                mp_draw.draw_landmarks(
                    img[y1:y2, x1:x2],
                    result.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2)
                )

# 결과 출력
cv2.imshow("Multiple Pose", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
