import cv2
import numpy as np

rows = 400
cols = 600

blank = np.zeros((rows,cols,3), dtype='uint8')
cv2.imshow('canvas', blank)

#                     cols,rows  cols,rows  b,g,r
cv2.rectangle(blank, (100,50), (500,100), (0,255,0), thickness=3)
cv2.imshow('canvas', blank)

cv2.circle(blank, (300,200), 50, (0,0,255), thickness=-1)
cv2.imshow('canvas', blank)

cv2.putText(blank, "Welcome to SOMA", (100,350), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255,255,0), 2)
cv2.imshow('canvas', blank)

# pip install Pillow
from PIL import ImageFont, ImageDraw, Image
def PutKRText(src, text, font_size, xy, bgr):
    fontpath = "fonts/gulim.ttc"
    # fontpath = "fonts/batang.ttc"
    font = ImageFont.truetype(fontpath, font_size)
    src_pil = Image.fromarray(src)
    draw = ImageDraw.Draw(src_pil)
    draw.text(xy, text, font=font, fill=bgr)
    target = np.array(src_pil)
    return target

blank = PutKRText(blank, "한글", 44, (260,50), (255,255,255))

cv2.imshow('canvas', blank)
cv2.waitKey(0)
