import cv2
import mediapipe as mp
import math

# 각도 계산 함수
def get_angle(a, b, c):
    ang = math.degrees(
        math.atan2(c.y - b.y, c.x - b.x) -
        math.atan2(a.y - b.y, a.x - b.x)
    )
    return abs(ang)

# MediaPipe 초기화
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

# 이미지 불러오기
img = cv2.imread("../../../Resources/Photos/fitness2.jpg")
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

with mp_pose.Pose(static_image_mode=True) as pose:
    result = pose.process(rgb)

if result.pose_landmarks:
    h, w, _ = img.shape
    lm = result.pose_landmarks.landmark

    # 포인트 가져오기 (오른쪽 기준)
    shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    elbow    = lm[mp_pose.PoseLandmark.RIGHT_ELBOW]
    wrist    = lm[mp_pose.PoseLandmark.RIGHT_WRIST]
    hip      = lm[mp_pose.PoseLandmark.RIGHT_HIP]
    knee     = lm[mp_pose.PoseLandmark.RIGHT_KNEE]
    ankle    = lm[mp_pose.PoseLandmark.RIGHT_ANKLE]

    # 각도 계산
    # elbow_angle = get_angle(lm[12], lm[14], lm[16])  # 어깨-팔꿈치-손목
    # knee_angle  = get_angle(lm[24], lm[26], lm[28])  # 엉덩이-무릎-발목
    # hip_angle   = get_angle(lm[12], lm[24], lm[26])  # 어깨-엉덩이-무릎
    elbow_angle = get_angle(shoulder, elbow, wrist)
    knee_angle  = get_angle(hip, knee, ankle)
    hip_angle   = get_angle(shoulder, hip, knee)

    # 결과 출력
    print(f"오른쪽 팔꿈치 각도: {elbow_angle:.1f}도")
    print(f"오른쪽 무릎 각도:   {knee_angle:.1f}도")
    print(f"오른쪽 엉덩이 각도: {hip_angle:.1f}도")

    # 시각화용 보조 함수
    def to_pixel(lm): return int(lm.x * w), int(lm.y * h)

    # 시각화 (선 + 각도 텍스트)
    cv2.putText(img, f"{int(elbow_angle)} deg", to_pixel(elbow),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,255), 2)
    cv2.putText(img, f"{int(knee_angle)} deg", to_pixel(knee),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,255), 2)
    cv2.putText(img, f"{int(hip_angle)} deg", to_pixel(hip),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,255), 2)

    mp_draw.draw_landmarks(
        img,
        result.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
        mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2)
    )

cv2.imshow("Pose with Angles", img)
cv2.waitKey(0); cv2.destroyAllWindows()


# 1. 오른쪽 팔꿈치 (Right Elbow) 각도
# shoulder → elbow → wrist
# 즉, 오른쪽 어깨(12) → 오른쪽 팔꿈치(14) → 오른쪽 손목(16)
# 팔을 접었는지, 펴졌는지를 판단하는 각도입니다
#
#        (12)
#         ● 어깨
#         |
#         |  ← 위팔
#         |
#        (14) ● 팔꿈치  ← 기준점
#         |
#         |  ← 아래팔
#         |
#        (16) ● 손목

# 2. 오른쪽 무릎 (Right Knee) 각도
# hip → knee → ankle
# 즉, 오른쪽 엉덩이(24) → 오른쪽 무릎(26) → 오른쪽 발목(28)
# 앉았는지, 다리를 뻗었는지를 판단하는 각도입니다
#
#         (24)
#          ● 엉덩이
#          |
#          |  ← 허벅지
#          |
#         (26) ● 무릎  ← 기준점
#          |
#          |  ← 종아리
#          |
#         (28) ● 발목

# 3. 오른쪽 엉덩이 (Right Hip) 각도
# shoulder → hip → knee
# 즉, 오른쪽 어깨(12) → 오른쪽 엉덩이(24) → 오른쪽 무릎(26)
# 상체가 얼마나 굽혀졌는지 (예: 허리를 숙였는지) 판단하는 각도입니다
#
#         (12)
#          ● 어깨
#          |
#          |  ← 몸통
#          |
#         (24) ● 엉덩이  ← 기준점
#          |
#          |  ← 허벅지
#          |
#         (26) ● 무릎
