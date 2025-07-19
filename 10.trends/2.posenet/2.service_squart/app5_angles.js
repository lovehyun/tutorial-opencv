async function setup() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    // 웹캠 연결
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;

    // PoseNet 모델 로드
    const net = await posenet.load();

    // 반복 감지 함수
    async function detectPose() {
        const pose = await net.estimateSinglePose(video, { flipHorizontal: false });

        // 배경 비디오와 관절 출력
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        // 관절 점 표시
        pose.keypoints.forEach(({ position, score }) => {
            if (score > 0.5) {
                ctx.beginPath();
                ctx.arc(position.x, position.y, 5, 0, 2 * Math.PI);
                ctx.fillStyle = 'red';
                ctx.fill();
            }
        });

        // 각도 기반 분석
        const { depth, angle } = squatAngleAnalysis(pose);

        // 메시지 출력
        let msg = '';
        let color = 'red';

        if (depth === 'deep') {
            msg = `Excellent Squat (${Math.round(angle)}°)`;
            color = 'green';
        } else if (depth === 'normal') {
            msg = `Good Squat (${Math.round(angle)}°)`;
            color = 'orange';
        } else if (depth === 'shallow') {
            msg = `Too Shallow (${Math.round(angle)}°)`;
            color = 'red';
        } else {
            msg = 'Pose Not Detected';
            color = 'gray';
        }

        ctx.font = '28px Arial';
        ctx.fillStyle = color;
        ctx.fillText(msg, 10, 50);

        requestAnimationFrame(detectPose);
    }

    detectPose();
}

// 각도 계산 함수 (A-B-C 각)
function getAngle(a, b, c) {
    const ab = { x: b.x - a.x, y: b.y - a.y };
    const cb = { x: b.x - c.x, y: b.y - c.y };

    const dot = ab.x * cb.x + ab.y * cb.y;
    const magAB = Math.sqrt(ab.x ** 2 + ab.y ** 2);
    const magCB = Math.sqrt(cb.x ** 2 + cb.y ** 2);

    const angleRad = Math.acos(dot / (magAB * magCB));
    return (angleRad * 180) / Math.PI;
}

// 스쿼트 깊이 분석 (무릎 각도 기준)
function squatAngleAnalysis(pose) {
    const hip = pose.keypoints.find((p) => p.part === 'leftHip');
    const knee = pose.keypoints.find((p) => p.part === 'leftKnee');
    const ankle = pose.keypoints.find((p) => p.part === 'leftAnkle');

    if (hip.score > 0.5 && knee.score > 0.5 && ankle.score > 0.5) {
        const angle = getAngle(hip.position, knee.position, ankle.position);

        if (angle < 90) return { depth: 'deep', angle };
        if (angle < 120) return { depth: 'normal', angle };
        return { depth: 'shallow', angle };
    }

    return { depth: 'unknown', angle: 0 };
}

setup();
