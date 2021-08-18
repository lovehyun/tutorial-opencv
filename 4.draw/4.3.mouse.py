import cv2

img = cv2.imread('../Resources/Photos/lenna.bmp')
backup = img.copy()

points = []

# mouse click event
def on_mouse(event, x, y, flags, param):
    global points

    if event == cv2.EVENT_LBUTTONDOWN:
        points = [(x, y)]
        cv2.circle(img, (x,y), 5, (255,0,255), thickness=-1)
    elif event == cv2.EVENT_LBUTTONUP:
        points.append((x, y))
        cv2.circle(img, (x,y), 5, (255,0,255), thickness=-1)
        cv2.rectangle(img, points[0], points[1], (0, 255, 0), 2)
        cv2.imshow('picture', img)

cv2.namedWindow('picture')
cv2.setMouseCallback('picture', on_mouse)

while True:
    cv2.imshow('picture', img)

    if len(points) == 2:
        pt1 = points[0] # (x1,y1)
        pt2 = points[1] # (x2,y2)
        min_x = min(pt1[0], pt2[0])
        max_x = max(pt1[0], pt2[0])
        min_y = min(pt1[1], pt2[1])
        max_y = max(pt1[1], pt2[1])

        try:
            roi = img[min_y:max_y, min_x:max_x]
            cv2.imshow('crop', roi)
        except cv2.error as e:
            print(e)

        points.clear()

    key = cv2.waitKey(1) & 0xFF
    if  key == ord('q'):
        break
    elif key == ord('r'):
        img = backup.copy()

cv2.destroyAllWindows()
