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

        pose.keypoints.forEach(({ position, score }) => {
            if (score > 0.5) {
                ctx.beginPath();
                ctx.arc(position.x, position.y, 5, 0, 2 * Math.PI);
                ctx.fillStyle = 'blue';
                ctx.fill();
            }
        });

        const { angle, status } = pushupAngleStatus(pose);

        if (status === 'down' && previousState === 'up') {
            previousState = 'down';
        } else if (status === 'up' && previousState === 'down') {
            previousState = 'up';
            pushupCount++;
            saveTodayCount(1);
        }

        ctx.font = '26px Arial';
        ctx.fillStyle = status === 'down' ? 'orange' : 'green';
        ctx.fillText(`PUSH-UP: ${pushupCount}`, 10, 50);
        ctx.fillStyle = 'black';
        ctx.fillText(`Elbow Angle: ${Math.round(angle)}°`, 10, 90);

        requestAnimationFrame(detectPose);
    }

    detectPose();
}

function getAngle(a, b, c) {
    const ab = { x: b.x - a.x, y: b.y - a.y };
    const cb = { x: b.x - c.x, y: b.y - c.y };
    const dot = ab.x * cb.x + ab.y * cb.y;
    const magAB = Math.sqrt(ab.x ** 2 + ab.y ** 2);
    const magCB = Math.sqrt(cb.x ** 2 + cb.y ** 2);
    const angleRad = Math.acos(dot / (magAB * magCB));
    return (angleRad * 180) / Math.PI;
}

function pushupAngleStatus(pose) {
    const l = pose.keypoints;
    const left = ['leftShoulder', 'leftElbow', 'leftWrist'].map((p) => l.find((k) => k.part === p));
    const right = ['rightShoulder', 'rightElbow', 'rightWrist'].map((p) => l.find((k) => k.part === p));

    let angles = [];

    if (left.every((k) => k.score > 0.5)) {
        angles.push(getAngle(left[0].position, left[1].position, left[2].position));
    }

    if (right.every((k) => k.score > 0.5)) {
        angles.push(getAngle(right[0].position, right[1].position, right[2].position));
    }

    if (angles.length === 0) return { angle: 0, status: 'unknown' };

    const avgAngle = angles.reduce((a, b) => a + b, 0) / angles.length;
    let status = 'idle';
    if (avgAngle < 90) status = 'down';
    else if (avgAngle > 140) status = 'up';

    return { angle: avgAngle, status };
}

// 날짜별 저장
function getTodayKey() {
    return new Date().toISOString().split('T')[0];
}

function saveTodayCount(count) {
    const key = getTodayKey();
    const prev = parseInt(localStorage.getItem(key) || '0');
    localStorage.setItem(key, prev + count);
}

setup();
