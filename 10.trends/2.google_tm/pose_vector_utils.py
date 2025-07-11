# pose_vector_utils.py
import numpy as np
import mediapipe as mp
import cv2

mp_pose = mp.solutions.pose

# Teachable Machine에서 학습에 사용한 관절 순서와 동일하게 맞춰야 합니다.
JOINT_NAMES = [
    'LEFT_SHOULDER', 'RIGHT_SHOULDER',
    'LEFT_ELBOW',    'RIGHT_ELBOW',
    'LEFT_WRIST',    'RIGHT_WRIST',
    'LEFT_HIP',      'RIGHT_HIP',
    'LEFT_KNEE',     'RIGHT_KNEE',
    'LEFT_ANKLE',    'RIGHT_ANKLE',
    'LEFT_HEEL',     'RIGHT_HEEL',
    'LEFT_FOOT_INDEX', 'RIGHT_FOOT_INDEX'
]

def extract_pose_vector(bgr_frame):
    """BGR 이미지를 받아 34-차원 (x, y) 벡터로 변환한다."""
    # MediaPipe Pose 추론
    with mp_pose.Pose(static_image_mode=False,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5) as pose:
        rgb = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if not results.pose_landmarks:
            # 관절이 감지되지 않으면 0으로 채운 벡터 반환
            return np.zeros(len(JOINT_NAMES) * 2, dtype=np.float32)

        lm = results.pose_landmarks.landmark
        vec = []
        for name in JOINT_NAMES:
            idx = getattr(mp_pose.PoseLandmark, name).value
            vec.extend([lm[idx].x, lm[idx].y])   # 정규화된 0–1 좌표
        return np.array(vec, dtype=np.float32)
