import cv2
import numpy as np

# 1. 원본 이미지 로드
img = cv2.imread('../Resources/Photos/cafe2.jpg')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2. 템플릿 이미지 로드 (미리 잘라둔 로고)
template = cv2.imread('../Resources/Photos/cafe2_cropped.jpg', cv2.IMREAD_GRAYSCALE)
tW, tH = template.shape[::-1]

# 3. 다중 스케일 탐색
found = None  # 최고 유사도 저장

for scale in np.linspace(0.2, 2.0, 30)[::-1]:  # 큰 크기부터 작은 크기로
    resized = cv2.resize(img_gray, None, fx=scale, fy=scale)
    r = img_gray.shape[1] / float(resized.shape[1])  # 비율 계산

    if resized.shape[0] < tH or resized.shape[1] < tW:
        print(f"[SKIP] scale={scale:.2f} - template bigger than resized image")
        break

    result = cv2.matchTemplate(resized, template, cv2.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    print(f"[INFO] scale={scale:.2f}, maxVal={maxVal:.4f}, location={maxLoc}")

    if found is None or maxVal > found[0]:
        found = (maxVal, maxLoc, r)

# 4. 최고 일치 위치 그리기
if found:
    maxVal, maxLoc, r = found
    startX = int(maxLoc[0] * r)
    startY = int(maxLoc[1] * r)
    endX = int((maxLoc[0] + tW) * r)
    endY = int((maxLoc[1] + tH) * r)

    print(f"\nBest match at scale ratio={r:.4f}, confidence={maxVal:.4f}, location=({startX}, {startY})")

    cv2.rectangle(img, (startX, startY), (endX, endY), (0, 255, 0), 2)
    cv2.putText(img, f"Match: {maxVal:.2f}", (startX, startY - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow("Detected", img)
else:
    print("No match found")

cv2.waitKey(0)
cv2.destroyAllWindows()
