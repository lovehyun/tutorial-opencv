
# Teachable Machine Pose 모델을 Python에서 사용하는 방법

이 문서는 Google Teachable Machine에서 학습한 포즈 분류 모델을 다운로드하고, 이를 Python 환경에서 사용하기 위한 절차를 정리한 가이드입니다.

---

## 1. Teachable Machine 모델 다운로드

1. [Teachable Machine](https://teachablemachine.withgoogle.com/)에 접속
2. Pose 프로젝트 생성 후 학습 수행
3. **Export Model → TensorFlow → 다운로드 (`.zip`)**

- 압축 파일에는 다음과 같은 파일이 포함됩니다:
  - `model.json`
  - `weights.bin`

> 이 모델은 TensorFlow.js 포맷이므로 Python에서는 직접 사용할 수 없습니다.

---

## 2. Node.js 및 TensorFlow.js Converter 설치

Python에서 사용하려면 모델을 TensorFlow 형식으로 변환해야 합니다.

```bash
npm install -g tensorflowjs_converter
```

---

## 3. 모델 변환

```bash
tensorflowjs_converter \
  --input_format=tfjs_layers_model \
  ./tm-my-model/model.json \
  ./converted_model/
```

- 변환 결과: `.h5` 또는 `.pb` 형식의 Keras 모델이 생성됩니다.

---

## 4. Python에서 모델 로드

```python
import tensorflow as tf

model = tf.keras.models.load_model("converted_model/model.h5")
```

---

## 5. MediaPipe 좌표 입력 준비

MediaPipe를 통해 추출한 관절 좌표를 모델에 입력할 수 있도록 배열로 변환합니다.

```python
import numpy as np

def landmarks_to_input(lm, mp_pose):
    input_data = []
    for name in ['LEFT_SHOULDER', 'RIGHT_SHOULDER', 'LEFT_ELBOW', 'RIGHT_ELBOW',
                 'LEFT_WRIST', 'RIGHT_WRIST', 'LEFT_HIP', 'RIGHT_HIP',
                 'LEFT_KNEE', 'RIGHT_KNEE', 'LEFT_ANKLE', 'RIGHT_ANKLE']:
        landmark = lm[getattr(mp_pose.PoseLandmark, name).value]
        input_data.extend([landmark.x, landmark.y])
    return np.array([input_data], dtype=np.float32)
```

---

## 6. 예측 수행

```python
input_tensor = landmarks_to_input(results.pose_landmarks.landmark, mp_pose)
prediction = model.predict(input_tensor)
predicted_class = np.argmax(prediction)
```

- `predicted_class`는 예측된 자세 클래스 번호입니다 (예: 0=스쿼트, 1=푸쉬업 등)

---

## 참고사항

- Teachable Machine 모델은 정적 포즈 기준 분류이므로 동작의 연속성 분석은 별도 처리 필요
- 정확도 향상을 위해 pose smoothing 또는 sequence 기반 입력 처리 가능

