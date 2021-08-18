import cv2

img = cv2.imread('../Resources/Photos/cat.jpg')
cv2.imshow('cat', img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Canny edge detector 알고리즘 프로세스
#  - Gaussian filter
#  - Finding the intensity gradient of the image
#  - Gradient magnitute thresholding or lower bound cut-off suppresion
#  - Double threshold
#  - Edge tracking by hysteresis

# 강한 엣지, 약한 엣지, No 엣지 - Tlow, Thigh
dst = cv2.Canny(gray, 50, 150)

cv2.imshow('cat', dst)

cv2.waitKey()
cv2.destroyAllWindows()
