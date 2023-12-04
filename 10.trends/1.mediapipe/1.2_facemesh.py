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
                    if idx in {145, 466, 291}:
                        # 주요 포인트 이름과 위치 주석
                        point_names = {
                            145: "Right eye lower",
                            466: "Left eye outer",
                            291: "Lips Upper outer",
                        }
                        point_name = point_names.get(idx, "Other")
                        cv2.putText(image, f"{idx}: {point_name}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

        # 영상 출력
        # 이미지 크기를 가로와 세로 각각 2배 확대
        image = cv2.resize(image, (0, 0), fx=2, fy=2)
        cv2.imshow('Face Mesh', image)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# 작업 완료 후 해제
cap.release()
cv2.destroyAllWindows()


# lipsUpperOuter: [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291]
# lipsLowerOuter: [146, 91, 181, 84, 17, 314, 405, 321, 375, 291]
# lipsUpperInner: [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308]
# lipsLowerInner: [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308]
# rightEyeUpper0: [246, 161, 160, 159, 158, 157, 173]
# rightEyeLower0: [33, 7, 163, 144, 145, 153, 154, 155, 133]
# rightEyeUpper1: [247, 30, 29, 27, 28, 56, 190]
# rightEyeLower1: [130, 25, 110, 24, 23, 22, 26, 112, 243]
# rightEyeUpper2: [113, 225, 224, 223, 222, 221, 189]
# rightEyeLower2: [226, 31, 228, 229, 230, 231, 232, 233, 244]
# rightEyeLower3: [143, 111, 117, 118, 119, 120, 121, 128, 245]
# rightEyebrowUpper: [156, 70, 63, 105, 66, 107, 55, 193]
# rightEyebrowLower: [35, 124, 46, 53, 52, 65]
# rightEyeIris: [473, 474, 475, 476, 477]
# leftEyeUpper0: [466, 388, 387, 386, 385, 384, 398]
# leftEyeLower0: [263, 249, 390, 373, 374, 380, 381, 382, 362]
# leftEyeUpper1: [467, 260, 259, 257, 258, 286, 414]
# leftEyeLower1: [359, 255, 339, 254, 253, 252, 256, 341, 463]
# leftEyeUpper2: [342, 445, 444, 443, 442, 441, 413]
# leftEyeLower2: [446, 261, 448, 449, 450, 451, 452, 453, 464]
# leftEyeLower3: [372, 340, 346, 347, 348, 349, 350, 357, 465]
# leftEyebrowUpper: [383, 300, 293, 334, 296, 336, 285, 417]
# leftEyebrowLower: [265, 353, 276, 283, 282, 295]
# leftEyeIris: [468, 469, 470, 471, 472]
