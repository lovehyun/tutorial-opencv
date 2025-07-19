async function setup() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    // 웹캠 연결
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;

    // 영상 준비 후 PoseNet 시작
    video.onloadeddata = async () => {
        console.log('📷 video ready');
        const net = await posenet.load();
        detectPose(net, video, ctx);
    };
}

async function detectPose(net, video, ctx) {
    const canvas = document.getElementById('canvas');

    async function poseLoop() {
        const pose = await net.estimateSinglePose(video, { flipHorizontal: false });

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        // 관절 점
        pose.keypoints.forEach((k) => {
            if (k.score > 0.5) {
                ctx.beginPath();
                ctx.arc(k.position.x, k.position.y, 5, 0, 2 * Math.PI);
                ctx.fillStyle = 'red';
                ctx.fill();
            }
        });

        // 관절 연결
        const skeleton = posenet.getAdjacentKeyPoints(pose.keypoints, 0.5);
        skeleton.forEach(([from, to]) => {
            ctx.beginPath();
            ctx.moveTo(from.position.x, from.position.y);
            ctx.lineTo(to.position.x, to.position.y);
            ctx.strokeStyle = 'blue';
            ctx.lineWidth = 2;
            ctx.stroke();
        });

        requestAnimationFrame(poseLoop); // 🔁 계속 호출
    }

    poseLoop();
}

setup();
