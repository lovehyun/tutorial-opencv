# Flask 웹 서버, 이미지 처리 및 시간 모듈 불러오기
from flask import Flask, request, jsonify, send_from_directory
import numpy as np, cv2, time
from rps_logic import infer_rps  # 손 모양 예측 함수 (가위/바위/보)

app = Flask(__name__)

# 점수, 게임 상태, 타이머 초기값 설정
score = {"Left": 0, "Right": 0}     # 왼쪽/오른쪽 플레이어 점수
phase = "countdown"                # 현재 게임 단계: countdown 또는 hold
phase_start = time.time()          # 현재 단계가 시작된 시간
COUNTDOWN = 5                      # 카운트다운 시간(초)
HOLD = 3                           # 결과 표시 유지 시간(초)
last_symbol = ("❓", "❓")           # 마지막 라운드에서 판별된 손 모양 이모지

# 승자 판정 함수 (1: 왼쪽 승, -1: 오른쪽 승, 0: 무승부)
def judge(l, r):
    table = {
        "rock": {"scissors": 1, "paper": -1, "rock": 0},
        "scissors": {"paper": 1, "rock": -1, "scissors": 0},
        "paper": {"rock": 1, "scissors": -1, "paper": 0}
    }
    return table.get(l, {}).get(r, 0)

# 루트 경로 접근 시 HTML 파일 전송
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

# 클라이언트에서 전송한 이미지로 손 모양 예측 및 게임 로직 수행
@app.route("/predict", methods=["POST"])
def predict():
    global phase, phase_start, score, last_symbol

    # 클라이언트가 보낸 이미지 데이터를 OpenCV 이미지로 변환
    img = cv2.imdecode(np.frombuffer(request.data, np.uint8), cv2.IMREAD_COLOR)
    moves = infer_rps(img)  # {"Left": ("rock", "✊"), "Right": ("scissors", "✌️")} 등 반환

    now = time.time()
    elapsed = now - phase_start  # 현재 phase 시작 후 경과 시간

    # Phase 1: countdown 단계에서 시간이 다 지나면 결과 판정
    if phase == "countdown" and elapsed >= COUNTDOWN:
        l_move, l_sym = moves.get("Left", ("unknown", "❓"))
        r_move, r_sym = moves.get("Right", ("unknown", "❓"))

        # 승자 판단 및 점수 반영
        res = judge(l_move, r_move)
        if res == 1:
            score["Left"] += 1
        elif res == -1:
            score["Right"] += 1

        last_symbol = (l_sym, r_sym)     # 결과 이모지 저장
        phase = "hold"                   # 다음 phase로 전환
        phase_start = now                # phase 시작 시간 갱신
        elapsed = 0                      # 새 phase 기준으로 시간 초기화

    # Phase 2: 결과 표시 유지 단계가 끝나면 다시 countdown 시작
    elif phase == "hold" and elapsed >= HOLD:
        phase = "countdown"
        phase_start = now
        elapsed = 0

    # 현재 phase 기준으로 남은 시간 계산
    if phase == "countdown":
        remaining = max(0, COUNTDOWN - int(elapsed))
    else:
        remaining = max(0, HOLD - int(elapsed))

    # JSON 형태로 클라이언트에 응답 (게임 상태 정보 전달)
    return jsonify({
        "phase": phase,
        "remaining": remaining,
        "symbol_left":  last_symbol[0],
        "symbol_right": last_symbol[1],
        "score_left":   score["Left"],
        "score_right":  score["Right"]
    })

# 개발 모드로 Flask 앱 실행
if __name__ == "__main__":
    app.run(debug=True)
