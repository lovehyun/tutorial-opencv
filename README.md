# OpenCV 튜토리얼

## OpenCV 설치
- 파이썬 공식 메인 패키지 : ` pip install opencv-python `
- 파이썬 공식 Contribution 패키지 : ` pip install opencv-contrib-python `
  - contrib 패키지는 조금 더 최신 SOTA (State-of-the-art) 기술이 포함되며, 이곳의 검증과 안정성을 토대로 메인 패키지에 탑재 됨
- Numpy 패키지 : ` pip install numpy `
  - C++기반의 OpenCV 에서의 자료구조는 Mat 을 사용하며, 이것이 파이썬에서 numpy 의 ndarray 타입으로 매핑되어 동일한 역할을 함

## 튜토리얼 코드 설명
1. basics : 영상처리 기초 지식 및 사진 다루기
2. process : OpenCV 각종 기본 라이브러리 사용
3. feature : OpenCV 라이브러리를 사용한 각종 피쳐(feature) 검출
4. draw : OpenCV 를 사용한 간단한 draw 기능
5. video : 동영상 처리, 웹캠 처리
6. detection : 각종 검출 (haar-cascade 등)
8. cnn : 기본 딥러닝 기술 (yolo 등)
9. cloud : cloud API 사용하기

## 주요 Document 링크

### OpenCV 공식 DOCs
- https://docs.opencv.org/
  - https://docs.opencv.org/4.5.3/
