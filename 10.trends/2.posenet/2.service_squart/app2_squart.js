async function setup() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    // 1. 웹캠 연결
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;

    // 2. PoseNet 모델 로드
    const net = await posenet.load();

    // 3. 자세 인식 반복 함수
    async function detectPose() {
        const pose = await net.estimateSinglePose(video, {
            flipHorizontal: false,
        });

        // 4. 캔버스 초기화 및 웹캠 화면 출력
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        // 5. 관절 위치 표시
        pose.keypoints.forEach(({ part, position, score }) => {
            if (score > 0.5) {
                ctx.beginPath();
                ctx.arc(position.x, position.y, 5, 0, 2 * Math.PI);
                ctx.fillStyle = 'red';
                ctx.fill();
            }
        });

        // 6. 스쿼트 판별 및 텍스트 출력
        const squatting = isSquatting(pose);
        ctx.font = '30px Arial';
        ctx.fillStyle = squatting ? 'green' : 'red';
        ctx.fillText(squatting ? 'GOOD SQUAT' : 'SQUAT LOWER', 10, 50);

        requestAnimationFrame(detectPose);
    }

    detectPose();
}

// 엉덩이가 무릎보다 아래로 내려갔는지 확인
function isSquatting(pose) {
    const leftHip = pose.keypoints.find((p) => p.part === 'leftHip');
    const leftKnee = pose.keypoints.find((p) => p.part === 'leftKnee');

    if (leftHip.score > 0.5 && leftKnee.score > 0.5) {
        return leftHip.position.y > leftKnee.position.y;
    }
    return false;
}

setup();

// 운동 분석 예제 - "스쿼트 자세 판단"
// 핵심 아이디어: 무릎과 엉덩이의 y 좌표를 비교
// "엉덩이가 무릎보다 내려갔는가?" → 스쿼트 성공 여부 판단
