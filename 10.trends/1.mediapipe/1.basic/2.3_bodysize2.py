import cv2
import mediapipe as mp
import math
import time

USER_HEIGHT = 170

def calculate_distance(point1, point2):
    return math.sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)

def main():
    # Mediapipe의 Pose 모듈 초기화
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    # 웹캠으로부터 영상을 받아오기
    cap = cv2.VideoCapture(0)

    # Pose 모듈 초기화
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        start_time = time.time()
        max_arm_length = 0

        while cap.isOpened():
            current_time = time.time()

            if current_time - start_time <= 10:
                # 처음 10초 동안 팔 길이 측정
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

                    # 어깨와 손목 사이의 거리 측정
                    shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
                    wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
                    arm_length = calculate_distance(shoulder, wrist)

                    # 최대 팔 길이 갱신
                    max_arm_length = max(max_arm_length, arm_length)

                    # 팔 길이를 빨간색 선으로 표시
                    cv2.line(image, (int(shoulder.x * image.shape[1]), int(shoulder.y * image.shape[0])),
                             (int(wrist.x * image.shape[1]), int(wrist.y * image.shape[0])), (0, 0, 255), 2)

                # 카운트 다운 표시
                countdown = 11 - int(current_time - start_time)
                cv2.putText(image, f"Countdown: {countdown}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                # 영상 출력
                # 이미지 크기를 가로와 세로 각각 3배 확대
                image = cv2.resize(image, (0, 0), fx=3, fy=3)
                cv2.imshow('Pose Detection', image)

            else:
                # 10초 이후에는 최대 팔 길이를 기준으로 계산
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

                    # 사용자의 키를 기준으로 비율 계산
                    user_height_pixels = max_arm_length
                    user_ratio = USER_HEIGHT / user_height_pixels

                    # 상반신 길이 계산
                    shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                    hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
                    upper_body_length = calculate_distance(shoulder, hip) * user_ratio

                    # 어깨 넓이 계산
                    left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
                    right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                    shoulder_width = calculate_distance(left_shoulder, right_shoulder) * user_ratio

                    # 팔 길이 계산
                    left_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
                    right_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
                    left_arm_length = calculate_distance(left_shoulder, left_wrist) * user_ratio
                    right_arm_length = calculate_distance(right_shoulder, right_wrist) * user_ratio

                    # 픽셀 크기와 user_ratio 출력
                    cv2.putText(image, f"Pixel Size: {user_height_pixels:.2f}", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                    cv2.putText(image, f"User Ratio: {user_ratio:.2f}", (50, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

                    # 결과 출력
                    cv2.putText(image, f"Upper Body Length: {int(upper_body_length)} cm", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)
                    cv2.putText(image, f"Shoulder Width: {int(shoulder_width)} cm", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)
                    cv2.putText(image, f"Left Arm Length: {int(left_arm_length)} cm", (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)
                    cv2.putText(image, f"Right Arm Length: {int(right_arm_length)} cm", (50, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)

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
