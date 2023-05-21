import pytesseract
from PIL import Image

def ocr_image(image_path, languages):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang=languages)
    return text

# 이미지 파일 경로
image_path = "/Users/jinnyfruit/PycharmProjects/Openeyes/Backend/static/downloads/test.png"

# OCR 할 언어 설정 (영어: eng, 한국어: kor)
languages = "eng+kor"

# 이미지에서 텍스트 추출
result = ocr_image(image_path, languages)

# 추출된 텍스트 출력
print(result)
