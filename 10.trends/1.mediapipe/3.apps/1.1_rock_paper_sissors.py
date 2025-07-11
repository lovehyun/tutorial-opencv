
import cv2
import mediapipe as mp

# MediaPipe hands 초기화
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# 손가락 인덱스: 4(엄지), 8(검지), 12(중지), 16(약지), 20(새끼)
FINGER_TIPS = [4, 8, 12, 16, 20]

# 손가락 상태 판단 함수 (True: 펴짐, False: 접힘)
def get_finger_states(hand_landmarks):
    finger_states = []

    # 엄지: x좌표 비교
    thumb_tip = hand_landmarks.landmark[4]
    thumb_ip = hand_landmarks.landmark[3]
    finger_states.append(thumb_tip.x < thumb_ip.x)  # 오른손 기준

    # 나머지 손가락: tip이 pip보다 위에 있는지(y좌표가 작음)
    for tip_id in FINGER_TIPS[1:]:
        tip = hand_landmarks.landmark[tip_id]
        pip = hand_landmarks.landmark[tip_id - 2]
        finger_states.append(tip.y < pip.y)

    return finger_states  # [엄지, 검지, 중지, 약지, 새끼]

# 손 모양 판별
def classify_hand(finger_states):
    if finger_states == [False, False, False, False, False]:
        return "바위" # ✊
    elif finger_states == [False, True, True, False, False]:
        return "가위" # ✌️
    elif finger_states == [True, True, True, True, True]:
        return "보" # ✋
    else:
        return "판별불가" # 🤔


# 한글 출력용 -->
from PIL import ImageFont, ImageDraw, Image
import numpy as np

# 한글 글꼴 경로 (Windows 기준: 맑은고딕)
FONT_PATH = "C:/Windows/Fonts/malgun.ttf"  # 또는 원하는 .ttf 경로
FONT_SIZE = 40
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

# PIL로 한글을 이미지에 그리기
def draw_text_pil(img, text, position=(10, 50), color=(0, 255, 0)):
    # OpenCV → PIL 이미지 변환
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    draw.text(position, text, font=font, fill=color)
    # PIL → OpenCV 이미지 변환
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

# 한글 출력용 <--


# 웹캠 실행
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 좌우 반전 및 RGB 변환
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # 손가락 상태 분석 및 결과 표시
            finger_states = get_finger_states(hand_landmarks)
            gesture = classify_hand(finger_states)

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            # cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)
            frame = draw_text_pil(frame, gesture, position=(10, 50), color=(0, 255, 0))

    cv2.imshow("가위 바위 보 인식기", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC 키 종료
        break

cap.release()
cv2.destroyAllWindows()
