import cv2
import numpy as np

img = cv2.imread("../Resources/Photos/cats.jpg")

name = "My Trackbar Window"
cv2.namedWindow(name)

red_value = 0
green_value = 0
blue_value = 0

def red_change(value):
    global red_value
    red_value = value - 255
    # print("Red changed: ", red_value)

def green_change(value):
    global green_value
    green_value = value - 255
    # print("Green changed: ", green_value)

def blue_change(value):
    global blue_value
    blue_value = value - 255
    # print("Blue changed: ", blue_value)

cv2.createTrackbar("brighness", name, 128, 255, lambda x : x)
cv2.createTrackbar("contrast", name, 10, 20, lambda x : x)
cv2.createTrackbar("red", name, 255, 510, red_change)
cv2.createTrackbar("green", name, 255, 510, green_change)
cv2.createTrackbar("blue", name, 255, 510, blue_change)

while cv2.waitKey(1) != ord('q'):
    brighness = cv2.getTrackbarPos("brighness", name) - 128
    contrast = (cv2.getTrackbarPos("contrast", name) - 10) / 10

    # color
    img_b = img[:,:,0].astype('int16')
    img_g = img[:,:,1].astype('int16')
    img_r = img[:,:,2].astype('int16')

    img_b = np.clip(img_b + blue_value, 0, 255).astype('uint8')
    img_g = np.clip(img_g + green_value, 0, 255).astype('uint8')
    img_r = np.clip(img_r + red_value, 0, 255).astype('uint8')

    mat = cv2.merge([img_b, img_g, img_r])

    # brightness
    mat = mat.astype('int16')
    mat = np.clip(mat + brighness, 0, 255).astype('uint8')

    # # contrast
    mat = mat.astype('int16')
    mat = np.clip(mat + ((mat - 128) * contrast), 0, 255).astype('uint8')

    cv2.imshow(name, mat)

cv2.destroyAllWindows()
