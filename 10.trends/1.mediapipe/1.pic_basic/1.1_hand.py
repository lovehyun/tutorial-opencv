import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# 이미지 읽기
img = cv2.imread("../../../Resources/Photos/hand.jpg")
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

with mp_hands.Hands(static_image_mode=True) as hands:  # 손 감지기
    results = hands.process(rgb)                       # 추론
    
    if results.multi_hand_landmarks:                   # 결과 확인
        hand_landmarks = results.multi_hand_landmarks[0]
        
        # 1. 주요 랜드마크 그리기
        mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        # 2. 주요 좌표값 출력
        for i, lm in enumerate(hand_landmarks.landmark):
            print(f"랜드마크 {i}: x={lm.x:.3f}, y={lm.y:.3f}, z={lm.z:.3f}")
            # x, y: 이미지의 가로/세로 비율 좌표 (0.0 ~ 1.0 사이)
            # z: 상대적인 깊이 (사진에서 직접 측정된 것이 아니라, MediaPipe가 '추정'(estimate)한 값)
            
        # 3. 손가락 끝 점들만 출력하기
        tip_ids = [4, 8, 12, 16, 20]  # 엄지~새끼손가락 끝
        for idx, i in enumerate(tip_ids):
            lm = hand_landmarks.landmark[i]
            # 픽셀로 변경
            h, w, _ = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            print(f"{i}번 손끝: x={cx:3d}, y={cy:3d}")
            
            # 이미지에 숫자 1~5 쓰기
            cv2.putText(img, str(idx + 1), (cx, cy),
                cv2.FONT_HERSHEY_SIMPLEX,     # 글꼴
                1,                            # 글자 크기
                (0, 0, 255),                  # 글자 색 (빨강)
                2)                            # 두께


cv2.imshow("Hand Landmarks", img)
cv2.waitKey(0); cv2.destroyAllWindows()
