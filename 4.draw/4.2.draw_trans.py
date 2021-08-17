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

alpha = 0.4
overlay = blank.copy()
cv2.putText(overlay, "Welcome to SOMA", (105,355), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255,255,0), 2)
cv2.addWeighted(overlay, alpha, blank, 1 - alpha, 0, blank)
cv2.imshow('canvas', blank)

print('press any key on image...')
cv2.waitKey()

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

# https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
def PutKRTextBG(src, text, font_size, xy, bgr, bg_trans, bg_bgr):
    # make base canvas to write text in RGBA channel in Image data format
    base = Image.fromarray(src).convert("RGBA")
    txt = Image.new("RGBA", base.size, (255,255,255,0))

    fontpath = "fonts/gulim.ttc"
    # fontpath = "fonts/batang.ttc"
    font = ImageFont.truetype(fontpath, font_size)
    draw = ImageDraw.Draw(txt)
    
    trans_value = int(bg_trans * 255)
    text_width, text_height = draw.textsize(text, font=font)
    
    rec_pos = (xy, xy[0] + text_width, xy[1] + text_height)
    draw.rectangle(rec_pos, fill=(bg_bgr)+(trans_value,))
    draw.text(xy, text, font=font, fill=(bgr)+(trans_value,))

    out = Image.alpha_composite(base, txt)
    target = np.array(out)
    return target


blank = PutKRText(blank, "한글입력 테스트", 44, (140,50), (255,255,255))
cv2.imshow('canvas', blank)
print('press any key on image...')
cv2.waitKey()

blank = PutKRTextBG(blank, "투명한글", 44, (210,180), (255,255,255), 0.7, (255,0,255))
cv2.imshow('canvas', blank)
cv2.waitKey()
