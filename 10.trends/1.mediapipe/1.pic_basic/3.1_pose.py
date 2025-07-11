import cv2
import mediapipe as mp

# 초기화
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

# 이미지 불러오기
img = cv2.imread("../../../Resources/Photos/fitness1.jpg")
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 포즈 감지기 생성
# mp_pose.Pose는 싱글-인스턴스(single person only) 모델입니다.
# 이미지에 여러 사람이 있어도, 내부 모델이 가장 명확하거나 중심에 가까운 사람 한 명만 추적합니다
with mp_pose.Pose(static_image_mode=True) as pose:
    result = pose.process(rgb)

# 결과 있으면 시각화
if result.pose_landmarks:
    mp_draw.draw_landmarks(
        img, 
        result.pose_landmarks, 
        mp_pose.POSE_CONNECTIONS,
        mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
        mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2)
    )

    # 좌표 출력 예시
    for i, lm in enumerate(result.pose_landmarks.landmark):
        h, w, _ = img.shape
        x, y = int(lm.x * w), int(lm.y * h)
        print(f"{i:2d}번 관절: x={x}, y={y}, z={lm.z:.3f}, visibility={lm.visibility:.2f}")

cv2.imshow("Pose Landmarks", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
