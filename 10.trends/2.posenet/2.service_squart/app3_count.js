let count = 0;
let previousState = 'up'; // 시작은 일어선 상태

async function setup() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    // 웹캠 연결
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;

    // PoseNet 로드
    const net = await posenet.load();

    // 분석 루프
    async function detectPose() {
        const pose = await net.estimateSinglePose(video, {
            flipHorizontal: false,
        });

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        // 관절 시각화
        pose.keypoints.forEach(({ position, score }) => {
            if (score > 0.5) {
                ctx.beginPath();
                ctx.arc(position.x, position.y, 5, 0, 2 * Math.PI);
                ctx.fillStyle = 'red';
                ctx.fill();
            }
        });

        // 상태 판별
        const squatting = isSquatting(pose);

        // 상태 전환 시 카운트
        if (previousState === 'up' && squatting) {
            previousState = 'down';
        } else if (previousState === 'down' && !squatting) {
            previousState = 'up';
            count += 1;
        }

        // 텍스트 출력
        ctx.font = '30px Arial';
        ctx.fillStyle = squatting ? 'green' : 'red';
        ctx.fillText(squatting ? 'SQUATTING' : 'STANDING', 10, 50);

        ctx.fillStyle = 'blue';
        ctx.fillText(`COUNT: ${count}`, 10, 90);

        requestAnimationFrame(detectPose);
    }

    detectPose();
}

// 엉덩이가 무릎보다 아래인지 확인
function isSquatting(pose) {
    const leftHip = pose.keypoints.find((p) => p.part === 'leftHip');
    const leftKnee = pose.keypoints.find((p) => p.part === 'leftKnee');

    if (leftHip.score > 0.5 && leftKnee.score > 0.5) {
        return leftHip.position.y > leftKnee.position.y + 15; // 여유 오차
    }
    return false;
}

setup();
