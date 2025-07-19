let pushupCount = 0;
let previousState = 'up';

async function setup() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;

    const net = await posenet.load();

    async function detectPose() {
        const pose = await net.estimateSinglePose(video, { flipHorizontal: false });

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        // 관절 표시
        pose.keypoints.forEach(({ position, score }) => {
            if (score > 0.5) {
                ctx.beginPath();
                ctx.arc(position.x, position.y, 5, 0, 2 * Math.PI);
                ctx.fillStyle = 'blue';
                ctx.fill();
            }
        });

        // 팔꿈치 각도 계산
        const { angle, status } = pushupAngleStatus(pose);

        // 상태 변화 감지하여 카운트
        if (status === 'down' && previousState === 'up') {
            previousState = 'down';
        } else if (status === 'up' && previousState === 'down') {
            previousState = 'up';
            pushupCount += 1;
        }

        // 텍스트 출력
        ctx.font = '28px Arial';
        ctx.fillStyle = status === 'down' ? 'orange' : 'green';
        ctx.fillText(`PUSH-UP: ${pushupCount}`, 10, 50);
        ctx.fillStyle = 'black';
        ctx.fillText(`Elbow Angle: ${Math.round(angle)}°`, 10, 90);

        requestAnimationFrame(detectPose);
    }

    detectPose();
}

// 세 점 사이 각도 계산
function getAngle(a, b, c) {
    const ab = { x: b.x - a.x, y: b.y - a.y };
    const cb = { x: b.x - c.x, y: b.y - c.y };

    const dot = ab.x * cb.x + ab.y * cb.y;
    const magAB = Math.sqrt(ab.x ** 2 + ab.y ** 2);
    const magCB = Math.sqrt(cb.x ** 2 + cb.y ** 2);

    const angleRad = Math.acos(dot / (magAB * magCB));
    return (angleRad * 180) / Math.PI;
}

// 팔꿈치 각도 기반 상태 판단
function pushupAngleStatus(pose) {
    const shoulder = pose.keypoints.find((p) => p.part === 'leftShoulder');
    const elbow = pose.keypoints.find((p) => p.part === 'leftElbow');
    const wrist = pose.keypoints.find((p) => p.part === 'leftWrist');

    if (shoulder.score > 0.5 && elbow.score > 0.5 && wrist.score > 0.5) {
        const angle = getAngle(shoulder.position, elbow.position, wrist.position);

        let status = 'idle';
        if (angle < 90) status = 'down';
        else if (angle > 140) status = 'up';

        return { angle, status };
    }

    return { angle: 0, status: 'unknown' };
}

setup();
