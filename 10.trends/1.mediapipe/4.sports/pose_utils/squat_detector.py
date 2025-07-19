from .pose_utils import calculate_angle
from .draw_utils import draw_angle_text, draw_joint_line

class SquatDetector:
    """스쿼트 자세 측정을 위한 클래스: 
    - 무릎 굽힘 각도(knee angle)
    - 허리 각도(back angle)를 이용해 스쿼트의 정확성을 판정
    """
    def __init__(self, knee_threshold=90, back_threshold=30):
        # 스쿼트가 제대로 내려갔는지 판단할 기준 무릎 각도
        self.knee_threshold = knee_threshold
        # 허리의 굽힘 정도를 판단할 기준 (180 - back_threshold 보다 작으면 비정상)
        self.back_threshold = back_threshold

    def detect(self, landmarks, w, h):
        # 좌표값을 픽셀 단위로 변환
        hip = [landmarks['hip'].x * w, landmarks['hip'].y * h]
        knee = [landmarks['knee'].x * w, landmarks['knee'].y * h]
        ankle = [landmarks['ankle'].x * w, landmarks['ankle'].y * h]
        shoulder = [landmarks['shoulder'].x * w, landmarks['shoulder'].y * h]

        # 무릎 각도: 엉덩이-무릎-발목을 기준으로 계산
        knee_angle = calculate_angle(hip, knee, ankle)

        # 허리 각도: 무릎-엉덩이-어깨를 기준으로 계산
        back_angle = calculate_angle(knee, hip, shoulder)

        # 무릎 각도가 기준 이하이면 depth 조건 만족
        depth_ok = knee_angle <= self.knee_threshold

        # 허리 각도가 기준 이상이면 back 조건 만족
        back_ok = back_angle >= (180 - self.back_threshold)

        # 두 조건이 모두 만족해야 OK로 간주
        return knee_angle, back_angle, depth_ok and back_ok

    def visualize(self, frame, landmarks, w, h, knee_angle, back_angle, ok):
        # 시각화용 관절 위치
        hip = [landmarks['hip'].x * w, landmarks['hip'].y * h]
        knee = [landmarks['knee'].x * w, landmarks['knee'].y * h]
        ankle = [landmarks['ankle'].x * w, landmarks['ankle'].y * h]
        shoulder = [landmarks['shoulder'].x * w, landmarks['shoulder'].y * h]

        # 무릎 각도 시각화
        draw_joint_line(frame, hip, knee, color=(255, 0, 0))
        draw_joint_line(frame, ankle, knee, color=(255, 0, 0))
        draw_angle_text(frame, knee, knee_angle, color=(0, 255, 0 if ok else 0))

        # 등 각도 시각화
        draw_joint_line(frame, shoulder, hip, color=(0, 0, 255))
        draw_angle_text(frame, hip, back_angle, color=(0, 255, 0 if ok else 0))
        