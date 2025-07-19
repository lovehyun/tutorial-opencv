import cv2
import numpy as np
import time

# 1. 원본 이미지 및 템플릿 로드
img = cv2.imread('../Resources/Photos/cafe2.jpg')
template = cv2.imread('../Resources/Photos/cafe2_cropped.jpg')

if img is None or template is None:
    print("이미지를 찾을 수 없습니다.")
    exit()

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

tH, tW = template_gray.shape[:2]

# 2. 출력용 이미지 복사
vis_img = img.copy()

# 3. 슬라이딩 윈도우 방식으로 매칭 수행
paused = False  # 일시정지 여부
step = 10  # 픽셀 간격 (1픽셀 단위는 너무 느릴 수 있음)

best_score = -1
best_loc = None

for y in range(0, img_gray.shape[0] - tH, step):
    for x in range(0, img_gray.shape[1] - tW, step):
        while paused:
            key = cv2.waitKey(0)
            if key == ord(' '):  # 스페이스로 다시 시작
                paused = False
                
        roi = img_gray[y:y+tH, x:x+tW]
        if roi.shape != template_gray.shape:
            continue

        # 매칭 점수 계산
        res = cv2.matchTemplate(roi, template_gray, cv2.TM_CCOEFF_NORMED) # TM_CCOEFF_NORMED, TM_CCORR_NORMED, TM_SQDIFF_NORMED
        # TM_CCOEFF_NORMED: 정규화된 상관 계수 (Normalized Cross-Correlation)
        # 결과 범위는 -1.0 ~ 1.0
        # - 1.0 : 완벽하게 일치 (매우 좋은 매칭)
        # - 0.0 : 전혀 상관 없음
        # - -1.0 : 완전히 반대되는 패턴
        score = res[0][0]
        
        # 결과 출력
        print(f"({x},{y}) → Score: {score:.3f}")
        
        if score > best_score:
            best_score = score
            best_loc = (x, y)

        # 시각화: 현재 비교 영역 표시
        display = vis_img.copy()
        cv2.rectangle(display, (x, y), (x + tW, y + tH), (0, 255, 255), 2)
        cv2.putText(display, f"Score: {score:.2f}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        cv2.imshow("Template Matching (Sliding)", display)

        # 슬로우 모션 효과 (속도 조절)
        key = cv2.waitKey(1)
        if key == 27:  # ESC: 종료
            cv2.destroyAllWindows()
            exit()
        elif key == ord(' '):  # 스페이스: 일시정지
            paused = True

        time.sleep(0.01)  # 부드러운 애니메이션을 위해 sleep

# 2. 최종 결과 출력
if best_loc:
    print(f"\nBest Match at: {best_loc} → Score: {best_score:.3f}")
    final_img = img.copy()
    x, y = best_loc
    cv2.rectangle(final_img, (x, y), (x + tW, y + tH), (0, 255, 0), 2)
    cv2.putText(final_img, f"Best: {best_score:.2f}", (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow("Best Match", final_img)
    cv2.waitKey(0)
    
cv2.destroyAllWindows()
