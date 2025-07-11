import cv2
import mediapipe as mp
import math
import time

def calculate_distance(point1, point2):
    return math.sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)

def main():
    # 사용자로부터 키 입력 받기
    user_height = float(input("사용자의 키를 입력하세요 (cm): "))

    # Mediapipe의 Pose 모듈 초기화
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    # 웹캠으로부터 영상을 받아오기
    cap = cv2.VideoCapture(0)

    # Pose 모듈 초기화
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        last_output_time = time.time()
        last_results = None

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                continue

            # 이미지를 RGB 형식으로 변환
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Pose 감지 수행
            results = pose.process(image_rgb)

            if results.pose_landmarks:
                # 감지된 관절에 번호와 함께 표시
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
                )

                # 현재 시간을 가져와서 이전 출력과의 시간 간격을 계산
                current_time = time.time()
                elapsed_time = current_time - last_output_time

                # 0.5초에 한 번씩 결과 갱신
                if elapsed_time > 0.5:
                    last_output_time = current_time  # 결과 출력 시간 업데이트

                    # 사용자의 키를 기준으로 비율 계산
                    user_height_pixels = calculate_distance(results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE],
                                                            results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HEEL])
                    user_ratio = user_height / user_height_pixels

                    # 상반신 길이 계산
                    shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                    hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
                    upper_body_length = calculate_distance(shoulder, hip) * user_ratio

                    # 팔 길이 계산
                    shoulder_to_wrist_length = calculate_distance(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER],
                                                                results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]) * user_ratio

                    # 다리 길이 계산
                    hip_to_heel_length = calculate_distance(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP],
                                                            results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HEEL]) * user_ratio

                    # 머리 길이 계산
                    head_to_neck_length = calculate_distance(results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE],
                                                            results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR]) * user_ratio

                    # 가슴둘레 계산
                    chest_circumference = calculate_distance(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER],
                                                            results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]) * user_ratio

                # 빨간색 선 그리기
                cv2.line(image,
                    (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image.shape[1]),
                    int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image.shape[0])),
                    (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HEEL].x * image.shape[1]),
                    int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HEEL].y * image.shape[0])),
                    (0, 0, 255), 2)

                # 픽셀 크기와 user_ratio 출력
                cv2.putText(image, f"Pixel Size: {user_height_pixels:.2f}", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                cv2.putText(image, f"User Ratio: {user_ratio:.2f}", (50, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

                # 결과 출력 (주요 포인트는 계속 출력)
                cv2.putText(image, f"Upper Body Length: {int(upper_body_length)} cm", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)
                cv2.putText(image, f"Arm Length: {int(shoulder_to_wrist_length)} cm", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)
                cv2.putText(image, f"Leg Length: {int(hip_to_heel_length)} cm", (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)
                cv2.putText(image, f"Head Length: {int(head_to_neck_length)} cm", (50, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)
                cv2.putText(image, f"Chest Circumference: {int(chest_circumference)} cm", (50, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)

            # 영상 출력
            # 이미지 크기를 가로와 세로 각각 3배 확대
            image = cv2.resize(image, (0, 0), fx=3, fy=3)
            cv2.imshow('Pose Detection', image)

            # 'q' 키를 누르면 종료
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # 작업 완료 후 해제
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
