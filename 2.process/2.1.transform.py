# https://opencv-python.readthedocs.io/en/latest/doc/10.imageTransformation/imageTransformation.html
import cv2
import numpy as np

img = cv2.imread('../Resources/Photos/cat.jpg')

rows,cols = img.shape[:2]

# part 1. transform
# 3개의 포인트를 통해 기하학적 변형
#   src (0,0), (cols,0),     (0,rows)
#   dst (0,0), (cols*0.7,0), (cols*0.3, rows)
src_points = np.float32([[0,0], [cols-1,0], [0,rows-1]])
dst_points = np.float32([[0,0], [int(0.7*(cols-1)),0], [int(0.3*(cols-1)),rows-1]])

affine_matrix = cv2.getAffineTransform(src_points, dst_points)
img_output = cv2.warpAffine(img, affine_matrix, (cols,rows))

cv2.imshow('original', img)
cv2.imshow('transform', img_output)
cv2.waitKey()

# part 2. mirror
#   src (0,0),    (cols,0), (0,rows)
#   dst (cols,0), (0,0),    (cols, rows)
src_points = np.float32([[0,0], [cols-1,0], [0,rows-1]])
dst_points = np.float32([[cols-1,0], [0,0], [cols-1,rows-1]])

affine_matrix = cv2.getAffineTransform(src_points,dst_points)
img_output = cv2.warpAffine(img,affine_matrix,(cols,rows))

cv2.imshow('transform', img_output)
cv2.waitKey()

# part 3. perspective transform - 4pt
#   src (cols*0.5,0), (cols,0), (cols*0.5,rows), (cols,rows)
#   dst (0,0),        (cols,0), (cols*0.33,rows) (cols*0.66,rows)
src_points = np.float32([[int(0.5*(cols-1)),0], [cols-1,0], [int(0.5*(cols-1)),rows-1], [cols-1,rows-1]])
dst_points = np.float32([[0,0], [cols-1,0], [int(0.33*cols),rows-1], [int(0.66*cols),rows-1]])

projective_matrix = cv2.getPerspectiveTransform(src_points,dst_points)
img_output = cv2.warpPerspective(img,projective_matrix,(cols,rows)) 

cv2.imshow('transform', img_output)
cv2.waitKey()

cv2.destroyAllWindows()
