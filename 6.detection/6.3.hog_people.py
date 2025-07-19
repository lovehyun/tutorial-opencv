import cv2

# 1. HOGDescriptor 생성 및 기본 사람 검출기 설정
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
# 사람(보행자, Pedestrian) 탐지를 위한 사전 학습된 SVM 모델의 weight입니다.
# 즉, 이 함수는 사람만 탐지할 수 있도록 훈련된 모델이며, 다음과 같은 특징이 있습니다:
# 탐지 가능한 유형
#  - 전체 몸체의 보행자(standing 사람)
#  - 측면 or 정면 기준
#  - 성인 크기
#  - 보통 상체/하체 포함된 서 있는 사람
# 탐지 불가능하거나 약한 경우
#  - 앉아 있는 사람, 누워 있는 사람
#  - 상반신/얼굴만 보이는 경우
#  - 어린이, 유아, 동물
#  - 다른 객체 (자동차, 자전거, 물건 등)
#  - 부분 가림, 멀리 있거나 너무 가까운 경우

# 2. 이미지 불러오기
img = cv2.imread('../Resources/Photos/group1.jpg')
if img is None:
    raise FileNotFoundError("people.jpg 파일을 찾을 수 없습니다.")

# 3. 사람 탐지 (detectMultiScale)
#    winStride: 윈도우 이동 간격, padding: 블록 패딩, scale: 이미지 피라미드 스케일
boxes, weights = hog.detectMultiScale(
    img,
    winStride=(8, 8),
    padding=(16, 16),
    scale=1.05
)

# 4. 탐지 결과 그리기
for (x, y, w, h), weight in zip(boxes, weights):
    # weight(신뢰도)도 텍스트로 표시
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(
        img,
        f"{weight:.2f}",
        (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

# 5. 결과 출력
cv2.imshow("HOG Person Detection", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
