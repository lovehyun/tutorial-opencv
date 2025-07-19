"""
realtime_sit_stand.py
웹캠 영상에서 실시간으로 '앉음 / 섬' 판별하기
"""
import cv2, mediapipe as mp, math, time

# ── 각도 계산 함수 ────────────────────────────────────────────
def angle(a, b, c):
    """세 점(a-b-c)으로 구성된 ∠abc 반환(도) – a,b,c 는 landmark 객체"""
    ang = math.degrees(
        math.atan2(c.y - b.y, c.x - b.x) -
        math.atan2(a.y - b.y, a.x - b.x)
    )
    return abs(ang)

# ── MediaPipe 초기화 ─────────────────────────────────────────
mp_pose  = mp.solutions.pose
mp_draw  = mp.solutions.drawing_utils
pose     = mp_pose.Pose(model_complexity=1)
state    = "분석 중…"          # 현재 자세 상태 문자열
timestamp = time.time()        # 최근 상태가 바뀐 시각

# ── 웹캠 루프 ────────────────────────────────────────────────
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ok, frame = cap.read()
    if not ok: break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = pose.process(rgb)

    if res.pose_landmarks:                    # 랜드마크 검출 성공
        lm = res.pose_landmarks.landmark
        # 오른쪽 관절: HIP(24) – KNEE(26) – ANKLE(28)
        hip, knee, ankle = lm[24], lm[26], lm[28]
        knee_ang = angle(hip, knee, ankle)

        # 상태 판별
        prev_state = state
        if knee_ang < 90:           # ① 앉음
            state = "앉음"
        elif knee_ang > 150:        # ② 섬
            state = "섬"
        else:                       # ③ 중간(움직임)
            state = "이동 중"

        # 상태가 바뀌었을 때만 로그 출력
        if state != prev_state:
            print(f"[{time.strftime('%H:%M:%S')}] 상태 변경 ➜ {state}")

        # 프레임에 각도·상태 표시
        cv2.putText(frame, f"Knee: {knee_ang:.1f} deg",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,255), 2)
        cv2.putText(frame, f"Status: {state}",
                    (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

        # 포즈 랜드마크 그리기 (옵션)
        mp_draw.draw_landmarks(
            frame, res.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_draw.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2),
            mp_draw.DrawingSpec(color=(0,0,255), thickness=2)
        )

    cv2.imshow("Sit / Stand Detector", frame)
    if cv2.waitKey(1) & 0xFF == 27:   # ESC 키
        break

# ── 정리 ────────────────────────────────────────────────────
cap.release(); cv2.destroyAllWindows(); pose.close()
