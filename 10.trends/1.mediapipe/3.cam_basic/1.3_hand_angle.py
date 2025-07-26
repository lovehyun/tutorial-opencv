import cv2, mediapipe as mp, time, math
import numpy as np

# 초기화
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
hands    = mp_hands.Hands()
cap      = cv2.VideoCapture(0)
prev     = time.time()

def calc_angle(a, b, c):
    """∠abc 각도 계산 (radian → degree)"""
    ba = np.array([a.x - b.x, a.y - b.y])
    bc = np.array([c.x - b.x, c.y - b.y])
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)

while cap.isOpened():
    ok, frame = cap.read()
    if not ok: break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hlm in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hlm, mp_hands.HAND_CONNECTIONS)

            # 필요한 landmark 가져오기
            wrist = hlm.landmark[0]
            thumb_tip = hlm.landmark[4]
            index_tip = hlm.landmark[8]

            h, w, _ = frame.shape
            cx, cy = int(wrist.x * w), int(wrist.y * h)
            tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)
            ix, iy = int(index_tip.x * w), int(index_tip.y * h)

            # 선 그리기
            cv2.line(frame, (cx, cy), (tx, ty), (0, 255, 0), 2)
            cv2.line(frame, (cx, cy), (ix, iy), (0, 255, 0), 2)

            # 각도 계산
            angle = int(calc_angle(thumb_tip, wrist, index_tip))

            # 부채꼴 시각화
            radius = 80
            start_angle = int(math.degrees(math.atan2(ty - cy, tx - cx)))
            end_angle   = int(math.degrees(math.atan2(iy - cy, ix - cx)))
            
            # OpenCV의 ellipse는 시작 각도가 시계방향이라 조정 필요
            cv2.ellipse(frame, (cx, cy), (radius, radius),
                        0, start_angle, end_angle, (0, 255, 0), -1)

            # 각도 텍스트 표시
            cv2.putText(frame, f"{angle} deg", (cx + 10, cy - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # FPS 표시
    curr = time.time()
    fps = 1 / (curr - prev)
    prev = curr
    cv2.putText(frame, f"{fps:.1f} FPS", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("Thumb–Index Angle", frame)
    if cv2.waitKey(1) & 0xFF == 27: break

# 종료
cap.release()
cv2.destroyAllWindows()
hands.close()
