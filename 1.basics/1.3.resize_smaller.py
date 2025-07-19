import cv2
import numpy as np

img = cv2.imread('../Resources/Photos/font.png')

cv2.imshow('original', img)

height = img.shape[0]
width = img.shape[1]
channel = img.shape[2]
print(img.shape)

# part 1. resize - 축소
scale = 0.5
height_to = int(height * scale)
width_to = int(width * scale)

print("From: (%d,%d,%d) => To: (%d,%d,%d)" % (height, width, channel, height_to, width_to, channel))

img_resized = np.empty((height_to, width_to, channel), dtype=np.uint8)
for h in range(height_to):
    for w in range(width_to):
        for c in range(channel):
            img_resized[h,w,c] = img[int(h/scale),int(w/scale),c]

cv2.imshow('my_resized', img_resized)

# interpolation
#  - cv2.INTER_NEAREST : 최근방 픽셀
#  - cv2.INTER_LINEAR : 2x2 픽셀 참조 (bilinear) - default
#  - cv2.INTER_CUBIC : 4x4 픽셀 참조 (bicubic)
#  - cv2.INTER_LANCZOS4 : 8x8 픽셀 참조 (Lanczos)
#  - cv2.INTER_AREA : 축소시 moire-free 영상 효율적 제공, 확대시 INTER_NEAREST와 유사
img_resized = cv2.resize(img, (width_to, height_to), interpolation=cv2.INTER_AREA)
cv2.imshow('resized', img_resized)
cv2.waitKey()
