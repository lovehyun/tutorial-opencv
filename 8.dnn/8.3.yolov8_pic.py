# pip install ultralytics
from ultralytics import YOLO
import cv2

# 모델 로드 (yolov8n은 가장 가볍고 빠름)
model = YOLO('yolov8n.pt')

# 이미지 읽기
img = cv2.imread('../Resources/Photos/group2.jpg')

# 객체 감지(추론) 수행
results = model(img)

# 결과 반복
for r in results:
    for box in r.boxes:
        # 사람 감지만 필터링
        # if int(box.cls[0]) == 0:  # 0 = 'person'
        
        cls_id = int(box.cls[0])  # 클래스 ID
        conf = float(box.conf[0])  # 신뢰도
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # 바운딩 박스

        label = model.names[cls_id]  # 클래스 이름 (예: person, car)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, f"{label} {conf:.2f}", (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

cv2.imshow("YOLO Detection", img)
cv2.waitKey(0)
cv2.destroyAllWindows()


# model = YOLO('yolov8n.pt') 이렇게 쓰면,
# 'yolov8n.pt'라는 **모델 가중치 파일(weight file)**이 로컬에 없을 경우 자동으로 다운로드합니다.
# 처음 한 번만 다운로드하면 이후는 캐시에서 불러옵니다.
# | 이름           | 특징               | 용량    | 사용 예             |
# | -------------- | ----------------- | ------- | ------------------ |
# | `'yolov8n.pt'` | Nano (가볍고 빠름) | \~5MB   | CPU 실험, 빠른 추론 |
# | `'yolov8s.pt'` | Small (균형잡힘)   | \~20MB  | 실시간 성능 + 정확도 |
# | `'yolov8m.pt'` | Medium (정확도↑)   | \~45MB  | 정확도 중요할 때     |
# | `'yolov8l.pt'` | Large             | \~75MB  | 정확도 매우 중요할 때  |
# | `'yolov8x.pt'` | XLarge            | \~130MB | 연구용, 리소스 많을 때 |
# 공식 링크: https://github.com/ultralytics/ultralytics
# 또는 직접 다운로드:
# https://github.com/ultralytics/assets/releases
