from .pose_utils import calculate_angle
from .draw_utils import draw_joint_line, draw_angle_text

class LungeDetector:
    """런지 동작에서 앞쪽 다리의 무릎 각도 및 안정성 판단
    요약:
    - 엉덩이-무릎-발목 세 점을 통해 앞다리 무릎의 굽힘 정도를 계산합니다.
    - knee_threshold를 기준으로 무릎이 충분히 굽혀졌는지(front_ok) 판단합니다.
    - landmarks_back는 현재 사용하지 않지만, 향후 뒤쪽 다리의 균형이나 직각 여부를 확인하는 기능으로 확장할 수 있습니다.
    """

    def __init__(self, knee_threshold=90):
        # 무릎 각도의 기준값 (기본적으로 90도 이하면 올바른 자세로 판단)
        self.knee_threshold = knee_threshold

    def detect(self, landmarks_front, landmarks_back, w, h):
        """
        앞다리의 관절 좌표를 이용해 무릎 각도를 계산하고
        기준 각도 이하일 경우 올바른 자세(front_ok = True)로 판정

        Parameters:
            landmarks_front: 앞다리의 관절 정보 (dict 형태, 'hip', 'knee', 'ankle' 키 포함)
            landmarks_back: 뒤쪽 다리의 관절 정보 (사용하지 않음)
            w, h: 이미지 프레임의 너비와 높이 (비율 좌표를 픽셀로 변환하기 위함)

        Returns:
            knee_angle_front: 앞무릎의 실제 각도 (float)
            front_ok: 기준 각도 이하면 True, 아니면 False
        """
        # 앞다리의 관절 좌표를 픽셀 단위로 변환
        hip_f = [landmarks_front['hip'].x * w, landmarks_front['hip'].y * h]
        knee_f = [landmarks_front['knee'].x * w, landmarks_front['knee'].y * h]
        ankle_f = [landmarks_front['ankle'].x * w, landmarks_front['ankle'].y * h]

        # 무릎 각도 계산: 엉덩이-무릎-발목
        knee_angle_front = calculate_angle(hip_f, knee_f, ankle_f)

        # 기준 각도 이하이면 좋은 자세로 간주
        front_ok = knee_angle_front <= self.knee_threshold

        return knee_angle_front, front_ok

    def visualize(self, frame, landmarks_front, w, h, knee_angle_front):
        hip_f = [landmarks_front['hip'].x * w, landmarks_front['hip'].y * h]
        knee_f = [landmarks_front['knee'].x * w, landmarks_front['knee'].y * h]
        ankle_f = [landmarks_front['ankle'].x * w, landmarks_front['ankle'].y * h]

        draw_joint_line(frame, hip_f, knee_f, color=(0, 0, 255))
        draw_joint_line(frame, knee_f, ankle_f, color=(0, 0, 255))
        draw_angle_text(frame, knee_f, knee_angle_front, color=(0, 0, 255))
