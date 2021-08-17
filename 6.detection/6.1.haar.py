# https://github.com/opencv/opencv/tree/master/data/haarcascades
import cv2

# img = cv2.imread('../Resources/Photos/group1.jpg')
# img = cv2.imread('../Resources/Photos/group2.jpg')
img = cv2.imread('../Resources/Photos/lady.jpg')
cv2.imshow('img', img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

face_cascade = cv2.CascadeClassifier('../Resources/Data/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('../Resources/Data/haarcascade_eye.xml')

faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

print(len(faces))

for (x,y,w,h) in faces:
    cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), thickness=2)
    cv2.putText(img, "FACE", (x,y-5), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255,255), 1)

    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh), (255,0,0), 2)
        cv2.putText(roi_color, "EYE", (ex,ey-5), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255,255), 1)

cv2.imshow("faces", img)

cv2.waitKey()
cv2.destroyAllWindows()
