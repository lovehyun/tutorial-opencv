import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

with mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5) as face_mesh:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image_rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # 랜드마크 좌표 추출
                landmarks = face_landmarks.landmark
                height, width, _ = image.shape

                # 얼굴 영역의 좌표 계산
                min_x, max_x = width, 0
                min_y, max_y = height, 0
                for landmark in landmarks:
                    x, y = int(landmark.x * width), int(landmark.y * height)
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)

                # 얼굴 영역 확대
                face_roi = image[min_y:max_y, min_x:max_x]
                face_roi = cv2.resize(face_roi, (face_roi.shape[1] * 2, face_roi.shape[0] * 2))

                # 얼굴 영역 표시
                cv2.imshow('Face ROI', face_roi)

                # 얼굴 메시 그리기
                mp_drawing.draw_landmarks(
                    image, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION,
                )

                # 얼굴 영역 주변에 랜드마크 번호 표시
                for idx, landmark in enumerate(landmarks):
                    x, y = int(landmark.x * width), int(landmark.y * height)
                    if min_x < x < max_x and min_y < y < max_y:
                        cv2.putText(image, str(idx), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1)

        cv2.imshow('Face Direction Detection', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
