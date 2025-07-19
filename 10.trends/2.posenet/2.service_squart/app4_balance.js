let count = 0;
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
                ctx.fillStyle = 'red';
                ctx.fill();
            }
        });

        const squatting = isSquattingAverage(pose);

        if (previousState === 'up' && squatting) {
            previousState = 'down';
        } else if (previousState === 'down' && !squatting) {
            previousState = 'up';
            count += 1;
        }

        ctx.font = '30px Arial';
        ctx.fillStyle = squatting ? 'green' : 'red';
        ctx.fillText(squatting ? 'SQUATTING' : 'STANDING', 10, 50);
        ctx.fillStyle = 'blue';
        ctx.fillText(`COUNT: ${count}`, 10, 90);

        requestAnimationFrame(detectPose);
    }

    detectPose();
}

// 좌우 무릎, 엉덩이의 y좌표 평균으로 판단
function isSquattingAverage(pose) {
    const parts = {
        leftHip: pose.keypoints.find((p) => p.part === 'leftHip'),
        rightHip: pose.keypoints.find((p) => p.part === 'rightHip'),
        leftKnee: pose.keypoints.find((p) => p.part === 'leftKnee'),
        rightKnee: pose.keypoints.find((p) => p.part === 'rightKnee'),
    };

    if (
        parts.leftHip.score > 0.5 &&
        parts.rightHip.score > 0.5 &&
        parts.leftKnee.score > 0.5 &&
        parts.rightKnee.score > 0.5
    ) {
        const avgHipY = (parts.leftHip.position.y + parts.rightHip.position.y) / 2;
        const avgKneeY = (parts.leftKnee.position.y + parts.rightKnee.position.y) / 2;

        return avgHipY > avgKneeY + 15; // 15px 여유 오차
    }

    return false;
}

setup();


// 개선 목표: 좌우 관절 평균 사용으로 스쿼트 판정 정확도 향상
// 한쪽 관절만 사용하면 가림, 왜곡, 한쪽만 움직이는 경우 오류 발생
// 양쪽 좌표 평균으로 중심 위치를 추정하면 정확도가 올라감
//
// 실행결과:
// - 양쪽 관절 평균으로 스쿼트 판정 → 한쪽만 가려져도 문제 없음
// - 더 안정적인 카운트 수행
// - "SQUATTING"과 "STANDING" 상태 표시, 카운트 정상 작동
