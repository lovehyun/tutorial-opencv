import cv2, mediapipe as mp, time
mp_hands, mp_draw = mp.solutions.hands, mp.solutions.drawing_utils
cap, hands = cv2.VideoCapture(0), mp_hands.Hands()
prev = time.time()

while cap.isOpened():
    ok, frame = cap.read();  rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hlm in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hlm, mp_hands.HAND_CONNECTIONS)

    # FPS 계산
    curr = time.time()
    fps  = 1/(curr - prev)
    prev = curr
    cv2.putText(frame, f"{fps:0.1f} FPS",
                (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Hands + FPS", frame)
    if cv2.waitKey(1) & 0xFF == 27: break

cap.release(); cv2.destroyAllWindows(); hands.close()
