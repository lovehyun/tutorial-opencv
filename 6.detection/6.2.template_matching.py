import cv2
import numpy as np

# 1. 원본 이미지 로드
img = cv2.imread('../Resources/Photos/cafe2.jpg')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2. 템플릿 이미지 로드 (미리 잘라둔 로고)
template = cv2.imread('../Resources/Photos/cafe2_cropped.jpg', cv2.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]

# 3. 템플릿 매칭
# 템플릿 매칭은 크기, 방향, 기하학적으로 정확히 일치해야만 인식이 됩니다.
# 회전되어 있거나, 크기가 달라졌거나, 원근감이 적용된 경우에는 템플릿 매칭이 실패할 수 있음.
res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.9  # 민감도 조절
loc = np.where(res >= threshold)

# 4. 결과 표시
for pt in zip(*loc[::-1]):
    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
    cv2.putText(img, "MATCH", (pt[0], pt[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# 5. 시각화
cv2.imshow('Detected Logo', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
