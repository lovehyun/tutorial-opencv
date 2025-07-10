
import cv2
import mediapipe as mp
import numpy as np
import time
from PIL import ImageFont, ImageDraw, Image

# 폰트 설정
FONT_KO = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 40)
FONT_EMOJI = ImageFont.truetype("C:/Windows/Fonts/seguiemj.ttf", 40)

# MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.5)

FINGER_TIPS = [4, 8, 12, 16, 20]

# 손가락 상태 판별
def get_finger_states(hand_landmarks, hand_label):
    finger_states = []
    if hand_label == "Right":
        finger_states.append(hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x)
    else:
        finger_states.append(hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x)
    for tip_id in FINGER_TIPS[1:]:
        tip = hand_landmarks.landmark[tip_id]
        pip = hand_landmarks.landmark[tip_id - 2]
        finger_states.append(tip.y < pip.y)
    return finger_states

# 손 모양 분류
def classify_hand(finger_states):
    if finger_states == [False, False, False, False, False]:
        return "rock", "✊"
    elif finger_states[1:3] == [True, True] and all(not f for f in finger_states[3:]):
        return "scissors", "✌️"
    elif all(finger_states):
        return "paper", "✋"
    else:
        return "unknown", "❓"

# 승자 판정
def judge(p1, p2):
    rules = {
        "rock": {"scissors": 1, "paper": -1, "rock": 0},
        "scissors": {"paper": 1, "rock": -1, "scissors": 0},
        "paper": {"rock": 1, "scissors": -1, "paper": 0}
    }
    return rules[p1][p2] if p1 in rules and p2 in rules else 0

# 텍스트 출력
def draw_text(img, text, pos, font, color=(0,255,0)):
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    draw.text(pos, text, font=font, fill=color)
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

# 초기 변수
score_left = 0
score_right = 0
cap = cv2.VideoCapture(0)

# 상태: countdown -> evaluate -> hold
phase = "countdown"
phase_start_time = time.time()
last_result = ("❓", "❓")
last_moves = ("unknown", "unknown")

countdown_duration = 5
hold_duration = 3

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 좌우 반전 (거울 모드)
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    
    # BGR → RGB로 변환 (MediaPipe는 RGB 사용)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # 손 인식 수행
    results = hands.process(rgb)

    # 손 인식 결과 저장 딕셔너리: {"Left": ("rock", "✊"), "Right": ("scissors", "✌️")}
    hand_info = {}
    if results.multi_handedness and results.multi_hand_landmarks:
        for i, handedness in enumerate(results.multi_handedness):
            label = handedness.classification[0].label
            hand_landmarks = results.multi_hand_landmarks[i]
            
            # 손가락 펴짐 여부 분석 → 가위/바위/보 분류
            finger_states = get_finger_states(hand_landmarks, label)
            move, symbol = classify_hand(finger_states)
            
            # 손 정보 저장
            hand_info[label] = (move, symbol)
            
            # 손 랜드마크 화면에 그리기
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # 현재 시각 및 phase 시작 후 경과 시간 계산
    now = time.time()
    elapsed = now - phase_start_time

    # 키보드 입력 감지
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC 키 → 종료
        break

    # ---------------------------
    # Phase 1: 카운트다운 단계
    # ---------------------------
    if phase == "countdown":
        remaining = int(countdown_duration - elapsed)
        frame = draw_text(frame, f"{remaining + 1}", (w//2 - 20, 50), FONT_KO)
        
        if elapsed >= countdown_duration:
            # 5초 카운트다운 끝나면 손 모양 분석 → 결과 판단
            left_move, left_result = hand_info.get("Left", ("unknown", "❓"))
            right_move, right_result = hand_info.get("Right", ("unknown", "❓"))
            
            # 승자 판단 (1: 왼쪽 승, -1: 오른쪽 승, 0: 무승부)
            result = judge(left_move, right_move)
            if result == 1:
                score_left += 1
            elif result == -1:
                score_right += 1
                
            # 결과 저장 (다음 단계에서 표시)
            last_result = (left_result, right_result)
            last_moves = (left_move, right_move)
            
            # 다음 단계로 전환: 결과 유지 단계
            phase = "hold"
            phase_start_time = now

    # ---------------------------
    # Phase 2: 결과 유지 단계
    # ---------------------------
    elif phase == "hold":
        # 화면 중앙에 결과 표시 ("✊ vs ✌️")
        frame = draw_text(frame, f"{last_result[0]} vs {last_result[1]}", (w//2 - 100, 50), FONT_EMOJI)

        # 왼쪽/오른쪽 플레이어의 손 모양 이모지
        frame = draw_text(frame, last_result[0], (50, 200), FONT_EMOJI)
        frame = draw_text(frame, last_result[1], (w - 100, 200), FONT_EMOJI)
        if elapsed >= hold_duration:
            # 결과 유지 시간(3초) 지나면 다시 카운트다운 시작
            phase = "countdown"
            phase_start_time = now

    # ---------------------------
    # 점수 표시 (항상 출력)
    # ---------------------------
    frame = draw_text(frame, f"Left: {score_left}", (50, h - 60), FONT_KO)
    frame = draw_text(frame, f"Right: {score_right}", (w - 200, h - 60), FONT_KO)

    # 최종적으로 화면 출력
    cv2.imshow("가위바위보 게임", frame)

cap.release()

cv2.destroyAllWindows()
