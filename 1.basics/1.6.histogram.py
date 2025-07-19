import cv2
import numpy as np
import matplotlib.pyplot as plt

# 이미지 로드 (컬러 또는 그레이스케일 가능)
img = cv2.imread('../Resources/Photos/cats.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow('original', img)

# 1. 직접 계산한 히스토그램
# 히스토그램 배열 초기화 (0~255 → 총 256개)
hist = [0] * 256

# 픽셀을 하나하나 순회하며 밝기값 빈도 세기
height, width = gray.shape
for h in range(height):
    for w in range(width):
        pixel = gray[h, w]
        hist[pixel] += 1

   
# 2. numpy 배열 연산
# hist, bins = np.histogram(gray.flatten(), bins=256, range=[0, 256])

# 히스토그램 시각화
plt.figure(figsize=(10,4))
plt.title("Histogram by NumPy")
plt.xlabel("Pixel Value (0~255)")
plt.ylabel("Count")
plt.plot(hist, color='black')
plt.xlim([0, 256])
plt.grid(True)
plt.show()


# 3. OpenCV로 히스토그램 계산 (grayscale용, channel=0)
hist_cv = cv2.calcHist([gray], [0], None, [256], [0, 256])
    
# 시각화
plt.figure(figsize=(10,4))
plt.title("Histogram by OpenCV")
plt.xlabel("Pixel Value (0~255)")
plt.ylabel("Count")
plt.plot(hist_cv, color='blue')
plt.xlim([0, 256])
plt.grid(True)
plt.show()


# 4. 색상별 채널 이름과 색 지정
colors = ('b', 'g', 'r')  # OpenCV는 BGR 순서

plt.figure(figsize=(10, 4))
plt.title('RGB Histogram by OpenCV')
plt.xlabel('Pixel Value (0~255)')
plt.ylabel('Count')

# 각 채널에 대해 히스토그램 계산 및 출력
for i, color in enumerate(colors):
    hist = cv2.calcHist([img], [i], None, [256], [0, 256])
    plt.plot(hist, color=color)
    plt.xlim([0, 256])

plt.grid(True)
plt.show()
