import cv2

def draw_joint_line(frame, pt1, pt2, color=(255, 0, 0), thickness=2):
    """두 관절을 선으로 연결"""
    cv2.line(frame, tuple(map(int, pt1)), tuple(map(int, pt2)), color, thickness)

def draw_angle_text(frame, position, angle, color=(0, 255, 0), scale=0.6, thickness=2):
    """관절 부근에 각도를 텍스트로 표시"""
    text = f"{int(angle)}°"
    cv2.putText(frame, text, tuple(map(int, position)), cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness)
