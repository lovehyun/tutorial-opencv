# main_app.py
import cv2
import mediapipe as mp

from pose_utils.squat_detector import SquatDetector
from pose_utils.pushup_detector import PushupDetector
from pose_utils.plank_detector import PlankDetector
from pose_utils.armcurl_detector import ArmCurlDetector
from pose_utils.lunge_detector import LungeDetector

# ----------------- 설정 -----------------
USE_SQUAT   = True
USE_PUSHUP  = False
USE_PLANK   = False
USE_ARMCURL = False
USE_LUNGE   = False
# ----------------------------------------

# 탐지기 인스턴스
squat_det   = SquatDetector()   if USE_SQUAT   else None
pushup_det  = PushupDetector()  if USE_PUSHUP  else None
plank_det   = PlankDetector()   if USE_PLANK   else None
armcurl_det = ArmCurlDetector() if USE_ARMCURL else None
lunge_det   = LungeDetector()   if USE_LUNGE   else None

# MediaPipe Pose
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    # --- 랜드마크 dict 구성(사용할 것만) -------------------
    if results.pose_landmarks:
        lm = results.pose_landmarks.landmark
        get = lambda name: lm[getattr(mp_pose.PoseLandmark, name).value]
        landmarks = {
            'shoulder' : get('LEFT_SHOULDER'),
            'elbow'    : get('LEFT_ELBOW'),
            'wrist'    : get('LEFT_WRIST'),
            'hip'      : get('LEFT_HIP'),
            'knee'     : get('LEFT_KNEE'),
            'ankle'    : get('LEFT_ANKLE')
        }
    # -----------------------------------------------------------------------------
    # | 운동 종류    | 표시 항목             | 의미                                   |
    # | ----------- | -------------------- | -------------------------------------- |
    # | **Squat**   | `Knee`, `Back`, `OK` | 무릎 굽힘 각도, 등 각도, 판별 결과       |
    # | **Pushup**  | `Reps`, `Elbow`      | 반복 횟수, 팔꿈치 각도                   |
    # | **Plank**   | `BodyAngle`, `OK`    | 어깨-엉덩이-발목의 일직선 각도, 판별 결과 |
    # | **ArmCurl** | `Reps`, `Elbow`      | 반복 횟수, 팔꿈치 각도                   |
    # | **Lunge**   | `Knee`, `OK`         | 앞쪽 다리 무릎 각도, 판별 결과            |
    
    # ---------- 각 운동 탐지 ----------
    overlay = []
    if results.pose_landmarks:
        if squat_det:
            knee_a, back_a, ok = squat_det.detect(landmarks, w, h)
            overlay.append(f"Squat  Knee:{knee_a:.0f}  Back:{back_a:.0f}  OK:{ok}")
            # Knee:85: 무릎 각도가 약 85도 → 깊이 있는 스쿼트.
            # Back:155: 허리와 어깨 라인의 각도 → 등을 곧게 유지했는지 확인.
            # OK:True: 이 두 조건을 모두 만족하면 자세가 올바르다고 판단.
            squat_det.visualize(frame, landmarks, w, h, knee_a, back_a, ok)

        if pushup_det:
            elbow_a, reps = pushup_det.detect(landmarks, w, h)
            overlay.append(f"PushUp Reps:{reps}  Elbow:{elbow_a:.0f}")
            pushup_det.visualize(frame, landmarks, w, h, elbow_a)

        if plank_det:
            body_a, ok = plank_det.detect(landmarks, w, h)
            overlay.append(f"Plank BodyAngle:{body_a:.0f}  OK:{ok}")
            plank_det.visualize(frame, landmarks, w, h, body_a)

        if armcurl_det:
            elbow_a, reps = armcurl_det.detect(landmarks, w, h)
            overlay.append(f"ArmCurl Reps:{reps}  Elbow:{elbow_a:.0f}")
            armcurl_det.visualize(frame, landmarks, w, h, elbow_a)
            
        if lunge_det:
            # 좌우 다리 구분이 필요하므로 landmarks_front를 LEFT로 설정 (예시)
            landmarks_front = {
                'hip'  : get('LEFT_HIP'),
                'knee' : get('LEFT_KNEE'),
                'ankle': get('LEFT_ANKLE')
            }
            knee_a, ok = lunge_det.detect(landmarks_front, None, w, h)
            overlay.append(f"Lunge Knee:{knee_a:.0f}  OK:{ok}")
            lunge_det.visualize(frame, landmarks_front, w, h, knee_a)

    # ---------- 화면 출력 ----------
    # if results.pose_landmarks:
        # mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    y = 30
    for text in overlay:
        cv2.putText(frame, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 0), 2)
        y += 25

    cv2.imshow("Fitness Tracker", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
