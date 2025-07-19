import numpy as np

def calculate_angle(a, b, c):
    """세 점 a-b-c를 기준으로 각도(degree)를 반환"""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ab = a - b
    cb = c - b

    cosine_angle = np.dot(ab, cb) / (np.linalg.norm(ab) * np.linalg.norm(cb))
    angle = np.degrees(np.arccos(cosine_angle))
    return angle
