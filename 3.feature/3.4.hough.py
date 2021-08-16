# https://opencv-python.readthedocs.io/en/latest/doc/25.imageHoughLineTransform/imageHoughLineTransform.html
import cv2
import numpy as np

img = cv2.imread('../Resources/Photos/shape2.png')
cv2.imshow('shape', img)
h, w = img.shape[:2]

img2 = img.copy()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

lines = cv2.HoughLines(gray, 1, np.pi/180, 100)
for line in lines:
    r, theta = line[0]
    tx, ty = np.cos(theta), np.sin(theta)
    x0, y0 = tx*r, ty*r
    cv2.circle(img2, (abs(x0), abs(y0)), 3, (0,0,255), -1)
    x1, y1 = int(x0 + w*(-ty)), int(y0 + h*tx)
    x2, y2 = int(x0 - w*(-ty)), int(y0 - h*tx)
    cv2.line(img2, (x1,y1), (x2,y2), (0,255,0), 1)

cv2.imshow('hough', img2)

cv2.waitKey()
cv2.destroyAllWindows()
