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
                mp_drawing.draw_landmarks(
                    image,
                    face_landmarks,
                    mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                )

                for idx, landmark in enumerate(face_landmarks.landmark):
                    h, w, c = image.shape
                    x, y = int(landmark.x * w), int(landmark.y * h)

                    if idx in {29, 390, 61, 291}:  # Selecting major points (eyes, mouth)
                        point_names = {
                            29: "Right eye",
                            390: "Left eye",
                            61: "Right mouth",
                            291: "Left mouth",
                        }
                        point_name = point_names.get(idx, "Other")
                        cv2.putText(image, f"{idx}: {point_name}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1)

        # 이미지 크기를 가로와 세로 각각 3배 확대
        image = cv2.resize(image, (0, 0), fx=3, fy=3)
        cv2.imshow('Face Mesh', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
