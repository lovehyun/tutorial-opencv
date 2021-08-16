import cv2
import numpy as np

img = cv2.imread('../Resources/Photos/shape.png')
cv2.imshow('shape', img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     [1 1 1]      [0.111 0.111 0.111]
# G = [1 1 1]  G = [0.111 0.111 0.111]
#     [1 1 1]      [0.111 0.111 0.111]
kernel = np.ones((3,3), dtype=np.float64) / 9
print(kernel)

dst = cv2.filter2D(gray, -1, kernel)

cv2.imshow('filter', dst)

cv2.waitKey()
cv2.destroyAllWindows()
