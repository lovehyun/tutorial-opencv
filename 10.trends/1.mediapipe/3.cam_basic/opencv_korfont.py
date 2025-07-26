import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

def draw_korean_text(img, text, position, font_path='C:/Windows/Fonts/malgun.ttf', font_size=32, color=(255, 255, 255)):
    """
    OpenCV 이미지 위에 한글 텍스트를 출력하는 함수

    Parameters:
        img (np.ndarray): OpenCV 이미지 (BGR)
        text (str): 출력할 한글 텍스트
        position (tuple): (x, y) 위치
        font_path (str): 사용할 한글 폰트 경로
        font_size (int): 폰트 크기
        color (tuple): 텍스트 색상 (B, G, R)
    
    Returns:
        np.ndarray: 텍스트가 그려진 OpenCV 이미지
    """
    # OpenCV → PIL 이미지로 변환
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    # 폰트 설정
    font = ImageFont.truetype(font_path, font_size)
    
    # 텍스트 그리기
    draw = ImageDraw.Draw(img_pil)
    draw.text(position, text, font=font, fill=(color[2], color[1], color[0]))  # RGB → BGR
    
    # PIL → OpenCV 이미지로 다시 변환
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)


if __name__ == "__main__":
    img = np.zeros((480, 640, 3), dtype=np.uint8)

    # 한글 텍스트 출력
    img = draw_korean_text(img, "안녕하세요 OpenCV", (50, 100), font_size=40, color=(0, 255, 255))
    img = draw_korean_text(img, "한글자판 특수문자 ☆★!", (50, 150), font_size=40, color=(0, 255, 255))

    cv2.imshow("Korean Text", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
