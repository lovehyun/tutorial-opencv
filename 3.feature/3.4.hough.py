# https://opencv-python.readthedocs.io/en/latest/doc/25.imageHoughLineTransform/imageHoughLineTransform.html
import cv2
import numpy as np

img = cv2.imread('../Resources/Photos/shape2.png')
cv2.imshow('shape', img)
h, w = img.shape[:2]

img2 = img.copy()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# part 1. hough lines

# HighLines(image, rho, theta, threshold, ...)
#  - ρ = x * cosθ + y * sinθ
#  - rho: Distance resolution of the accumulator in pixels
#  - theta: Angle resolution of the accumulator in radians
lines = cv2.HoughLines(gray, 1, np.pi/180, 100)
for line in lines:
    r, theta = line[0]
    tx, ty = np.cos(theta), np.sin(theta)
    x0, y0 = tx*r, ty*r
    cv2.circle(img2, (abs(x0), abs(y0)), 3, (0,0,255), -1)
    x1, y1 = int(x0 + w*(-ty)), int(y0 + h*tx)
    x2, y2 = int(x0 - w*(-ty)), int(y0 - h*tx)
    cv2.line(img2, (x1,y1), (x2,y2), (0,255,0), 1)

cv2.imshow('houghlines', img2)

# part 2. hough circle
img3 = img.copy()

circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 50, param1=100, param2=30, minRadius=0, maxRadius=0)
circles = np.uint16(np.around(circles))
for circle in circles[0,:]:
    cv2.circle(img3, (circle[0], circle[1]), circle[2], (0,0,255), 1)

cv2.imshow('houghcircles', img3)

cv2.waitKey()
cv2.destroyAllWindows()
