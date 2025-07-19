# 주의: matplotlib의 Tkinter 기반 GUI (_tkagg) 백엔드가
# OpenCV GUI 이벤트 루프(cv2.imshow() / cv2.waitKey())와 충돌

import cv2
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg') # 중요: TkAgg 대신 Qt 백엔드 사용
import matplotlib.pyplot as plt

def show_histogram(image, title="Histogram"):
    """실시간 히스토그램 그래프 출력 (non-blocking)"""
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])

    plt.clf()  # 이전 그래프 지우기
    plt.title(title)
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.plot(hist, color='black')
    plt.xlim([0, 256])
    plt.grid(True)
    plt.draw()
    plt.pause(0.001)  # GUI 충돌 방지하면서 갱신

# 1. 이미지 불러오기 및 전처리
img = cv2.imread('../Resources/Photos/cats.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
equalized = cv2.equalizeHist(gray) # equalizeHist()는 1채널 (Grayscale)만 처리 가능

# 2. Matplotlib 준비
plt.ion()  # interactive 모드 켜기
plt.figure(figsize=(10, 4))

# 3. 초기 화면 출력
cv2.imshow("Image", gray)
show_histogram(gray, "Original Histogram")

print("키보드 입력 (이미지창에서):")
print("  o - 원본 이미지 + 히스토그램")
print("  e - 평활화 이미지 + 히스토그램")
print("  esc - 종료")

while True:
    key = cv2.waitKey(0)

    if key == 27:  # esc
        break
    elif key == ord('o'):
        cv2.imshow("Image", gray)
        show_histogram(gray, "Original Histogram")
    elif key == ord('e'):
        cv2.imshow("Image", equalized)
        show_histogram(equalized, "Equalized Histogram")

cv2.destroyAllWindows()
plt.ioff()
plt.close()
