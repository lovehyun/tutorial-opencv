import cv2

img = cv2.imread('../Resources/Photos/cat.jpg')
cv2.imshow('cat', img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
dst = cv2.Canny(gray, 50, 150)

cv2.imshow('cat', dst)

cv2.waitKey()
cv2.destroyAllWindows()
