from .pose_utils import calculate_angle
from .draw_utils import draw_joint_line, draw_angle_text

class PlankDetector:
    """플랭크 자세 유지 여부 감지 클래스
    - 어깨-엉덩이-발목을 잇는 선의 각도가 일직선(180도)에 가까운지를 통해 판별
    요약:
    - 포인트: 어깨 → 엉덩이 → 발목 3점 사이의 몸통 각도를 측정함.
    - 기준: 180도 ± threshold 범위 내면 바른 플랭크 자세로 판단.
    - 반환값: (실제 몸통 각도, True/False)로 유지 여부 평가.
    """

    def __init__(self, straight_threshold=10):
        # 180도에서 얼마나 오차가 허용되는지를 설정 (기본값: ±10도)
        self.straight_threshold = straight_threshold

    def detect(self, landmarks, w, h):
        # 각 관절의 좌표를 이미지 크기에 맞게 픽셀 단위로 변환
        shoulder = [landmarks['shoulder'].x * w, landmarks['shoulder'].y * h]
        hip = [landmarks['hip'].x * w, landmarks['hip'].y * h]
        ankle = [landmarks['ankle'].x * w, landmarks['ankle'].y * h]

        # 어깨-엉덩이-발목 사이의 각도 계산
        body_angle = calculate_angle(shoulder, hip, ankle)

        # 180도에 가까운지 여부 판단 (기울어진 정도가 허용 범위 이내면 True)
        straight_ok = abs(180 - body_angle) < self.straight_threshold

        # 현재 몸통 각도와 플랭크 자세 유지 성공 여부를 반환
        return body_angle, straight_ok

    def visualize(self, frame, landmarks, w, h, body_angle):
        shoulder = [landmarks['shoulder'].x * w, landmarks['shoulder'].y * h]
        hip = [landmarks['hip'].x * w, landmarks['hip'].y * h]
        ankle = [landmarks['ankle'].x * w, landmarks['ankle'].y * h]

        draw_joint_line(frame, shoulder, hip, color=(0, 255, 255))
        draw_joint_line(frame, hip, ankle, color=(0, 255, 255))
        draw_angle_text(frame, hip, body_angle, color=(0, 255, 255))
