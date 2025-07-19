import cv2
import mediapipe as mp
import numpy as np

# MediaPipe 초기화
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=5)  # 여러 손 인식 허용
FINGER_TIPS = [4, 8, 12, 16, 20]

# 손가락 상태 판단
def get_finger_states(landmarks):
    finger_states = []
    finger_states.append(landmarks[4].x < landmarks[3].x)  # 엄지 (x축)
    for tip_id in FINGER_TIPS[1:]:  # 검지~새끼 (y축)
        tip = landmarks[tip_id]
        pip = landmarks[tip_id - 2]
        finger_states.append(tip.y < pip.y)
    return finger_states

# 손 모양 분류
def classify_hand(finger_states):
    if finger_states == [False, True, True, False, False]:
        return "Sissors"
    if finger_states == [False, False, False, False, False]:
        return "Rock"
    if finger_states == [True, True, True, True, True]:
        return "Paper"
    return "Other"

# 이미지 불러오기
img = cv2.imread("../../../Resources/Photos/hand_right_rps.jpg")
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
results = hands.process(rgb)

if results.multi_hand_landmarks:
    for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
        # 손가락 상태 및 결과 판단
        states = get_finger_states(hand_landmarks.landmark)
        result = classify_hand(states)

        # 손의 중심 좌표 계산 (평균)
        cx = int(np.mean([lm.x for lm in hand_landmarks.landmark]) * img.shape[1])
        cy = int(np.mean([lm.y for lm in hand_landmarks.landmark]) * img.shape[0])

        print(f"손 {idx+1} - 결과: {result}, 중심 위치: ({cx}, {cy})")

        # 시각화
        mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.putText(img, f"{result}", (cx - 40, cy - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
else:
    print("손이 감지되지 않았습니다.")

cv2.imshow("RPS Detection", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
