from .pose_utils import calculate_angle
from .draw_utils import draw_joint_line, draw_angle_text

class ArmCurlDetector:
    """바이셉 컬 반복 횟수 측정"""
    def __init__(self, curl_threshold=40):
        self.curl_threshold = curl_threshold
        self.state = 'down'
        self.reps = 0

    def detect(self, landmarks, w, h):
        shoulder = [landmarks['shoulder'].x * w, landmarks['shoulder'].y * h]
        elbow = [landmarks['elbow'].x * w, landmarks['elbow'].y * h]
        wrist = [landmarks['wrist'].x * w, landmarks['wrist'].y * h]

        elbow_angle = calculate_angle(shoulder, elbow, wrist)
        if self.state == 'down' and elbow_angle < self.curl_threshold:
            self.state = 'up'
        elif self.state == 'up' and elbow_angle > self.curl_threshold + 30:
            self.state = 'down'
            self.reps += 1
        return elbow_angle, self.reps

    def visualize(self, frame, landmarks, w, h, elbow_angle):
        shoulder = [landmarks['shoulder'].x * w, landmarks['shoulder'].y * h]
        elbow = [landmarks['elbow'].x * w, landmarks['elbow'].y * h]
        wrist = [landmarks['wrist'].x * w, landmarks['wrist'].y * h]

        draw_joint_line(frame, shoulder, elbow, color=(128, 0, 128))
        draw_joint_line(frame, wrist, elbow, color=(128, 0, 128))
        draw_angle_text(frame, elbow, elbow_angle, color=(128, 0, 128))
