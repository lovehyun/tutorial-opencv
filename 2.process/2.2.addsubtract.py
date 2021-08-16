import cv2

img1 = cv2.imread('../Resources/Photos/cat.jpg')
img2 = cv2.imread('../Resources/Photos/park.jpg')

cv2.imshow('cat', img1)
cv2.imshow('park', img2)

# part 1. addition
add1 = cv2.add(img1, img2)
cv2.imshow('add', add1)

# part 2. addition #2
add2 = cv2.addWeighted(img1, 0.7, img2, 0.3, 1.0)
cv2.imshow('add2', add2)

# part 3. subtraction
sub1 = cv2.subtract(img2, img1)
cv2.imshow('sub1', sub1)

sub2 = cv2.subtract(img1, img2)
cv2.imshow('sub2', sub2)

cv2.waitKey()
cv2.destroyAllWindows()
