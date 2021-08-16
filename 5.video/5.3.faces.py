import cv2

# cap = cv2.VideoCapture('../Resources/Videos/Zootopia.mp4')
cap = cv2.VideoCapture(0)

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)
delay = int(1000 / fps)

print('Frame width: ', width)
print('Frame height: ',height)
print('frame fps:', fps)

face_cascade = cv2.CascadeClassifier('../Resources/Data/haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('frame', frame)

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # faces = face_cascade.detectMultiScale(gray)
    # for (x,y,w,h) in faces:
    #     cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 255, 0), thickness=2)
    #     cv2.putText(frame, "FACE", (x,y), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 255), 1)
    #     cv2.imshow('frame', frame)

    dst = cv2.Canny(frame, 50, 200)
    cv2.imshow('canny', dst)

    if cv2.waitKey(delay) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
