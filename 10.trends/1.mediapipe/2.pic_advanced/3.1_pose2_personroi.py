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

# 사람 감지
boxes, _ = hog.detectMultiScale(img, winStride=(8,8))

# Pose 추정기
with mp_pose.Pose(static_image_mode=True) as pose:
    for (x, y, w, h) in boxes:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)

        roi = rgb[y:y+h, x:x+w]
        result = pose.process(roi)

        if result.pose_landmarks:
            # 좌표를 원본 이미지 기준으로 조정
            for i, lm in enumerate(result.pose_landmarks.landmark):
                x_lm = int(x + lm.x * w)
                y_lm = int(y + lm.y * h)
                cv2.circle(img, (x_lm, y_lm), 2, (0, 255, 0), -1)

            mp_draw.draw_landmarks(
                img[y:y+h, x:x+w],  # 잘라낸 부분에만 시각화
                result.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2)
            )

# 결과 출력
cv2.imshow("Multiple Pose", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
