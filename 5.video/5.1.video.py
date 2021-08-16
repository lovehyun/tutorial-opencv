import cv2

cap = cv2.VideoCapture('../Resources/Videos/dog.mp4')
# cap = cv2.VideoCapture('../Resources/Videos/Zootopia.mp4')

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv2.CAP_PROP_FPS)
delay = int(1000/fps)

print('Frame width: ', width)
print('Frame height: ', height)
print('Frame count: ', count)
print('Frame FPS: ', fps)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('video', frame)

    # if cv2.waitKey(1) & 0xFF == 27:
    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
