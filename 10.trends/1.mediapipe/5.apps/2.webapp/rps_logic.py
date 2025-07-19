# rps_logic.py
import cv2, mediapipe as mp, numpy as np, time
from PIL import ImageFont, ImageDraw, Image

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.5)

FINGER_TIPS = [4, 8, 12, 16, 20]

def classify(vector):
    # finger_states 로부터 "rock"/"paper"/"scissors"
    if vector == [False]*5:
        return "rock", "✊"
    if vector[1:3] == [True, True] and vector[3:] == [False, False]:
        return "scissors", "✌️"
    if all(vector):
        return "paper", "✋"
    return "unknown", "❓"

def infer_rps(bgr):
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)
    moves = {}
    if res.multi_handedness and res.multi_hand_landmarks:
        for i, h in enumerate(res.multi_handedness):
            label  = h.classification[0].label  # "Left"/"Right"
            lm     = res.multi_hand_landmarks[i]
            finger = []
            # 엄지
            if label == "Right":
                finger.append(lm.landmark[4].x < lm.landmark[3].x)
            else:
                finger.append(lm.landmark[4].x > lm.landmark[3].x)
            # 나머지 손가락
            for tip in FINGER_TIPS[1:]:
                finger.append(lm.landmark[tip].y < lm.landmark[tip-2].y)
            moves[label] = classify(finger)
    return moves  # {"Left":("rock","✊"), ...}
