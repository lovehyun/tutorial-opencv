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
enhance = 50
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
else:
    mat = img.astype('int16')
    bright = np.clip(mat + enhance, 0, 255)
    bright = bright.astype('uint8')

cv2.imshow('brightness', bright)

# part2. contrast - 컨셉
factor = 0.5
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
