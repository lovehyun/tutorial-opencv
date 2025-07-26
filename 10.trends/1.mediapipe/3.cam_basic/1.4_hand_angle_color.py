import cv2, mediapipe as mp, time, math, os
import numpy as np
from datetime import datetime

# 초기화
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
hands    = mp_hands.Hands()
cap      = cv2.VideoCapture(0)
prev     = time.time()

show_landmarks = True

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
            
            # landmark show/hide 에 따라 표시
            if show_landmarks:
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

            # 각도에 따라 색상 결정
            if angle <= 45:
                arc_color = (0, 255, 0)       # 초록
            elif angle <= 90:
                arc_color = (0, 165, 255)     # 주황 (OpenCV의 주황 BGR값)
            else:
                arc_color = (0, 0, 255)       # 빨강

            # 부채꼴 시각화
            radius = 80
            start_rad = math.atan2(ty - cy, tx - cx)
            end_rad   = math.atan2(iy - cy, ix - cx)
            start_deg = math.degrees(start_rad)
            end_deg   = math.degrees(end_rad)

            # 각도를 0~360 범위로 정규화
            start_deg %= 360
            end_deg   %= 360

            # 시계 방향이 되도록 보정
            angle_diff = (end_deg - start_deg) % 360
            if angle_diff > 180: # 내각이 아니라 외각이 그려질 경우 180도 초과
                start_deg, end_deg = end_deg, start_deg  # 반대로
                angle_diff = (end_deg - start_deg) % 360

            # 부채꼴을 위한 오버레이 이미지 생성
            overlay = frame.copy()

            # OpenCV의 ellipse는 시작 각도가 시계방향이라 조정 필요
            cv2.ellipse(overlay, (cx, cy), (radius, radius),
                        0, start_deg, end_deg, arc_color, -1)

            # 오버레이와 원본 프레임 합성 (투명도 alpha 적용)
            alpha = 0.4  # 투명도 (0: 완전 투명, 1: 불투명)
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

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
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'): break  # ESC
    elif key == ord('c'):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{ts}.jpg"
        cv2.imwrite(filename, frame)
        print(f"[✓] Saved: {filename}")
    elif key == ord('d'):
        show_landmarks = not show_landmarks
        print("[INFO] Landmarks:", "ON" if show_landmarks else "OFF")

# 종료
cap.release()
cv2.destroyAllWindows()
hands.close()
