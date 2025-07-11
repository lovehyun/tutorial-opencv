const vid = document.getElementById('vid');
navigator.mediaDevices.getUserMedia({ video: true }).then((s) => (vid.srcObject = s));

// 이전 상태 저장
let prevPhase = '';

function sendFrame() {
    const c = document.createElement('canvas');
    c.width = vid.videoWidth;
    c.height = vid.videoHeight;
    c.getContext('2d').drawImage(vid, 0, 0);
    c.toBlob((b) => {
        fetch('/predict', { method: 'POST', body: b })
            .then((r) => r.json())
            .then((d) => {
                // phase가 바뀌었을 때만 메시지 업데이트
                if (d.phase !== prevPhase) {
                    prevPhase = d.phase;
                }

                // 카운트다운 또는 유지시간 표시
                if (d.phase === 'countdown') {
                    document.getElementById('count').innerText = `Next in ${d.remaining}`;
                } else {
                    document.getElementById('count').innerText = `Showing ${d.remaining}`;
                }

                // 심볼과 점수는 항상 업데이트
                document.getElementById('sym').innerText = `${d.symbol_left}  vs  ${d.symbol_right}`;
                document.getElementById('score').innerText = `Left ${d.score_left}  :  Right ${d.score_right}`;
            });
    }, 'image/jpeg');
}
setInterval(sendFrame, 500); // 0.5초마다 전송
