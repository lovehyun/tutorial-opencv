# Yolo : https://github.com/pjreddie/darknet/
# https://github.com/pjreddie/darknet/blob/master/data/coco.names

import numpy as np
import cv2

# Yolo 모델 로딩
def load_yolo():
    net = cv2.dnn.readNet('../Resources/Data/yolov3.weights', '../Resources/Data/yolov3.cfg')
    classes = []

    with open('../Resources/Data/coco.names', 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    return net, classes, colors, output_layers

# 이미지 로딩
def load_image():
    img = cv2.imread('../Resources/Photos/group2.jpg')
    # img = cv2.resize(img, None, fx=0.4, fy=0.4)
    
    height, width, channels = img.shape

    return img, height, width, channels

# 개체 검출
def detect_objects(img, net, output_layers):
    blob = cv2.dnn.blobFromImage(img, 1/255, (416,416), mean=(0,0,0), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(output_layers)

    return outputs

# 검출 개체 바운딩 박스 추가
def get_box_dimensions(outputs, height, width):
    boxes = []
    class_ids = []
    confidences = []

    for out in outputs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # 개체 검출
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # 좌표
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    return boxes, confidences, class_ids

# 화면에 정보 출력
def draw_labels(boxes, confidences, colors, class_ids, classes, img):
    # 노이즈 제거
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # 화면에 표시하기
    font = cv2.FONT_HERSHEY_SIMPLEX
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 20), font, 1, color, 2)

    cv2.imshow('Image', img)


net, classes, colors, output_layers = load_yolo()
img, height, width, channels = load_image()
outputs = detect_objects(img, net, output_layers)
boxes, confidences, class_ids = get_box_dimensions(outputs, height, width)
draw_labels(boxes, confidences, colors, class_ids, classes, img)

cv2.waitKey(0)
cv2.destroyAllWindows()
