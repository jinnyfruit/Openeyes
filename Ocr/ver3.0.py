import pytesseract
from PIL import Image
import os

# Tesseract 실행 파일 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

# TESSDATA_PREFIX 환경 변수 설정
os.environ["TESSDATA_PREFIX"] = r"/Users/jinnyfruit/Desktop/tessdata"

def ocr_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, config='--oem 3 --psm 6 -l kor')
    return text

# 이미지 파일 경로
image_path = "/Backend/static/downloads/test.png"

# 이미지에서 텍스트 추출
result = ocr_image(image_path)

# 추출된 텍스트 출력
print(result)
