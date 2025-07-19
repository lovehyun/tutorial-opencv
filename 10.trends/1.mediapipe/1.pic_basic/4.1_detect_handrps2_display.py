import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.7)
FINGER_TIPS = [4, 8, 12, 16, 20]

def draw_landmarks_and_bbox(image, hand_landmarks):
    """손 랜드마크와 바운딩 박스를 그려주는 함수"""
    h, w, _ = image.shape
    
    # 랜드마크 그리기
    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    # 바운딩 박스 계산
    x_coords = [landmark.x * w for landmark in hand_landmarks.landmark]
    y_coords = [landmark.y * h for landmark in hand_landmarks.landmark]
    
    x_min, x_max = int(min(x_coords)), int(max(x_coords))
    y_min, y_max = int(min(y_coords)), int(max(y_coords))
    
    # 바운딩 박스 그리기 (여유 공간 추가)
    padding = 20
    x_min = max(0, x_min - padding)
    y_min = max(0, y_min - padding)  
    x_max = min(w, x_max + padding)
    y_max = min(h, y_max + padding)
    
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
    
    # 주요 포인트에 번호 표시
    important_points = [0, 4, 8, 12, 16, 20]  # 손목, 각 손가락 끝
    point_names = ['손목', '엄지', '검지', '중지', '약지', '새끼']
    
    for i, (point_idx, name) in enumerate(zip(important_points, point_names)):
        landmark = hand_landmarks.landmark[point_idx]
        x, y = int(landmark.x * w), int(landmark.y * h)
        cv2.circle(image, (x, y), 8, (255, 0, 0), -1)
        cv2.putText(image, f"{point_idx}({name})", (x+10, y-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    return image

def get_finger_states(landmarks):
    finger_states = []
    
    # 엄지 판단 (더 정확하게)
    # 엄지가 펴져있으면: TIP이 손목 쪽에서 더 멀리 있음
    thumb_tip = landmarks[4]
    thumb_ip = landmarks[3]
    thumb_mcp = landmarks[2]
    
    # 엄지가 펴졌는지 판단: TIP이 MCP보다 손목에서 더 멀리 있으면 펴진 것
    wrist = landmarks[0]
    thumb_tip_dist = ((thumb_tip.x - wrist.x)**2 + (thumb_tip.y - wrist.y)**2)**0.5
    thumb_mcp_dist = ((thumb_mcp.x - wrist.x)**2 + (thumb_mcp.y - wrist.y)**2)**0.5
    thumb_extended = thumb_tip_dist > thumb_mcp_dist
    finger_states.append(thumb_extended)
    
    # 나머지 손가락들: TIP이 PIP보다 위에(y값이 작으면) 펴진 것
    for tip_id in FINGER_TIPS[1:]:  # [8, 12, 16, 20]
        tip = landmarks[tip_id]       # 손가락 끝
        pip = landmarks[tip_id - 2]   # 두번째 관절
        finger_extended = tip.y < pip.y  # 끝이 관절보다 위에 있으면 펴진 것
        finger_states.append(finger_extended)
        
    return finger_states

def classify_hand(finger_states):
    # 디버깅을 위해 손가락 상태를 출력
    finger_names = ["엄지", "검지", "중지", "약지", "새끼"]
    print("손가락 상태:")
    for i, (name, state) in enumerate(zip(finger_names, finger_states)):
        print(f"  {name}: {'펴짐' if state else '접힘'}")
    print(f"패턴: {finger_states}")
    
    # 가위바위보 판단
    if finger_states == [False, True, True, False, False]:
        return "가위"
    elif finger_states == [False, False, False, False, False]:
        return "바위"  
    elif finger_states == [True, True, True, True, True]:
        return "보"
    else:
        # 유사한 패턴도 체크해보기
        extended_count = sum(finger_states)
        print(f"펴진 손가락 개수: {extended_count}")
        
        # 가위 변형 (엄지가 살짝 펴져있을 수 있음)
        if finger_states[1] and finger_states[2] and not finger_states[3] and not finger_states[4]:
            return "가위 (변형)"
        # 보 변형 (엄지가 접혀있을 수 있음) 
        elif extended_count >= 4 and finger_states[1] and finger_states[2] and finger_states[3] and finger_states[4]:
            return "보 (변형)"
        # 바위 변형
        elif extended_count <= 1:
            return "바위 (변형)"
            
        return f"기타 (펴진 손가락: {extended_count}개)"

# 이미지 불러오기
img_path = "../../../Resources/Photos/hand_rps.jpg"
print(f"이미지 경로: {img_path}")

img = cv2.imread(img_path)
if img is None:
    print("이미지를 불러올 수 없습니다. 경로를 확인하세요.")
    exit()

print(f"이미지 크기: {img.shape}")
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
results = hands.process(rgb)

if results.multi_hand_landmarks:
    print("손 감지됨!")
    for hand_landmarks in results.multi_hand_landmarks:
        # 랜드마크 좌표 몇 개 출력해서 확인
        print("주요 랜드마크 좌표:")
        print(f"  손목(0): x={hand_landmarks.landmark[0].x:.3f}, y={hand_landmarks.landmark[0].y:.3f}")
        print(f"  엄지끝(4): x={hand_landmarks.landmark[4].x:.3f}, y={hand_landmarks.landmark[4].y:.3f}")
        print(f"  검지끝(8): x={hand_landmarks.landmark[8].x:.3f}, y={hand_landmarks.landmark[8].y:.3f}")
        
        # 랜드마크와 바운딩 박스 그리기
        img_with_landmarks = img.copy()
        img_with_landmarks = draw_landmarks_and_bbox(img_with_landmarks, hand_landmarks)
        
        states = get_finger_states(hand_landmarks.landmark)
        result = classify_hand(states)
        
        # 결과를 이미지에 텍스트로 표시
        cv2.putText(img_with_landmarks, f"Result: {result}", (10, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # 손가락 상태를 이미지에 표시
        finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
        for i, (name, state) in enumerate(zip(finger_names, states)):
            status = "Extended" if state else "Folded"
            color = (0, 255, 0) if state else (0, 0, 255)
            cv2.putText(img_with_landmarks, f"{name}: {status}", (10, 100 + i*30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # 이미지 화면에 표시
        cv2.imshow('Hand Detection Result', img_with_landmarks)
        print("결과 이미지가 화면에 표시됩니다. 아무 키나 누르면 종료됩니다.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        print(f"\n최종 결과: {result}")
else:
    print("손이 감지되지 않았습니다.")
    print("이미지에 손이 명확하게 보이는지 확인하세요.")
