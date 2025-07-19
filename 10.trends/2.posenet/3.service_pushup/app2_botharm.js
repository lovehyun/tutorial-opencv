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

        // 팔꿈치 각도 상태 분석
        const { angle, status } = pushupAngleStatusWithBothArms(pose);

        // 상태 전환 시 카운트
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
        ctx.fillText(`Avg Elbow Angle: ${Math.round(angle)}°`, 10, 90);

        requestAnimationFrame(detectPose);
    }

    detectPose();
}

// 각도 계산
function getAngle(a, b, c) {
    const ab = { x: b.x - a.x, y: b.y - a.y };
    const cb = { x: b.x - c.x, y: b.y - c.y };

    const dot = ab.x * cb.x + ab.y * cb.y;
    const magAB = Math.sqrt(ab.x ** 2 + ab.y ** 2);
    const magCB = Math.sqrt(cb.x ** 2 + cb.y ** 2);

    const angleRad = Math.acos(dot / (magAB * magCB));
    return (angleRad * 180) / Math.PI;
}

// 양쪽 팔을 이용한 팔굽혀펴기 분석
function pushupAngleStatusWithBothArms(pose) {
    const parts = {
        lShoulder: pose.keypoints.find((p) => p.part === 'leftShoulder'),
        lElbow: pose.keypoints.find((p) => p.part === 'leftElbow'),
        lWrist: pose.keypoints.find((p) => p.part === 'leftWrist'),
        rShoulder: pose.keypoints.find((p) => p.part === 'rightShoulder'),
        rElbow: pose.keypoints.find((p) => p.part === 'rightElbow'),
        rWrist: pose.keypoints.find((p) => p.part === 'rightWrist'),
    };

    let angles = [];

    if (parts.lShoulder.score > 0.5 && parts.lElbow.score > 0.5 && parts.lWrist.score > 0.5) {
        const leftAngle = getAngle(parts.lShoulder.position, parts.lElbow.position, parts.lWrist.position);
        angles.push(leftAngle);
    }

    if (parts.rShoulder.score > 0.5 && parts.rElbow.score > 0.5 && parts.rWrist.score > 0.5) {
        const rightAngle = getAngle(parts.rShoulder.position, parts.rElbow.position, parts.rWrist.position);
        angles.push(rightAngle);
    }

    if (angles.length === 0) {
        return { angle: 0, status: 'unknown' };
    }

    const avgAngle = angles.reduce((a, b) => a + b, 0) / angles.length;
    let status = 'idle';

    if (avgAngle < 90) status = 'down';
    else if (avgAngle > 140) status = 'up';

    return { angle: avgAngle, status };
}
