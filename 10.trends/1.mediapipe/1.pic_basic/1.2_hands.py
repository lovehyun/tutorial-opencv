import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# 이미지 읽기
img = cv2.imread("../../../Resources/Photos/hands.jpg")
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 여러 손 감지를 위한 설정
with mp_hands.Hands(static_image_mode=True, max_num_hands=5) as hands:
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hlm in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hlm, mp_hands.HAND_CONNECTIONS)

            for i, point in enumerate(hlm.landmark):
                print(f"손의 {i}번 랜드마크 → x:{point.x:.2f}, y:{point.y:.2f}, z:{point.z:.2f}")

cv2.imshow("Multiple Hands", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
