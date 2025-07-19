import cv2
import numpy as np

img = cv2.imread('../Resources/Photos/cats.jpg')
print(img.shape)

height = img.shape[0]
width = img.shape[1]
channel = img.shape[2]

cv2.imshow('original', img)

concept = True

# part 1. brightness - 컨셉
enhance = 50 # 밝기 조정 값 (+: 밝게, -: 어둡게)
bright = np.zeros(img.shape, np.uint8)
if concept is True:
    for h in range(height):
        if (h % 10 == 0): print('processing... %.3f' % (100*h/height))

        for w in range(width):
            for c in range(channel):
                pixel = img[h,w,c] + enhance
                if (pixel > 255):
                    bright[h,w,c] = 255
                elif (pixel < 0):
                    bright[h,w,c] = 0
                else:
                    bright[h,w,c] = pixel
else: # numpy를 이용한 벡터화 연산
    mat = img.astype('int16') # 오버플로우 방지를 위한 타입 변환
    bright = np.clip(mat + enhance, 0, 255) # 범위 클리핑
    bright = bright.astype('uint8') # 다시 이미지용 타입으로 변환

cv2.imshow('brightness', bright)


# part2. contrast - 컨셉
factor = 0.5 # 대비 조정 계수 (0: 변화 없음, 양수: 선명하게, 음수: 흐리게)
contrast = np.zeros(img.shape, np.uint8)
if concept is True:
    for h in range(height):
        if (h % 10 == 0): print('processing... %.3f' % (100*h/height))

        for w in range(width):
            for c in range(channel):
                pixel = img[h,w,c] + ((img[h,w,c] - 128) * factor)
                if (pixel > 255):
                    contrast[h,w,c] = 255
                elif (pixel < 0):
                    contrast[h,w,c] = 0
                else:
                    contrast[h,w,c] = pixel
else:
    mat = img.astype('int16')
    contrast = np.clip(mat + ((mat - 128) * factor), 0, 255)
    contrast = contrast.astype('uint8')

cv2.imshow('contrast', contrast)
cv2.waitKey()
