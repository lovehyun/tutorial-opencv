"""
mediapipe_quickstart.py
웹캠으로 손·얼굴·포즈 랜드마크를 동시에 시각화하는 기초 예제
"""
import cv2
import mediapipe as mp
import time

# ---------- 초기화 ----------
mp_drawing = mp.solutions.drawing_utils
mp_hands   = mp.solutions.hands
mp_face    = mp.solutions.face_detection
mp_pose    = mp.solutions.pose

# 각 솔루션 인스턴스(성능/정확도 균형 기본값)
hands = mp_hands.Hands(model_complexity=0,
                       max_num_hands=2,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)

face  = mp_face.FaceDetection(model_selection=0,
                              min_detection_confidence=0.5)

pose  = mp_pose.Pose(model_complexity=1,
                     enable_segmentation=False)

# ---------- 웹캠 루프 ----------
cap = cv2.VideoCapture(0)
prev = time.time()

while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
        print("❌  웹캠 프레임을 읽을 수 없습니다.")
        break

    # MediaPipe는 RGB 이미지를 기대하므로 변환
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 1) Hands
    hand_results = hands.process(rgb)
    if hand_results.multi_hand_landmarks:
        for hlm in hand_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hlm, mp_hands.HAND_CONNECTIONS)

    # 2) Face Detection
    face_results = face.process(rgb)
    if face_results.detections:
        for det in face_results.detections:
            mp_drawing.draw_detection(frame, det)

    # 3) Pose
    pose_results = pose.process(rgb)
    if pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame,
            pose_results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS)

    # FPS 계산 & 표시
    curr = time.time()
    fps  = 1 / (curr - prev)
    prev = curr
    cv2.putText(frame, f"FPS: {fps:0.1f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # 창에 출력
    cv2.imshow("MediaPipe Quickstart", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC 키
        break

# ---------- 정리 ----------
cap.release()
cv2.destroyAllWindows()
hands.close()
face.close()
pose.close()
