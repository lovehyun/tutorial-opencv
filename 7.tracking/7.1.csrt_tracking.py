# pip install opencv-contrib-python

import cv2

# 1. 비디오 열기
cap = cv2.VideoCapture('../Resources/Videos/Zootopia.mp4')

# 2. 첫 프레임에서 ROI(추적할 대상) 지정
ret, frame = cap.read()
bbox = cv2.selectROI("Select Object", frame, False)  # 마우스로 객체 선택

# 3. 트래커 생성 및 초기화
tracker = cv2.TrackerCSRT_create()  # KCF, MOSSE 등으로 교체 가능
# OpenCV 4.x 기준으로는 cv2.TrackerCSRT_create() 를 사용하지만,
# OpenCV 3.x에서는 cv2.Tracker_create('CSRT') 형태를 써야함.

tracker.init(frame, bbox)

# 4. 프레임마다 추적
while True:
    ret, frame = cap.read()
    if not ret:
        break

    success, bbox = tracker.update(frame)  # bbox: (x, y, w, h)

    if success:
        x, y, w, h = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Tracking", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Lost", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    cv2.imshow("Tracking", frame)
    if cv2.waitKey(30) & 0xFF == 27:  # ESC 키로 종료
        break

cap.release()
cv2.destroyAllWindows()
