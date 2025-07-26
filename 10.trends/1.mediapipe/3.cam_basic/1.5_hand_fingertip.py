import cv2, mediapipe as mp, time, math
import numpy as np
from datetime import datetime

# ─── Settings ───
ZOOM_ACTIVATE_MIN = 40
ZOOM_ACTIVATE_MAX = 60
ZOOM_DEACTIVATE_THRESHOLD = 20
ZOOM_HOLD_DURATION = 1.0
ZOOM_MIN, ZOOM_MAX = 1.0, 3.0

# ─── State Variables ───
pinch_zoom_mode = False
zoom_active = False
zoom_hold_start = None
zoom_factor = 1.0
initial_pinch_distance = None
show_landmarks = True

# ─── Init ───
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2)
cap = cv2.VideoCapture(0)
prev_time = time.time()

# ─── Utilities ───
def draw_fps(frame, fps):
    cv2.putText(frame, f"{fps:.1f} FPS", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

def draw_status_text(frame, enabled, zoom):
    status = f"Pinch Mode: {'ON' if enabled else 'OFF'} / Zoom: {'ON' if zoom_active else 'OFF'}"
    color = (0, 255, 0) if enabled else (100, 100, 100)
    cv2.putText(frame, status, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    cv2.putText(frame, f"Zoom: {zoom_factor:.2f}x", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

def draw_dotted_line(img, pt1, pt2, color=(0, 255, 0), thickness=2, gap=10):
    dist = math.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1])
    pts = []
    for i in np.arange(0, dist, gap):
        r = i / dist
        x = int(pt1[0] * (1 - r) + pt2[0] * r)
        y = int(pt1[1] * (1 - r) + pt2[1] * r)
        pts.append((x, y))
    for i in range(0, len(pts) - 1, 2):
        cv2.line(img, pts[i], pts[i + 1], color, thickness)

def draw_transparent_circle(img, center, radius=50, color=(0, 255, 255), alpha=0.4):
    overlay = img.copy()
    cv2.circle(overlay, center, radius, color, -1)
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

def get_landmark_tip_coords(landmark, indices, shape):
    h, w = shape[:2]
    return [(int(landmark[i].x * w), int(landmark[i].y * h)) for i in indices]

# ─── Zoom Renderer ───
def apply_zoom(frame, zoom):
    if zoom == 1.0:
        return frame
    h, w = frame.shape[:2]
    center = (w // 2, h // 2)
    nw, nh = int(w / zoom), int(h / zoom)
    x1, y1 = center[0] - nw // 2, center[1] - nh // 2
    x2, y2 = x1 + nw, y1 + nh
    cropped = frame[y1:y2, x1:x2]
    return cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)

# ─── Core Features ───
def process_index_distance(frame, hand_list):
    if len(hand_list) == 2:
        pt1 = get_landmark_tip_coords(hand_list[0].landmark, [8], frame.shape)[0]
        pt2 = get_landmark_tip_coords(hand_list[1].landmark, [8], frame.shape)[0]
        dist = math.hypot(pt1[0] - pt2[0], pt1[1] - pt2[1])
        mid = ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2)
        cv2.circle(frame, pt1, 8, (255, 0, 0), -1)
        cv2.circle(frame, pt2, 8, (255, 0, 0), -1)
        draw_dotted_line(frame, pt1, pt2)
        cv2.putText(frame, f"{dist:.1f}px", (mid[0] + 10, mid[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

def process_pinch_zoom(frame, hand_list):
    global zoom_factor, initial_pinch_distance, zoom_hold_start, zoom_active

    if len(hand_list) == 0:
        zoom_hold_start = None
        return

    hand = hand_list[0]
    thumb, index = get_landmark_tip_coords(hand.landmark, [4, 8], frame.shape)
    current_distance = math.hypot(index[0] - thumb[0], index[1] - thumb[1])
    mid = ((thumb[0] + index[0]) // 2, (thumb[1] + index[1]) // 2)

    # 엄지와 검지에 파란 원
    cv2.circle(frame, thumb, 8, (255, 0, 0), -1)
    cv2.circle(frame, index, 8, (255, 0, 0), -1)
    # 엄지와 검지를 잇는 파란 선
    cv2.line(frame, thumb, index, (255, 0, 0), 2)
    # 거리 텍스트 표시
    cv2.putText(frame, f"{current_distance:.1f}px", (mid[0] + 10, mid[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    
    if zoom_active:
        if current_distance < ZOOM_DEACTIVATE_THRESHOLD:
            if zoom_hold_start is None:
                zoom_hold_start = time.time()
            elif time.time() - zoom_hold_start > ZOOM_HOLD_DURATION:
                zoom_active = False
                initial_pinch_distance = None
                print("[✘] Zoom Deactivated")
        else:
            zoom_hold_start = None
            if initial_pinch_distance is None:
                initial_pinch_distance = current_distance
            ratio = current_distance / initial_pinch_distance
            zoom_factor = np.clip(ratio, ZOOM_MIN, ZOOM_MAX)
            draw_transparent_circle(frame, mid, radius=60, color=(0, 255, 255), alpha=0.3)
            cv2.putText(frame, f"{current_distance:.1f}px", (mid[0] + 10, mid[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    else:
        if ZOOM_ACTIVATE_MIN <= current_distance <= ZOOM_ACTIVATE_MAX:
            if zoom_hold_start is None:
                zoom_hold_start = time.time()
            elif time.time() - zoom_hold_start > ZOOM_HOLD_DURATION:
                zoom_active = True
                initial_pinch_distance = current_distance
                print("[✔] Zoom Activated")
        else:
            zoom_hold_start = None
        # 항상 거리 표시
        cv2.putText(frame, f"{current_distance:.1f}px", (mid[0] + 10, mid[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

# ─── Main Loop ───
while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
        break
    frame = cv2.flip(frame, 1)
    raw_frame = frame.copy()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    hand_list = results.multi_hand_landmarks if results.multi_hand_landmarks else []

    if pinch_zoom_mode:
        process_pinch_zoom(frame, hand_list)
    else:
        process_index_distance(frame, hand_list)

    if show_landmarks:
        for hlm in hand_list:
            mp.solutions.drawing_utils.draw_landmarks(frame, hlm, mp_hands.HAND_CONNECTIONS)

    frame = apply_zoom(frame, zoom_factor)

    now = time.time()
    fps = 1 / (now - prev_time)
    prev_time = now

    draw_fps(frame, fps)
    draw_status_text(frame, pinch_zoom_mode, zoom_active)

    cv2.imshow("Zoom Hand Tracker", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('h'):
        print("""
[ 도움말 ]
 - q 또는 ESC : 종료
 - c : 현재 화면 캡처
 - p : 핀치 줌 모드 ON/OFF 전환
 - d : 손가락 랜드마크 ON/OFF
 - r : 줌 배율 초기화
 - 핀치 모드는 키보드로만 ON/OFF 가능합니다.
 - 핀치 모드 중에는 엄지-검지 사이 거리가 40~60px에서 1초 이상 유지되면 줌이 활성화됩니다.
   반대로 20px 이하에서 1초 이상 유지되면 줌이 비활성화됩니다.
""")
    elif key == ord('q') or key == 27:
        break
    elif key == ord('c'):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{ts}.jpg"
        cv2.imwrite(filename, raw_frame)
        print(f"[✓] Saved: {filename}")
    elif key == ord('p'):
        pinch_zoom_mode = not pinch_zoom_mode
        zoom_hold_start = None
        initial_pinch_distance = None
        zoom_active = False
        print(f"[INFO] Pinch Mode {'ON' if pinch_zoom_mode else 'OFF'}")
    elif key == ord('d'):
        show_landmarks = not show_landmarks
    elif key == ord('r'):
        zoom_factor = 1.0
        initial_pinch_distance = None
        print("[↺] Zoom Reset")

# ─── Cleanup ───
cap.release()
cv2.destroyAllWindows()
hands.close()
