import cv2

# part 1. 이미지 로딩
img = cv2.imread('../Resources/Photos/lenna.bmp')
cv2.imshow('picture', img)

# part 2. 이미지 자료구조
print(type(img), img.shape)
h = img.shape[0]
w = img.shape[1]
c = img.shape[2]
print('height: %d, width: %d, channel: %d' % (h, w, c))

# part3. 이미지 픽셀
p = img[0,0]
print("BGR at 0,0 : ", p)

cv2.waitKey()
cv2.destroyAllWindows()
