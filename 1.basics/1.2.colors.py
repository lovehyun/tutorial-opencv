import cv2
import numpy as np

img = cv2.imread('../Resources/Photos/cats.jpg')

height = img.shape[0]
width = img.shape[1]

cv2.imshow('img', img)
cv2.waitKey()

# part 1. color channel
img_b = img[:,:,0]
img_g = img[:,:,1]
img_r = img[:,:,2]

print('blue', img_b)
print('green', img_g)
print('red', img_r)

cv2.imshow('blue', img_b)
cv2.imshow('green', img_g)
cv2.imshow('red', img_r)
cv2.waitKey()

# part 2. color channel #2
blank = np.zeros(img.shape[:2], dtype='uint8')

img_b2 = cv2.merge([img_b, blank, blank])
img_g2 = cv2.merge([blank, img_g, blank])
img_r2 = cv2.merge([blank, blank, img_r])

cv2.imshow('blue', img_b2)
cv2.imshow('green', img_g2)
cv2.imshow('red', img_r2)

merged = cv2.merge([img_b, img_g, img_r])

cv2.imshow('merged', merged)
cv2.waitKey()

# part 3. gray scale
my_gray1 = np.zeros((height, width), np.uint8)
my_gray2 = np.zeros((height, width), np.uint8)
my_gray3 = np.zeros((height, width, 3), np.uint8)

for h in range(height):
    if (h % 10 == 0): print('processing... %.3f' % (100*h/height))

    for w in range(width):
        # common sense? : Y = 0.333 * R + 0.333 * G + 0.333 * B
        my_gray1[h,w] = np.clip(0.333 * img[h,w,0] + 0.333 * img[h,w,1] + 0.333 * img[h,w,2], 0, 255)
        # luminosity formula (CCIR 601) : Y = 0.299 * R + 0.587 * G + 0.114 * B
        my_gray2[h,w] = np.clip(0.114 * img[h,w,0] + 0.587 * img[h,w,1] + 0.229 * img[h,w,2], 0, 255)
        # sepia formula - not a grayscale
        # newR = (0.393 * R + 0.769 * G + 0.189 * B)
        # newG = (0.349 * R + 0.686 * G + 0.168 * B)
        # newB = (0.272 * R + 0.534 * G + 0.131 * B)
        newR = np.clip(0.189 * img[h,w,0] + 0.769 * img[h,w,1] + 0.393 * img[h,w,2], 0, 255)
        newG = np.clip(0.168 * img[h,w,0] + 0.686 * img[h,w,1] + 0.349 * img[h,w,2], 0, 255)
        newB = np.clip(0.131 * img[h,w,0] + 0.534 * img[h,w,1] + 0.272 * img[h,w,2], 0, 255)
        my_gray3[h,w] = [newB, newG, newR]

cv2.imshow('my_gray1', my_gray1)
cv2.imshow('my_gray2', my_gray2)
cv2.imshow('my_gray3', my_gray3)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray', gray)

cv2.waitKey(0)
cv2.destroyAllWindows()
