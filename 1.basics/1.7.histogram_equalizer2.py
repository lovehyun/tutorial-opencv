import cv2
import numpy as np
import matplotlib.pyplot as plt

def calc_color_histogram(image):
    """R/G/B 채널별 히스토그램을 계산하고 0,255 제거"""
    hist_data = []
    for i in range(3):  # B, G, R
        hist = cv2.calcHist([image], [i], None, [256], [0, 256])
        hist[0] = 0
        hist[255] = 0
        hist_data.append(hist)
    return hist_data

def plot_color_histograms(original_hists, equalized_hists):
    """하나의 창에 RGB 히스토그램을 상하로 비교 시각화"""
    colors = ('b', 'g', 'r')
    x = np.arange(256)

    plt.figure(figsize=(12, 6))

    # 원본 이미지 히스토그램
    plt.subplot(2, 1, 1)
    plt.title("Original RGB Histogram")
    for hist, color in zip(original_hists, colors):
        plt.plot(x, hist, color=color)
    plt.xlim([0, 256])
    plt.grid(True)

    # 평활화 이미지 히스토그램
    plt.subplot(2, 1, 2)
    plt.title("Equalized RGB Histogram")
    for hist, color in zip(equalized_hists, colors):
        plt.plot(x, hist, color=color)
    plt.xlim([0, 256])
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# 1. 이미지 로드 및 YCrCb 변환
# - Y  : 밝기 (Luminance, 휘도) (수식 : Y = 0.299R + 0.587G + 0.114B) → 초록(G)은 간접적으로 Y(밝기)에서 유도됩니다.
# - Cr : 색상 성분 (수식 : 빨강 - Y) → 적색 차분 (R이 Y보다 얼마나 강한가)
# - Cb : 색상 성분 (수식 : 파랑 - Y) → 청색 차분 (B가 Y보다 얼마나 강한가)
img = cv2.imread('../Resources/Photos/cats.jpg')
ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
equalized_color = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

# 2. OpenCV로 이미지 출력
cv2.imshow("Original Image", img)
cv2.imshow("Equalized Color Image", equalized_color)

# 3. 히스토그램 계산 및 비교 그래프 출력
original_hists = calc_color_histogram(img)
equalized_hists = calc_color_histogram(equalized_color)
plot_color_histograms(original_hists, equalized_hists)

# 4. 종료 대기
cv2.waitKey(0)
cv2.destroyAllWindows()
