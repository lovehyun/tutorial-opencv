from .pose_utils import calculate_angle
from .draw_utils import draw_joint_line, draw_angle_text

class PushupDetector:
    """푸쉬업 동작 감지 클래스
    - 팔꿈치 각도를 기반으로 '내려감' → '올라감' 상태 전이를 감지하고 반복 횟수를 측정
    요약:
    - elbow_angle: 팔꿈치가 얼마나 굽혀졌는지를 나타내며, 이 각도를 기준으로 동작 상태를 전이합니다.
    - 상태 전이: up → down → up이 하나의 푸쉬업 반복으로 간주됩니다.
    - 반복 조건: 굽힘이 40° 미만 → 다시 70° 이상으로 펴질 때 (+30 여유).
    """

    def __init__(self, elbow_down=40):
        # 팔꿈치가 이 각도 이하로 굽혀졌을 때 'down' 상태로 판단
        self.elbow_down = elbow_down
        self.state = 'up'  # 초기 상태는 올라가 있는 상태로 시작
        self.reps = 0      # 반복 횟수 초기화

    def detect(self, landmarks, w, h):
        # 포즈 랜드마크 좌표를 이미지 해상도에 맞게 픽셀 좌표로 변환
        shoulder = [landmarks['shoulder'].x * w, landmarks['shoulder'].y * h]
        elbow = [landmarks['elbow'].x * w, landmarks['elbow'].y * h]
        wrist = [landmarks['wrist'].x * w, landmarks['wrist'].y * h]

        # 어깨-팔꿈치-손목 사이의 각도를 계산
        elbow_angle = calculate_angle(shoulder, elbow, wrist)

        # 올라가 있는 상태에서 각도가 기준 이하로 작아지면 내려감으로 전환
        if self.state == 'up' and elbow_angle < self.elbow_down:
            self.state = 'down'

        # 내려간 상태에서 각도가 다시 충분히 펴지면 반복 1회로 간주
        elif self.state == 'down' and elbow_angle > self.elbow_down + 30:
            self.state = 'up'
            self.reps += 1

        # 현재 팔꿈치 각도와 누적 반복 횟수 반환
        return elbow_angle, self.reps

    def visualize(self, frame, landmarks, w, h, elbow_angle):
        shoulder = [landmarks['shoulder'].x * w, landmarks['shoulder'].y * h]
        elbow = [landmarks['elbow'].x * w, landmarks['elbow'].y * h]
        wrist = [landmarks['wrist'].x * w, landmarks['wrist'].y * h]

        draw_joint_line(frame, shoulder, elbow, color=(255, 0, 0))
        draw_joint_line(frame, wrist, elbow, color=(255, 0, 0))
        draw_angle_text(frame, elbow, elbow_angle, color=(0, 255, 0))
