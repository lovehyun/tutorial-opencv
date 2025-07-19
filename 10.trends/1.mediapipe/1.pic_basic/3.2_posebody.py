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
        h, w, _ = img.shape
        landmarks = result.pose_landmarks.landmark

        # 얼굴이 아닌 몸통 관절 인덱스만 추출 (9번 이상)
        # body_idxs = list(range(9, 33))
        body_idxs = list(range(11, 33))

        # 연결선도 얼굴 제외하고 그리기
        for conn in mp_pose.POSE_CONNECTIONS:
            if conn[0] in body_idxs and conn[1] in body_idxs:
                x1, y1 = int(landmarks[conn[0]].x * w), int(landmarks[conn[0]].y * h)
                x2, y2 = int(landmarks[conn[1]].x * w), int(landmarks[conn[1]].y * h)
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # 관절 점 그리기 (몸통만)
        for i in body_idxs:
            cx, cy = int(landmarks[i].x * w), int(landmarks[i].y * h)
            cv2.circle(img, (cx, cy), 4, (0, 0, 255), -1)

        # 좌표 출력 예시
        # ------------------ 좌표 출력 ------------------
        print("몸통·팔다리 관절 좌표 (총", len(body_idxs), "개)")
        for i in body_idxs:
            lm = landmarks[i]
            x_px, y_px = int(lm.x * w), int(lm.y * h)
            print(f"{i:2d}번: x={x_px:4d}, y={y_px:4d}, z={lm.z:+.3f}, vis={lm.visibility:.2f}")

# MediaPipe Pose는 기본적으로 얼굴 일부도 함께 포함된 "33개 포인트"를 제공합니다.
# 그래서 아무 설정 안 하면 얼굴(눈, 코, 귀 등) 도 같이 잡혀서 나오는 겁니다.
# 관절 번호	부위
# 0	코 (nose)
# 1, 2	좌우 눈 내부
# 3, 4	좌우 눈 외부
# 5, 6	좌우 귀
# 7, 8	입 좌/우
#  추가로 9, 10까지 제거 시 턱 부위도 사라짐

cv2.imshow("Pose Landmarks", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
