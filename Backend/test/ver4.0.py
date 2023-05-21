import pytesseract
from PIL import Image
import os

# Tesseract 실행 파일 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

# TESSDATA_PREFIX 환경 변수 설정
os.environ["TESSDATA_PREFIX"] = r"/Users/jinnyfruit/Desktop/tessdata"

def ocr_image(image_path, lang):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang=lang)
    return text

# 이미지 파일 경로
image_path = "/Users/jinnyfruit/PycharmProjects/Openeyes/Backend/static/downloads/test.png"

# 한국어 OCR 수행
result_kor = ocr_image(image_path, lang="kor")
print("한국어 OCR 결과:")
print(result_kor)

# 영어 OCR 수행
result_eng = ocr_image(image_path, lang="eng")
print("영어 OCR 결과:")
print(result_eng)

