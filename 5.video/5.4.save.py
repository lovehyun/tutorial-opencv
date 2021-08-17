import cv2
from datetime import datetime

cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output.avi', fourcc, 25.0, (640,480))

recording = False
count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    count += 1

    # 이미지 반전,  0:상하, 1 : 좌우
    frame = cv2.flip(frame, 1)

    if recording:
        out.write(frame)
        cv2.rectangle(frame, (10,10), (width-10,height-10), (0,255,0), thickness=2)
        if (count % 2):
            cv2.circle(frame, (50,50), 10, (0,0,255), thickness=-1)

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 32: # space
        cv2.waitKey(0)
    elif key == ord('c'):
        now_str = datetime.today().strftime("%Y%m%d%H%M%S")
        cv2.imwrite('output-%s.png' % now_str, frame)
        cv2.rectangle(frame, (10,10), (width-10,height-10), (255,255,255), thickness=2)
        cv2.imshow('frame', frame)
        cv2.waitKey(100)
    elif key == ord('r'):
        recording = not recording
    elif key == ord('q'):
        break

out.release()
cap.release()

cv2.destroyAllWindows()
