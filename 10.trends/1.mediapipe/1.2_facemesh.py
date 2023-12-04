import cv2
import mediapipe as mp

# Mediapipe의 FaceMesh 모듈 초기화
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# 웹캠으로부터 영상을 받아오기
cap = cv2.VideoCapture(0)

# FaceMesh 모듈 초기화
with mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5) as face_mesh:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        # 이미지를 RGB 형식으로 변환
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 얼굴 특징점 검출
        results = face_mesh.process(image_rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # 특징점 그리기
                mp_drawing.draw_landmarks(
                    image,
                    face_landmarks,
                    mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                )

                # 주요 포인트 번호 및 이름 표시
                for idx, landmark in enumerate(face_landmarks.landmark):
                    h, w, c = image.shape
                    x, y = int(landmark.x * w), int(landmark.y * h)

                    # 주요 포인트에 번호 추가
                    if idx in {1, 7, 10, 152, 234, 454, 151, 389}:
                        # 주요 포인트 이름과 위치 주석
                        point_names = {
                            1: "Right eye inner",
                            7: "Right eye top",
                            10: "Right eye bottom",
                            152: "Left eye inner",
                            234: "Left eye top",
                            454: "Left eye bottom",
                            151: "Right mouth corner",
                            389: "Left mouth corner",
                        }
                        point_name = point_names.get(idx, "Other")
                        # cv2.putText(image, f"{idx}: {point_name}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

        # 영상 출력
        cv2.imshow('Face Mesh', image)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# 작업 완료 후 해제
cap.release()
cv2.destroyAllWindows()
