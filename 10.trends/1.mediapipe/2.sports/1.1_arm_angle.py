import cv2
import mediapipe as mp
import numpy as np
import math

# MediaPipe의 도구들 초기화
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    """
    세 점(a, b, c)을 기준으로 b를 꼭짓점으로 한 각도를 계산
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    # 코사인 법칙으로 각도 계산
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)

# 웹캠 열기
cap = cv2.VideoCapture(0)

# MediaPipe Pose 사용
with mp_pose.Pose(min_detection_confidence=0.5,
                  min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # 거울 모드
        h, w, _ = frame.shape

        # BGR -> RGB 변환 후 포즈 인식
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # 왼팔 관절
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * w,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * h]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * w,
                        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * h]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * w,
                        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * h]

            # 오른팔 관절
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * w,
                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * h]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * w,
                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * h]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x * w,
                        landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * h]

            # 왼팔 선 그리기 (초록색)
            cv2.line(frame, tuple(map(int, left_shoulder)), tuple(map(int, left_elbow)), (0, 255, 0), 3)
            cv2.line(frame, tuple(map(int, left_wrist)), tuple(map(int, left_elbow)), (0, 255, 0), 3)

            # 오른팔 선 그리기 (파란색)
            cv2.line(frame, tuple(map(int, right_shoulder)), tuple(map(int, right_elbow)), (255, 0, 0), 3)
            cv2.line(frame, tuple(map(int, right_wrist)), tuple(map(int, right_elbow)), (255, 0, 0), 3)


            # 각도 계산 및 표시
            left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
            right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

            cv2.putText(frame, f"{int(left_angle)} deg", tuple(map(int, left_elbow)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.putText(frame, f"{int(right_angle)} deg", tuple(map(int, right_elbow)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)


            # 전체 포즈 연결선 그리기
            # mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # 영상 출력
        cv2.imshow('팔 각도 인식', frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC 키로 종료
            break

cap.release()
cv2.destroyAllWindows()
