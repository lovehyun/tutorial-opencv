import cv2
import numpy as np

img = cv2.imread('../Resources/Photos/lady.jpg')

cv2.imshow('lady', img)

blur = cv2.GaussianBlur(img, (5,5), 0)
cv2.imshow('Gaussian', blur)
cv2.waitKey()

repeat = 5

blur33 = blur77 = img
for r in range(repeat):
    print('Repeat ', r)
    blur33 = cv2.blur(blur33, (3,3))
    blur77 = cv2.blur(blur77, (7,7))
    cv2.imshow('blur33', blur33)
    cv2.imshow('blur77', blur77)
    
    cv2.waitKey()

cv2.destroyAllWindows()
