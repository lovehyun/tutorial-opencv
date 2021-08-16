import cv2
import numpy as np

img = cv2.imread('../Resources/Photos/lady.jpg')
rows, cols = img.shape[:2]
print(img.shape)

cv2.imshow('original', img)

repeat = 5

# part 1. blue, kernel-size
blur33 = blur77 = img
for r in range(repeat):
    print('Repeat ', r)
    blur33 = cv2.blur(blur33, (3,3))
    blur77 = cv2.blur(blur77, (7,7))
    cv2.imshow('blur33', blur33)
    cv2.imshow('blur77', blur77)
    
    cv2.waitKey()

# part 2. blue - 컨셉 이해
blur00 = np.zeros(img.shape, dtype=np.uint8)
for r in range(1,rows-1):
    if (r % 10 == 0): print('processing... %.3f' % (100*r/rows))
    for c in range(1,cols-1):
        for l in range(3):
            pixel = np.int16(0) \
                + img[r-1,c-1,l] + img[r-1,c,l] + img[r-1,c+1,l] \
                + img[r,c-1,l] + img[r,c,l] + img[r,c+1,l] \
                + img[r+1,c-1,l] + img[r+1,c,l] + img[r+1,c+1,l]
            blur00[r,c,l] = int(pixel / 9)

cv2.imshow('blur00', blur00)
cv2.waitKey()

# part 3. gaussian blur
# GaussianBlur(src, ksize, sigmaX)
#  - ksize : 커널 크기
#  - sigmaX : x방향 sigma
blur = cv2.GaussianBlur(img, (5,5), 0)
cv2.imshow('Gaussian', blur)
cv2.waitKey()

cv2.destroyAllWindows()
