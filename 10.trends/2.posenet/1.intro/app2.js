function waitForVideo(video) {
    return new Promise(resolve => {
        if (video.readyState >= 2) {
            resolve(); // 이미 준비된 경우 즉시 실행
        } else {
            video.onloadeddata = () => resolve();
        }
    });
}

async function setup() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    // 1. 웹캠 연결
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;

    // 2. PoseNet 모델 로딩
    await waitForVideo(video); // ✅ 명시적으로 video 준비 대기
    const net = await posenet.load();
    detectPose(net, video, canvas, ctx);
}

async function detectPose(net, video, canvas, ctx) {
    const pose = await net.estimateSinglePose(video, { flipHorizontal: false });

    // 1. 배경 비디오 복사
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // 2. 관절 점 그리기
    pose.keypoints.forEach((k) => {
        if (k.score > 0.5) {
            ctx.beginPath();
            ctx.arc(k.position.x, k.position.y, 5, 0, 2 * Math.PI);
            ctx.fillStyle = 'red';
            ctx.fill();
        }
    });

    // 3. 관절 연결 (스켈레톤)
    drawSkeleton(pose.keypoints, ctx);

    requestAnimationFrame(() => detectPose(net, video, canvas, ctx));
}

// 관절 연결
function drawSkeleton(keypoints, ctx) {
    const adjacentKeyPoints = posenet.getAdjacentKeyPoints(keypoints, 0.5);
    adjacentKeyPoints.forEach(([from, to]) => {
        ctx.beginPath();
        ctx.moveTo(from.position.x, from.position.y);
        ctx.lineTo(to.position.x, to.position.y);
        ctx.strokeStyle = 'blue';
        ctx.lineWidth = 2;
        ctx.stroke();
    });
}

setup();
