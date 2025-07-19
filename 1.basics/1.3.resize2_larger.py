import cv2
import numpy as np

img = cv2.imread('../Resources/Photos/font.png')

cv2.imshow('original', img)

height = img.shape[0]
width = img.shape[1]
channel = img.shape[2]
print(img.shape)


# part 2. resize - 확대
scale = 3.0
height_to = int(height * scale)
width_to = int(width * scale)

print("From: (%d,%d,%d) => To: (%d,%d,%d)" % (height, width, channel, height_to, width_to, channel))

# 0. 기본 구조
img_resized = np.zeros((height_to, width_to, channel), dtype=np.uint8)
for h in range(height_to):
    for w in range(width_to):
        orig_h = int(h / scale)
        orig_w = int(w / scale)
        
        # img_resized[h, w] = img[orig_h, orig_w]
        
        # 여기 자체가 [(R, G, B)] 백터라서 굳이 아래 채널 별도로 돌지 않아도 무방함
        for c in range(channel):
            img_resized[h,w,c] = img[orig_h, orig_w, c]

            
# 1. 0으로 초기화된 빈 이미지에 원본 픽셀만 확대해서 채우기
img_empty = np.zeros((height_to, width_to, channel), dtype=np.uint8)
for h in range(height):
    for w in range(width):
        img_empty[int(h*scale), int(w*scale)] = img[h, w]
cv2.imshow('empty_fill', img_empty)


# 2. 최근접 이웃 방식 (Nearest Neighbor): cv2.INTER_NEAREST
img_nearest = np.zeros((height_to, width_to, channel), dtype=np.uint8)
for h in range(height_to):
    for w in range(width_to):
        orig_h = int(h / scale)
        orig_w = int(w / scale)
        img_nearest[h, w] = img[orig_h, orig_w]
cv2.imshow('nearest_fill', img_nearest)


# 3. 좌우 픽셀의 평균값 보간 (수평만 처리)
img_interp = np.zeros((height_to, width_to, channel), dtype=np.uint8)
for h in range(height):
    # 각 행의 열 방향으로 (마지막 열 제외: w+1을 위해)
    for w in range(width - 1):
        left = img[h, w] # 현재 픽셀
        right = img[h, w + 1] # 오른쪽 픽셀
        
        # scale 배 확대이므로, w와 w+1 사이에 scale만큼의 공간이 생김
        for i in range(int(scale)):
            interp_w = int(w * scale + i) # 확대된 이미지에서의 가로 위치
            ratio = i / scale # 보간 비율 (0.0 ~ 1.0 사이)
            
            # 선형 보간: 두 픽셀 사이 값을 비율에 따라 계산
            value = (1 - ratio) * left + ratio * right
            
            # 결과 이미지는 h축도 확대되어야 하므로 int(h * scale)로 위치 계산
            img_interp[int(h * scale), interp_w] = value.astype(np.uint8)

# 남은 픽셀 처리 (마지막 열(w = width - 1)은 오른쪽 이웃이 없으므로 복사로 마무리)
for h in range(height):
    img_interp[int(h * scale), int((width - 1) * scale):] = img[h, width - 1]
cv2.imshow('horizontal_interp', img_interp)


# 4. OpenCV 고급 보간 방식 (Lanczos4)
img_cv_resized = cv2.resize(img, (width_to, height_to), interpolation=cv2.INTER_LANCZOS4)
cv2.imshow('cv_resize_lanczos4', img_cv_resized)

cv2.waitKey()
cv2.destroyAllWindows()
