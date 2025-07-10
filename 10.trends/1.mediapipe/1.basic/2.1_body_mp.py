import cv2
import mediapipe as mp

# Mediapipe의 Pose 모듈 초기화
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# 웹캠으로부터 영상을 받아오기
cap = cv2.VideoCapture(0)

# Pose 모듈 초기화
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        # 이미지를 RGB 형식으로 변환
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Pose 감지 수행
        results = pose.process(image_rgb)

        if results.pose_landmarks:
            # 감지된 관절에 번호와 함께 표시
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
            )

        # 영상 출력
        cv2.imshow('Pose Detection', image)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# 작업 완료 후 해제
cap.release()
cv2.destroyAllWindows()
