import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)
FINGER_TIPS = [4, 8, 12, 16, 20]
# MediaPipe는 아래처럼 21개의 landmark를 제공합니다:
# 엄지:   1(MCP) - 2 - 3(IP) - 4(TIP)
# 검지:   5(MCP) - 6 - 7(PIP) - 8(TIP)
# 중지:   9(MCP) -10 -11(PIP) -12(TIP)
# 약지:  13(MCP) -14 -15(PIP) -16(TIP)
# 새끼:  17(MCP) -18 -19(PIP) -20(TIP)

def get_finger_states(landmarks):
    finger_states = []
    
    # 엄지 (x축 기준): 오른손 기준으로 TIP.x < IP.x이면 펴짐(True)
    # - 펴진 엄지: TIP이 왼쪽 → landmarks[4].x < landmarks[3].x → True
    # - 접힌 엄지: TIP이 오른쪽 → landmarks[4].x > landmarks[3].x → False
    finger_states.append(landmarks[4].x < landmarks[3].x)
    
    # 나머지 손가락들 (검지, 중지, 약지, 새끼): y좌표 기준으로 펴짐 여부 판단
    for tip_id in FINGER_TIPS[1:]:  # [8, 12, 16, 20]
        # 나머지 손가락 (y축 기준): 손가락이 펴졌다면, TIP은 PIP보다 위에 있음 (y값이 더 작음)
        tip = landmarks[tip_id]           # TIP
        pip = landmarks[tip_id - 2]       # PIP (두 번째 마디)
        finger_states.append(tip.y < pip.y)  # TIP이 더 위에 있으면 펴진 것
        
    return finger_states  # ex: [True, True, False, False, False]

def classify_hand(finger_states):
    # 각 항목은 해당 손가락이 펴졌는지(True) 또는 접혔는지(False)를 나타냅니다.
    if finger_states == [False, True, True, False, False]:
        return "가위"
    if finger_states == [False, False, False, False, False]:
        return "바위"
    if finger_states == [True, True, True, True, True]:
        return "보"
    return "기타"

# 이미지 불러오기
img = cv2.imread("../../../Resources/Photos/hand_rps.jpg")
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
results = hands.process(rgb)

if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
        states = get_finger_states(hand_landmarks.landmark)
        result = classify_hand(states)
        print(f"결과: {result}")
else:
    print("손이 감지되지 않았습니다.")
