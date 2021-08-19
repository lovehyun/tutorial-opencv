# https://pillow.readthedocs.io/en/stable/reference/Image.html
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime


# https://docs.aws.amazon.com/rekognition/latest/dg/images-displaying-bounding-boxes.html
def mark_face_image(photo, location, filename=None):
    image = Image.open(photo)
    img_width, img_height = image.size

    left = img_width * location['Left']
    top = img_height * location['Top']
    width = img_width * location['Width']
    height = img_height * location['Height']

    points = (
        (left, top), # left top
        (left + width, top), # right top
        (left + width, top + height), # right bottom
        (left , top + height), # left bottom
        (left, top) # back to left top
    )

    draw = ImageDraw.Draw(image)
    draw.line(points, fill='#00FF00', width=2)
    # Alternatively can draw rectangle. However you can't set line width.
    # draw.rectangle([left,top, left + width, top + height], outline='#00d400')

    if filename:
        image.save(filename)

    return image

def merge_two_images(image1, location1, image2, location2, text):
    images = [image1, image2]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    img1_width, img1_height = image1.size
    left1 = img1_width * location1['Left']
    top1 = img1_height * location1['Top']
    width1 = img1_width * location1['Width']
    height1 = img1_height * location1['Height']

    img2_width, img2_height = image2.size
    left2 = img2_width * location2['Left']
    top2 = img2_height * location2['Top']
    width2 = img2_width * location2['Width']
    height2 = img2_height * location2['Height']

    point1 = ((left1, top1), (img1_width + left2, top2)) # left top
    point2 = ((left1 + width1, top1), (img1_width + left2 + width2, top2)) # right top
    point3 = ((left1 + width1, top1 + height1), (img1_width + left2 + width2, top2 + height2)) # right bottom
    point4 = ((left1 , top1 + height1), (img1_width + left2, top2 + height2)) # left bottom

    draw = ImageDraw.Draw(new_im)
    draw.line(point1, fill='#00D400', width=1)
    draw.line(point2, fill='#00D400', width=1)
    draw.line(point3, fill='#00D400', width=1)
    draw.line(point4, fill='#00D400', width=1)

    font = ImageFont.truetype('fonts/arial.ttf', 25)
    w, h = font.getsize(text)
    x = img1_width + left2
    y = top2 - h - 2
    draw.rectangle((x, y, x + w, y + h), fill='black')
    draw.text((x, y), text, fill='white', font=font, align='left')

    now = datetime.now()
    nowDateTime = now.strftime('%Y%m%d_%H%M%S')
    new_im.save('output-%s.jpg' % format(nowDateTime))
