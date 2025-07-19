// app.js
async function setup() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    // 웹캠 연결
    const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
    });
    video.srcObject = stream;

    // PoseNet 모델 로드
    const net = await posenet.load();

    // 반복 분석 함수
    async function detect() {
        const pose = await net.estimateSinglePose(video, {
            flipHorizontal: false,
        });

        // 화면 그리기
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        // 관절 그리기
        pose.keypoints.forEach(({ position, score }) => {
            if (score > 0.5) {
                ctx.beginPath();
                ctx.arc(position.x, position.y, 5, 0, 2 * Math.PI);
                ctx.fillStyle = 'red';
                ctx.fill();
            }
        });

        requestAnimationFrame(detect);
    }

    detect();
}

setup();
