import cv2, mediapipe as mp
mp_hands, mp_draw = mp.solutions.hands, mp.solutions.drawing_utils

cap   = cv2.VideoCapture(0)
hands = mp_hands.Hands(      # 동영상용 기본 설정
          max_num_hands=2,
          min_detection_confidence=0.5,
          min_tracking_confidence=0.5)

while cap.isOpened():
    ok, frame = cap.read()
    if not ok: break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hlm in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hlm, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Webcam Hands", frame)
    if cv2.waitKey(1) & 0xFF == 27:   # ESC 키
        break

cap.release(); cv2.destroyAllWindows(); hands.close()
