import cv2

img = cv2.imread('../Resources/Photos/shape2.png')
cv2.imshow('shape', img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#      [-1  0  +1]       [-1 -2 -1]
# Gx = [-2  0  +2]  Gy = [ 0  0  0]
#      [-1  0  +1]       [+1 +2 +1]
sobel_x = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=3)
sobel_x = cv2.convertScaleAbs(sobel_x)

sobel_y = cv2.Sobel(gray, cv2.CV_8U, 0, 1, ksize=3)
sobel_y = cv2.convertScaleAbs(sobel_y)

sobel_xy = cv2.addWeighted(sobel_x, 1, sobel_y, 1, 0)

cv2.imshow('sobel_x', sobel_x)
cv2.imshow('sobel_y', sobel_y)
cv2.imshow('sobel_xy', sobel_xy)

cv2.waitKey()
cv2.destroyAllWindows()
