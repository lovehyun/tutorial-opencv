import cv2

cap = cv2.VideoCapture(0)

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)

print('Frame width: ', width)
print('Frame height: ',height)
print('Frame fps: ', fps)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('video', frame)

    edge = cv2.Canny(frame, 50, 200)
    cv2.imshow('canny', edge)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
